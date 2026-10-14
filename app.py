import os
import pandas as pd
import streamlit as st
from modules.utils import load_models
from modules.landing import render_landing_page
from modules.siem import render_siem_page
from modules.currency import render_currency_page
from modules.arrest import render_arrest_page
from modules.phishing import render_phishing_page
from modules.network import render_network_page
from modules.shield import render_shield_page
from modules.database import init_db

# Initialize database threat registry
init_db()

# Set page configuration with a premium icon and title
st.set_page_config(
    page_title="SURAJYA-AI: Public Safety Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# PREMIUM COMMAND-CENTER CSS DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Manrope:wght@300;400;500;600;700;800&display=swap');

    /* ── Design Tokens ── */
    :root {
        --bg-base: #080B14;
        --bg-sidebar: #0C1120;
        --bg-surface: #111827;
        --bg-elevated: #161F31;
        --bg-hover: #1C2640;
        --border-primary: #273449;
        --border-subtle: #1E293B;
        --cyan-primary: #22D3EE;
        --blue-primary: #3B82F6;
        --violet-accent: #8B5CF6;
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --success: #34D399;
        --warning: #FBBF24;
        --critical: #FB7185;
        --font-heading: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --transition-smooth: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ── Global Reset & Base ── */
    .stApp {
        background-color: var(--bg-base) !important;
        color: var(--text-primary) !important;
        font-family: var(--font-body) !important;
    }
    
    .stApp > header {
        background-color: transparent !important;
    }

    /* Remove default streamlit padding excess */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-base); }
    ::-webkit-scrollbar-thumb { background: var(--border-primary); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

    /* ── Typography ── */
    h1, h2, h3 {
        font-family: var(--font-heading) !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em !important;
    }
    h1 { font-weight: 800 !important; font-size: 1.75rem !important; }
    h2 { font-weight: 700 !important; font-size: 1.35rem !important; }
    h3 { font-weight: 600 !important; font-size: 1.1rem !important; }
    p, li, span { color: var(--text-secondary) !important; }

    /* ── Premium Card System ── */
    .sj-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 24px;
        transition: var(--transition-smooth);
        position: relative;
        overflow: hidden;
    }
    .sj-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(34,211,238,0.15), transparent);
    }
    .sj-card:hover {
        border-color: var(--border-primary);
        transform: translateY(-1px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }

    /* Glass Card (legacy compat) */
    .glass-card, .role-card, .ops-card, .ticker-card, .chat-container {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-lg) !important;
        padding: 24px !important;
        transition: var(--transition-smooth) !important;
        position: relative !important;
    }
    .glass-card:hover, .role-card:hover {
        border-color: var(--border-primary) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
    }

    /* ── Metric Cards ── */
    .sj-metric-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 20px 24px;
        transition: var(--transition-smooth);
        position: relative;
        overflow: hidden;
    }
    .sj-metric-card::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--cyan-primary), var(--blue-primary));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .sj-metric-card:hover {
        border-color: var(--border-primary);
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }
    .sj-metric-card:hover::after {
        opacity: 1;
    }
    .sj-metric-icon {
        width: 40px; height: 40px;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 18px;
        margin-bottom: 14px;
    }
    .sj-metric-label {
        font-family: var(--font-body);
        font-size: 11.5px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: var(--text-muted) !important;
        margin-bottom: 6px;
    }
    .sj-metric-value {
        font-family: var(--font-heading);
        font-size: 28px;
        font-weight: 800;
        color: var(--text-primary) !important;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    .sj-metric-source {
        font-size: 11px;
        color: var(--text-muted) !important;
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid var(--border-subtle);
    }

    /* Card Title & Value (legacy compat) */
    .card-title {
        font-family: var(--font-body) !important;
        font-size: 11.5px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        color: var(--text-muted) !important;
        margin-bottom: 8px !important;
    }
    .card-value {
        font-family: var(--font-heading) !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em !important;
    }
    .card-footer {
        font-size: 11px !important;
        color: var(--text-muted) !important;
        margin-top: 8px !important;
        padding-top: 8px !important;
        border-top: 1px solid var(--border-subtle) !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-subtle) !important;
    }
    section[data-testid="stSidebar"] h1 {
        font-family: var(--font-heading) !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        letter-spacing: -0.01em !important;
    }
    section[data-testid="stSidebar"] h2 {
        font-family: var(--font-heading) !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar section labels */
    .sj-nav-section {
        font-family: var(--font-body);
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: var(--text-muted) !important;
        padding: 16px 0 6px 4px;
        margin-top: 4px;
    }

    /* ── Sidebar Radio Nav Items ── */
    div.row-widget.stRadio [data-testid="stWidgetLabel"] {
        display: none !important;
    }
    div.row-widget.stRadio div[role="radiogroup"] label input[type="radio"] {
        display: none !important;
    }
    div.row-widget.stRadio div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
        font-size: 13.5px !important;
    }
    div.row-widget.stRadio > div[role="radiogroup"] {
        gap: 4px !important;
    }
    div.row-widget.stRadio > div[role="radiogroup"] label {
        background: transparent !important;
        border: 1px solid transparent !important;
        padding: 10px 14px !important;
        border-radius: var(--radius-sm) !important;
        transition: var(--transition-smooth) !important;
        width: 100% !important;
        cursor: pointer !important;
        font-family: var(--font-body) !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
    }
    div.row-widget.stRadio > div[role="radiogroup"] label:hover {
        background: rgba(34,211,238,0.04) !important;
        color: var(--text-primary) !important;
    }
    div.row-widget.stRadio > div[role="radiogroup"] label[data-checked="true"] {
        background: rgba(34,211,238,0.08) !important;
        border-color: rgba(34,211,238,0.2) !important;
        color: var(--cyan-primary) !important;
        font-weight: 600 !important;
        box-shadow: inset 3px 0 0 var(--cyan-primary) !important;
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0 !important;
    }

    /* ── Buttons ── */
    div.stButton > button {
        background: var(--bg-surface) !important;
        color: var(--cyan-primary) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: var(--radius-sm) !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        font-family: var(--font-body) !important;
        transition: var(--transition-smooth) !important;
        letter-spacing: 0.01em !important;
    }
    div.stButton > button:hover {
        background: rgba(34,211,238,0.08) !important;
        border-color: rgba(34,211,238,0.35) !important;
        color: #fff !important;
        box-shadow: 0 0 15px rgba(34,211,238,0.1) !important;
    }
    div.stButton > button:active {
        background: rgba(34,211,238,0.12) !important;
        transform: scale(0.98) !important;
    }
    div.stButton > button:focus {
        border-color: var(--cyan-primary) !important;
        box-shadow: 0 0 0 2px rgba(34,211,238,0.2) !important;
    }

    /* Primary action button variant */
    .sj-btn-primary {
        background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(59,130,246,0.15)) !important;
        border-color: rgba(34,211,238,0.3) !important;
    }

    /* ── Inputs ── */
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
    }
    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea, div[data-baseweb="select"] span {
        color: var(--text-primary) !important;
        background: transparent !important;
        font-family: var(--font-body) !important;
    }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
        border-color: rgba(34,211,238,0.4) !important;
        box-shadow: 0 0 0 2px rgba(34,211,238,0.1) !important;
    }

    /* Selectbox popup */
    ul[role="listbox"] {
        background-color: var(--bg-elevated) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: var(--radius-md) !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.5) !important;
    }
    ul[role="listbox"] li {
        color: var(--text-secondary) !important;
        transition: all 0.15s ease !important;
    }
    ul[role="listbox"] li:hover {
        background-color: rgba(34,211,238,0.08) !important;
        color: var(--text-primary) !important;
    }

    /* ── Alerts ── */
    .custom-alert {
        padding: 16px 20px !important;
        border-radius: var(--radius-md) !important;
        margin-bottom: 16px !important;
        font-weight: 500 !important;
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-subtle) !important;
    }
    .alert-red {
        border-left: 3px solid var(--critical) !important;
        background: rgba(251,113,133,0.04) !important;
    }
    .alert-red h3, .alert-red h4 { color: var(--critical) !important; }
    .alert-red p { color: #FDA4AF !important; }
    .alert-green {
        border-left: 3px solid var(--success) !important;
        background: rgba(52,211,153,0.04) !important;
    }
    .alert-green h3, .alert-green h4 { color: var(--success) !important; }
    .alert-green p { color: #6EE7B7 !important; }
    .alert-orange {
        border-left: 3px solid var(--warning) !important;
        background: rgba(251,191,36,0.04) !important;
    }
    .alert-orange h3, .alert-orange h4 { color: var(--warning) !important; }
    .alert-orange p { color: #FCD34D !important; }

    /* ── Chat Bubbles ── */
    .chat-bubble {
        padding: 14px 18px !important;
        border-radius: 14px !important;
        max-width: 80% !important;
        line-height: 1.6 !important;
        font-size: 14px !important;
    }
    .chat-citizen {
        background-color: var(--bg-elevated) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-subtle) !important;
    }
    .chat-agent {
        background: rgba(34,211,238,0.04) !important;
        color: var(--cyan-primary) !important;
        border-left: 3px solid var(--cyan-primary) !important;
        border: 1px solid rgba(34,211,238,0.12) !important;
        border-left: 3px solid var(--cyan-primary) !important;
    }

    /* ── Role Cards ── */
    .role-citizen { border-top: 2px solid var(--success) !important; }
    .role-bank { border-top: 2px solid var(--cyan-primary) !important; }
    .role-police { border-top: 2px solid var(--violet-accent) !important; }
    .role-gov { border-top: 2px solid var(--critical) !important; }

    /* ── Command Header ── */
    .sj-header {
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 20px 28px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 16px;
        position: relative;
        overflow: hidden;
    }
    .sj-header::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, var(--cyan-primary), var(--blue-primary), var(--violet-accent));
        opacity: 0.5;
    }
    .sj-header-brand {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .sj-header-shield {
        width: 44px; height: 44px;
        background: linear-gradient(135deg, rgba(34,211,238,0.12), rgba(139,92,246,0.12));
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        border: 1px solid rgba(34,211,238,0.2);
    }
    .sj-header-shield svg {
        width: 24px; height: 24px;
    }
    .sj-header-title {
        font-family: var(--font-heading);
        font-size: 20px;
        font-weight: 800;
        background: linear-gradient(135deg, var(--cyan-primary), var(--blue-primary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }
    .sj-header-subtitle {
        font-size: 12.5px;
        color: var(--text-muted);
        font-weight: 400;
        margin-top: 2px;
    }
    .sj-header-status {
        display: flex;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    .sj-status-dot {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        color: var(--text-muted);
    }
    .sj-status-dot .dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: var(--success);
        box-shadow: 0 0 8px rgba(52,211,153,0.4);
        animation: pulse-dot 2s ease-in-out infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; box-shadow: 0 0 8px rgba(52,211,153,0.4); }
        50% { opacity: 0.6; box-shadow: 0 0 4px rgba(52,211,153,0.2); }
    }

    /* ── Section Dividers ── */
    hr {
        border: none !important;
        border-top: 1px solid var(--border-subtle) !important;
        margin: 20px 0 !important;
    }

    /* ── Data Tables ── */
    .stDataFrame {
        border-radius: var(--radius-md) !important;
        overflow: hidden !important;
    }

    /* ── Streamlit Metrics ── */
    div[data-testid="stMetric"] {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-md) !important;
        padding: 16px !important;
    }
    div[data-testid="stMetric"] label {
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 11px !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-family: var(--font-heading) !important;
        font-weight: 800 !important;
    }

    /* ── File Uploader ── */
    section[data-testid="stFileUploader"] {
        border: 1px dashed var(--border-primary) !important;
        border-radius: var(--radius-md) !important;
        background: rgba(17,24,39,0.5) !important;
    }

    /* ── Checkbox ── */
    div[data-testid="stCheckbox"] label span {
        color: var(--text-secondary) !important;
    }

    /* ── Expander ── */
    details {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-md) !important;
    }

    /* ── Tabs ── */
    button[data-baseweb="tab"] {
        color: var(--text-muted) !important;
        font-weight: 500 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--cyan-primary) !important;
    }

    /* ── Code blocks ── */
    pre {
        background: var(--bg-base) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* ── Toast / Success / Warning / Error / Info  ── */
    div[data-testid="stAlert"] {
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border-subtle) !important;
    }

    /* ── Sidebar Brand Block ── */
    .sj-sidebar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 4px 16px 4px;
        margin-bottom: 8px;
        border-bottom: 1px solid var(--border-subtle);
    }
    .sj-sidebar-shield {
        width: 38px; height: 38px;
        background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(59,130,246,0.15));
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        border: 1px solid rgba(34,211,238,0.2);
        flex-shrink: 0;
    }
    .sj-sidebar-title {
        font-family: var(--font-heading);
        font-size: 15px;
        font-weight: 800;
        color: var(--text-primary);
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .sj-sidebar-desc {
        font-size: 10.5px;
        color: var(--text-muted);
        font-weight: 400;
        margin-top: 1px;
    }

    /* ── Sidebar Footer ── */
    .sj-sidebar-footer {
        position: fixed;
        bottom: 0;
        width: inherit;
        padding: 12px 16px;
        border-top: 1px solid var(--border-subtle);
        background: var(--bg-sidebar);
        font-size: 10px;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .sj-sidebar-footer .dot-green {
        width: 5px; height: 5px;
        background: var(--success);
        border-radius: 50%;
        box-shadow: 0 0 5px rgba(52,211,153,0.5);
    }

    /* ── Reduced Motion ── */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0s !important;
            transition-duration: 0s !important;
        }
    }

    /* ── Mobile Responsive ── */
    @media (max-width: 768px) {
        .sj-header {
            flex-direction: column;
            align-items: flex-start;
            padding: 16px 20px;
        }
        .sj-header-status {
            width: 100%;
            justify-content: flex-start;
        }
        .sj-metric-value {
            font-size: 22px;
        }
        .card-value {
            font-size: 22px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load dataframes and pre-trained models
@st.cache_data
def load_data():
    cyber_df = pd.read_csv("cybersecurity_large_synthesized_data.csv") if os.path.exists("cybersecurity_large_synthesized_data.csv") else pd.DataFrame()
    financial_df = pd.read_csv("Synthetic_Financial_datasets_small.csv") if os.path.exists("Synthetic_Financial_datasets_small.csv") else pd.DataFrame()
    return cyber_df, financial_df

cyber_df, financial_df = load_data()
models = load_models()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR: Refined Intelligence Navigation Panel
# ─────────────────────────────────────────────────────────────────────────────

# Brand block
st.sidebar.markdown("""
<div class='sj-sidebar-brand'>
    <div class='sj-sidebar-shield'>
        <svg viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
    </div>
    <div>
        <div class='sj-sidebar-title'>SURAJYA-AI</div>
        <div class='sj-sidebar-desc'>Public Safety Intelligence</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation sections
st.sidebar.markdown("<div class='sj-nav-section'>Overview</div>", unsafe_allow_html=True)

selected_tab = st.sidebar.radio(
    "Choose Active Platform Component:",
    [
        "🏠 SURAJYA-AI Platform Hub",
        "📊 SIEM-Lite & Command Hotspots",
        "💵 Counterfeit Currency Identification",
        "📞 Digital Arrest scam detection",
        "📧 Phishing Email Analyzer",
        "🕸️ Fraud Network Graph Intelligence",
        "💬 Citizen Fraud Shield"
    ],
    label_visibility="collapsed"
)

# Sidebar footer
st.sidebar.markdown("""
<div style='margin-top: 30px; padding: 12px 4px; border-top: 1px solid #1E293B;'>
    <div style='display: flex; align-items: center; gap: 6px; margin-bottom: 4px;'>
        <div style='width: 5px; height: 5px; background: #34D399; border-radius: 50%; box-shadow: 0 0 5px rgba(52,211,153,0.5);'></div>
        <span style='font-size: 10.5px; color: #64748B;'>All Systems Operational</span>
    </div>
    <span style='font-size: 10px; color: #475569;'>v2.0 · Threat Engine Active</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# COMMAND-CENTER HEADER
# ─────────────────────────────────────────────────────────────────────────────
from datetime import datetime
current_time = datetime.now().strftime("%d %b %Y · %H:%M IST")

st.markdown(f"""
<div class='sj-header'>
    <div class='sj-header-brand'>
        <div class='sj-header-shield'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
        </div>
        <div>
            <div class='sj-header-title'>SURAJYA-AI PUBLIC SAFETY SUITE</div>
            <div class='sj-header-subtitle'>Multi-Agency Threat Mitigation & Real-time Digital Fraud Countermeasures</div>
        </div>
    </div>
    <div class='sj-header-status'>
        <div class='sj-status-dot'>
            <div class='dot'></div>
            <span>Threat Engine Active</span>
        </div>
        <div class='sj-status-dot'>
            <span style='color: #475569;'>⏱</span>
            <span>{current_time}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ROUTE TO MODULES
# ─────────────────────────────────────────────────────────────────────────────
if selected_tab == "🏠 SURAJYA-AI Platform Hub":
    render_landing_page()
elif selected_tab == "📊 SIEM-Lite & Command Hotspots":
    render_siem_page(cyber_df)
elif selected_tab == "💵 Counterfeit Currency Identification":
    render_currency_page(models)
elif selected_tab == "📞 Digital Arrest scam detection":
    render_arrest_page(models)
elif selected_tab == "📧 Phishing Email Analyzer":
    render_phishing_page(models)
elif selected_tab == "🕸️ Fraud Network Graph Intelligence":
    render_network_page(financial_df)
elif selected_tab == "💬 Citizen Fraud Shield":
    render_shield_page()
