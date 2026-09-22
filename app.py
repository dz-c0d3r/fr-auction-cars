import streamlit as st

st.set_page_config(
    page_title="FR Auction Cars",
    page_icon="🔨",
    layout="centered",
)

PROFILES = {
    "Alcopa Auction (2026)": {
        "mode": "percent",
        "rate": 14.40,
        "min_fee": 360.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 225.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 80.0,
        "live_house": 45.0,
        "storage_day": 0.0,
        "note": "Profil Alcopa 2026. Le forfait de 225 € correspond au cas CIRANO ; certains lots peuvent être à 140 €. MOBA/recharge restent à ajouter si indiqués.",
    },
    "Interencheres — judiciaire standard": {
        "mode": "percent",
        "rate": 14.28,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 72.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "note": "Interencheres indique 14,28 % TTC pour les ventes judiciaires et 72 € TTC de frais Internet véhicule si refacturés. Les conditions du lot peuvent prévoir d'autres frais.",
    },
    "APONEM — VP volontaire (13 % + 200 €)": {
        "mode": "percent",
        "rate": 13.0,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 200.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 72.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "note": "Profil observé sur plusieurs lots APONEM en septembre 2026. Certains véhicules ont 300 € de dossier : vérifie toujours le lot.",
    },
    "APONEM — VP volontaire (13 % + 300 €)": {
        "mode": "percent",
        "rate": 13.0,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 300.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 72.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "note": "Profil observé sur plusieurs VP APONEM. Le montant du dossier varie selon le lot.",
    },
    "APONEM — utilitaire (15 % + 300 €)": {
        "mode": "percent",
        "rate": 15.0,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 300.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 72.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "note": "Profil observé sur des utilitaires APONEM. Des lots particuliers affichent des dossiers supérieurs : saisis le montant exact de l'annonce.",
    },
    "VPauto — frais de vente inclus": {
        "mode": "included",
        "rate": 0.0,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 200.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 80.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "note": "VPauto annonce sur de nombreux lots que les frais de vente sont inclus dans le prix, hors dossier et Interencheres.",
    },
    "VPauto — électrique + certificat batterie": {
        "mode": "included",
        "rate": 0.0,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 285.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 80.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "note": "Profil VPauto observé pour les électriques avec certificat de santé batterie : 285 € de dossier + 80 € Interencheres, frais de vente inclus.",
    },
    "Concarneau — judiciaire (exemple observé)": {
        "mode": "percent",
        "rate": 14.28,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 70.0,
        "availability": 0.0,
        "admin": 54.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 72.0,
        "live_house": 0.0,
        "storage_day": 20.0,
        "note": "Exemple observé : 14,28 % + 70 € CT + 54 € dossier administratif + frais Interencheres + gardiennage éventuel.",
    },
    "Giraudeau — volontaire dégressif (exemple)": {
        "mode": "tiered",
        "rate": 0.0,
        "min_fee": 0.0,
        "tier_threshold": 3000.0,
        "tier_rate_1": 15.0,
        "tier_rate_2": 12.5,
        "dossier": 99.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 30.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "note": "Exemple de barème dégressif publié : 15 % jusqu'à 3 000 €, puis 12,5 % au-delà, + 99 € dossier et 30 € Live. Vérifie la vente concernée.",
    },
    "BCA France — Mix / Premium / Utilitaires / Accidentés": {
        "mode": "percent",
        "rate": 3.9,
        "min_fee": 500.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 18.0,
        "fees_vat": 20.0,
        "note": "BCA France — frais acheteur 3,9 % HT du prix d'adjudication TTC, minimum 500 € HT. Profil courant pour Mix, Premium, Utilitaires, véhicules accidentés, Véhiposte, Click'N Go, Tesla Trade-In, etc.",
    },
    "BCA France — Mise à prix 50 € / En panne": {
        "mode": "percent",
        "rate": 3.9,
        "min_fee": 390.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 18.0,
        "fees_vat": 20.0,
        "note": "BCA France — 3,9 % HT, minimum 390 € HT pour les ventes Mise à prix 50 € et véhicules en panne.",
    },
    "BCA France — VO pour pièces": {
        "mode": "percent",
        "rate": 3.9,
        "min_fee": 250.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 18.0,
        "fees_vat": 20.0,
        "note": "BCA France — 3,9 % HT avec minimum 250 € HT pour les véhicules vendus pour pièces.",
    },
    "BCA France — Leasing": {
        "mode": "fixed",
        "rate": 0.0,
        "min_fee": 500.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 18.0,
        "fees_vat": 20.0,
        "note": "BCA France — forfait acheteur 500 € HT par véhicule sur les ventes Leasing.",
    },
    "BCA France — Ventes européennes 100 % BEV": {
        "mode": "fixed",
        "rate": 0.0,
        "min_fee": 500.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 40.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 18.0,
        "fees_vat": 20.0,
        "note": "BCA France — forfait 500 € HT. Le supplément AVILOO de 40 € HT s'applique uniquement si le véhicule dispose du rapport de santé batterie.",
    },
    "BCA France — Alphabet": {
        "mode": "fixed",
        "rate": 0.0,
        "min_fee": 350.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 18.0,
        "fees_vat": 20.0,
        "note": "BCA France — forfait acheteur Alphabet 350 € HT par véhicule.",
    },
    "BCA France — Hertz": {
        "mode": "fixed",
        "rate": 0.0,
        "min_fee": 250.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 18.0,
        "fees_vat": 20.0,
        "note": "BCA France — forfait acheteur Hertz 250 € HT par véhicule.",
    },
    "BCA France — Euroshop": {
        "mode": "percent",
        "rate": 3.0,
        "min_fee": 450.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 18.0,
        "fees_vat": 20.0,
        "note": "BCA France — Euroshop : 3 % HT avec minimum 450 € HT.",
    },
    "AUTO1.com France — tarifs 08/04/2026": {
        "mode": "included",
        "rate": 0.0,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 15.0,
        "note": "AUTO1 est une plateforme B2B réservée aux professionnels auto. La commission d'enchère (jusqu'à 1 950 € net selon le véhicule) est indiquée comme incluse dans l'offre. S'ajoutent surtout logistique + administratif selon le pays d'origine, puis options éventuelles.",
    },
    "Personnalisé": {
        "mode": "percent",
        "rate": 0.0,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "note": "Saisis exactement les frais indiqués dans la fiche du lot et les conditions de vente.",
    },
}

