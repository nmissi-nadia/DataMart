import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))
from generate_data import generate_ecommerce_data

@st_cache_data_placeholder
def load_data():
    return generate_ecommerce_data(n_orders=5000)

def format_number(value, prefix="", suffix=""):
    if value >= 1_000_000:
        return f"{prefix}{value/1_000_000:.1f}M{suffix}"
    elif value >= 1_000:
        return f"{prefix}{value/1_000:.1f}K{suffix}"
    return f"{prefix}{value:.0f}{suffix}"

def compute_kpis(df):
    total_revenue = df[df["status"] == "Livré"]["revenue"].sum()
    total_margin = df[df["status"] == "Livré"]["margin"].sum()
    total_orders = len(df)
    avg_basket = df[df["status"] == "Livré"]["revenue"].mean()
    conversion_rate = len(df[df["status"] == "Livré"]) / total_orders * 100
    return {
        "revenue": total_revenue,
        "margin": total_margin,
        "orders": total_orders,
        "avg_basket": avg_basket,
        "conversion_rate": conversion_rate,
    }
