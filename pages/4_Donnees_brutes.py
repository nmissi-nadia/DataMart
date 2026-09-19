import streamlit as st
from utils.data_loader import load_data, render_sidebar_filters
from utils.ui import apply_ui_settings

st.set_page_config(page_title="Données brutes | DataMart", page_icon="??", layout="wide")
apply_ui_settings()

df_raw = load_data()
df, df_all, _ = render_sidebar_filters(df_raw)

st.markdown('<h2 style="margin-bottom: 20px;"><i class="fa-solid fa-list-ul"></i>  Données Brutes</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Total lignes", f"{len(df_all):,}")
col2.metric("Filtrées (livré)", f"{len(df):,}")
col3.metric("Colonnes", len(df.columns))

st.dataframe(df.head(500), use_container_width=True, hide_index=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("■  Télécharger CSV", csv, "datamart_filtered.csv", "text/csv")