MODE_LABELS = {
    "percent": "Pourcentage",
    "fixed": "Forfait fixe",
    "included": "Frais de vente inclus dans le marteau",
    "tiered": "Barème par tranches",
}

AUTO1_ORIGIN_FEES = {
    "France": {"logistics": 319.0, "domestic": 99.0, "export": 109.0},
    "Autriche": {"logistics": 309.0, "domestic": 159.0, "export": 169.0},
    "Belgique": {"logistics": 299.0, "domestic": 119.0, "export": 159.0},
    "Allemagne": {"logistics": 299.0, "domestic": 119.0, "export": 159.0},
    "Danemark": {"logistics": 279.0, "domestic": 129.0, "export": 139.0},
    "Espagne": {"logistics": 279.0, "domestic": 199.0, "export": 265.0},
    "Finlande": {"logistics": 249.0, "domestic": 119.0, "export": 129.0},
    "Italie": {"logistics": 239.0, "domestic": 339.0, "export": 399.0},
    "Pays-Bas": {"logistics": 279.0, "domestic": 109.0, "export": 205.0},
    "Pologne": {"logistics": 179.0, "domestic": 79.0, "export": 109.0},
    "Portugal": {"logistics": 209.0, "domestic": 209.0, "export": 209.0},
    "Suède": {"logistics": 302.0, "domestic": 89.0, "export": 169.0},
}


def eur(value: float) -> str:
    return f"{value:,.2f} €".replace(",", " ").replace(".", ",")


