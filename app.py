import streamlit as st

st.set_page_config(
    page_title="FR Auction Cars",
    page_icon="🔨",
    layout="centered",
)

def eur(value: float) -> str:
    return f"{value:,.2f} €".replace(",", " ").replace(".", ",")

def auction_total(
    hammer: float,
    buyer_rate_pct: float,
    min_buyer_fee: float,
    sale_fee: float,
    live_fee: float,
    moba_fee: float,
    recharge_fee: float,
    registration_fee: float,
    transport_fee: float,
    repair_budget: float,
):
    buyer_fee = max(hammer * buyer_rate_pct / 100.0, min_buyer_fee)
    auction_invoice = hammer + buyer_fee + sale_fee + live_fee + moba_fee + recharge_fee
    grand_total = auction_invoice + registration_fee + transport_fee + repair_budget
    return buyer_fee, auction_invoice, grand_total

def max_hammer_for_budget(
    budget: float,
    buyer_rate_pct: float,
    min_buyer_fee: float,
    fixed_extras: float,
):
    if budget <= fixed_extras:
        return 0.0

    rate = buyer_rate_pct / 100.0
    remaining = budget - fixed_extras

    percentage_candidate = remaining / (1.0 + rate)
    if percentage_candidate * rate >= min_buyer_fee:
        return max(0.0, percentage_candidate)

    return max(0.0, remaining - min_buyer_fee)

st.title("🔨 FR Auction Cars")
st.caption("Calculateur de coût total pour les enchères automobiles en France")

with st.sidebar:
    st.header("⚙️ Paramètres")
    st.caption("Valeurs Alcopa 2026 préremplies — toutes modifiables.")

    buyer_rate_pct = st.number_input(
        "Frais d'adjudication (%)",
        min_value=0.0,
        max_value=100.0,
        value=14.40,
        step=0.10,
        format="%.2f",
    )
    min_buyer_fee = st.number_input(
        "Minimum frais d'adjudication (€ TTC)",
        min_value=0.0,
        value=360.0,
        step=10.0,
    )

    cirano = st.toggle("Garantie CIRANO", value=True)
    sale_fee_default = 225.0 if cirano else 140.0
    sale_fee = st.number_input(
        "Frais de vente (€ TTC)",
        min_value=0.0,
        value=sale_fee_default,
        step=5.0,
    )

    platform = st.selectbox(
        "Mode d'enchère",
        ["Interencheres LIVE", "Alcopa LIVE / enchère plafond", "En salle"],
    )
    live_defaults = {
        "Interencheres LIVE": 80.0,
        "Alcopa LIVE / enchère plafond": 45.0,
        "En salle": 0.0,
    }
    live_fee = st.number_input(
        "Frais plateforme (€ TTC)",
        min_value=0.0,
        value=live_defaults[platform],
        step=5.0,
    )

    st.divider()
    st.subheader("Options")
    use_moba = st.toggle("Check-up batterie MOBA", value=False)
    moba_fee = 45.0 if use_moba else 0.0

    use_recharge = st.toggle("Recharge batterie de traction", value=False)
    recharge_fee = 25.0 if use_recharge else 0.0

tab1, tab2, tab3 = st.tabs([
    "💶 Coût total",
    "🎯 Enchère max",
    "📊 Paliers",
])

with tab1:
    hammer = st.number_input(
        "Prix remporté / prix au marteau (€)",
        min_value=0.0,
        value=20000.0,
        step=100.0,
    )

    c1, c2 = st.columns(2)
    with c1:
        registration_fee = st.number_input(
            "Carte grise (€)",
            min_value=0.0,
            value=0.0,
            step=10.0,
        )
        transport_fee = st.number_input(
            "Transport / déplacement (€)",
            min_value=0.0,
            value=0.0,
            step=25.0,
        )

    with c2:
        repair_budget = st.number_input(
            "Entretien / réparations (€)",
            min_value=0.0,
            value=0.0,
            step=50.0,
        )

    buyer_fee, auction_invoice, total = auction_total(
        hammer,
        buyer_rate_pct,
        min_buyer_fee,
        sale_fee,
        live_fee,
        moba_fee,
        recharge_fee,
        registration_fee,
        transport_fee,
        repair_budget,
    )

    st.divider()

    m1, m2, m3 = st.columns(3)
    m1.metric("Prix marteau", eur(hammer))
    m2.metric("Frais enchères", eur(auction_invoice - hammer))
    m3.metric("TOTAL", eur(total))

    st.subheader("Détail")
    lines = [
        ("Prix d'adjudication", hammer),
        (f"Frais d'adjudication ({buyer_rate_pct:.2f} %)", buyer_fee),
        ("Frais de vente", sale_fee),
        (f"Plateforme — {platform}", live_fee),
    ]
    if moba_fee:
        lines.append(("Check-up batterie MOBA", moba_fee))
    if recharge_fee:
        lines.append(("Recharge batterie", recharge_fee))
    if registration_fee:
        lines.append(("Carte grise", registration_fee))
    if transport_fee:
        lines.append(("Transport / déplacement", transport_fee))
    if repair_budget:
        lines.append(("Entretien / réparations", repair_budget))

    for label, amount in lines:
        left, right = st.columns([3, 1])
        left.write(label)
        right.markdown(f"**{eur(amount)}**")

    st.success(f"Total à prévoir : **{eur(total)}**")
    st.caption(f"Bordereau d'enchères estimé : {eur(auction_invoice)}")

