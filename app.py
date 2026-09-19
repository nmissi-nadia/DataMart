import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))
from generate_data import generate_ecommerce_data

# ─── CONFIG ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataMart Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background-color: #0f1117; }
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; max-width: 1400px; }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1e2130 0%, #252a3a 100%);
        border: 1px solid #2d3250;
        border-radius: 16px;
        padding: 20px 24px;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 16px 16px 0 0;
    }
    .kpi-card.green::before  { background: linear-gradient(90deg, #00d4aa, #00a896); }
    .kpi-card.blue::before   { background: linear-gradient(90deg, #4f8ef7, #7b61ff); }
    .kpi-card.orange::before { background: linear-gradient(90deg, #ff7f50, #ff5733); }
    .kpi-card.purple::before { background: linear-gradient(90deg, #c084fc, #9333ea); }
    .kpi-card.teal::before   { background: linear-gradient(90deg, #22d3ee, #0ea5e9); }

    .kpi-label { color: #8b9ab1; font-size: 0.72rem; font-weight: 600;
                 text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px; }
    .kpi-value { color: #f0f4ff; font-size: 1.85rem; font-weight: 700; line-height: 1.1; }
    .kpi-delta { font-size: 0.78rem; margin-top: 6px; font-weight: 500; }
    .kpi-delta.up   { color: #00d4aa; }
    .kpi-delta.down { color: #ff5c5c; }

    /* Section headers */
    .section-header {
        color: #e2e8f0; font-size: 1.05rem; font-weight: 600;
        margin: 18px 0 10px 0; display: flex; align-items: center; gap: 8px;
    }
    .section-header span { color: #4f8ef7; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #0f1117 100%);
        border-right: 1px solid #1e2130;
    }
    [data-testid="stSidebar"] .block-container { padding-top: 2rem; }

    .sidebar-logo {
        text-align: center; padding: 0 0 24px 0;
        border-bottom: 1px solid #1e2130; margin-bottom: 20px;
    }
    .sidebar-logo h2 { color: #f0f4ff; font-size: 1.2rem; font-weight: 700; margin: 0; }
    .sidebar-logo p  { color: #8b9ab1; font-size: 0.72rem; margin: 4px 0 0 0; }

    /* Nav pills */
    .nav-section { color: #4f8ef7; font-size: 0.68rem; font-weight: 700;
                   text-transform: uppercase; letter-spacing: 1.5px; margin: 16px 0 6px 4px; }

    /* Hide default elements */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ─── DATA ────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return generate_ecommerce_data(n_orders=5000)

df_raw = load_data()


# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>📊 DataMart</h2>
        <p>Analytics Dashboard v2.0</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section">Navigation</div>', unsafe_allow_html=True)
    page = st.radio("", ["🏠 Vue d'ensemble", "📈 Ventes & Tendances",
                         "🧠 Segmentation Client", "🔮 Prédictions ML",
                         "📋 Données brutes"],
                    label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="nav-section">Filtres</div>', unsafe_allow_html=True)

    years = sorted(df_raw["year"].unique())
    selected_years = st.multiselect("Année", years, default=years)

    categories = sorted(df_raw["category"].unique())
    selected_cats = st.multiselect("Catégorie", categories, default=categories)

    regions = sorted(df_raw["region"].unique())
    selected_regions = st.multiselect("Région", regions, default=regions)

    statuses = sorted(df_raw["status"].unique())
    selected_status = st.multiselect("Statut", statuses, default=["Livré"])

    st.markdown("---")
    st.caption("Projet Portfolio | Data Science Master")
    st.caption("Built with Streamlit + Plotly")


# ─── FILTER DATA ────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["year"].isin(selected_years) &
    df_raw["category"].isin(selected_cats) &
    df_raw["region"].isin(selected_regions) &
    df_raw["status"].isin(selected_status)
].copy()

df_all = df_raw[
    df_raw["year"].isin(selected_years) &
    df_raw["category"].isin(selected_cats) &
    df_raw["region"].isin(selected_regions)
].copy()

COLORS = {
    "primary":   "#4f8ef7",
    "success":   "#00d4aa",
    "warning":   "#ff7f50",
    "danger":    "#ff5c5c",
    "purple":    "#c084fc",
    "teal":      "#22d3ee",
    "bg":        "#1e2130",
    "text":      "#f0f4ff",
    "muted":     "#8b9ab1",
}

PALETTE = [COLORS["primary"], COLORS["success"], COLORS["warning"],
           COLORS["purple"], COLORS["teal"], COLORS["danger"],
           "#f59e0b", "#10b981", "#6366f1"]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORS["text"], family="Inter"),
    margin=dict(t=30, b=10, l=10, r=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["muted"])),
    xaxis=dict(gridcolor="#1e2130", linecolor="#2d3250",
               tickfont=dict(color=COLORS["muted"])),
    yaxis=dict(gridcolor="#1e2130", linecolor="#2d3250",
               tickfont=dict(color=COLORS["muted"])),
)


# ─── KPI HELPER ─────────────────────────────────────────────────────────────
def kpi_card(label, value, delta=None, color="green"):
    delta_html = ""
    if delta is not None:
        sign = "▲" if delta >= 0 else "▼"
        cls  = "up" if delta >= 0 else "down"
        delta_html = f'<div class="kpi-delta {cls}">{sign} {abs(delta):.1f}% vs période préc.</div>'
    return f"""
    <div class="kpi-card {color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>"""

def fmt(v, prefix="", suffix="", decimals=1):
    if v >= 1_000_000: return f"{prefix}{v/1_000_000:.{decimals}f}M{suffix}"
    if v >= 1_000:     return f"{prefix}{v/1_000:.{decimals}f}K{suffix}"
    return f"{prefix}{v:.{decimals}f}{suffix}"


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — VUE D'ENSEMBLE
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠 Vue d'ensemble":
    st.markdown("## 🏠 Vue d'ensemble")
    st.caption(f"Données filtrées : **{len(df):,}** commandes livrées")

    # KPIs
    rev   = df["revenue"].sum()
    marg  = df["margin"].sum()
    aov   = df["revenue"].mean() if len(df) > 0 else 0
    uq    = df["customer_id"].nunique()
    cr    = len(df) / len(df_all) * 100 if len(df_all) > 0 else 0
    marg_pct = marg / rev * 100 if rev > 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi_card("Chiffre d'affaires", fmt(rev, "€", decimals=2), 12.4, "green"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Marge brute", f"{fmt(marg, '€')} ({marg_pct:.0f}%)", 3.1, "blue"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Panier moyen", fmt(aov, "€"), -1.8, "orange"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Clients uniques", fmt(uq), 8.7, "purple"), unsafe_allow_html=True)
    with c5: st.markdown(kpi_card("Taux livraison", f"{cr:.1f}%", 2.3, "teal"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Revenue timeline + Category donut
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="section-header"><span>📈</span> Évolution du CA mensuel</div>', unsafe_allow_html=True)
        monthly = (df.groupby("month")["revenue"]
                     .sum().reset_index()
                     .sort_values("month"))
        monthly["ma3"] = monthly["revenue"].rolling(3).mean()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly["month"], y=monthly["revenue"],
            name="CA", marker_color=COLORS["primary"],
            marker_opacity=0.6,
        ))
        fig.add_trace(go.Scatter(
            x=monthly["month"], y=monthly["ma3"],
            name="Moyenne mobile 3M", line=dict(color=COLORS["success"], width=2.5),
            mode="lines",
        ))
        fig.update_layout(**CHART_LAYOUT, height=280,
                          xaxis_tickangle=-45, xaxis_nticks=12,
                          legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header"><span>🍩</span> CA par catégorie</div>', unsafe_allow_html=True)
        cat_rev = df.groupby("category")["revenue"].sum().reset_index()
        fig2 = go.Figure(go.Pie(
            labels=cat_rev["category"], values=cat_rev["revenue"],
            hole=0.60, marker_colors=PALETTE,
            textinfo="percent", textfont_size=11,
            hovertemplate="<b>%{label}</b><br>CA: €%{value:,.0f}<extra></extra>",
        ))
        fig2.update_layout(**CHART_LAYOUT, height=280,
                           showlegend=True,
                           legend=dict(orientation="v", x=1.0, y=0.5,
                                       font=dict(size=10, color=COLORS["muted"])))
        st.plotly_chart(fig2, use_container_width=True)

    # Row 3: Channel + Region + Day heatmap
    col3, col4, col5 = st.columns([1, 1, 1])

    with col3:
        st.markdown('<div class="section-header"><span>📡</span> Canal d\'acquisition</div>', unsafe_allow_html=True)
        chan = df.groupby("channel").agg(revenue=("revenue","sum"), orders=("order_id","count")).reset_index()
        fig3 = go.Figure(go.Bar(
            x=chan["revenue"], y=chan["channel"],
            orientation="h", marker_color=PALETTE[:len(chan)],
            text=[fmt(v, "€") for v in chan["revenue"]], textposition="outside",
            hovertemplate="<b>%{y}</b><br>CA: %{text}<extra></extra>",
        ))
        fig3.update_layout(**CHART_LAYOUT, height=220,
                           xaxis=dict(showticklabels=False, showgrid=False, linecolor="#2d3250"),
                           yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="#2d3250",
                                      tickfont=dict(color=COLORS["muted"])))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header"><span>🗺️</span> Top régions</div>', unsafe_allow_html=True)
        region_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=True).tail(6)
        fig4 = go.Figure(go.Bar(
            x=region_rev.values, y=region_rev.index,
            orientation="h", marker_color=COLORS["teal"],
            marker_opacity=0.85,
            text=[fmt(v, "€") for v in region_rev.values], textposition="outside",
        ))
        fig4.update_layout(**CHART_LAYOUT, height=220,
                           xaxis=dict(showticklabels=False, showgrid=False, linecolor="#2d3250"),
                           yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="#2d3250",
                                      tickfont=dict(color=COLORS["muted"], size=10)))
        st.plotly_chart(fig4, use_container_width=True)

    with col5:
        st.markdown('<div class="section-header"><span>📦</span> Statut des commandes</div>', unsafe_allow_html=True)
        stat = df_all.groupby("status")["order_id"].count().reset_index()
        stat.columns = ["status", "count"]
        colors_map = {"Livré":"#00d4aa","En cours":"#4f8ef7","Annulé":"#ff5c5c","Retourné":"#ff7f50"}
        fig5 = go.Figure(go.Pie(
            labels=stat["status"], values=stat["count"],
            hole=0.55, marker_colors=[colors_map.get(s, "#8b9ab1") for s in stat["status"]],
            textinfo="percent+label", textfont_size=10,
        ))
        fig5.update_layout(**CHART_LAYOUT, height=220, showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 — VENTES & TENDANCES
# ════════════════════════════════════════════════════════════════════════════
elif page == "📈 Ventes & Tendances":
    st.markdown("## 📈 Analyse des Ventes & Tendances")

    # Weekly heatmap
    st.markdown('<div class="section-header"><span>🗓️</span> Heatmap — Volume de commandes par jour et semaine</div>', unsafe_allow_html=True)

    df_heat = df_all.copy()
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    day_fr    = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
    df_heat["day_of_week"] = pd.Categorical(df_heat["day_of_week"], categories=day_order, ordered=True)
    heat_data = (df_heat.groupby(["week","day_of_week"])["order_id"]
                        .count().reset_index()
                        .pivot(index="day_of_week", columns="week", values="order_id")
                        .fillna(0))

    fig_h = go.Figure(go.Heatmap(
        z=heat_data.values, x=[f"S{c}" for c in heat_data.columns],
        y=day_fr, colorscale=[[0,"#1e2130"],[0.5,"#4f8ef7"],[1,"#00d4aa"]],
        showscale=True,
        hovertemplate="Semaine %{x} — %{y}<br>Commandes: %{z}<extra></extra>",
    ))
    fig_h.update_layout(**CHART_LAYOUT, height=270,
                        xaxis=dict(nticks=20, gridcolor="rgba(0,0,0,0)",
                                   tickfont=dict(color=COLORS["muted"], size=9),
                                   linecolor="#2d3250"),
                        yaxis=dict(gridcolor="rgba(0,0,0,0)",
                                   tickfont=dict(color=COLORS["muted"]), linecolor="#2d3250"))
    st.plotly_chart(fig_h, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header"><span>📊</span> CA par catégorie et mois</div>', unsafe_allow_html=True)
        cat_month = df.groupby(["month","category"])["revenue"].sum().reset_index()
        fig_cm = px.bar(cat_month, x="month", y="revenue", color="category",
                        color_discrete_sequence=PALETTE,
                        labels={"revenue":"CA (€)","month":"Mois","category":"Catégorie"})
        fig_cm.update_layout(**CHART_LAYOUT, height=300,
                             xaxis_tickangle=-45, xaxis_nticks=12,
                             legend=dict(orientation="h", y=-0.3, font=dict(size=10)))
        st.plotly_chart(fig_cm, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header"><span>💳</span> Mode de paiement vs panier moyen</div>', unsafe_allow_html=True)
        pay = df.groupby("payment_method").agg(
            avg_basket=("revenue","mean"),
            volume=("order_id","count")
        ).reset_index()
        fig_pay = go.Figure()
        fig_pay.add_trace(go.Bar(
            x=pay["payment_method"], y=pay["avg_basket"],
            name="Panier moyen", marker_color=COLORS["purple"],
            text=[f"€{v:.0f}" for v in pay["avg_basket"]], textposition="outside",
        ))
        fig_pay.add_trace(go.Scatter(
            x=pay["payment_method"], y=pay["volume"],
            name="Volume", mode="markers+lines",
            marker=dict(size=12, color=COLORS["success"]),
            line=dict(color=COLORS["success"], width=2),
            yaxis="y2",
        ))
        fig_pay.update_layout(
            **CHART_LAYOUT, height=300,
            yaxis2=dict(overlaying="y", side="right",
                        tickfont=dict(color=COLORS["success"]),
                        gridcolor="rgba(0,0,0,0)", linecolor="#2d3250"),
            legend=dict(orientation="h", y=1.1),
        )
        st.plotly_chart(fig_pay, use_container_width=True)

    # Price distribution
    st.markdown('<div class="section-header"><span>💰</span> Distribution des prix par catégorie</div>', unsafe_allow_html=True)
    fig_box = go.Figure()
    for i, cat in enumerate(categories):
        sub = df[df["category"] == cat]["unit_price"]
        fig_box.add_trace(go.Box(
            y=sub, name=cat, marker_color=PALETTE[i % len(PALETTE)],
            boxmean="sd", line=dict(width=1.5),
        ))
    fig_box.update_layout(**CHART_LAYOUT, height=300, showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 — SEGMENTATION CLIENT (RFM)
# ════════════════════════════════════════════════════════════════════════════
elif page == "🧠 Segmentation Client":
    st.markdown("## 🧠 Segmentation Client — Analyse RFM")
    st.info("**RFM = Recency · Frequency · Monetary** — Une méthode d'analyse marketing pour identifier vos meilleurs clients.")

    snapshot = df["order_date"].max()
    rfm = (df.groupby("customer_id")
             .agg(
                 recency=("order_date", lambda x: (snapshot - x.max()).days),
                 frequency=("order_id", "count"),
                 monetary=("revenue", "sum"),
             )
             .reset_index())

    # Score RFM (quintiles)
    rfm["R_score"] = pd.qcut(rfm["recency"], 4, labels=[4,3,2,1]).astype(int)
    rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1,2,3,4]).astype(int)
    rfm["M_score"] = pd.qcut(rfm["monetary"], 4, labels=[1,2,3,4]).astype(int)
    rfm["RFM_score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

    def segment(score):
        if score >= 10: return "Champions 🏆"
        if score >= 8:  return "Fidèles ⭐"
        if score >= 6:  return "Potentiels 🌱"
        return "À risque ⚠️"

    rfm["segment"] = rfm["RFM_score"].apply(segment)

    seg_colors = {
        "Champions 🏆": "#00d4aa",
        "Fidèles ⭐":    "#4f8ef7",
        "Potentiels 🌱": "#f59e0b",
        "À risque ⚠️":   "#ff5c5c",
    }

    col1, col2, col3, col4 = st.columns(4)
    for col, seg in zip([col1,col2,col3,col4], seg_colors):
        count = len(rfm[rfm["segment"] == seg])
        rev   = rfm[rfm["segment"] == seg]["monetary"].sum()
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-top: 3px solid {seg_colors[seg]};">
                <div class="kpi-label">{seg}</div>
                <div class="kpi-value">{count}</div>
                <div style="color:{seg_colors[seg]};font-size:0.8rem;margin-top:4px">
                    CA: {fmt(rev, "€")}
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header"><span>🎯</span> Scatter RFM — Fréquence vs Monétaire</div>', unsafe_allow_html=True)
        fig_rfm = px.scatter(
            rfm, x="frequency", y="monetary", color="segment",
            size="RFM_score", hover_data=["customer_id","recency"],
            color_discrete_map=seg_colors,
            labels={"frequency":"Fréquence (nb commandes)","monetary":"CA total (€)","segment":"Segment"},
        )
        fig_rfm.update_layout(**CHART_LAYOUT, height=350)
        st.plotly_chart(fig_rfm, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header"><span>📊</span> Répartition des segments</div>', unsafe_allow_html=True)
        seg_dist = rfm.groupby("segment").agg(
            clients=("customer_id","count"),
            ca=("monetary","sum")
        ).reset_index()
        fig_seg = go.Figure()
        fig_seg.add_trace(go.Bar(
            name="Nb clients", x=seg_dist["segment"], y=seg_dist["clients"],
            marker_color=[seg_colors[s] for s in seg_dist["segment"]],
            marker_opacity=0.8,
        ))
        fig_seg.update_layout(**CHART_LAYOUT, height=350, showlegend=False,
                              xaxis=dict(tickfont=dict(size=10, color=COLORS["muted"]),
                                         linecolor="#2d3250", gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_seg, use_container_width=True)

    # Table
    st.markdown('<div class="section-header"><span>📋</span> Top 20 clients (Champions)</div>', unsafe_allow_html=True)
    top_clients = rfm[rfm["segment"] == "Champions 🏆"].sort_values("monetary", ascending=False).head(20)
    st.dataframe(
        top_clients[["customer_id","recency","frequency","monetary","RFM_score","segment"]]
        .rename(columns={"customer_id":"Client","recency":"Récence (j)",
                         "frequency":"Fréq.","monetary":"CA (€)","RFM_score":"Score"}),
        use_container_width=True, hide_index=True,
    )


# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 — PRÉDICTIONS ML
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔮 Prédictions ML":
    st.markdown("## 🔮 Prédictions Machine Learning")

    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import classification_report, mean_absolute_error, r2_score
    import warnings
    warnings.filterwarnings("ignore")

    tab1, tab2 = st.tabs(["🎯 Prédiction du Churn", "💰 Prédiction du CA client"])

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
            st.markdown('<div class="section-header"><span>🔍</span> Importance des variables</div>', unsafe_allow_html=True)
            fig_fi = go.Figure(go.Bar(
                x=fi["Importance"], y=fi["Feature"],
                orientation="h", marker_color=COLORS["primary"],
                text=[f"{v:.3f}" for v in fi["Importance"]], textposition="outside",
            ))
            fig_fi.update_layout(**CHART_LAYOUT, height=280,
                                 xaxis=dict(showticklabels=False, showgrid=False, linecolor="#2d3250"),
                                 yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="#2d3250",
                                            tickfont=dict(color=COLORS["muted"])))
            st.plotly_chart(fig_fi, use_container_width=True)

        with col2:
            st.markdown('<div class="section-header"><span>🎯</span> Clients à risque par segment CA</div>', unsafe_allow_html=True)
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
            fig_risk.update_layout(**CHART_LAYOUT, height=280,
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

        st.markdown('<div class="section-header"><span>📊</span> Valeurs réelles vs prédites</div>', unsafe_allow_html=True)
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
        fig_pred.update_layout(**CHART_LAYOUT, height=380,
                               xaxis_title="CA réel (€)", yaxis_title="CA prédit (€)")
        st.plotly_chart(fig_pred, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 5 — DONNÉES BRUTES
# ════════════════════════════════════════════════════════════════════════════
elif page == "📋 Données brutes":
    st.markdown("## 📋 Données Brutes")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total lignes", f"{len(df_all):,}")
    col2.metric("Filtrées (livré)", f"{len(df):,}")
    col3.metric("Colonnes", len(df.columns))

    st.dataframe(df.head(500), use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Télécharger CSV", csv, "datamart_filtered.csv", "text/csv")
