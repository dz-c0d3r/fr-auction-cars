import streamlit as st

from auction_math import calculate, eur, max_hammer_at_step, max_hammer_for_budget

MERCIER_VOLUNTARY = "Mercier Auto — volontaire (2026)"
MERCIER_JUDICIAL = "Mercier Auto — judiciaire (2026)"
MERCIER_CONDITIONS_URL = "https://www.mercier.com/p/conditions-generales-de-vente/"
MERCIER_SALE_URL = "https://www.mercier.com/auto/vente/vente-vehicules-mixte-01a11587-e2f0-7111-82bf-c2c388f9b058/"
GOLF_LOT_URL = "https://www.interencheres.com/vehicules/vente-de-vehicules-a-marcq-en-baroeul-59-689782/lot-89424537.html"

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
    MERCIER_VOLUNTARY: {
        "mode": "percent",
        "rate": 14.28,
        "min_fee": 360.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 120.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 60.0,
        "live_house": 30.0,
        "storage_day": 20.0,
        "fees_vat": 0.0,
        "note": "Mercier Auto : 14,28 % TTC (minimum 360 € en volontaire), dossier 120 € TTC + supplément Live de 30 € sur Mercier Live ou 60 € sur Interencheres. Les forfaits totaux sont donc 120 / 150 / 180 €. Barème voitures et utilitaires ; hors prestige et poids lourds.",
    },
    MERCIER_JUDICIAL: {
        "mode": "percent",
        "rate": 14.28,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 120.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 60.0,
        "live_house": 30.0,
        "storage_day": 20.0,
        "fees_vat": 0.0,
        "note": "Mercier Auto judiciaire : 14,28 % TTC, sans le minimum volontaire de 360 €. Dossier et canal préremplis selon le barème Mercier, à confirmer pour le lot. Une vente mixte n'indique pas à elle seule la nature de chaque lot.",
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
        "dossier": 150.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 80.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "note": "VPauto : les enchères sont portées frais de vente inclus. Frais de dossier actuels : 150 € TTC pour thermique/hybride/EV sans certificat batterie.",
    },
    "VPauto — électrique + certificat batterie": {
        "mode": "included",
        "rate": 0.0,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 235.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 80.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "note": "VPauto : enchères frais de vente inclus. Pour un électrique avec certificat de santé batterie, les frais de dossier actuels sont de 235 € TTC.",
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
    "Enchères du Domaine — État français": {
        "mode": "percent",
        "rate": 11.0,
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
        "fees_vat": 0.0,
        "note": "Ventes du Domaine : taxe domaniale forfaitaire de 11 % ajoutée au prix d'adjudication. Pour les véhicules de fourrière, des frais de garde peuvent s'ajouter directement auprès du gardien.",
    },
    "OVEO — barème services 2026": {
        "mode": "tiered",
        "rate": 0.0,
        "min_fee": 0.0,
        "tier_threshold": 10000.0,
        "tier_rate_1": 7.0,
        "tier_rate_2": 5.0,
        "dossier": 0.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 5.0,
        "fees_vat": 20.0,
        "note": "OVEO : frais de service progressifs, 7 % sur les premiers 10 000 € puis 5 % au-delà. Base HT si TVA véhicule récupérable, sinon base TTC. Stockage possible à 5 € HT/jour après 12 jours ouvrés.",
    },
    "Autorola France — barème standard": {
        "mode": "autorola",
        "rate": 0.0,
        "min_fee": 0.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 35.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "fees_vat": 20.0,
        "note": "Autorola France : barème acheteur HT selon le prix vendu TTC, de 325 € HT à 1 825 € HT, plus 35 € HT de frais administratifs.",
    },
    "Autorola France — ventes à frais fixes 300 € HT": {
        "mode": "fixed",
        "rate": 0.0,
        "min_fee": 300.0,
        "tier_threshold": 0.0,
        "tier_rate_1": 0.0,
        "tier_rate_2": 0.0,
        "dossier": 35.0,
        "ct": 0.0,
        "availability": 0.0,
        "admin": 0.0,
        "warranty": 0.0,
        "battery": 0.0,
        "other": 0.0,
        "live_inter": 0.0,
        "live_house": 0.0,
        "storage_day": 0.0,
        "fees_vat": 20.0,
        "note": "Plusieurs ventes France actuelles Autorola annoncent explicitement des frais acheteurs fixes de 300 € HT. Le forfait administratif standard de 35 € HT est laissé séparément et modifiable.",
    },
    "Agorastore — barème véhicules 15 % + dossier": {
        "mode": "percent",
        "rate": 15.0,
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
        "fees_vat": 20.0,
        "note": "Barème Agorastore observé dans des contrats publics 2026 : 15 % HT du prix final + frais de dossier véhicule de 10 à 500 € HT selon la mise à prix. Certains lots ont un barème différent : vérifie la fiche.",
    },
    "Agorastore — prix affiché frais inclus": {
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
        "storage_day": 0.0,
        "fees_vat": 0.0,
        "note": "À utiliser lorsque la fiche Agorastore indique explicitement « frais inclus dans le prix affiché ». Des lots 2026 affichent par exemple 14,4 % + 90 € TTC ou 18 % + dossier, déjà inclus dans le prix affiché.",
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
    "Enchères VO — frais selon la vente": {
        "mode": "fixed",
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
        "fees_vat": 0.0,
        "note": "Enchères VO : le tarif dépend de la vente. Certaines offres grand public sont affichées tous frais inclus ; une vente de collection 2026 publiée avec Enchères VO affichait 20 % TTC. Entre le taux/forfait exact indiqué dans les conditions du lot.",
    },
    "Ayvens Carmarket France — frais variables": {
        "mode": "fixed",
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
        "fees_vat": 0.0,
        "note": "Ayvens Carmarket confirme des frais en plus du prix du véhicule, ainsi que transport et éventuellement COC, mais ne publie pas de barème France unique. Saisis le montant affiché dans ton espace Carmarket.",
    },
    "Arval MotorTrade France — frais de gestion variables": {
        "mode": "fixed",
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
        "fees_vat": 0.0,
        "note": "Arval MotorTrade indique que des frais de gestion sont dus à l'achat, mais le montant n'est pas publié publiquement et doit être obtenu auprès du responsable de compte. Entre ici le montant de ton offre/facture.",
    },
    "OPENLANE Europe — achat depuis la France": {
        "mode": "fixed",
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
        "fees_vat": 0.0,
        "note": "OPENLANE 2026 : frais d'enchère + frais pays + parfois frais vendeur, tous variables et affichés sur le véhicule. Options publiques : Optimo 160 €, prise en charge 85 € si transport international organisé par l'acheteur, document EX 110 € hors UE.",
    },
    "Clickar / Leasys France": {
        "mode": "fixed",
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
        "storage_day": 10.0,
        "fees_vat": 20.0,
        "note": "Clickar/Leasys : les CGV publiques n'indiquent pas de commission acheteur standard ; prix véhicule hors immatriculation, carburant et acheminement. Gardiennage : 10 € HT/jour après le délai d'enlèvement de 10 jours ouvrés.",
    },
    "CarOnSale — frais à partir de 99 €": {
        "mode": "fixed",
        "rate": 0.0,
        "min_fee": 99.0,
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
        "fees_vat": 0.0,
        "note": "CarOnSale : inscription gratuite, frais uniquement si achat réussi. Le site public indique des frais à partir de 99 €, plafonnés, avec montant exact visible dans le compte. Modifie le forfait selon le véhicule.",
    },
    "eCarsTrade — véhicules provenant de France": {
        "mode": "ecars_other",
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
        "fees_vat": 0.0,
        "note": "eCarsTrade : pour une voiture provenant de France (catégorie « autres pays »), commission + administratif : 250 € jusqu'à 5k, 300 € jusqu'à 10k, 350 € jusqu'à 20k, puis 400 € + 50 € par tranche de 10k supplémentaire. Transport sur devis.",
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
    "autorola": "Barème Autorola par prix",
    "ecars_other": "Barème eCarsTrade (France/autres pays)",
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



def load_mercier_golf_preset():
    """Example only: no assumed repairs, registration costs or paid deposit."""
    profile = MERCIER_VOLUNTARY
    defaults = PROFILES[profile]
    st.session_state.update({
        "sale_profile": profile,
        f"mode_{profile}": "percent",
        f"rate_{profile}": 14.28,
        f"min_{profile}": 360.0,
        f"fees_vat_{profile}": 0.0,
        f"platform_{profile}": "Interencheres LIVE / Chrono",
        f"live_{profile}_Interencheres LIVE / Chrono": 60.0,
        f"mercier_energy_{profile}": "Hybride rechargeable (PHEV)",
        f"mercier_battery_{profile}_Hybride rechargeable (PHEV)": False,
        f"mercier_price_basis_{profile}": "TTC",
        f"mercier_vehicle_vat_{profile}": 20.0,
        f"mercier_deposit_{profile}": 0.0,
        f"storage_rate_{profile}": 20.0,
        f"storage_days_{profile}": 0,
        "hammer_main": 10000.0,
        "budget_max": 12000.0,
        "budget_scope": "Tout compris",
        "reuse_after_sale": True,
        "bid_increment": 100.0,
        "registration_main": 0.0,
        "transport_main": 0.0,
        "repairs_main": 0.0,
        "reg_budget": 0.0,
        "transport_budget": 0.0,
        "repair_budget": 0.0,
        "grid_start": 8000,
        "grid_stop": 12000,
        "grid_step": 500,
        "mercier_golf_example": True,
    })
    for field in ("dossier", "ct", "availability", "admin", "warranty", "other"):
        st.session_state[f"{field}_{profile}"] = float(defaults[field])


if st.query_params.get("preset") == "mercier-golf-gte" and not st.session_state.get("mercier_link_loaded"):
    load_mercier_golf_preset()
    st.session_state["mercier_link_loaded"] = True


st.title("🔨 FR Auction Cars")
st.caption("Calculateur multi-maisons pour estimer le vrai coût d'un véhicule aux enchères")
st.button(
    "Charger l'exemple Golf GTE PHEV — Mercier",
    on_click=load_mercier_golf_preset,
    help="Exemple modifiable : 10 000 € au marteau, budget de 12 000 €, Interencheres, aucun supplément batterie ni frais après vente présumés.",
)

with st.sidebar:
    st.header("🏛️ Profil de vente")

    profile_name = st.selectbox(
        "Maison / type de vente",
        list(PROFILES.keys()),
        index=0,
        key="sale_profile",
    )
    p = PROFILES[profile_name]
    is_auto1 = profile_name.startswith("AUTO1.com")
    is_bca = profile_name.startswith("BCA France")
    is_oveo = profile_name.startswith("OVEO")
    is_agorastore = profile_name.startswith("Agorastore")
    is_openlane = profile_name.startswith("OPENLANE")
    is_mercier = profile_name.startswith("Mercier Auto")
    hammer_vat_rate = 0.0
    deposit_paid = 0.0

    st.info(p["note"])

    if is_mercier:
        st.caption(f"[Barème Mercier]({MERCIER_CONDITIONS_URL}) · vérifié le 26/10/2026")
        mercier_energy = st.selectbox(
            "Motorisation",
            ["Thermique", "Hybride (HEV)", "Hybride rechargeable (PHEV)", "Électrique (BEV)"],
            key=f"mercier_energy_{profile_name}",
        )
        if mercier_energy == "Hybride rechargeable (PHEV)":
            st.caption("PHEV : aucun supplément électrique ou batterie automatique. Active uniquement un supplément confirmé pour le lot.")
        mercier_price_basis = st.radio(
            "Montant saisi pour l'enchère",
            ["TTC", "HT à convertir en TTC"],
            key=f"mercier_price_basis_{profile_name}",
            help="Les tarifs Mercier Auto de ce profil sont TTC. La mention TVA récupérable ne déclenche aucune majoration ni déduction automatique.",
        )
        if mercier_price_basis == "HT à convertir en TTC":
            hammer_vat_rate = st.number_input(
                "TVA du véhicule à ajouter au montant HT (%)",
                min_value=0.0,
                max_value=30.0,
                value=20.0,
                step=1.0,
                key=f"mercier_vehicle_vat_{profile_name}",
            )
            st.caption("Saisie d'un équivalent HT : conversion en TTC avant calcul des frais. Vérifie si les enchères réelles sont annoncées HT ou TTC.")

    mode_options = ["percent", "fixed", "included", "tiered", "autorola", "ecars_other"]
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

    elif mode == "ecars_other":
        rate = 0.0
        min_fee = 0.0
        tier_threshold = 0.0
        tier_rate_1 = 0.0
        tier_rate_2 = 0.0
        st.caption("Commission eCarsTrade calculée automatiquement selon le montant de l'offre pour un véhicule provenant de France.")

    elif mode == "autorola":
        rate = 0.0
        min_fee = 0.0
        tier_threshold = 0.0
        tier_rate_1 = 0.0
        tier_rate_2 = 0.0
        st.caption("Barème Autorola standard appliqué automatiquement selon le prix vendu TTC.")

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
        help="Mercier : les taux et frais préremplis sont déjà TTC (0 % de TVA supplémentaire). Pour des frais publiés HT, la TVA éventuelle doit être ajoutée.",
        key=f"fees_vat_{profile_name}",
        disabled=is_mercier,
    )

    buyer_fee_base_factor = 1.0
    if is_oveo:
        oveo_recoverable_vat = st.toggle(
            "OVEO : TVA du véhicule récupérable",
            value=True,
            key="oveo_recoverable_vat",
        )
        if oveo_recoverable_vat:
            buyer_fee_base_factor = 1 / 1.20
            st.caption("OVEO calcule alors ses frais sur le prix HT du véhicule (prix TTC ÷ 1,20).")
        else:
            st.caption("TVA non récupérable : OVEO calcule ses frais sur le prix TTC.")


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
        if is_mercier:
            st.caption("Le supplément Live s'ajoute au dossier de 120 €. Ne rajoute pas une deuxième fois le forfait total ni les frais Interencheres génériques.")
            if platform == "LIVE de la maison":
                st.caption(f"Mercier Live : supplément général 30 €. La [vente du 26/10/2026]({MERCIER_SALE_URL}) annonce 180 € au total en ligne sans distinguer les canaux : saisis 60 € ici si ce forfait t'est confirmé.")

    st.divider()
    st.subheader("🧾 Frais fixes du lot")

    if is_agorastore and profile_name == "Agorastore — barème véhicules 15 % + dossier":
        agora_starting_price = st.number_input(
            "Mise à prix du lot (€ HT)",
            min_value=0.0,
            value=5000.0,
            step=100.0,
            key="agora_starting_price",
            help="Le barème de dossier public consulté est déterminé selon la mise à prix.",
        )
        if agora_starting_price <= 500:
            dossier = 10.0
        elif agora_starting_price <= 1000:
            dossier = 40.0
        elif agora_starting_price <= 3000:
            dossier = 150.0
        elif agora_starting_price <= 5000:
            dossier = 200.0
        elif agora_starting_price <= 12500:
            dossier = 400.0
        else:
            dossier = 500.0
        st.caption(f"Frais de dossier calculés automatiquement : {dossier:.0f} € HT")
        ct_fee = 0.0
        availability_fee = 0.0
        admin_fee = 0.0
        warranty_fee = 0.0
        battery_fee = 0.0
        other_fee = 0.0
        included_commission = 0.0
    elif is_auto1:
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
        if is_mercier:
            mercier_battery_confirmed = st.checkbox(
                "Supplément batterie de 40 € confirmé par Mercier",
                value=False,
                key=f"mercier_battery_{profile_name}_{mercier_energy}",
                help="Le tarif publié vise les véhicules électriques / rapports de batterie. Il n'est pas appliqué automatiquement aux hybrides rechargeables.",
            )
            battery_fee = 40.0 if mercier_battery_confirmed else 0.0
        else:
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

    if is_openlane:
        st.divider()
        st.subheader("🌍 Options OPENLANE")

        openlane_optimo = st.toggle("Service Optimo (+160 €)", value=False, key="openlane_optimo")
        openlane_pickup = st.toggle("Prise en charge transport perso international (+85 €)", value=False, key="openlane_pickup")
        openlane_ex = st.toggle("Document export EX hors UE (+110 €)", value=False, key="openlane_ex")

        if openlane_optimo:
            other_fee += 160.0
        if openlane_pickup:
            other_fee += 85.0
        if openlane_ex:
            other_fee += 110.0

        st.caption("Ajoute dans « Dossier / frais de vente fixes » le total frais d'enchère + frais pays + éventuels frais vendeur affichés sur la fiche du véhicule.")

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
    if is_mercier:
        st.caption("Enlèvement au plus tard le vendredi suivant la vente ; au-delà, 20 € TTC/jour. Entre uniquement les jours de retard facturés.")
        st.divider()
        st.subheader("Acompte et solde")
        deposit_paid = st.number_input(
            "Acompte déjà imputé à la facture (€)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key=f"mercier_deposit_{profile_name}",
            help="Saisis un acompte effectivement payé et déduit du bordereau. Une empreinte bancaire simplement bloquée n'est pas encore un acompte.",
        )
        st.caption("Empreinte Live habituelle : 2 000 €, transformée en acompte si tu remportes le lot. Elle ne s'ajoute pas au prix et ne change pas ton plafond.")

if is_mercier:
    st.info(f"**{mercier_energy}** · **{platform}** · Dossier + canal : **{eur(dossier + live_fee)}** · Supplément batterie : **{eur(battery_fee)}**")
    if st.session_state.get("mercier_golf_example"):
        st.caption(f"[Exemple Golf GTE — lot 304]({GOLF_LOT_URL}) : PHEV, 29/12/2022, 215 347 km, toit ouvrant à revoir. La vente est mixte ; le préréglage initial utilise le profil volontaire par prudence. Les montants de 10 000 € et 12 000 € sont des exemples modifiables. Ajoute tes frais après vente.")

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
        buyer_fee_base_factor=buyer_fee_base_factor,
        hammer_vat_rate=hammer_vat_rate,
    )

    st.divider()

    m1, m2, m3 = st.columns(3)
    m1.metric("À payer à la maison", eur(result["auction_invoice"]))
    m2.metric("Dont frais enchères", eur(result["auction_invoice"] - result["hammer_ttc"]))
    m3.metric("Budget tout compris", eur(result["grand_total"]))
    if hammer_vat_rate:
        st.caption(f"Prix saisi HT : {eur(hammer)} · TVA véhicule : {eur(result['hammer_vat_amount'])} · Prix véhicule TTC : {eur(result['hammer_ttc'])}")

    st.subheader("Détail")

    lines = [("Prix du véhicule TTC", result["hammer_ttc"])]

    if result["adjudication_fee"]:
        if mode == "tiered":
            label = f"Frais acheteur ({tier_rate_1:.2f}% / {tier_rate_2:.2f}%)"
        elif mode == "autorola":
            label = "Frais acheteur Autorola (barème)"
        elif mode == "ecars_other":
            label = "Commission eCarsTrade"
        elif mode == "fixed":
            label = "Frais acheteur fixes"
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
    if is_mercier and deposit_paid:
        if deposit_paid > result["auction_invoice"]:
            st.warning("L'acompte saisi dépasse le bordereau estimé : vérifie son montant.")
        else:
            st.info(f"Acompte déjà payé : **{eur(deposit_paid)}** · Solde à régler à Mercier : **{eur(result['auction_invoice'] - deposit_paid)}**. Le coût d'achat reste inchangé.")

with tabs[1]:
    budget_scope = st.radio(
        "Ce que couvre ton budget",
        ["Tout compris", "Facture de la maison uniquement"],
        key="budget_scope",
        horizontal=True,
    )
    budget = st.number_input(
        "Budget maximum disponible (€ TTC)",
        min_value=0.0,
        value=25000.0,
        step=100.0,
        key="budget_max",
    )

    reuse_after_sale = st.checkbox(
        "Reprendre les frais après vente de Coût total",
        value=True,
        key="reuse_after_sale",
        disabled=budget_scope != "Tout compris",
        help="La carte grise, le transport et les réparations sont repris automatiquement. Décoche pour simuler une autre réserve dans cet onglet.",
    )
    if reuse_after_sale:
        st.session_state["reg_budget"] = registration_fee
        st.session_state["transport_budget"] = transport_fee
        st.session_state["repair_budget"] = repair_budget

    d1, d2 = st.columns(2)
    with d1:
        reg_budget = st.number_input(
            "Carte grise (€)",
            min_value=0.0,
            value=0.0,
            step=10.0,
            key="reg_budget",
            disabled=budget_scope != "Tout compris" or reuse_after_sale,
        )
        transport_budget = st.number_input(
            "Transport (€)",
            min_value=0.0,
            value=0.0,
            step=25.0,
            key="transport_budget",
            disabled=budget_scope != "Tout compris" or reuse_after_sale,
        )

    with d2:
        repair_budget2 = st.number_input(
            "Réparations / entretien (€)",
            min_value=0.0,
            value=0.0,
            step=50.0,
            key="repair_budget",
            disabled=budget_scope != "Tout compris" or reuse_after_sale,
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
        "registration_fee": reg_budget if budget_scope == "Tout compris" else 0.0,
        "transport_fee": transport_budget if budget_scope == "Tout compris" else 0.0,
        "repair_budget": repair_budget2 if budget_scope == "Tout compris" else 0.0,
        "fee_vat_rate": fee_vat_rate,
        "buyer_fee_base_factor": buyer_fee_base_factor,
        "hammer_vat_rate": hammer_vat_rate,
    }

    bid_increment = st.number_input(
        "Pas d'enchère pour arrondir le plafond (€)",
        min_value=1.0,
        value=100.0,
        step=50.0,
        key="bid_increment",
        help="Le plafond est arrondi au multiple inférieur de ce pas. Adapte-le aux paliers acceptés pendant la vente.",
    )
    max_hammer = max_hammer_for_budget(budget, calc_kwargs)
    max_bid = max_hammer_at_step(budget, calc_kwargs, bid_increment)
    bid_unit = "HT saisi" if hammer_vat_rate else "TTC"
    st.metric(f"Enchère maximale au palier choisi ({bid_unit})", eur(max_bid))
    st.caption(f"Limite au centime avant arrondi au palier : {eur(max_hammer)} ({bid_unit}).")
    if max_bid <= 0:
        st.warning("Ce budget ne permet aucune mise positive au pas choisi, une fois les frais et réserves déduits.")
    else:
        max_result = calculate(hammer=max_bid, **calc_kwargs)
        next_bid = max_bid + bid_increment
        next_result = calculate(hammer=next_bid, **calc_kwargs)
        st.success(
            f"À ce plafond : **{eur(max_result['auction_invoice'])}** à payer à la maison · "
            f"**{eur(max_result['grand_total'])}** pour le budget retenu · "
            f"**{eur(budget - max_result['grand_total'])}** de marge."
        )
        st.warning(
            f"Le palier suivant à {eur(next_bid)} coûterait {eur(next_result['grand_total'])}, "
            f"soit {eur(next_result['grand_total'] - budget)} au-dessus de ton budget."
        )
        if hammer_vat_rate:
            st.caption(f"Équivalent du plafond en prix véhicule TTC : {eur(max_result['hammer_ttc'])}. Utilise cette base si la vente annonce ses enchères TTC.")
        if is_mercier and deposit_paid:
            st.caption("L'acompte n'est pas déduit du budget : il fait déjà partie du coût de la voiture.")

with tabs[2]:
    st.write("Visualise instantanément le coût réel à plusieurs niveaux d'enchère.")
    include_after_sale = st.checkbox(
        "Inclure les frais après vente saisis dans Coût total",
        value=True,
        key="grid_after_sale",
    )
    if hammer_vat_rate:
        st.caption("Les paliers ci-dessous sont des montants saisis HT, convertis en TTC pour calculer le bordereau.")

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
            registration_fee=registration_fee if include_after_sale else 0.0,
            transport_fee=transport_fee if include_after_sale else 0.0,
            repair_budget=repair_budget if include_after_sale else 0.0,
            fee_vat_rate=fee_vat_rate,
            buyer_fee_base_factor=buyer_fee_base_factor,
            hammer_vat_rate=hammer_vat_rate,
        )

        rows.append({
            "Prix saisi HT" if hammer_vat_rate else "Prix marteau TTC": eur(current),
            "Frais enchères": eur(r["auction_invoice"] - r["hammer_ttc"]),
            "Total bordereau": eur(r["auction_invoice"]),
            "Budget total": eur(r["grand_total"]),
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
- **Mercier Auto** : volontaire/judiciaire, 14,28 % TTC, dossier + canal, PHEV distinct d'un électrique et supplément batterie uniquement sur confirmation ;
- **Interencheres judiciaire** : taux judiciaire + frais Internet véhicule ;
- **APONEM** : profils 13 % ou 15 % + dossier variable ;
- **VPauto** : frais de vente inclus + dossier + frais Interencheres ;
- **Domaine** : taxe domaniale de 11 % ;
- **OVEO** : barème progressif 7 % / 5 % + TVA et stockage ;
- **Autorola France** : barème standard 325–1 825 € HT ou ventes à forfait 300 € HT ;
- **Agorastore** : barème 15 % + dossier par mise à prix, ou mode « frais inclus » selon le lot ;
- **Enchères VO** : profil variable selon la vente ;
- **Ayvens Carmarket** et **Arval MotorTrade** : frais variables à saisir d'après le compte/lot ;
- **OPENLANE** : frais enchère/pays/vendeur variables + options publiques ;
- **Clickar / Leasys** : frais annexes + gardiennage 10 € HT/j ;
- **CarOnSale** : frais à partir de 99 €, exacts visibles dans le compte ;
- **eCarsTrade France** : commission automatique par tranche ;
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