def buyer_fee(
    hammer: float,
    mode: str,
    rate: float,
    min_fee: float,
    tier_threshold: float,
    tier_rate_1: float,
    tier_rate_2: float,
) -> float:
    if hammer <= 0 or mode == "included":
        return 0.0

    if mode == "fixed":
        return min_fee

    if mode == "tiered":
        first = min(hammer, tier_threshold) * tier_rate_1 / 100.0
        second = max(hammer - tier_threshold, 0.0) * tier_rate_2 / 100.0
        return first + second

    return max(hammer * rate / 100.0, min_fee)


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
):
    adjudication_fee_net = buyer_fee(
        hammer,
        mode,
        rate,
        min_fee,
        tier_threshold,
        tier_rate_1,
        tier_rate_2,
    )
    storage_fee_net = storage_days * storage_day_fee

    auction_extras_net = (
        dossier
        + live_fee
        + ct_fee
        + availability_fee
        + admin_fee
        + warranty_fee
        + battery_fee
        + other_fee
        + storage_fee_net
    )

    taxable_fees_net = adjudication_fee_net + auction_extras_net
    fee_vat_amount = taxable_fees_net * fee_vat_rate / 100.0
    auction_invoice = hammer + taxable_fees_net + fee_vat_amount
    grand_total = auction_invoice + registration_fee + transport_fee + repair_budget

    return {
        "adjudication_fee": adjudication_fee_net,
        "storage_fee": storage_fee_net,
        "auction_extras": auction_extras_net,
        "fee_vat_amount": fee_vat_amount,
        "auction_invoice": auction_invoice,
        "grand_total": grand_total,
    }


def max_hammer_for_budget(budget: float, calc_kwargs: dict) -> float:
    if budget <= 0:
        return 0.0

    low = 0.0
    high = budget

    for _ in range(80):
        mid = (low + high) / 2.0
        result = calculate(hammer=mid, **calc_kwargs)
        if result["grand_total"] <= budget:
            low = mid
        else:
            high = mid

    return low


st.title("🔨 FR Auction Cars")
st.caption("Calculateur multi-maisons pour estimer le vrai coût d'un véhicule aux enchères")

