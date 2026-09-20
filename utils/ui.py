import streamlit as st

COLORS = {
    "primary":   "#0284c7",  # Material Blue (Primary)
    "secondary": "#f8fafc",  # Light background
    "accent":    "#0369a1",  # Darker blue
    "bg":        "#f1f5f9",  # Page background
    "text":      "#1e293b",  # Dark text for readability
    "muted":     "#64748b",  # Secondary text
    
    # Status colors
    "success":   "#10b981",  # Emerald
    "warning":   "#f59e0b",  # Amber
    "danger":    "#ef4444",  # Red
    "purple":    "#8b5cf6",  # Violet
    "teal":      "#14b8a6",  # Teal
}

# Material Design Palette for Charts
PALETTE = ["#0284c7", "#38bdf8", "#818cf8", "#34d399", "#fbbf24", "#f87171"]

CHART_LAYOUT = dict(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font=dict(color=COLORS["text"], family="Inter"),
    margin=dict(t=40, b=20, l=20, r=20),
    legend=dict(bgcolor="rgba(255,255,255,0.8)", font=dict(color=COLORS["muted"])),
    xaxis=dict(gridcolor="#e2e8f0", linecolor="#cbd5e1",
               tickfont=dict(color=COLORS["muted"])),
    yaxis=dict(gridcolor="#e2e8f0", linecolor="#cbd5e1",
               tickfont=dict(color=COLORS["muted"])),
)

def apply_ui_settings():
    st.set_page_config(layout="wide", page_title="DataMart")
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        .main { background-color: #f1f5f9; } /* Light gray background */
        .block-container { padding-top: 1.5rem; padding-bottom: 1rem; max-width: 1400px; }

        /* KPI Cards - Material Design */
        .kpi-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px 24px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            border: 1px solid #e2e8f0;
        }
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        
        /* Colored Top Accent Line */
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
        }
        .kpi-card.green::before  { background-color: #10b981; }
        .kpi-card.blue::before   { background-color: #0284c7; }
        .kpi-card.orange::before { background-color: #f59e0b; }
        .kpi-card.purple::before { background-color: #8b5cf6; }
        .kpi-card.teal::before   { background-color: #14b8a6; }

        .kpi-label { color: #64748b; font-size: 0.75rem; font-weight: 600;
                     text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
        .kpi-value { color: #0f172a; font-size: 1.85rem; font-weight: 700; line-height: 1.1; }
        .kpi-delta { font-size: 0.8rem; margin-top: 8px; font-weight: 500; display: flex; align-items: center; gap: 4px; }
        .kpi-delta.up   { color: #10b981; }
        .kpi-delta.down { color: #ef4444; }

        /* Section headers */
        .section-header {
            color: #1e293b; font-size: 1.15rem; font-weight: 600;
            margin: 24px 0 12px 0; display: flex; align-items: center; gap: 8px;
        }
        .section-header i { color: #0284c7; }
        
        /* h2 Headers */
        h2 { color: #0f172a; font-weight: 700; }
        h2 i { color: #0284c7; }

        /* Sidebar Material */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
            box-shadow: 2px 0 8px rgba(0,0,0,0.05);
        }
        [data-testid="stSidebar"] * {
            color: #1e293b !important;
        }
        [data-testid="stSidebar"] .block-container { padding-top: 2rem; }

        .sidebar-logo {
            text-align: center; padding: 0 0 24px 0;
            border-bottom: 1px solid #e2e8f0; margin-bottom: 20px;
        }
        .sidebar-logo h2 { color: #0f172a !important; font-size: 1.3rem; font-weight: 700; margin: 0; }
        .sidebar-logo p  { color: #64748b !important; font-size: 0.75rem; margin: 4px 0 0 0; font-weight: 500; }

        /* Hide default elements */
        #MainMenu, footer, header { visibility: hidden; }
        .stDeployButton { display: none; }
    </style>
    """, unsafe_allow_html=True)

def kpi_card(label, value, delta=None, color="green"):
    delta_html = ""
    if delta is not None:
        sign = '<i class="fa-solid fa-arrow-trend-up"></i>' if delta >= 0 else '<i class="fa-solid fa-arrow-trend-down"></i>'
        cls  = "up" if delta >= 0 else "down"
        delta_html = f'<div class="kpi-delta {cls}">{sign} <span>{abs(delta):.1f}% vs période préc.</span></div>'
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
