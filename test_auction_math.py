"""Financial regression checks; run with python -m unittest -v."""

import unittest

from auction_math import buyer_fee, calculate, eur, max_hammer_at_step, max_hammer_for_budget


def mercier(**overrides):
    settings = dict(
        mode="percent", rate=14.28, min_fee=360.0,
        tier_threshold=0.0, tier_rate_1=0.0, tier_rate_2=0.0,
        dossier=120.0, live_fee=60.0, ct_fee=0.0,
        availability_fee=0.0, admin_fee=0.0, warranty_fee=0.0,
        battery_fee=0.0, other_fee=0.0, storage_days=0,
        storage_day_fee=20.0, registration_fee=0.0,
        transport_fee=0.0, repair_budget=0.0,
        fee_vat_rate=0.0, buyer_fee_base_factor=1.0,
    )
    settings.update(overrides)
    return settings


class MercierInvoiceTests(unittest.TestCase):
    def test_channels_use_one_dossier_plus_one_live_surcharge(self):
        for live_fee, expected in [(0, 11548), (30, 11578), (60, 11608)]:
            with self.subTest(live_fee=live_fee):
                result = calculate(10000, **mercier(live_fee=live_fee))
                self.assertEqual(result["adjudication_fee"], 1428)
                self.assertEqual(result["auction_invoice"], expected)
                self.assertEqual(result["fee_vat_amount"], 0)

    def test_battery_surcharge_requires_an_explicit_amount(self):
        normal = calculate(10000, **mercier())
        confirmed = calculate(10000, **mercier(battery_fee=40))
        self.assertEqual(normal["auction_invoice"], 11608)
        self.assertEqual(confirmed["auction_invoice"], 11648)

    def test_voluntary_and_judicial_minimum(self):
        voluntary = calculate(2000, **mercier())
        judicial = calculate(2000, **mercier(min_fee=0))
        self.assertEqual(voluntary["adjudication_fee"], 360)
        self.assertEqual(voluntary["auction_invoice"], 2540)
        self.assertEqual(judicial["adjudication_fee"], 285.60)
        self.assertEqual(judicial["auction_invoice"], 2465.60)
        self.assertEqual(calculate(2500, **mercier())["auction_invoice"], 3040)
        self.assertEqual(calculate(2600, **mercier())["auction_invoice"], 3151.28)

    def test_ht_input_is_converted_before_ttc_commission(self):
        result = calculate(10000, **mercier(hammer_vat_rate=20))
        self.assertEqual(result["hammer_ttc"], 12000)
        self.assertEqual(result["hammer_vat_amount"], 2000)
        self.assertEqual(result["adjudication_fee"], 1713.60)
        self.assertEqual(result["auction_invoice"], 13893.60)

    def test_invoice_excludes_post_sale_costs_and_reserves(self):
        result = calculate(10000, **mercier(
            registration_fee=565.76, transport_fee=200, repair_budget=2000,
        ))
        self.assertEqual(result["auction_invoice"], 11608)
        self.assertEqual(result["grand_total"], 14373.76)

    def test_storage_is_charged_only_for_entered_days(self):
        result = calculate(10000, **mercier(storage_days=3))
        self.assertEqual(result["storage_fee"], 60)
        self.assertEqual(result["auction_invoice"], 11668)


