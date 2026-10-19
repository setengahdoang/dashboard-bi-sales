import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
import os
from datetime import datetime


st.set_page_config(
    page_title="Projek Dashboard Manufaktur",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

    /* ── Root & Main Area ── */
    .stApp {
        background-color: #0b0c0e;
        color: #f4f4f5;
        font-family: 'Inter', sans-serif;
    }
    
    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #101216 !important;
        border-right: 1px solid #1e2229;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown label,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: #9ca3af !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stRadio label {
        color: #9ca3af !important;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
    }

    /* ── Hide default streamlit branding ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Glass Card ── */
    .glass-card {
        background: #13151b;
        border: 1px solid #20232c;
        border-radius: 0.75rem;
        padding: 1.25rem 1.5rem;
        transition: all 0.2s ease;
    }
    .glass-card:hover {
        border-color: #383c47;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: #13151b;
        border: 1px solid #20232c;
        border-radius: 0.75rem;
        padding: 1.25rem 1.5rem;
        transition: all 0.2s ease;
        min-height: 125px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .metric-card:hover {
        border-color: #383c47;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        transform: translateY(-2px);
    }
    .metric-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.03em;
        line-height: 1.2;
        color: #ffffff;
    }
    .metric-value.small-text {
        font-size: 1.25rem;
    }
    .metric-subtext {
        font-size: 0.7rem;
        color: #6b7280;
        margin-top: 0.25rem;
        font-weight: 500;
    }

    /* ── Status Cards (clickable) ── */
    .status-card {
        background: #13151b;
        border: 1px solid #20232c;
        border-radius: 0.75rem;
        padding: 1.25rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .status-card:hover {
        transform: translateY(-2px);
        border-color: #383c47;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }
    .status-label {
        margin-bottom: 0.5rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.75rem;
        border-radius: 9999px;
        border: 1px solid #2a2e39;
        background: #181b22;
        color: #d1d5db;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.12em;
    }
    .status-value {
        font-size: 2rem;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        color: #ffffff;
    }

    /* ── Section Headings ── */
    .section-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Tables ── */
    .dataframe-container {
        background: #13151b;
        border: 1px solid #20232c;
        border-radius: 0.75rem;
        overflow: hidden;
    }

    /* Override Streamlit dataframe styles */
    .stDataFrame {
        border: none !important;
    }

    /* ── Filter active indicator ── */
    .filter-active-bar {
        background: #13151b;
        border: 1px solid #262933;
        border-radius: 0.75rem;
        padding: 0.75rem 1.25rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
    }
    .filter-active-bar .pulse-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #e4e4e7;
        margin-right: 10px;
        animation: pulse-animation 2s infinite;
    }
    @keyframes pulse-animation {
        0% { box-shadow: 0 0 0 0 rgba(255,255,255,0.4); }
        70% { box-shadow: 0 0 0 8px rgba(255,255,255,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); }
    }
    
    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid #20232c;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #71717a;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-size: 0.85rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
        color: #ffffff !important;
        border-bottom: 2px solid #ffffff !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.25); }
    
    /* ── Plotly chart background fix ── */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }

    /* ── Sidebar header ── */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding: 0.5rem;
    }
    .sidebar-brand-icon {
        background: #181b22;
        border: 1px solid #262933;
        padding: 0.5rem;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .sidebar-brand-text h2 {
        font-family: 'Outfit', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .sidebar-brand-text p {
        font-size: 0.6rem;
        color: #9ca3af;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        margin: 0;
    }
    
    /* ── Animations ── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeInUp 0.4s ease forwards;
    }
    
    /* ── Download button ── */
    .stDownloadButton > button {
        background: #181b22 !important;
        border: 1px solid #2a2e39 !important;
        color: #e4e4e7 !important;
        border-radius: 0.5rem !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        background: #222631 !important;
        border-color: #3f4555 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    /* ── Selectbox styling ── */
    .stSelectbox > div > div {
        background-color: #14161d !important;
        border: 1px solid #262933 !important;
        border-radius: 0.5rem !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)




GOOGLE_SHEETS_URL = os.getenv(
    "GOOGLE_SHEETS_URL",
    ""
)


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Exact replica of backend/main.py preprocess_dataframe."""
    df.columns = df.columns.str.strip()

    if 'IDPA' in df.columns:
        df['IDPA_Internal'] = df['IDPA'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    else:
        df['IDPA_Internal'] = "N/A"

    revenue_cols = ['Revenue', 'revenue', 'REVENUE', 'hargaPelanggan', 'Harga']
    found_cols = [c for c in revenue_cols if c in df.columns]
    if found_cols:
        primary_col = found_cols[0]
        s = df[primary_col].astype(str).str.replace('Rp', '', case=False).str.replace('.', '', regex=False).str.replace(',', '', regex=False)
        df['Revenue_Internal'] = pd.to_numeric(s.str.replace(r'[^0-9]', '', regex=True), errors='coerce').fillna(0)
        for fallback_col in found_cols[1:]:
            mask_zero = df['Revenue_Internal'] == 0
            if mask_zero.any():
                s2 = df.loc[mask_zero, fallback_col].astype(str).str.replace('Rp', '', case=False).str.replace('.', '', regex=False).str.replace(',', '', regex=False)
                fallback_vals = pd.to_numeric(s2.str.replace(r'[^0-9]', '', regex=True), errors='coerce').fillna(0)
                df.loc[mask_zero, 'Revenue_Internal'] = fallback_vals
    else:
        df['Revenue_Internal'] = 0

    df['Status_Cek'] = ""
    if 'STATUS SO' in df.columns:
        df['Status_Cek'] += df['STATUS SO'].astype(str) + " "
    if 'statusPA' in df.columns:
        df['Status_Cek'] += df['statusPA'].astype(str)
    df['Status_Cek'] = df['Status_Cek'].str.upper().str.strip()

    update_col = next((c for c in ['UPDATE', 'Update', 'update'] if c in df.columns), None)
    if update_col:
        df['UPDATE_Internal'] = df[update_col].astype(str).str.strip().replace(r'^#.*', '-', regex=True)
    else:
        df['UPDATE_Internal'] = "-"

    date_col = next((c for c in ['CREATEDON', 'createdon', 'Date', 'date', 'Tanggal', 'tanggal'] if c in df.columns), None)
    if date_col:
        df['Date_Internal'] = pd.to_datetime(df[date_col], errors='coerce')
        df['Aging_Hari'] = (datetime.now() - df['Date_Internal']).dt.days.fillna(0).astype(int)
        df['Tahun_Filter'] = df['Date_Internal'].dt.year.fillna(0).astype(int)
    else:
        df['Date_Internal'] = pd.NaT
        df['Aging_Hari'] = 0
        df['Tahun_Filter'] = 0

    prod_col = next((c for c in ['namaProduk', 'Produk', 'produk', 'Product', 'product'] if c in df.columns), None)
    if prod_col:
        df['Produk_Internal'] = df[prod_col].astype(str).str.strip()
    else:
        df['Produk_Internal'] = "N/A"

    cust_col = next((c for c in ['CUSTOMERNAME', 'CustomerName', 'customer', 'Customer', 'Pelanggan'] if c in df.columns), None)
    if cust_col:
        df['Customer_Internal'] = df[cust_col].astype(str).str.strip().str.upper()
        df['Customer_Internal'] = df['Customer_Internal'].str.replace(r'PT\.?\s*', 'PT ', regex=True).str.replace(r'TBK\.?\s*', 'TBK', regex=True).str.replace(',', '', regex=False)
    else:
        df['Customer_Internal'] = "N/A"

    if 'namaSales' not in df.columns:
        for c in ['Sales', 'sales', 'NamaSales', 'SALES']:
            if c in df.columns:
                df['namaSales'] = df[c]
                break
        if 'namaSales' not in df.columns:
            df['namaSales'] = "N/A"

    if 'SBUNODE' not in df.columns:
        for c in ['SBU', 'sbu', 'Sbu']:
            if c in df.columns:
                df['SBUNODE'] = df[c]
                break
        if 'SBUNODE' not in df.columns:
            df['SBUNODE'] = "N/A"

    for col in df.columns:
        if col == 'Date_Internal':
            continue
        if df[col].dtype == 'object':
            df[col] = df[col].fillna("-").astype(str)
        else:
            df[col] = df[col].fillna(0)

    return df


@st.cache_data(ttl=300, show_spinner=False)
def load_data() -> pd.DataFrame:
    """Fetch data from Google Sheets with retry logic, cached for 5 minutes."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(GOOGLE_SHEETS_URL, timeout=30)
            response.raise_for_status()
            df = pd.read_csv(io.StringIO(response.text), low_memory=False)
            return preprocess_dataframe(df)
        except Exception as e:
            if attempt == max_retries - 1:
                st.error(f"❌ Gagal memuat data dari Google Sheets setelah {max_retries} percobaan: {e}")
                return pd.DataFrame()
            import time
            time.sleep(2)
    return pd.DataFrame()


def apply_filters(df: pd.DataFrame, tahun: str, sales: str, sbu: str, status: str, customer: str) -> pd.DataFrame:
    """Exact replica of backend/main.py apply_filters."""
    if df.empty:
        return df
    dff = df.copy()

    if tahun and tahun != "Semua Tahun":
        try:
            dff = dff[dff['Tahun_Filter'] == int(tahun)]
        except (ValueError, TypeError):
            pass

    if sales and sales != "Semua Sales" and 'namaSales' in dff.columns:
        dff = dff[dff['namaSales'] == sales]

    if sbu and sbu != "Semua SBU" and 'SBUNODE' in dff.columns:
        dff = dff[dff['SBUNODE'] == sbu]

    if customer and customer != "Semua Pelanggan" and 'Customer_Internal' in dff.columns:
        dff = dff[dff['Customer_Internal'] == customer]

    if status and status != "SEMUA":
        if 'Status_Cek' in dff.columns:
            if status == "OPEN":
                mask = (dff['Status_Cek'].str.contains("OPEN", na=False)) & (~dff['Status_Cek'].str.contains("CANCEL", na=False))
                dff = dff[mask]
            elif status == "CLOSE":
                dff = dff[dff['Status_Cek'].str.contains("CLOSE", na=False)]
            elif status == "CANCEL":
                dff = dff[dff['Status_Cek'].str.contains("CANCEL", na=False)]

    return dff


def format_currency(val: float) -> str:
    """Format number as Indonesian Rupiah."""
    return f"Rp {val:,.0f}".replace(",", ".")


def format_durasi(hari: int) -> str:
    """Exact replica of backend aging duration formatter."""
    try:
        h = int(hari)
        if h < 0:
            return "0 Hari"
        res = []
        if h // 365 > 0:
            res.append(f"{h // 365} Tahun")
        if (h % 365) // 30 > 0:
            res.append(f"{(h % 365) // 30} Bulan")
        if (h % 365) % 30 > 0 or not res:
            res.append(f"{(h % 365) % 30} Hari")
        return " ".join(res)
    except (ValueError, TypeError):
        return "0 Hari"


def kategori_aging(hari: int) -> str:
    """Exact replica of backend aging category."""
    try:
        h = int(hari)
        if h <= 14:
            return "0-14 Hari"
        elif h <= 30:
            return "15-30 Hari"
        elif h <= 365:
            return "31-365 Hari"
        return "> 365 Hari"
    except (ValueError, TypeError):
        return "N/A"




with st.spinner("⚡ Menghubungkan ke Sales Engine..."):
    df_raw = load_data()

if df_raw.empty:
    st.error("🚫 Data kosong. Periksa koneksi Google Sheets atau coba lagi.")
    st.stop()




with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">⚡</div>
        <div class="sidebar-brand-text">
            <h2>MANUFAKTUR DASH</h2>
            <p>Active System</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size: 0.9rem; font-weight: 600; color: #f4f4f5; margin-bottom: 0.5rem;">Control Panel</div>', unsafe_allow_html=True)

    years = sorted([int(t) for t in df_raw['Tahun_Filter'].unique() if int(t) > 0])
    year_options = ["Semua Tahun"] + [str(y) for y in years]

    sales_list = sorted([str(s) for s in df_raw['namaSales'].dropna().unique() if str(s) not in ['-', 'N/A', 'nan']])
    sales_options = ["Semua Sales"] + sales_list

    sbu_list = sorted([str(s) for s in df_raw['SBUNODE'].dropna().unique() if str(s) not in ['-', 'N/A', 'nan']])
    sbu_options = ["Semua SBU"] + sbu_list

    customer_list = sorted([str(s) for s in df_raw['Customer_Internal'].dropna().unique() if str(s) not in ['-', 'N/A', 'nan']])
    customer_options = ["Semua Pelanggan"] + customer_list

    st.markdown("")
    sel_tahun = st.selectbox("📅 Pilih Tahun", year_options, key="filter_year")
    sel_sales = st.selectbox("👤 Pilih Sales", sales_options, key="filter_sales")
    sel_sbu = st.selectbox("🏢 Pilih SBU", sbu_options, key="filter_sbu")
    sel_customer = st.selectbox("🔍 Pilih Pelanggan", customer_options, key="filter_customer")

    st.markdown("---")

    if 'status_filter' not in st.session_state:
        st.session_state.status_filter = "SEMUA"

    status_options = ["SEMUA", "OPEN", "CLOSE", "CANCEL"]
    sel_status = st.radio("📊 Filter Status", status_options, index=status_options.index(st.session_state.status_filter), key="filter_status_radio", horizontal=True)
    st.session_state.status_filter = sel_status

    st.markdown("---")

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.caption("Dashboard v3.0 • Streamlit Edition")




df = apply_filters(df_raw, sel_tahun, sel_sales, sel_sbu, st.session_state.status_filter, sel_customer)

df_no_status = apply_filters(df_raw, sel_tahun, sel_sales, sel_sbu, None, sel_customer)

mask_open = (df_no_status['Status_Cek'].str.contains("OPEN", na=False)) & (~df_no_status['Status_Cek'].str.contains("CANCEL", na=False))
mask_closed = df_no_status['Status_Cek'].str.contains("CLOSE", na=False)
mask_cancel = df_no_status['Status_Cek'].str.contains("CANCEL", na=False)

count_open = int(df_no_status[mask_open]['IDPA_Internal'].nunique())
count_closed = int(df_no_status[mask_closed]['IDPA_Internal'].nunique())
count_cancel = int(df_no_status[mask_cancel]['IDPA_Internal'].nunique())

total_pa = int(df['IDPA_Internal'].nunique())
total_revenue = float(df['Revenue_Internal'].sum())
conversion_rate = (count_closed / total_pa * 100) if total_pa > 0 else 0.0


st.markdown("""
<div class="fade-in" style="margin-bottom: 2rem;">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div style="background: #e4e4e7; width: 4px; height: 44px; border-radius: 9999px;"></div>
        <div>
            <h1 style="font-family: 'Outfit', sans-serif; font-size: 2.25rem; font-weight: 700; letter-spacing: -0.03em; margin: 0; color: #ffffff;">
                Projek Dashboard Manufaktur
            </h1>
            <p style="color: #9ca3af; font-size: 1rem; margin: 0;">
                Analisis Performa dan Tracking Dashboard
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div class="metric-label">📽️ Total Proyek (PA)</div>
        <div class="metric-value">{total_pa:,}</div>
        <div class="metric-subtext">Unique projects processed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    rev_display = format_currency(total_revenue)
    size_class = "small-text" if len(rev_display) > 18 else ""
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div class="metric-label">📈 Total Pendapatan</div>
        <div class="metric-value {size_class}">{rev_display}</div>
        <div class="metric-subtext">Combined revenue value</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div class="metric-label">⏱️ Active Projects</div>
        <div class="metric-value">{count_open:,}</div>
        <div class="metric-subtext">Currently running</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div class="metric-label">✅ Conversion Rate</div>
        <div class="metric-value">{conversion_rate:.1f}%</div>
        <div class="metric-subtext">Closing probability</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)




if st.session_state.status_filter != "SEMUA":
    st.markdown(f"""
    <div class="filter-active-bar fade-in">
        <div style="display: flex; align-items: center;">
            <span class="pulse-dot"></span>
            <span style="color: #f4f4f5; font-weight: 500;">
                Tampilan saat ini dikunci untuk Status: <strong style="color: #ffffff; text-transform: uppercase;">{st.session_state.status_filter}</strong>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)




st.markdown('<div class="section-title fade-in">📊 Project Tracking Status</div>', unsafe_allow_html=True)

col_o, col_c, col_x = st.columns(3)

with col_o:
    st.markdown(f"""
    <div class="status-card fade-in">
        <div class="status-label"><span class="status-badge">OPEN</span></div>
        <div class="status-value">{count_open:,}</div>
        <div class="metric-subtext">Gunakan sidebar untuk filter</div>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    st.markdown(f"""
    <div class="status-card fade-in">
        <div class="status-label"><span class="status-badge">CLOSE</span></div>
        <div class="status-value">{count_closed:,}</div>
        <div class="metric-subtext">Gunakan sidebar untuk filter</div>
    </div>
    """, unsafe_allow_html=True)

with col_x:
    st.markdown(f"""
    <div class="status-card fade-in">
        <div class="status-label"><span class="status-badge">CANCEL</span></div>
        <div class="status-value">{count_cancel:,}</div>
        <div class="metric-subtext">Gunakan sidebar untuk filter</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)


chart_left, chart_right = st.columns(2)
with chart_left:
    st.markdown('<div class="section-title">📈 Tren Rilis Proyek Per Bulan</div>', unsafe_allow_html=True)
    
    df_date = df.dropna(subset=['Date_Internal']).copy()
    if not df_date.empty:
        kamus_bulan = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun',
                       7: 'Jul', 8: 'Ags', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'}
        df_date['Bulan_Angka'] = df_date['Date_Internal'].dt.month
        df_date['Bulan'] = df_date['Bulan_Angka'].map(kamus_bulan)
        trend = df_date.groupby(['Bulan_Angka', 'Bulan'])['IDPA_Internal'].nunique().reset_index().sort_values('Bulan_Angka')

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=trend['Bulan'], y=trend['IDPA_Internal'],
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#d1d5db', width=2.5, shape='spline'),
            fillcolor='rgba(255, 255, 255, 0.05)',
            marker=dict(size=5, color='#ffffff', line=dict(color='#111318', width=1.5)),
            hovertemplate='<b>%{x}</b><br>%{y} Projects<extra></extra>',
        ))
        fig_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#9ca3af', family='Inter'),
            margin=dict(l=20, r=20, t=10, b=40),
            height=350,
            xaxis=dict(showgrid=False, showline=False, tickfont=dict(size=11, color='#9ca3af')),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', showline=False, tickfont=dict(size=11, color='#9ca3af')),
            hoverlabel=dict(bgcolor='#181b22', bordercolor='#2a2e39', font=dict(color='#ffffff', size=12)),
        )
        st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Tidak ada data tren untuk filter yang dipilih.")