with tab2:
    budget = st.number_input(
        "Budget maximum tout compris (€)",
        min_value=0.0,
        value=25000.0,
        step=100.0,
    )

    d1, d2 = st.columns(2)
    with d1:
        reg_budget = st.number_input(
            "Carte grise (€)",
            min_value=0.0,
            value=0.0,
            step=10.0,
            key="reg2",
        )
        transport_budget = st.number_input(
            "Transport (€)",
            min_value=0.0,
            value=0.0,
            step=25.0,
            key="trans2",
        )
    with d2:
        repair_budget2 = st.number_input(
            "Réparations / entretien (€)",
            min_value=0.0,
            value=0.0,
            step=50.0,
            key="rep2",
        )

    fixed_extras = (
        sale_fee
        + live_fee
        + moba_fee
        + recharge_fee
        + reg_budget
        + transport_budget
        + repair_budget2
    )

    max_hammer = max_hammer_for_budget(
        budget,
        buyer_rate_pct,
        min_buyer_fee,
        fixed_extras,
    )

    buyer_fee2, invoice2, total2 = auction_total(
        max_hammer,
        buyer_rate_pct,
        min_buyer_fee,
        sale_fee,
        live_fee,
        moba_fee,
        recharge_fee,
        reg_budget,
        transport_budget,
        repair_budget2,
    )

    st.metric("Enchère maximale théorique", eur(max_hammer))
    st.warning("Pendant une vente, arrondis ce montant vers le bas au palier précédent pour garder une marge.")
    st.caption(
        f"Frais d'adjudication estimés : {eur(buyer_fee2)} · "
        f"bordereau : {eur(invoice2)} · total : {eur(total2)}"
    )

with tab3:
    st.write("Visualise rapidement le coût total à différents niveaux d'enchère.")

    start = st.number_input("Départ (€)", min_value=0, value=15000, step=500)
    stop = st.number_input("Fin (€)", min_value=int(start), value=max(int(start), 30000), step=500)
    step = st.number_input("Pas (€)", min_value=100, value=1000, step=100)

    rows = []
    current = int(start)
    while current <= int(stop):
        fee, invoice, total = auction_total(
            current,
            buyer_rate_pct,
            min_buyer_fee,
            sale_fee,
            live_fee,
            moba_fee,
            recharge_fee,
            0.0,
            0.0,
            0.0,
        )
        rows.append({
            "Prix marteau": eur(current),
            "Frais enchères": eur(invoice - current),
            "Total bordereau": eur(invoice),
        })
        current += int(step)

    st.dataframe(rows, use_container_width=True, hide_index=True)

with st.expander("ℹ️ Hypothèses Alcopa 2026"):
    st.markdown(
        """
- Frais d'adjudication automobile : **14,40 % TTC**, minimum **360 € TTC**.
- Frais de vente France : **225 € TTC** avec CIRANO, **140 € TTC** sinon.
- Alcopa LIVE / enchère plafond : **45 € TTC**.
- Interencheres LIVE : **80 € TTC**.
- Check-up batterie MOBA : **45 € TTC** si applicable.
- Recharge batterie de traction : **25 € TTC** si demandée et applicable.

Les conditions propres à une vente ou à un lot peuvent différer. Le bordereau de la maison de vente fait foi.
"""
    )
    st.link_button(
        "Consulter les CGV Alcopa",
        "https://s3.eu-west-3.amazonaws.com/public-doc.alcopa-auction.fr/CGV/Alcopa-Auction_CGV_FR.pdf",
    )

st.caption("FR Auction Cars · Calculateur indicatif d'enchères automobiles")
