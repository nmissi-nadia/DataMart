# 📊 DataMart Analytics Dashboard

Dashboard analytics interactif pour l'analyse d'un dataset e-commerce — projet portfolio Data Science.

## 🚀 Lancement rapide

```bash
# 1. Cloner / dézipper le projet
cd projet1_ecommerce_dashboard

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app.py
```

L'application s'ouvre automatiquement sur `http://localhost:8501`

## 📌 Fonctionnalités

| Page | Contenu |
|------|---------|
| 🏠 Vue d'ensemble | KPIs, CA mensuel, répartition catégories/régions |
| 📈 Ventes & Tendances | Heatmap hebdo, distribution prix, analyse canal |
| 🧠 Segmentation RFM | Analyse Recency-Frequency-Monetary, scatter clients |
| 🔮 Prédictions ML | Churn prediction (Random Forest) + CA forecast (GBM) |
| 📋 Données brutes | Table filtrée + export CSV |

## 🛠️ Stack technique

- **Python** · **Pandas** · **NumPy** — Data wrangling
- **Plotly** — Visualisations interactives
- **Streamlit** — Interface web
- **Scikit-learn** — Random Forest, Gradient Boosting, RFM scoring

## 📂 Structure

```
projet1_ecommerce_dashboard/
├── app.py                  ← Application principale (5 pages)
├── requirements.txt
├── data/
│   └── generate_data.py    ← Générateur de données synthétiques (5000 commandes)
└── README.md
```

## 🌐 Déploiement Streamlit Cloud (gratuit)

1. Pusher le dossier sur GitHub
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Connecter le repo → Deploy
4. Partager le lien sur LinkedIn 🎉

## 💡 Idées d'améliorations

- Connecter à une vraie base PostgreSQL
- Ajouter une page "Forecasting" avec Prophet
- Intégrer des alertes (Slack/email) si churn détecté
- Authentification utilisateur (st.secrets)
