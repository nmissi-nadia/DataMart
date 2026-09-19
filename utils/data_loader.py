import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))
from generate_data import generate_ecommerce_data

@st.cache_data
def load_data():
    return generate_ecommerce_data(n_orders=5000)

def render_sidebar_filters(df_raw):
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2>📊 DataMart</h2>
            <p>Analytics Dashboard v2.0</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="nav-section">Filtres Globaux</div>', unsafe_allow_html=True)

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
    
    return df, df_all, categories