class BidCeilingTests(unittest.TestCase):
    def assert_ceiling(self, budget, settings, step, expected):
        ceiling = max_hammer_at_step(budget, settings, step)
        self.assertEqual(ceiling, expected)
        self.assertLessEqual(calculate(ceiling, **settings)["grand_total"], budget)
        self.assertGreater(calculate(round(ceiling + step, 2), **settings)["grand_total"], budget)

    def test_cent_rounding_can_fit_exact_budget(self):
        settings = mercier()
        self.assertEqual(max_hammer_for_budget(12000, settings), 10343.02)
        self.assert_ceiling(12000, settings, 0.01, 10343.02)
        self.assertEqual(calculate(10343.02, **settings)["grand_total"], 12000)
        self.assertEqual(calculate(10343.03, **settings)["grand_total"], 12000.01)

    def test_selectable_bid_steps(self):
        self.assert_ceiling(12000, mercier(), 100, 10300)
        self.assert_ceiling(12000, mercier(), 500, 10000)
        self.assert_ceiling(12000, mercier(battery_fee=40), 100, 10300)

    def test_reserve_reduces_affordable_bid(self):
        self.assert_ceiling(12000, mercier(repair_budget=2000), 100, 8500)

    def test_minimum_fee_is_respected_by_inverse_calculation(self):
        self.assert_ceiling(2540, mercier(), 100, 2000)
        self.assert_ceiling(2465.60, mercier(min_fee=0), 100, 2000)

    def test_no_positive_bid_when_budget_is_insufficient(self):
        for budget in [0, 100, 540]:
            with self.subTest(budget=budget):
                self.assertEqual(max_hammer_for_budget(budget, mercier()), 0)
        self.assertEqual(max_hammer_at_step(600, mercier(), 100), 0)
        self.assertEqual(max_hammer_for_budget(1000, mercier(repair_budget=2000)), 0)

    def test_ht_ceiling_uses_input_currency_basis(self):
        self.assert_ceiling(12000, mercier(hammer_vat_rate=20), 100, 8600)

    def test_invalid_steps_are_rejected(self):
        for step in [0, -100, 0.001]:
            with self.subTest(step=step), self.assertRaises(ValueError):
                max_hammer_at_step(12000, mercier(), step)


class ExistingTariffRegressionTests(unittest.TestCase):
    def test_all_existing_buyer_fee_modes(self):
        cases = [
            (10000, "percent", 14.4, 360, 0, 0, 0, 1440),
            (1000, "percent", 14.4, 360, 0, 0, 0, 360),
            (10000, "fixed", 0, 500, 0, 0, 0, 500),
            (10000, "included", 99, 500, 0, 0, 0, 0),
            (5000, "tiered", 0, 0, 3000, 15, 12.5, 700),
            (15000, "tiered", 0, 0, 10000, 7, 5, 950),
            (4999, "autorola", 0, 0, 0, 0, 0, 325),
            (5000, "autorola", 0, 0, 0, 0, 0, 425),
            (50000, "autorola", 0, 0, 0, 0, 0, 1825),
            (5000, "ecars_other", 0, 0, 0, 0, 0, 250),
            (5000.01, "ecars_other", 0, 0, 0, 0, 0, 300),
            (10000.01, "ecars_other", 0, 0, 0, 0, 0, 350),
            (20000.01, "ecars_other", 0, 0, 0, 0, 0, 400),
            (30000, "ecars_other", 0, 0, 0, 0, 0, 400),
            (30000.01, "ecars_other", 0, 0, 0, 0, 0, 450),
        ]
        for *arguments, expected in cases:
            with self.subTest(arguments=arguments):
                self.assertEqual(buyer_fee(*arguments), expected)

    def test_bca_fees_have_separate_vat(self):
        result = calculate(20000, **mercier(
            rate=3.9, min_fee=500, dossier=0, live_fee=0, fee_vat_rate=20,
        ))
        self.assertEqual(result["adjudication_fee"], 780)
        self.assertEqual(result["fee_vat_amount"], 156)
        self.assertEqual(result["auction_invoice"], 20936)

    def test_oveo_fee_base_factor_is_preserved(self):
        result = calculate(12000, **mercier(
            mode="tiered", min_fee=0, tier_threshold=10000,
            tier_rate_1=7, tier_rate_2=5, dossier=0, live_fee=0,
            fee_vat_rate=20, buyer_fee_base_factor=1 / 1.2,
        ))
        self.assertEqual(result["adjudication_fee"], 700)
        self.assertEqual(result["auction_invoice"], 12840)

    def test_ceilings_handle_tariff_jumps(self):
        settings = mercier(mode="autorola", dossier=35, live_fee=0, fee_vat_rate=20)
        ceiling = max_hammer_for_budget(5431, settings)
        self.assertEqual(ceiling, 4999)
        self.assertGreater(calculate(4999.01, **settings)["grand_total"], 5431)

    def test_money_format_uses_half_up_rounding(self):
        self.assertEqual(eur(10343.025), "10 343,03 €")


if __name__ == "__main__":
    unittest.main()