with st.sidebar:
    st.header("🏛️ Profil de vente")

    profile_name = st.selectbox(
        "Maison / type de vente",
        list(PROFILES.keys()),
        index=0,
    )
    p = PROFILES[profile_name]
    is_auto1 = profile_name.startswith("AUTO1.com")
    is_bca = profile_name.startswith("BCA France")

    st.info(p["note"])

    mode_options = ["percent", "fixed", "included", "tiered"]
    mode = st.selectbox(
        "Type de frais acheteur",
        mode_options,
        index=mode_options.index(p["mode"]),
        format_func=lambda x: MODE_LABELS[x],
        key=f"mode_{profile_name}",
    )

    if mode == "percent":
        rate = st.number_input(
            "Frais d'adjudication (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(p["rate"]),
            step=0.10,
            format="%.2f",
            key=f"rate_{profile_name}",
        )
        min_fee = st.number_input(
            "Minimum de frais (€ TTC)",
            min_value=0.0,
            value=float(p["min_fee"]),
            step=10.0,
            key=f"min_{profile_name}",
        )
        tier_threshold = 0.0
        tier_rate_1 = 0.0
        tier_rate_2 = 0.0

    elif mode == "fixed":
        min_fee = st.number_input(
            "Forfait acheteur (€ HT si TVA sur frais > 0)",
            min_value=0.0,
            value=float(p["min_fee"]),
            step=10.0,
            key=f"fixed_{profile_name}",
        )
        rate = 0.0
        tier_threshold = 0.0
        tier_rate_1 = 0.0
        tier_rate_2 = 0.0

    elif mode == "tiered":
        tier_threshold = st.number_input(
            "Seuil de tranche (€)",
            min_value=0.0,
            value=float(p["tier_threshold"]),
            step=100.0,
            key=f"threshold_{profile_name}",
        )
        tier_rate_1 = st.number_input(
            "Taux tranche 1 (%)",
            min_value=0.0,
            value=float(p["tier_rate_1"]),
            step=0.10,
            key=f"tier1_{profile_name}",
        )
        tier_rate_2 = st.number_input(
            "Taux au-delà du seuil (%)",
            min_value=0.0,
            value=float(p["tier_rate_2"]),
            step=0.10,
            key=f"tier2_{profile_name}",
        )
        rate = 0.0
        min_fee = 0.0

    else:
        rate = 0.0
        min_fee = 0.0
        tier_threshold = 0.0
        tier_rate_1 = 0.0
        tier_rate_2 = 0.0
        st.success("Les frais acheteur en % sont considérés comme déjà inclus dans le prix marteau.")

    fee_vat_rate = st.number_input(
        "TVA sur les frais (%)",
        min_value=0.0,
        max_value=30.0,
        value=float(p.get("fees_vat", 0.0)),
        step=1.0,
        help="BCA publie ses frais en HT. Pour une facture française classique, 20 % de TVA sur les frais permet d'estimer le décaissement TTC.",
        key=f"fees_vat_{profile_name}",
    )

    st.divider()
    st.subheader("🌐 Canal d'enchère")

    if is_auto1:
        platform = "AUTO1.com"
        live_fee = 0.0
        st.success("AUTO1.com : pas de frais Live séparés. La commission d'enchère est incluse dans l'offre affichée.")
    else:
        platform = st.selectbox(
            "Canal",
            ["Interencheres LIVE / Chrono", "LIVE de la maison", "Salle / ordre hors Internet"],
            key=f"platform_{profile_name}",
        )

        if platform == "Interencheres LIVE / Chrono":
            default_live = p["live_inter"]
        elif platform == "LIVE de la maison":
            default_live = p["live_house"]
        else:
            default_live = 0.0

        live_fee = st.number_input(
            "Frais Internet / plateforme (€ TTC)",
            min_value=0.0,
            value=float(default_live),
            step=1.0,
            key=f"live_{profile_name}_{platform}",
        )

    st.divider()
    st.subheader("🧾 Frais fixes du lot")

    if is_auto1:
        auto1_origin = st.selectbox(
            "Pays de provenance du véhicule",
            list(AUTO1_ORIGIN_FEES.keys()),
            index=0,
            key="auto1_origin",
        )
        auto1_admin_mode = st.radio(
            "Service administratif",
            ["Domestique", "Export"],
            horizontal=True,
            key="auto1_admin_mode",
        )
        origin = AUTO1_ORIGIN_FEES[auto1_origin]

        dossier = st.number_input(
            "AUTO1 — frais logistique (€ net)",
            min_value=0.0,
            value=float(origin["logistics"]),
            step=1.0,
            key=f"auto1_logistics_{auto1_origin}",
        )
        admin_default = origin["domestic"] if auto1_admin_mode == "Domestique" else origin["export"]
        admin_fee = st.number_input(
            "AUTO1 — service administratif (€ net)",
            min_value=0.0,
            value=float(admin_default),
            step=1.0,
            key=f"auto1_admin_{auto1_origin}_{auto1_admin_mode}",
        )

        second_tires = st.toggle("Manutention du 2e jeu de pneus (+29 € net)", value=False, key="auto1_tires")
        other_fee = 29.0 if second_tires else 0.0

        included_commission = st.number_input(
            "Commission d'enchère incluse dans l'offre (€ net, informatif)",
            min_value=0.0,
            max_value=1950.0,
            value=0.0,
            step=10.0,
            key="auto1_commission_info",
            help="Ne s'ajoute pas au total : AUTO1 indique que cette commission est comprise dans l'offre. Le minimum applicable est affiché sur le véhicule et le montant final sur la confirmation de vente.",
        )
        st.caption(
            "Grille AUTO1 France du 08/04/2026 : montants nets de TVA. "
            "Le traitement TVA dépend de la facture ; des services B2B intracommunautaires peuvent être en autoliquidation."
        )

        ct_fee = 0.0
        availability_fee = 0.0
        warranty_fee = 0.0
        battery_fee = 0.0
    else:
        included_commission = 0.0
        dossier = st.number_input(
            "Dossier / frais de vente fixes (€)",
            min_value=0.0,
            value=float(p["dossier"]),
            step=10.0,
            key=f"dossier_{profile_name}",
        )
        ct_fee = st.number_input(
            "Contrôle technique (€)",
            min_value=0.0,
            value=float(p["ct"]),
            step=10.0,
            key=f"ct_{profile_name}",
        )
        availability_fee = st.number_input(
            "Mise à disposition (€)",
            min_value=0.0,
            value=float(p["availability"]),
            step=10.0,
            key=f"availability_{profile_name}",
        )
        admin_fee = st.number_input(
            "Administratif / carte grise via étude (€)",
            min_value=0.0,
            value=float(p["admin"]),
            step=10.0,
            key=f"admin_{profile_name}",
        )
        warranty_fee = st.number_input(
            "Garantie mécanique (€)",
            min_value=0.0,
            value=float(p["warranty"]),
            step=10.0,
            key=f"warranty_{profile_name}",
        )
        battery_fee = st.number_input(
            "Certificat / santé batterie (€)",
            min_value=0.0,
            value=float(p["battery"]),
            step=5.0,
            key=f"battery_{profile_name}",
        )
        other_fee = st.number_input(
            "Autres frais fixes (€)",
            min_value=0.0,
            value=float(p["other"]),
            step=10.0,
            key=f"other_{profile_name}",
        )

    if is_bca:
        st.divider()
        st.subheader("🇫🇷 Options BCA France")

        bca_registration = st.toggle("Premier compte BCA : inscription unique (+99 € HT)", value=False, key=f"bca_registration_{profile_name}")
        bca_export = st.toggle("Frais export (+140 € HT)", value=False, key=f"bca_export_{profile_name}")
        bca_pickup = st.toggle("Retrait / collecte (+30 € HT)", value=False, key=f"bca_pickup_{profile_name}")
        bca_recovery = st.toggle("Recovery fee (+40 € HT)", value=False, key=f"bca_recovery_{profile_name}")

        if bca_registration:
            other_fee += 99.0
        if bca_export:
            other_fee += 140.0
        if bca_pickup:
            other_fee += 30.0
        if bca_recovery:
            other_fee += 40.0

        if profile_name == "BCA France — Ventes européennes 100 % BEV":
            has_aviloo = st.toggle("Le véhicule a un rapport AVILOO (+40 € HT)", value=True, key="bca_aviloo")
            battery_fee = 40.0 if has_aviloo else 0.0

        st.caption(
            "Stockage BCA France : 18 € HT/jour. La facturation démarre généralement au 14e jour pour un véhicule roulant acheté depuis la France, "
            "et au 22e jour pour VHU/accidenté/non roulant. Entre uniquement les jours réellement facturés dans la section Gardiennage."
        )

    st.divider()
    st.subheader("🅿️ Gardiennage")

    storage_day_fee = st.number_input(
        "Tarif par jour (€)",
        min_value=0.0,
        value=float(p["storage_day"]),
        step=5.0,
        key=f"storage_rate_{profile_name}",
    )
    storage_days = st.number_input(
        "Nombre de jours facturés",
        min_value=0,
        value=0,
        step=1,
        key=f"storage_days_{profile_name}",
    )

