import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import load_data, render_sidebar_filters
from utils.ui import inject_custom_css, kpi_card, fmt, COLORS, PALETTE, CHART_LAYOUT

# ─── CONFIG ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataMart Analytics",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()

# ─── DATA & SIDEBAR ─────────────────────────────────────────────────────────
df_raw = load_data()
df, df_all, categories = render_sidebar_filters(df_raw)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — VUE D'ENSEMBLE
# ════════════════════════════════════════════════════════════════════════════
st.markdown("## :material/home: Vue d'ensemble")
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
    st.markdown('<div class="section-header"><span>:material/monitoring:</span> Évolution du CA mensuel</div>', unsafe_allow_html=True)
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
    fig.update_layout(**CHART_LAYOUT).update_layout(height=280,
                      xaxis_tickangle=-45, xaxis_nticks=12,
                      legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-header"><span>:material/pie_chart:</span> CA par catégorie</div>', unsafe_allow_html=True)
    cat_rev = df.groupby("category")["revenue"].sum().reset_index()
    fig2 = go.Figure(go.Pie(
        labels=cat_rev["category"], values=cat_rev["revenue"],
        hole=0.60, marker_colors=PALETTE,
        textinfo="percent", textfont_size=11,
        hovertemplate="<b>%{label}</b><br>CA: €%{value:,.0f}<extra></extra>",
    ))
    fig2.update_layout(**CHART_LAYOUT).update_layout(height=280,
                       showlegend=True,
                       legend=dict(orientation="v", x=1.0, y=0.5,
                                   font=dict(size=10, color=COLORS["muted"])))
    st.plotly_chart(fig2, use_container_width=True)

# Row 3: Channel + Region + Day heatmap
col3, col4, col5 = st.columns([1, 1, 1])

with col3:
    st.markdown('<div class="section-header"><span>:material/campaign:</span> Canal d\'acquisition</div>', unsafe_allow_html=True)
    chan = df.groupby("channel").agg(revenue=("revenue","sum"), orders=("order_id","count")).reset_index()
    fig3 = go.Figure(go.Bar(
        x=chan["revenue"], y=chan["channel"],
        orientation="h", marker_color=PALETTE[:len(chan)],
        text=[fmt(v, "€") for v in chan["revenue"]], textposition="outside",
        hovertemplate="<b>%{y}</b><br>CA: %{text}<extra></extra>",
    ))
    fig3.update_layout(**CHART_LAYOUT).update_layout(height=220,
                       xaxis=dict(showticklabels=False, showgrid=False, linecolor="#2d3250"),
                       yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="#2d3250",
                                  tickfont=dict(color=COLORS["muted"])))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown('<div class="section-header"><span>:material/map:</span> Top régions</div>', unsafe_allow_html=True)
    region_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=True).tail(6)
    fig4 = go.Figure(go.Bar(
        x=region_rev.values, y=region_rev.index,
        orientation="h", marker_color=COLORS["teal"],
        marker_opacity=0.85,
        text=[fmt(v, "€") for v in region_rev.values], textposition="outside",
    ))
    fig4.update_layout(**CHART_LAYOUT).update_layout(height=220,
                       xaxis=dict(showticklabels=False, showgrid=False, linecolor="#2d3250"),
                       yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="#2d3250",
                                  tickfont=dict(color=COLORS["muted"], size=10)))
    st.plotly_chart(fig4, use_container_width=True)

with col5:
    st.markdown('<div class="section-header"><span>:material/inventory_2:</span> Statut des commandes</div>', unsafe_allow_html=True)
    stat = df_all.groupby("status")["order_id"].count().reset_index()
    stat.columns = ["status", "count"]
    colors_map = {"Livré":"#00d4aa","En cours":"#4f8ef7","Annulé":"#ff5c5c","Retourné":"#ff7f50"}
    fig5 = go.Figure(go.Pie(
        labels=stat["status"], values=stat["count"],
        hole=0.55, marker_colors=[colors_map.get(s, "#8b9ab1") for s in stat["status"]],
        textinfo="percent+label", textfont_size=10,
    ))
    fig5.update_layout(**CHART_LAYOUT).update_layout(height=220, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
