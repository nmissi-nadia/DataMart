#  DataMart Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Material Design](https://img.shields.io/badge/UI-Material_Design-0081CB?logo=material-design)](https://material.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Projet Portfolio Data Science & Analytics** - Un tableau de bord e-commerce interactif avec une interface Material Design moderne, intégrant des analyses descriptives, une segmentation client (RFM) et du Machine Learning prédictif.

---

##  Contexte Business

Dans le domaine du e-commerce, comprendre le comportement des clients et anticiper les tendances est vital. Ce tableau de bord a été conçu pour répondre à trois problématiques clés d'un Data Manager / Business Analyst :
1. **Suivi des Performances (KPIs)** : Chiffre d'affaires, volume de commandes, panier moyen.
2. **Connaissance Client (Segmentation)** : Identifier les meilleurs clients via un algorithme RFM (Récence, Fréquence, Montant).
3. **Anticipation (Machine Learning)** : Prédire le churn (attrition) et prévoir l'évolution des ventes grâce à des modèles prédictifs.

---

##  Lancement rapide

```bash
# 1. Cloner le projet
git clone https://github.com/nmissi-nadia/DataMart.git
cd DataMart

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python -m streamlit run app.py
```
L'application s'ouvre automatiquement sur `http://localhost:8501`.

---

##  Stack technique

- **Data Wrangling** : `Python`, `Pandas`, `NumPy`
- **Machine Learning** : `Scikit-learn` (Random Forest, Gradient Boosting, KMeans)
- **Data Visualization** : `Plotly` (Graphiques interactifs avancés)
- **Frontend / UI** : `Streamlit`, `CSS` (Material Design, FontAwesome)

---

##  Structure du projet

```text
DataMart/
├── app.py                      ← Vue d'ensemble (KPIs)
├── pages/
│   ├── 1_Ventes_&_Tendances.py ← Analyse temporelle et canaux
│   ├── 2_Segmentation_Client.py← Score RFM et clusters
│   ├── 3_Predictions_ML.py     ← Modèles prédictifs
│   └── 4_Donnees_brutes.py     ← Table interactive et export
├── utils/
│   ├── ui.py                   ← Design System (Material Design)
│   └── data_loader.py          ← Générateur de données synthétiques
└── requirements.txt
```

