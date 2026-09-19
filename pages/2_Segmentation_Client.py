import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data, render_sidebar_filters
from utils.ui import inject_custom_css, fmt, COLORS, CHART_LAYOUT

st.set_page_config(page_title="Segmentation Client | DataMart", page_icon="??", layout="wide")
inject_custom_css()

df_raw = load_data()
df, _, _ = render_sidebar_filters(df_raw)

st.markdown('<h2 style="margin-bottom: 20px;"><i class="fa-solid fa-brain"></i>  Segmentation Client — Analyse RFM</h2>', unsafe_allow_html=True)
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
    if score >= 10: return "Champions "
    if score >= 8:  return "Fidèles "
    if score >= 6:  return "Potentiels "
    return "À risque "

rfm["segment"] = rfm["RFM_score"].apply(segment)

seg_colors = {
    "Champions ": "#00d4aa",
    "Fidèles ":    "#4f8ef7",
    "Potentiels ": "#f59e0b",
    "À risque ":   "#ff5c5c",
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
    st.markdown('<div class="section-header"><i class="fa-solid fa-mouse-pointer"></i>  Scatter RFM — Fréquence vs Monétaire</div>', unsafe_allow_html=True)
    fig_rfm = px.scatter(
        rfm, x="frequency", y="monetary", color="segment",
        size="RFM_score", hover_data=["customer_id","recency"],
        color_discrete_map=seg_colors,
        labels={"frequency":"Fréquence (nb commandes)","monetary":"CA total (€)","segment":"Segment"},
    )
    fig_rfm.update_layout(**CHART_LAYOUT).update_layout(height=350)
    st.plotly_chart(fig_rfm, use_container_width=True)

with col2:
    st.markdown('<div class="section-header"><i class="fa-solid fa-chart-simple"></i>  Répartition des segments</div>', unsafe_allow_html=True)
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
    fig_seg.update_layout(**CHART_LAYOUT).update_layout(height=350, showlegend=False,
                          xaxis=dict(tickfont=dict(size=10, color=COLORS["muted"]),
                                     linecolor="#2d3250", gridcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig_seg, use_container_width=True)

# Table
st.markdown('<div class="section-header"><i class="fa-solid fa-list-ul"></i>  Top 20 clients (Champions)</div>', unsafe_allow_html=True)
top_clients = rfm[rfm["segment"] == "Champions "].sort_values("monetary", ascending=False).head(20)
st.dataframe(
    top_clients[["customer_id","recency","frequency","monetary","RFM_score","segment"]]
    .rename(columns={"customer_id":"Client","recency":"Récence (j)",
                     "frequency":"Fréq.","monetary":"CA (€)","RFM_score":"Score"}),
    use_container_width=True, hide_index=True,
)