with chart_right:
    st.markdown('<div class="section-title">🏢 Top 10 Pelanggan</div>', unsafe_allow_html=True)

    tab_rev, tab_pa = st.tabs(["💰 By Revenue", "📦 By PA"])

    with tab_rev:
        if not df.empty and 'Customer_Internal' in df.columns:
            top_rev = df.groupby('Customer_Internal')['Revenue_Internal'].sum().sort_values(ascending=False).head(10).reset_index()
            if not top_rev.empty:
                top_rev['Revenue_Display'] = top_rev['Revenue_Internal'].apply(lambda x: f"{x:,.0f}".replace(",", "."))

                fig_rev = go.Figure(go.Bar(
                    x=top_rev['Revenue_Internal'],
                    y=top_rev['Customer_Internal'],
                    orientation='h',
                    marker=dict(
                        color=top_rev['Revenue_Internal'],
                        colorscale=[[0, '#262933'], [0.5, '#4b5563'], [1, '#d1d5db']],
                        line=dict(width=0),
                    ),
                    hovertemplate='<b>%{y}</b><br>Rp %{x:,.0f}<extra></extra>',
                ))
                fig_rev.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#9ca3af', family='Inter', size=11),
                    margin=dict(l=10, r=20, t=10, b=20),
                    height=320,
                    yaxis=dict(autorange='reversed', showgrid=False, showline=False, tickfont=dict(size=10, color='#9ca3af')),
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', showline=False, tickfont=dict(size=10, color='#9ca3af')),
                    hoverlabel=dict(bgcolor='#181b22', bordercolor='#2a2e39', font=dict(color='#ffffff', size=12)),
                )
                st.plotly_chart(fig_rev, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("Tidak ada data revenue.")
        else:
            st.info("Tidak ada data pelanggan.")

    with tab_pa:
        if not df.empty and 'Customer_Internal' in df.columns:
            agg_dict = {'IDPA_Internal': 'nunique', 'Revenue_Internal': 'sum'}
            if 'namaSales' in df.columns:
                agg_dict['namaSales'] = 'first'
            if 'SBUNODE' in df.columns:
                agg_dict['SBUNODE'] = 'first'
            top_pa = df.groupby('Customer_Internal').agg(agg_dict).sort_values(by='IDPA_Internal', ascending=False).head(10).reset_index()

            if not top_pa.empty:
                display_df = pd.DataFrame({
                    'No': range(1, len(top_pa) + 1),
                    'Nama Pelanggan': top_pa['Customer_Internal'],
                    'Sales': top_pa.get('namaSales', '-'),
                    'SBU': top_pa.get('SBUNODE', '-'),
                    'Jumlah PA': top_pa['IDPA_Internal'],
                    'Revenue': top_pa['Revenue_Internal'].apply(lambda x: f"Rp {x:,.0f}".replace(",", ".")),
                })
                st.dataframe(display_df, use_container_width=True, hide_index=True, height=320)
            else:
                st.info("Tidak ada data PA pelanggan.")
        else:
            st.info("Tidak ada data pelanggan.")


st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)




