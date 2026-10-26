"""Auction totals and affordable bid ceilings, independent from Streamlit.

Amounts supplied by the UI are non-negative. Public functions keep float-based
interfaces for Streamlit; monetary arithmetic and comparisons use Decimal.
"""

from decimal import Decimal, ROUND_HALF_UP


CENT = Decimal("0.01")
HUNDRED = Decimal("100")
ZERO = Decimal("0")


def _decimal(value) -> Decimal:
    number = value if isinstance(value, Decimal) else Decimal(str(value))
    if not number.is_finite():
        raise ValueError("Les montants doivent être des nombres finis.")
    return number


def _money(value) -> Decimal:
    return _decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


def eur(value: float) -> str:
    return f"{_money(value):,.2f} €".replace(",", " ").replace(".", ",")


def _buyer_fee(
    hammer: Decimal,
    mode: str,
    rate: float,
    min_fee: float,
    tier_threshold: float,
    tier_rate_1: float,
    tier_rate_2: float,
) -> Decimal:
    if hammer <= ZERO or mode == "included":
        return ZERO

    if mode == "fixed":
        return _decimal(min_fee)

    if mode == "tiered":
        threshold = _decimal(tier_threshold)
        first = min(hammer, threshold) * _decimal(tier_rate_1) / HUNDRED
        second = max(hammer - threshold, ZERO) * _decimal(tier_rate_2) / HUNDRED
        return first + second

    if mode == "ecars_other":
        if hammer <= 5000:
            return Decimal("250")
        if hammer <= 10000:
            return Decimal("300")
        if hammer <= 20000:
            return Decimal("350")
        extra_steps = max(0, int((hammer - Decimal("20000.01")) // 10000))
        return Decimal("400") + extra_steps * Decimal("50")

    if mode == "autorola":
        brackets = [
            (4999, 325),
            (7499, 425),
            (9999, 525),
            (14999, 625),
            (19999, 725),
            (24999, 825),
            (29999, 925),
            (34999, 1025),
            (39999, 1225),
            (44999, 1425),
            (49999, 1625),
        ]
        for upper, fee in brackets:
            if hammer <= upper:
                return Decimal(fee)
        return Decimal("1825")

    return max(hammer * _decimal(rate) / HUNDRED, _decimal(min_fee))


def buyer_fee(
    hammer: float,
    mode: str,
    rate: float,
    min_fee: float,
    tier_threshold: float,
    tier_rate_1: float,
    tier_rate_2: float,
) -> float:
    """Return the existing buyer-fee tariff rounded to the nearest cent."""
    return float(_money(_buyer_fee(
        _decimal(hammer), mode, rate, min_fee,
        tier_threshold, tier_rate_1, tier_rate_2,
    )))


def calculate(
    hammer: float,
    mode: str,
    rate: float,
    min_fee: float,
    tier_threshold: float,
    tier_rate_1: float,
    tier_rate_2: float,
    dossier: float,
    live_fee: float,
    ct_fee: float,
    availability_fee: float,
    admin_fee: float,
    warranty_fee: float,
    battery_fee: float,
    other_fee: float,
    storage_days: int,
    storage_day_fee: float,
    registration_fee: float,
    transport_fee: float,
    repair_budget: float,
    fee_vat_rate: float = 0.0,
    buyer_fee_base_factor: float = 1.0,
    hammer_vat_rate: float = 0.0,
) -> dict:
    """Compute the auction invoice and the total including external costs.

    ``hammer_vat_rate`` is zero for a TTC bid. Set it only when the amount
    entered is HT and needs conversion to TTC. Published TTC fees must keep
    ``fee_vat_rate=0``. Deposits are payments, not costs, and are intentionally
    absent from this calculation and from the bid ceiling.
    """
    hammer_amount = _money(hammer)
    hammer_vat_amount = _money(hammer_amount * _decimal(hammer_vat_rate) / HUNDRED)
    hammer_ttc = hammer_amount + hammer_vat_amount
    fee_base = hammer_ttc * _decimal(buyer_fee_base_factor)
    adjudication_fee_net = _money(_buyer_fee(
        fee_base, mode, rate, min_fee,
        tier_threshold, tier_rate_1, tier_rate_2,
    ))
    storage_fee_net = _money(_decimal(storage_days) * _decimal(storage_day_fee))
    auction_extras_net = _money(sum(
        (_decimal(value) for value in (
            dossier, live_fee, ct_fee, availability_fee, admin_fee,
            warranty_fee, battery_fee, other_fee, storage_fee_net,
        )),
        ZERO,
    ))
    taxable_fees_net = adjudication_fee_net + auction_extras_net
    fee_vat_amount = _money(taxable_fees_net * _decimal(fee_vat_rate) / HUNDRED)
    auction_invoice = _money(hammer_ttc + taxable_fees_net + fee_vat_amount)
    grand_total = _money(
        auction_invoice + _money(registration_fee)
        + _money(transport_fee) + _money(repair_budget)
    )

    return {
        "hammer_ttc": float(hammer_ttc),
        "hammer_vat_amount": float(hammer_vat_amount),
        "adjudication_fee": float(adjudication_fee_net),
        "storage_fee": float(storage_fee_net),
        "auction_extras": float(auction_extras_net),
        "fee_vat_amount": float(fee_vat_amount),
        "auction_invoice": float(auction_invoice),
        "grand_total": float(grand_total),
    }


def max_hammer_at_step(budget: float, calc_kwargs: dict, step: float = 100.0) -> float:
    """Largest positive multiple of ``step`` affordable within ``budget``.

    The search uses the same rounded total as the invoice, including minimum
    fees, tier changes, VAT and external expenses. Return 0 when no positive
    bid is affordable. The returned bid uses the input's HT/TTC denomination.
    """
    increment = _decimal(step)
    if increment <= ZERO or increment != _money(increment):
        raise ValueError("Le pas doit être positif et exprimé au centime près.")
    available = _decimal(budget)
    if available <= ZERO:
        return 0.0

    low = 0
    high = int(available // increment)
    while low < high:
        mid = (low + high + 1) // 2
        candidate = increment * mid
        result = calculate(hammer=candidate, **calc_kwargs)
        if _decimal(result["grand_total"]) <= available:
            low = mid
        else:
            high = mid - 1
    return float(increment * low)


def max_hammer_for_budget(budget: float, calc_kwargs: dict) -> float:
    """Largest affordable bid to the cent; 0 means no positive bid fits."""
    return max_hammer_at_step(budget, calc_kwargs, step=0.01)
