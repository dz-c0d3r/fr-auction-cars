# FR Auction Cars

Calculateur Streamlit pour estimer le coût réel d'un véhicule acheté aux enchères en France.

## Fonctions

- prix au marteau → coût total estimé ;
- frais d'adjudication en pourcentage avec minimum ;
- CIRANO / hors CIRANO ;
- Interencheres LIVE, Alcopa LIVE ou vente en salle ;
- MOBA et recharge batterie ;
- carte grise, transport et budget réparations ;
- calcul inverse : budget total → enchère maximale ;
- tableau de paliers pour suivre une enchère en direct ;
- profil AUTO1.com France avec frais logistiques/administratifs selon le pays de provenance.
- profils Mercier Auto volontaire / judiciaire, canaux salle / Mercier Live / Interencheres ;
- distinction hybride rechargeable (PHEV) / électrique et supplément batterie uniquement après confirmation ;
- montant du bordereau, budget total et solde après acompte affichés séparément ;
- plafond au centime et au pas choisi, avec coût du palier suivant.
- reprise automatique des frais après vente dans le plafond (désactivable pour simuler une autre réserve).

## Déploiement Streamlit Community Cloud

1. Ouvrir https://share.streamlit.io
2. Cliquer sur **Create app**
3. Choisir le dépôt `dz-c0d3r/fr-auction-cars`
4. Branche : `main`
5. Main file path : `app.py`
6. Choisir le sous-domaine `fr-auction-cars` s'il est disponible
7. Cliquer sur **Deploy**

URL souhaitée : https://fr-auction-cars.streamlit.app

Les paramètres de frais sont préremplis mais restent modifiables dans l'interface.


## AUTO1.com France

Le profil AUTO1 utilise la grille tarifaire officielle applicable au 08/04/2026 : commission d'enchère incluse dans l'offre, frais logistiques et administratifs variables selon le pays de provenance, manutention du second jeu de pneus et stationnement éventuel. Les montants de la grille sont indiqués nets de TVA.

## Plateformes prises en charge

- Alcopa Auction
- Mercier Auto
- Interencheres (volontaire/judiciaire selon profil)
- APONEM
- VPauto
- BCA France
- AUTO1.com France
- Enchères du Domaine
- OVEO
- Autorola France
- Agorastore
- Enchères VO
- Ayvens Carmarket
- Arval MotorTrade
- OPENLANE
- Clickar / Leasys
- CarOnSale
- eCarsTrade

Les profils à barème public sont calculés automatiquement. Quand une plateforme n'affiche pas de barème public unique, le profil reste volontairement paramétrable afin d'utiliser le montant indiqué dans le compte ou la fiche du véhicule.

## Mercier Auto (vérifié le 26 octobre 2026)

Pour les voitures et utilitaires ordinaires, hors prestige et poids lourds :

| Poste TTC | Salle | Mercier Live | Interencheres |
|---|---:|---:|---:|
| Commission | 14,28 % | 14,28 % | 14,28 % |
| Dossier | 120 € | 120 € | 120 € |
| Supplément canal | 0 € | 30 € | 60 € |
| Total fixe standard | 120 € | 150 € | 180 € |

Le minimum de commission de 360 € s'applique au profil volontaire, pas au profil judiciaire. Les 150 / 180 € représentent les forfaits totaux, et ne sont pas additionnés aux 120 € une deuxième fois. Le forfait Internet générique Interencheres n'est pas ajouté séparément.

Le supplément batterie de 40 € est **désactivé par défaut**, y compris sur les PHEV. Il faut cocher sa confirmation explicite pour le compter. Le gardiennage est de 20 € TTC par jour de retard saisi ; l'enlèvement doit intervenir au plus tard le vendredi suivant la vente.

La page de la vente du 26 octobre mentionne 180 € « en ligne » sans distinguer Mercier Live. L'interface signale cette différence avec le tarif général de 150 € sur Mercier Live et laisse le supplément de canal modifiable.

- [Conditions Mercier](https://www.mercier.com/p/conditions-generales-de-vente/)
- [Vente du 26 octobre 2026](https://www.mercier.com/auto/vente/vente-vehicules-mixte-01a11587-e2f0-7111-82bf-c2c388f9b058/)
- [Exemple Golf GTE PHEV prérempli](https://fr-auction-cars.streamlit.app/?preset=mercier-golf-gte)

L'exemple utilise 10 000 € TTC au marteau, un budget illustratif de 12 000 €, Interencheres et aucun supplément batterie, frais après vente ou acompte présumé. La nature du lot dans cette vente mixte reste à confirmer ; le profil volontaire est retenu par prudence. Une saisie HT peut être convertie explicitement en TTC ; la mention « TVA récupérable » ne déclenche aucune conversion ou déduction automatique.

À 10 000 € TTC, la facture Mercier / Interencheres standard est de **11 608 €**. Un acompte réellement imputé de 2 000 € laisse **9 608 €** à régler, sans modifier le coût total ni le plafond.

## Vérification des calculs

Les calculs monétaires sont isolés dans `auction_math.py` et arrondis au centime avec `Decimal` / `ROUND_HALF_UP`. L'inversion utilise le même calcul de facture et recherche le plus grand centime ou multiple du pas qui respecte le budget.

```bash
python -m unittest -v test_auction_math.py test_app.py
```

