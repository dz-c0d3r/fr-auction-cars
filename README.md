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
- tableau de paliers pour suivre une enchère en direct.

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