tabs = st.tabs([
    "💶 Coût total",
    "🎯 Enchère max",
    "📊 Paliers",
    "ℹ️ Guide",
])

with tabs[0]:
    hammer = st.number_input(
        "Prix remporté / prix au marteau (€)",
        min_value=0.0,
        value=20000.0,
        step=100.0,
        key="hammer_main",
    )

    st.subheader("Après la vente")
    c1, c2 = st.columns(2)

    with c1:
        registration_fee = st.number_input(
            "Carte grise finale (€)",
            min_value=0.0,
            value=0.0,
            step=10.0,
            key="registration_main",
        )
        transport_fee = st.number_input(
            "Transport / déplacement (€)",
            min_value=0.0,
            value=0.0,
            step=25.0,
            key="transport_main",
        )

    with c2:
        repair_budget = st.number_input(
            "Entretien / réparations (€)",
            min_value=0.0,
            value=0.0,
            step=50.0,
            key="repairs_main",
        )

    result = calculate(
        hammer=hammer,
        mode=mode,
        rate=rate,
        min_fee=min_fee,
        tier_threshold=tier_threshold,
        tier_rate_1=tier_rate_1,
        tier_rate_2=tier_rate_2,
        dossier=dossier,
        live_fee=live_fee,
        ct_fee=ct_fee,
        availability_fee=availability_fee,
        admin_fee=admin_fee,
        warranty_fee=warranty_fee,
        battery_fee=battery_fee,
        other_fee=other_fee,
        storage_days=int(storage_days),
        storage_day_fee=storage_day_fee,
        registration_fee=registration_fee,
        transport_fee=transport_fee,
        repair_budget=repair_budget,
        fee_vat_rate=fee_vat_rate,
    )

    st.divider()

    m1, m2, m3 = st.columns(3)
    m1.metric("Prix marteau", eur(hammer))
    m2.metric("Frais enchères", eur(result["auction_invoice"] - hammer))
    m3.metric("TOTAL", eur(result["grand_total"]))

    st.subheader("Détail")

    lines = [("Prix d'adjudication", hammer)]

    if result["adjudication_fee"]:
        if mode == "tiered":
            label = f"Frais acheteur ({tier_rate_1:.2f}% / {tier_rate_2:.2f}%)"
        else:
            label = f"Frais d'adjudication ({rate:.2f} %)"
        lines.append((label, result["adjudication_fee"]))
    elif mode == "included":
        if is_auto1:
            lines.append(("Commission AUTO1 incluse dans l'offre", included_commission))
        else:
            lines.append(("Frais de vente inclus dans le prix marteau", 0.0))

    dossier_label = "AUTO1 — frais logistique" if is_auto1 else "Dossier / frais fixes"
    admin_label = "AUTO1 — service administratif" if is_auto1 else "Administratif"
    other_label = "AUTO1 — 2e jeu de pneus" if is_auto1 else "Autres frais"

    fixed_lines = [
        (dossier_label, dossier),
        (f"Plateforme — {platform}", live_fee),
        ("Contrôle technique", ct_fee),
        ("Mise à disposition", availability_fee),
        (admin_label, admin_fee),
        ("Garantie mécanique", warranty_fee),
        ("Certificat / santé batterie", battery_fee),
        (other_label, other_fee),
        (f"Gardiennage ({int(storage_days)} j)", result["storage_fee"]),
        ("Carte grise finale", registration_fee),
        ("Transport / déplacement", transport_fee),
        ("Entretien / réparations", repair_budget),
    ]

    lines.extend((label, amount) for label, amount in fixed_lines if amount)

    if result["fee_vat_amount"]:
        lines.append((f"TVA sur les frais ({fee_vat_rate:.0f} %)", result["fee_vat_amount"]))

    for label, amount in lines:
        left, right = st.columns([3, 1])
        left.write(label)
        right.markdown(f"**{eur(amount)}**")

    st.success(f"Total à prévoir : **{eur(result['grand_total'])}**")
    st.caption(f"Bordereau de la maison de vente estimé : {eur(result['auction_invoice'])}")