st.markdown('<div class="section-title">🛍️ Layanan Produk</div>', unsafe_allow_html=True)

tab_prod_sum, tab_prod_det = st.tabs(["📊 Ringkasan Produk", "🏢 Detail Pembeli per Produk"])

with tab_prod_sum:
    if not df.empty:
        stats = df.groupby('Produk_Internal').agg(
            transactions=('IDPA_Internal', 'nunique'),
            customers=('Customer_Internal', 'nunique')
        ).reset_index()
        top_buyers = df.groupby(['Produk_Internal', 'Customer_Internal'])['IDPA_Internal'].nunique().reset_index()
        top_buyers = top_buyers.sort_values(by=['Produk_Internal', 'IDPA_Internal'], ascending=[True, False]).drop_duplicates(subset=['Produk_Internal'], keep='first')
        merged = pd.merge(stats, top_buyers[['Produk_Internal', 'Customer_Internal']], on='Produk_Internal', how='left').sort_values(by='transactions', ascending=False)

        display_prod = pd.DataFrame({
            'No': range(1, len(merged) + 1),
            'Layanan Produk': merged['Produk_Internal'].values,
            'Total Transaksi (PA)': merged['transactions'].values,
            'Total PT Pembeli': merged['customers'].values,
            'Top Pelanggan': merged['Customer_Internal'].values,
        })
        st.dataframe(display_prod, use_container_width=True, hide_index=True, height=400)
    else:
        st.info("Data Kosong")

