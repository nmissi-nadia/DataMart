import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data, render_sidebar_filters
from utils.ui import inject_custom_css, fmt, COLORS, PALETTE, CHART_LAYOUT

st.set_page_config(page_title="Ventes & Tendances | DataMart", page_icon="??", layout="wide")
inject_custom_css()

df_raw = load_data()
df, df_all, categories = render_sidebar_filters(df_raw)

st.markdown("## :material/monitoring: Analyse des Ventes & Tendances")

# Weekly heatmap
st.markdown('<div class="section-header"><span>:material/calendar_month:</span> Heatmap — Volume de commandes par jour et semaine</div>', unsafe_allow_html=True)

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
fig_h.update_layout(**CHART_LAYOUT).update_layout(height=270,
                    xaxis=dict(nticks=20, gridcolor="rgba(0,0,0,0)",
                               tickfont=dict(color=COLORS["muted"], size=9),
                               linecolor="#2d3250"),
                    yaxis=dict(gridcolor="rgba(0,0,0,0)",
                               tickfont=dict(color=COLORS["muted"]), linecolor="#2d3250"))
st.plotly_chart(fig_h, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header"><span>:material/bar_chart:</span> CA par catégorie et mois</div>', unsafe_allow_html=True)
    cat_month = df.groupby(["month","category"])["revenue"].sum().reset_index()
    fig_cm = px.bar(cat_month, x="month", y="revenue", color="category",
                    color_discrete_sequence=PALETTE,
                    labels={"revenue":"CA (€)","month":"Mois","category":"Catégorie"})
    fig_cm.update_layout(**CHART_LAYOUT).update_layout(height=300,
                         xaxis_tickangle=-45, xaxis_nticks=12,
                         legend=dict(orientation="h", y=-0.3, font=dict(size=10)))
    st.plotly_chart(fig_cm, use_container_width=True)

with col2:
    st.markdown('<div class="section-header"><span>:material/credit_card:</span> Mode de paiement vs panier moyen</div>', unsafe_allow_html=True)
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
    fig_pay.update_layout(**CHART_LAYOUT).update_layout(
        height=300,
        yaxis2=dict(overlaying="y", side="right",
                    tickfont=dict(color=COLORS["success"]),
                    gridcolor="rgba(0,0,0,0)", linecolor="#2d3250"),
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig_pay, use_container_width=True)

# Price distribution
st.markdown('<div class="section-header"><span>:material/payments:</span> Distribution des prix par catégorie</div>', unsafe_allow_html=True)
fig_box = go.Figure()
for i, cat in enumerate(categories):
    sub = df[df["category"] == cat]["unit_price"]
    fig_box.add_trace(go.Box(
        y=sub, name=cat, marker_color=PALETTE[i % len(PALETTE)],
        boxmean="sd", line=dict(width=1.5),
    ))
fig_box.update_layout(**CHART_LAYOUT).update_layout(height=300, showlegend=False)
st.plotly_chart(fig_box, use_container_width=True)
