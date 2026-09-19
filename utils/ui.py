import streamlit as st

COLORS = {
    "primary":   "#0ea5e9",  # Sky blue (Brand primary)
    "secondary": "#f8fafc",  # Light slate
    "accent":    "#0284c7",  # Darker blue
    "bg":        "#0f172a",  # Deep slate (Background)
    "text":      "#f1f5f9",
    "muted":     "#94a3b8",
    # Mapped semantic colors to the unified blue/slate theme
    "success":   "#38bdf8",
    "warning":   "#0284c7",
    "danger":    "#0c4a6e",
    "purple":    "#0284c7",
    "teal":      "#38bdf8",
}

# Simplified 3-color palette for charts (Primary, Light, Dark)
PALETTE = ["#0ea5e9", "#38bdf8", "#0284c7", "#7dd3fc", "#0369a1"]

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

def apply_ui_settings():
    st.set_page_config(layout="wide", page_title="DataMart")
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)
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
            background-color: #0f172a;
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