with tab_prod_det:
    if not df.empty:
        pt = df.groupby('Produk_Internal')['IDPA_Internal'].nunique().reset_index()
        pt.columns = ['Produk_Internal', 'Total_PA_Produk']
        df_det = df.groupby(['Produk_Internal', 'Customer_Internal'])['IDPA_Internal'].nunique().reset_index()
        df_det = pd.merge(df_det, pt, on='Produk_Internal').sort_values(by=['Total_PA_Produk', 'IDPA_Internal'], ascending=[False, False])

        display_det = pd.DataFrame({
            'No': range(1, len(df_det) + 1),
            'Layanan Produk': df_det['Produk_Internal'].values,
            'Nama Perusahaan (PT)': df_det['Customer_Internal'].values,
            'Jumlah Transaksi (PA)': df_det['IDPA_Internal'].values,
        })
        st.dataframe(display_det, use_container_width=True, hide_index=True, height=400)
    else:
        st.info("Data Kosong")


st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)




st.markdown('<div class="section-title">📋 DETAIL UPDATE PROGRESS</div>', unsafe_allow_html=True)

if not df.empty:
    agg_rules = {'Revenue_Internal': 'sum'}
    if 'namaSales' in df.columns:
        agg_rules['namaSales'] = 'first'
    if 'SBUNODE' in df.columns:
        agg_rules['SBUNODE'] = 'first'
    if 'STATUS SO' in df.columns:
        agg_rules['STATUS SO'] = 'first'
    if 'UPDATE_Internal' in df.columns:
        agg_rules['UPDATE_Internal'] = 'first'

    df_progress = df.groupby(['Customer_Internal', 'IDPA_Internal']).agg(agg_rules).reset_index()

    display_progress = pd.DataFrame({
        'No': range(1, len(df_progress) + 1),
        'Nama Pelanggan': df_progress['Customer_Internal'].values,
        'Sales': df_progress.get('namaSales', pd.Series(['-'] * len(df_progress))).values,
        'SBU': df_progress.get('SBUNODE', pd.Series(['-'] * len(df_progress))).values,
        'IDPA': df_progress['IDPA_Internal'].values,
        'Total Revenue': df_progress['Revenue_Internal'].apply(lambda x: f"Rp {x:,.0f}".replace(",", ".")).values,
        'Status SO': df_progress.get('STATUS SO', pd.Series(['-'] * len(df_progress))).values,
        'On Progress': df_progress.get('UPDATE_Internal', pd.Series(['-'] * len(df_progress))).values,
    })

    col_dl1, col_dl2, _ = st.columns([1, 1, 4])
    with col_dl1:
        csv_progress = display_progress.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv_progress, "progress_data.csv", "text/csv")

    st.dataframe(display_progress, use_container_width=True, hide_index=True, height=500)
