import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_data, render_sidebar_filters
from utils.ui import apply_ui_settings, fmt, COLORS, CHART_LAYOUT

st.set_page_config(page_title="Prédictions ML | DataMart", page_icon="??", layout="wide")
apply_ui_settings()

df_raw = load_data()
df, _, _ = render_sidebar_filters(df_raw)

st.markdown('<h2 style="margin-bottom: 20px;"><i class="fa-solid fa-robot"></i>  Prédictions Machine Learning</h2>', unsafe_allow_html=True)

from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings("ignore")

tab1, tab2 = st.tabs(["■  Prédiction du Churn", "■  Prédiction du CA client"])

with tab1:
    st.markdown("**Objectif :** Identifier les clients risquant de ne plus commander (churn = 0 commande depuis > 90 jours)")

    snapshot = df_raw["order_date"].max()
    customer_features = (df_raw.groupby("customer_id")
                         .agg(
                             recency=("order_date", lambda x: (snapshot - x.max()).days),
                             frequency=("order_id","count"),
                             monetary=("revenue","sum"),
                             avg_basket=("revenue","mean"),
                             unique_cats=("category","nunique"),
                         ).reset_index())
    customer_features["churn"] = (customer_features["recency"] > 90).astype(int)

    X = customer_features[["recency","frequency","monetary","avg_basket","unique_cats"]]
    y = customer_features["churn"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    with st.spinner("Entraînement du modèle..."):
        model = RandomForestClassifier(n_estimators=150, max_depth=8, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = (y_pred == y_test).mean()
    churn_rate = y.mean()

    c1,c2,c3 = st.columns(3)
    c1.metric("Précision du modèle", f"{acc:.1%}")
    c2.metric("Taux de churn global", f"{churn_rate:.1%}")
    c3.metric("Clients à risque", f"{int(churn_rate * len(customer_features))}")

    # Feature importance
    fi = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header"><i class="fa-solid fa-magnifying-glass"></i>  Importance des variables</div>', unsafe_allow_html=True)
        fig_fi = go.Figure(go.Bar(
            x=fi["Importance"], y=fi["Feature"],
            orientation="h", marker_color=COLORS["primary"],
            text=[f"{v:.3f}" for v in fi["Importance"]], textposition="outside",
        ))
        fig_fi.update_layout(**CHART_LAYOUT).update_layout(height=280,
                             xaxis=dict(showticklabels=False, showgrid=False, linecolor="#2d3250"),
                             yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="#2d3250",
                                        tickfont=dict(color=COLORS["muted"])))
        st.plotly_chart(fig_fi, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header"><i class="fa-solid fa-mouse-pointer"></i>  Clients à risque par segment CA</div>', unsafe_allow_html=True)
        customer_features["churn_proba"] = model.predict_proba(X)[:, 1]
        customer_features["risk"] = pd.cut(customer_features["churn_proba"],
                                            bins=[0,0.33,0.66,1],
                                            labels=["Faible","Moyen","Élevé"])
        risk_dist = customer_features.groupby("risk")["monetary"].sum().reset_index()
        fig_risk = go.Figure(go.Bar(
            x=risk_dist["risk"], y=risk_dist["monetary"],
            marker_color=[COLORS["success"], COLORS["warning"], COLORS["danger"]],
            text=[fmt(v, "€") for v in risk_dist["monetary"]], textposition="outside",
        ))
        fig_risk.update_layout(**CHART_LAYOUT).update_layout(height=280,
                               xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="#2d3250",
                                          tickfont=dict(color=COLORS["muted"])),
                               yaxis=dict(showticklabels=False, showgrid=False, linecolor="#2d3250"))
        st.plotly_chart(fig_risk, use_container_width=True)

with tab2:
    st.markdown("**Objectif :** Prédire le CA futur d'un client basé sur son historique")

    X2 = customer_features[["recency","frequency","avg_basket","unique_cats"]]
    y2 = customer_features["monetary"]

    X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.25, random_state=42)

    with st.spinner("Entraînement GBM..."):
        gbm = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
        gbm.fit(X2_train, y2_train)

    y2_pred = gbm.predict(X2_test)
    mae = mean_absolute_error(y2_test, y2_pred)
    r2  = r2_score(y2_test, y2_pred)

    c1, c2 = st.columns(2)
    c1.metric("R² Score", f"{r2:.3f}", "Excellent si > 0.8")
    c2.metric("MAE (€)", f"{mae:.1f}", "Erreur moyenne absolue")

    st.markdown('<div class="section-header"><i class="fa-solid fa-chart-simple"></i>  Valeurs réelles vs prédites</div>', unsafe_allow_html=True)
    pred_df = pd.DataFrame({"Réel": y2_test.values, "Prédit": y2_pred})
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(
        x=pred_df["Réel"], y=pred_df["Prédit"],
        mode="markers", marker=dict(color=COLORS["primary"], opacity=0.5, size=5),
        name="Prédictions",
    ))
    max_val = max(pred_df["Réel"].max(), pred_df["Prédit"].max())
    fig_pred.add_trace(go.Scatter(
        x=[0, max_val], y=[0, max_val],
        mode="lines", line=dict(color=COLORS["success"], dash="dash", width=2),
        name="Ligne parfaite",
    ))
    fig_pred.update_layout(**CHART_LAYOUT).update_layout(height=380,
                           xaxis_title="CA réel (€)", yaxis_title="CA prédit (€)")
    st.plotly_chart(fig_pred, use_container_width=True)