with tabs[1]:
    budget = st.number_input(
        "Budget maximum tout compris (€)",
        min_value=0.0,
        value=25000.0,
        step=100.0,
        key="budget_max",
    )

    d1, d2 = st.columns(2)
    with d1:
        reg_budget = st.number_input(
            "Carte grise (€)",
            min_value=0.0,
            value=0.0,
            step=10.0,
            key="reg_budget",
        )
        transport_budget = st.number_input(
            "Transport (€)",
            min_value=0.0,
            value=0.0,
            step=25.0,
            key="transport_budget",
        )

    with d2:
        repair_budget2 = st.number_input(
            "Réparations / entretien (€)",
            min_value=0.0,
            value=0.0,
            step=50.0,
            key="repair_budget",
        )

    calc_kwargs = {
        "mode": mode,
        "rate": rate,
        "min_fee": min_fee,
        "tier_threshold": tier_threshold,
        "tier_rate_1": tier_rate_1,
        "tier_rate_2": tier_rate_2,
        "dossier": dossier,
        "live_fee": live_fee,
        "ct_fee": ct_fee,
        "availability_fee": availability_fee,
        "admin_fee": admin_fee,
        "warranty_fee": warranty_fee,
        "battery_fee": battery_fee,
        "other_fee": other_fee,
        "storage_days": int(storage_days),
        "storage_day_fee": storage_day_fee,
        "registration_fee": reg_budget,
        "transport_fee": transport_budget,
        "repair_budget": repair_budget2,
        "fee_vat_rate": fee_vat_rate,
    }

    max_hammer = max_hammer_for_budget(budget, calc_kwargs)
    max_result = calculate(hammer=max_hammer, **calc_kwargs)

    st.metric("Enchère maximale théorique", eur(max_hammer))
    st.warning("En Live, garde une marge et arrondis au palier inférieur.")
    st.caption(
        f"Bordereau estimé : {eur(max_result['auction_invoice'])} · "
        f"Total tout compris : {eur(max_result['grand_total'])}"
    )