else:
    st.info("Data Kosong")


st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)




st.markdown('<div class="section-title">⏳ Analisis Aging Proyek</div>', unsafe_allow_html=True)

if not df.empty and 'Aging_Hari' in df.columns:
    df_aging = df.copy()
    df_aging['tanggal_rilis'] = df_aging['Date_Internal'].dt.strftime('%Y-%m-%d').fillna('-') if 'Date_Internal' in df.columns else "-"
    df_aging['kategori'] = df_aging['Aging_Hari'].apply(kategori_aging)
    df_aging['durasi'] = df_aging['Aging_Hari'].apply(format_durasi)

    cols_needed = ['Customer_Internal', 'IDPA_Internal', 'tanggal_rilis', 'Status_Cek', 'Aging_Hari', 'durasi', 'kategori']
    existing_cols = [c for c in cols_needed if c in df_aging.columns]
    df_aging_display = df_aging[existing_cols].sort_values(by='Aging_Hari', ascending=False).reset_index(drop=True)

    display_aging = pd.DataFrame({
        'No': range(1, len(df_aging_display) + 1),
        'Nama Pelanggan': df_aging_display['Customer_Internal'].values,
        'IDPA': df_aging_display['IDPA_Internal'].values,
        'Tanggal Rilis': df_aging_display['tanggal_rilis'].values,
        'Status': df_aging_display['Status_Cek'].values,
        'Total Hari': df_aging_display['Aging_Hari'].values,
        'Durasi': df_aging_display['durasi'].values,
        'Kategori Aging': df_aging_display['kategori'].values,
    })

    aging_summary = df_aging_display['kategori'].value_counts()
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    aging_cats = [("0-14 Hari", col_a1), ("15-30 Hari", col_a2),
                  ("31-365 Hari", col_a3), ("> 365 Hari", col_a4)]

    for cat_name, col_widget in aging_cats:
        with col_widget:
            count_val = int(aging_summary.get(cat_name, 0))
            st.markdown(f"""
            <div class="status-card" style="min-height: 80px;">
                <div class="status-label"><span class="status-badge">{cat_name}</span></div>
                <div class="status-value" style="font-size: 1.5rem; margin-top: 0.25rem;">{count_val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

    col_dl3, col_dl4, _ = st.columns([1, 1, 4])
    with col_dl3:
        csv_aging = display_aging.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv_aging, "aging_data.csv", "text/csv", key="dl_aging")

    st.dataframe(display_aging, use_container_width=True, hide_index=True, height=500)
else:
    st.info("Data Kosong")




st.markdown("<div style='height: 3rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 2rem 0; border-top: 1px solid #1e2229;">
    <p style="color: #6b7280; font-size: 0.75rem; margin: 0;">
        Dashboard Manufaktur v3.0 • Streamlit Edition • Data synced from Google Sheets
    </p>
</div>
""", unsafe_allow_html=True)