with tabs[2]:
    st.write("Visualise instantanément le coût réel à plusieurs niveaux d'enchère.")

    start = st.number_input("Départ (€)", min_value=0, value=15000, step=500, key="grid_start")
    stop = st.number_input(
        "Fin (€)",
        min_value=int(start),
        value=max(int(start), 30000),
        step=500,
        key="grid_stop",
    )
    step = st.number_input("Pas (€)", min_value=100, value=1000, step=100, key="grid_step")

    rows = []
    current = int(start)

    while current <= int(stop):
        r = calculate(
            hammer=current,
            mode=mode,
            rate=rate,
            min_fee=min_fee,
            tier_threshold=tier_threshold,
            tier_rate_1=tier_rate_1,
            tier_rate_2=tier_rate_2,
            dossier=dossier,
            live_fee=live_fee,
            ct_fee=ct_fee,
            availability_fee=availability_fee,
            admin_fee=admin_fee,
            warranty_fee=warranty_fee,
            battery_fee=battery_fee,
            other_fee=other_fee,
            storage_days=int(storage_days),
            storage_day_fee=storage_day_fee,
            registration_fee=0.0,
            transport_fee=0.0,
            repair_budget=0.0,
            fee_vat_rate=fee_vat_rate,
        )

        rows.append({
            "Prix marteau": eur(current),
            "Frais enchères": eur(r["auction_invoice"] - current),
            "Total bordereau": eur(r["auction_invoice"]),
        })
        current += int(step)

    st.dataframe(rows, use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("Pourquoi les frais changent-ils ?")
    st.markdown(
        """
Le prix marteau n'est souvent qu'une partie du coût réel.

**Les principaux facteurs sont :**

- **nature de la vente** : volontaire, judiciaire ou mixte ;
- **maison de vente** : les frais volontaires sont fixés par chaque maison ;
- **canal d'enchère** : Interencheres Live/Chrono, Live propre à la maison ou salle ;
- **type de lot** : VP, utilitaire, électrique, véhicule garanti ou non ;
- **frais fixes** : dossier, mise à disposition, contrôle technique, formalités administratives ;
- **batterie** : certificat de santé, MOBA ou recharge selon les opérateurs ;
- **retard d'enlèvement** : gardiennage/parking facturé à la journée ;
- **professionnel / TVA** : la TVA récupérable dépend du lot et du régime de facturation, elle n'est donc pas déduite automatiquement ici.
"""
    )

    st.warning(
        "La fiche du lot et les conditions de vente priment toujours sur le profil prérempli. "
        "Certains lots d'une même maison ont des frais différents."
    )

    st.subheader("Exemples actuellement pris en charge")
    st.markdown(
        """
- **Alcopa** : pourcentage + minimum + forfait + canal Live ;
- **Interencheres judiciaire** : taux judiciaire + frais Internet véhicule ;
- **APONEM** : profils 13 % ou 15 % + dossier variable ;
- **VPauto** : frais de vente inclus + dossier + frais Interencheres ;
- **BCA France** : profils Mix/Premium, En panne, pièces, Leasing, BEV, Alphabet, Hertz et Euroshop + TVA/frais annexes ;
- **AUTO1.com France** : commission incluse dans l'offre + logistique/admin selon provenance + pneus/transport/parking éventuels ;
- **Concarneau** : judiciaire + CT + administratif + gardiennage ;
- **barème dégressif** : deux taux selon un seuil ;
- **Personnalisé** : tous les champs sont libres.
"""
    )

st.caption(
    "FR Auction Cars · Calculateur indicatif. Les conditions de la maison de vente et du lot font foi."
)
