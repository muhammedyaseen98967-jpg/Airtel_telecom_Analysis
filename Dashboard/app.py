import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================================
# DOMAIN C | NETWORK USAGE DASHBOARD
# SQL sources: usage_daily, v_usage_month, customer_features
# Change DB_PATH to your SQLite database file.
# ==========================================================

# app.py is expected inside the Dashboard folder.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / "data" / "raw" / "airtel.db"

st.set_page_config(page_title="Domain C — Network Usage | Telecom Analytics", page_icon="▥", layout="wide", initial_sidebar_state="expanded")


def ensure_usage_month_view():
    """Create the monthly usage view from usage_daily when it is missing."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE VIEW IF NOT EXISTS v_usage_month AS
            SELECT
                customer_id,
                strftime('%Y-%m', usage_date) AS month,
                SUM(data_mb) AS total_mb,
                COUNT(DISTINCT usage_date) AS usage_days
            FROM usage_daily
            GROUP BY customer_id, strftime('%Y-%m', usage_date)
        """)
        conn.commit()


def q(sql, params=None):
    """Execute SQL and return a DataFrame. Metrics are calculated in SQL."""
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(sql, conn, params=params or [])


ensure_usage_month_view()


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root {
  --bg:#090705; --surface:#17100C; --panel:#21160F; --panel-hi:#2B1B11;
  --text:#FFF6EC; --muted:#C3AD98; --line:#4B3323;
  --orange:#E87932; --amber:#F2A64D; --gold:#F3C77E; --green:#7ED6A2;
  --airtel-red:#E52B32; --airtel-coral:#F15A38;
}
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp {
  background:
    radial-gradient(ellipse at 78% 0%,rgba(207,111,48,.20),transparent 34%),
    radial-gradient(ellipse at 8% 100%,rgba(126,62,29,.15),transparent 34%),
    #090705;
  color:var(--text);
}
[data-testid="stHeader"] { background:rgba(9,7,5,.82); }
[data-testid="stToolbar"] { right:1rem; }
[data-testid="stMain"] {
  background:linear-gradient(145deg,#21170F 0%,#17100B 52%,#20140D 100%);
  border:1px solid #3D291B; border-radius:0 22px 22px 0;
  margin:14px 14px 14px 0; min-height:calc(100vh - 28px);
  box-shadow:0 20px 60px rgba(0,0,0,.32);
}
.block-container { max-width:1780px; padding:1.45rem 1.65rem 1.2rem; }
[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#0D0907 0%,#17100B 56%,#0B0806 100%);
  border-right:1px solid #422D1E; min-width:258px !important;
}
[data-testid="stSidebar"] > div:first-child { padding:1.35rem 1rem; }
[data-testid="stSidebar"] * { color:#FFF4E8 !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 {
  color:#FFF8F0 !important; font-family:'Space Grotesk',sans-serif;
}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
  color:#D8C3AE !important; font-weight:650; font-size:12px;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background:linear-gradient(145deg,#2B1C12,#1E140E) !important;
  border:1px solid #684326 !important; border-radius:11px !important; min-height:44px;
  transition:all .18s ease;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:hover,
[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
  border-color:#F0A04B !important; box-shadow:0 0 0 2px rgba(232,121,50,.20),0 4px 16px rgba(232,121,50,.12);
}
[data-testid="stSidebar"] [data-baseweb="select"] *,
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] input {
  color:#FFF4E8 !important; -webkit-text-fill-color:#FFF4E8 !important;
}
[data-baseweb="popover"] [role="option"] { color:#2B1B11 !important; }
.brand-box { display:flex; align-items:center; gap:12px; padding:7px 4px 21px; }
.brand-mark {
  width:46px; height:46px; display:flex; align-items:center; justify-content:center;
  border-radius:15px; overflow:hidden;
  background:linear-gradient(145deg,#FFF0D8 0%,#F4A34C 20%,#E52B32 68%,#A7192B 100%);
  border:1px solid rgba(255,220,165,.48);
  box-shadow:0 8px 24px rgba(229,43,50,.25),inset 0 1px 0 rgba(255,255,255,.38);
}
.brand-mark svg { width:30px; height:30px; display:block; }
.brand-name { color:#FFF8F0 !important; font-family:'Space Grotesk',sans-serif; font-size:16px; line-height:1.08; font-weight:700; }
.brand-sub { color:#D6A77D !important; font-size:8px; letter-spacing:1.45px; font-weight:800; margin-top:5px; }
.hero-panel {
  position:relative; overflow:hidden; padding:20px 23px 18px; margin:0 0 16px;
  border-radius:19px; border:1px solid rgba(228,145,75,.26);
  background:
    radial-gradient(ellipse at 92% 5%,rgba(226,129,57,.24),transparent 38%),
    linear-gradient(125deg,rgba(64,39,24,.92),rgba(31,20,14,.96) 52%,rgba(48,28,17,.92));
  box-shadow:0 14px 36px rgba(0,0,0,.22),inset 0 1px 0 rgba(255,255,255,.06);
}
.hero-panel:after {
  content:""; position:absolute; width:260px; height:260px; right:-95px; top:-160px;
  border-radius:50%; border:1px solid rgba(255,190,119,.12);
  box-shadow:0 0 0 22px rgba(255,190,119,.025),0 0 0 48px rgba(255,190,119,.018);
  pointer-events:none;
}
.side-nav { display:flex; flex-direction:column; gap:7px; margin:2px 0 18px; }
.side-nav-item {
  padding:11px 13px; border-radius:11px; color:#D8C4B0;
  font-size:13px; font-weight:600; transition:all .18s ease;
}
.side-nav-item:hover {
  background:rgba(225,126,54,.13); color:#FFF8EF;
  transform:translateX(2px);
}
.side-nav-item.active {
  color:#FFF8EF; background:linear-gradient(100deg,rgba(221,113,47,.40),rgba(117,57,27,.18));
  border:1px solid rgba(242,166,77,.28); box-shadow:inset 3px 0 #F0A04B,0 5px 18px rgba(0,0,0,.14);
}
.side-divider { height:1px; background:#493021; margin:14px 0 19px; }
.dashboard-meta {
  display:flex; align-items:center; gap:10px; margin:0 0 9px;
  color:#D4A77D; font-size:10px; letter-spacing:1.7px; font-weight:800;
}
.domain-chip {
  display:inline-flex; align-items:center; padding:5px 9px; border-radius:20px;
  color:#F7C98B; background:rgba(218,121,53,.12); border:1px solid rgba(231,145,72,.30);
  font-size:9px; letter-spacing:1.1px; font-weight:800;
}
.dashboard-heading { margin:0 0 4px; padding:0; border:0; }
.dashboard-heading h1 {
  margin:0; color:#FFF7EF; font-family:'Space Grotesk',sans-serif;
  font-size:clamp(34px,3.2vw,46px); line-height:1.05; font-weight:700; letter-spacing:-1.5px;
  text-shadow:0 3px 25px rgba(232,121,50,.10);
}
.dashboard-subtitle { color:#E6B98F; font-size:14px; font-weight:500; margin-top:9px; }
.reader-line { color:#BCA58E; font-size:12px; margin:8px 0 17px; }
div[data-testid="stTabs"] { margin:0 0 16px; border-bottom:1px solid #493225; }
div[data-testid="stTabs"] button {
  font-family:'DM Sans',sans-serif; font-size:13px; font-weight:700;
  color:#BDAA99; padding:10px 17px; transition:all .18s ease;
}
div[data-testid="stTabs"] button:hover { color:#FFD09A; }
div[data-testid="stTabs"] button[aria-selected="true"] {
  color:#FFD09A; border-bottom:2px solid transparent;
  border-image:linear-gradient(90deg,#D66E2F,#F3C77E) 1;
}
h2,h3 { color:#FFF4E9 !important; font-family:'Space Grotesk',sans-serif; font-weight:700; }
.metric-card {
  position:relative; overflow:hidden;
  background:linear-gradient(145deg,#382317 0%,#28190F 56%,#1D130D 100%);
  border:1px solid #604027; border-radius:17px; padding:18px 19px;
  min-height:116px; box-shadow:0 11px 30px rgba(0,0,0,.27);
  transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease;
}
.metric-card:hover {
  transform:translateY(-3px); border-color:#D88B4C;
  box-shadow:0 14px 34px rgba(0,0,0,.34),0 0 0 1px rgba(232,121,50,.10);
}
.metric-card:before {
  content:""; position:absolute; top:0; left:0; right:0; height:3px;
  background:linear-gradient(90deg,#A94C24,#E87932,#F3C77E);
}
.metric-label { color:#D9BEA5; font-size:11px; font-weight:700; letter-spacing:.2px; }
.metric-value {
  background:linear-gradient(100deg,#FFF1DB 0%,#F4BC76 55%,#E98743 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
  font-family:'Space Grotesk',sans-serif; font-size:29px; font-weight:700;
  margin-top:9px; line-height:1.1;
}
.metric-note { color:#B99E87; font-size:10px; margin-top:7px; }
div[data-testid="stPlotlyChart"] {
  background:linear-gradient(145deg,#302015 0%,#21160F 58%,#1A110C 100%);
  border:1px solid #684326; border-radius:17px; padding:8px 10px;
  box-shadow:0 10px 28px rgba(0,0,0,.22);
  transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease;
}
div[data-testid="stPlotlyChart"]:hover {
  border-color:#E89A50; transform:translateY(-2px);
  box-shadow:0 14px 34px rgba(0,0,0,.32),0 0 0 1px rgba(232,121,50,.08);
}
[data-testid="stDataFrame"],[data-testid="stTable"] {
  background:linear-gradient(145deg,#2A1B12,#1A120D);
  border:1px solid #65432B; border-radius:15px; overflow:hidden;
  box-shadow:0 9px 24px rgba(0,0,0,.20); padding:5px;
}
[data-testid="stDataFrame"] * { color:#F5EBDD; }
[data-testid="stDataFrame"]:hover,[data-testid="stTable"]:hover {
  border-color:#D98B4B; box-shadow:0 12px 28px rgba(0,0,0,.28),0 0 0 1px rgba(232,121,50,.10);
}
[data-testid="stExpander"] { border:1px solid #503521; border-radius:13px; background:#21160F; }
[data-testid="stExpander"] summary { color:#F2E5D7; }
.stCaption,small { color:#B7A28E !important; }
hr { border-color:#493225; }
[data-testid="stAlert"] { background:#2B1D13; color:#F5EBDD; border:1px solid #684326; }
.stButton > button {
  border-radius:11px; border:1px solid #8A542F; color:#FFF1E0;
  background:linear-gradient(110deg,#8E451F,#C56A2F 58%,#D98C43);
  font-weight:700; transition:all .18s ease;
}
.stButton > button:hover {
  border-color:#F0B66E; color:#FFFFFF; filter:brightness(1.12);
  box-shadow:0 5px 18px rgba(207,111,48,.22); transform:translateY(-1px);
}
@media (max-width: 900px) {
  .block-container { padding:1rem .8rem; }
  [data-testid="stMain"] { margin:0; border-radius:0; }
  .dashboard-heading h1 { font-size:31px; letter-spacing:-.8px; }
}


\n</style>
""", unsafe_allow_html=True)


def metric_card(label, value, note=""):
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)



def blend_hex(c1, c2, t):
    x = [int(c1[i:i+2], 16) for i in (1, 3, 5)]
    y = [int(c2[i:i+2], 16) for i in (1, 3, 5)]
    z = [round(a + (b-a)*t) for a, b in zip(x, y)]
    return "#{:02X}{:02X}{:02X}".format(*z)


def bar_gradient(n, offset=0):
    stops = ["#87421F", "#B95C2A", "#E87932", "#F0A34D", "#F5CD86"]
    if n < 2:
        return [stops[2]] * n
    result = []
    for i in range(n):
        p = i / (n-1) * (len(stops)-1)
        j = min(int(p), len(stops)-2)
        result.append(blend_hex(stops[j], stops[j+1], p-j))
    return result[offset:] + result[:offset]


def style_chart(fig, height=300):
    palette = ["#E87932", "#F3C77E", "#C9682E", "#D99555", "#A85A2B", "#F0B66F"]
    fig.update_layout(
        height=height, margin=dict(l=14, r=14, t=48, b=16),
        paper_bgcolor="#21160F", plot_bgcolor="#21160F", colorway=palette,
        font=dict(family="DM Sans", color="#F0E3D5", size=12),
        title=dict(font=dict(size=15, color="#FFF2E4", family="Space Grotesk"), x=.02, xanchor="left"),
        legend=dict(orientation="h", y=-.2, font=dict(color="#D3BEA9")),
        hoverlabel=dict(bgcolor="#382317", bordercolor="#E58A3A", font=dict(color="#FFF4E8", family="DM Sans", size=12)),
        hovermode="x unified",
        xaxis=dict(showgrid=False, linecolor="#63442D", tickfont=dict(color="#CBB69F"), zeroline=False),
        yaxis=dict(gridcolor="#3D2B1E", zeroline=False, tickfont=dict(color="#CBB69F")),
    )
    for i, trace in enumerate(fig.data):
        color = palette[i % len(palette)]
        if trace.type == "bar":
            n = len(trace.y) if trace.y is not None else 0
            trace.marker.color = bar_gradient(n, i)
            trace.marker.line.color = "rgba(255,218,166,0.45)"
            trace.marker.line.width = .5
            trace.marker.opacity = .97
        elif trace.type == "pie":
            n = len(trace.labels) if trace.labels is not None else 5
            trace.marker.colors = bar_gradient(n)
            trace.marker.line.color = "#21160F"
            trace.marker.line.width = 1.5
        elif trace.type in ("scatter", "scattergl"):
            if trace.mode and "lines" in trace.mode:
                trace.line.color = color
                trace.line.width = 2.8
            if trace.mode and "markers" in trace.mode:
                trace.marker.color = color
                trace.marker.line.color = "#F3C77E"
                trace.marker.line.width = .6
    fig.update_layout(coloraxis_showscale=False)
    return fig


# ------------------------- Sidebar filters -------------------------
st.sidebar.markdown("""
<div class="brand-box">
  <div class="brand-mark">
    <svg viewBox="0 0 40 40" aria-label="Airtel mark">
      <path d="M8 27.5c4.2-1.1 7.6-3.7 10.2-7.8 2.1-3.3 3.9-6.9 7.4-8.7 2.6-1.3 5.2-.7 6.7 1.2-3.8-.2-5.8 2.4-7.7 5.8-2.2 4-4.7 8.1-9.2 10.5-2.6 1.4-5.2 1.5-7.4-1z" fill="#fff8ef"/>
      <path d="M9.2 15.2c2.7-3.1 6.1-4.7 10.1-4.6-2.8 1.4-4.5 3.5-6 6.2-1.4 2.5-2.8 4.8-5.4 6.4-.8-2.7-.3-5.5 1.3-8z" fill="#fff8ef" opacity=".92"/>
      <path d="M18.2 29.5c3.7-1.2 6.4-3.8 8.4-7.3 1.4-2.4 2.8-4.8 5.4-6.2-.1 4.8-2.3 9.1-6.3 12-2.4 1.7-5 2.3-7.5 1.5z" fill="#fff8ef" opacity=".78"/>
    </svg>
  </div>
  <div>
    <div class="brand-name">airtel</div>
    <div class="brand-name">Telecom Analytics</div>
    <div class="brand-sub">NETWORK INTELLIGENCE</div>
  </div>
</div>
<div class="side-nav">
  <div class="side-nav-item active">◉ &nbsp; Dashboard</div>
  <div class="side-nav-item">▣ &nbsp; Overview</div>
  <div class="side-nav-item">▤ &nbsp; Month Detail</div>
</div>
<div class="side-divider"></div>
""", unsafe_allow_html=True)
st.sidebar.title("Filters")

# Populate filters from actual database values to avoid mismatched labels.
connection_values = q("""
    SELECT DISTINCT connection_type FROM customer_features
    WHERE connection_type IS NOT NULL ORDER BY connection_type
""")["connection_type"].astype(str).tolist()
experiment_values = q("""
    SELECT DISTINCT ab_group FROM customer_features
    WHERE ab_group IS NOT NULL ORDER BY ab_group
""")["ab_group"].astype(str).tolist()

connection_filter = st.sidebar.selectbox(
    "Connection Type", ["All"] + connection_values, index=0, key="connection_filter"
)
experiment_filter = st.sidebar.selectbox(
    "Experiment Group", ["All"] + experiment_values, index=0, key="experiment_filter"
)
if st.sidebar.button("Reset filters", width="stretch"):
    st.session_state["connection_filter"] = "All"
    st.session_state["experiment_filter"] = "All"
    st.rerun()

filter_conditions = []
filter_params = []
if connection_filter != "All":
    filter_conditions.append("c.connection_type = ?")
    filter_params.append(connection_filter)
if experiment_filter != "All":
    filter_conditions.append("c.ab_group = ?")
    filter_params.append(experiment_filter)
filter_sql = " AND ".join(filter_conditions) if filter_conditions else "1=1"

# ------------------------- SQL data queries -------------------------
monthly_usage = q(f"""
    SELECT m.month,
           COUNT(DISTINCT m.customer_id) AS active_subs,
           ROUND(SUM(m.total_mb) / 1024.0 / 1024.0, 2) AS total_tb
    FROM v_usage_month m
    JOIN customer_features c ON c.customer_id = m.customer_id
    WHERE {filter_sql}
    GROUP BY m.month ORDER BY m.month
""", filter_params)

monthly_per_sub = q(f"""
    SELECT m.month,
           ROUND(AVG(m.total_mb) / 1024.0, 2) AS avg_gb_per_sub,
           ROUND(AVG(m.usage_days), 1) AS avg_days
    FROM v_usage_month m
    JOIN customer_features c ON c.customer_id = m.customer_id
    WHERE {filter_sql}
    GROUP BY m.month ORDER BY m.month
""", filter_params)

monthly_device = q(f"""
    SELECT c.device_type,
           ROUND(SUM(m.total_mb) / 1024.0 / 1024.0, 2) AS total_tb
    FROM v_usage_month m
    JOIN customer_features c ON c.customer_id = m.customer_id
    WHERE {filter_sql}
    GROUP BY c.device_type ORDER BY total_tb DESC
""", filter_params)

plan_usage = q(f"""
    SELECT plan_name, monthly_gb,
           ROUND(AVG(total_data_mb) / 1024.0 / 6.0, 2) AS actual_gb_per_month
    FROM customer_features c
    WHERE usage_days > 0 AND {filter_sql}
    GROUP BY plan_name, monthly_gb ORDER BY monthly_gb
""", filter_params)
quartiles = q(f"""
    WITH n AS (
        SELECT mb_per_active_day AS mb,
               NTILE(4) OVER (ORDER BY mb_per_active_day) AS q
        FROM customer_features c
        WHERE usage_days > 0 AND {filter_sql}
    )
    SELECT q, COUNT(*) AS subs, ROUND(MIN(mb), 0) AS min_mb, ROUND(MAX(mb), 0) AS max_mb
    FROM n GROUP BY q ORDER BY q
""", filter_params)

# N3: monthly data usage by A/B experiment group.
ab_month_table = q(f"""
    SELECT
        strftime('%Y-%m', u.usage_date) AS month,
        c.ab_group AS experiment_group,
        COUNT(*) AS usage_records,
        ROUND(AVG(u.data_mb), 2) AS avg_mb_per_usage_day
    FROM usage_daily u
    JOIN customer_features c ON c.customer_id = u.customer_id
    WHERE {filter_sql}
    GROUP BY month, c.ab_group
    ORDER BY month, c.ab_group
""", filter_params)

# ------------------------- Page heading -------------------------
st.markdown("""
<div class="hero-panel">
  <div class="dashboard-meta">
    <span class="domain-chip">DOMAIN C</span>
    <span>NETWORK USAGE</span>
    <span style="margin-left:auto;color:#D9B28D;letter-spacing:.5px;">JAN 2025 — JUN 2025</span>
  </div>
  <div class="dashboard-heading">
    <h1>Airtel Telecom Analytics</h1>
  </div>
</div>
""", unsafe_allow_html=True)
overview_tab, detail_tab = st.tabs(["Overview", "Month Detail"])


# ========================= OVERVIEW TAB =========================
with overview_tab:
    st.subheader("Network Overview")
    latest_active = int(monthly_usage.active_subs.iloc[-1]) if not monthly_usage.empty else 0
    k1, k2, k3 = st.columns(3)
    with k1:
        metric_card("Base Scale", "22,000", "Fixed dataset subscriber scale")
    with k2:
        metric_card("Additional Daily Data Used by Group B (N4)", "+473.38 MB", "Compared with Group A during the offer period")
    with k3:
        metric_card("Latest Active Subscribers", f"{latest_active:,}", "Responds to filters")

    st.markdown("---")
    left, right = st.columns([2, 1])
    with left:
        if not monthly_usage.empty:
            fig = px.area(monthly_usage, x="month", y="total_tb", markers=True,
                          title="Monthly Network Traffic Remains Within a Stable Range",
                          labels={"month": "Month", "total_tb": "Total Data Carried (TB)"})
            fig.update_traces(line=dict(width=3, color="#E58A3A"), fill="tozeroy")
            fig.add_hline(y=monthly_usage.total_tb.mean(), line_dash="dash",
                          annotation_text="Period average", annotation_position="top left", annotation_font_color="#F0B66E")
            st.plotly_chart(style_chart(fig, 410), width="stretch")
    with right:
        if not monthly_usage.empty:
            fig = px.bar(monthly_usage, x="month", y="active_subs",
                         title="Monthly Active Network Users",
                         labels={"month": "Month", "active_subs": "Active Subscribers"})
            st.plotly_chart(style_chart(fig, 410), width="stretch")

    b1, b2, b3 = st.columns(3)
    with b1:
        if not ab_month_table.empty:
            fig = px.line(ab_month_table, x="month", y="avg_mb_per_usage_day",
                          color="experiment_group", markers=True,
                          title="Monthly Data Usage — Group A vs Group B",
                          labels={"month": "Month", "avg_mb_per_usage_day": "Average MB per Usage Day",
                                  "experiment_group": "Experiment Group"})
            fig.add_vrect(x0="2025-05", x1="2025-06", fillcolor="rgba(229,138,58,0.13)",
                          line_width=0, annotation_text="Offer period", annotation_position="top left")
            st.plotly_chart(style_chart(fig, 280), width="stretch")
    with b2:
        if not monthly_device.empty:
            fig = px.pie(monthly_device, names="device_type", values="total_tb", hole=.55,
                      title="Network Traffic by Device Type")
            fig.update_traces(textposition="inside", textinfo="label+percent")
            st.plotly_chart(style_chart(fig, 280), width="stretch")
    with b3:
        if not plan_usage.empty:
            fig = px.bar(plan_usage, x="plan_name", y="actual_gb_per_month",
                          title="Actual Data Usage by Plan",
                          labels={"plan_name": "Plan", "actual_gb_per_month": "Actual GB per Month"})
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(style_chart(fig, 280), width="stretch")
    st.caption("Fixed cards: Base Scale and documented N4 offer-period finding. Charts and the group table respond to both filters.")

    st.markdown("#### Experiment Group — Monthly Usage Summary")
    st.caption("SQL result from N3 · average data per usage-day record (MB).")
    if not ab_month_table.empty:
        st.dataframe(
            ab_month_table,
            hide_index=True,
            width="stretch",
            height=245,
            column_config={
                "month": st.column_config.TextColumn("Month"),
                "experiment_group": st.column_config.TextColumn("Experiment Group"),
                "usage_records": st.column_config.NumberColumn("Usage Records", format="%d"),
                "avg_mb_per_usage_day": st.column_config.NumberColumn("Average MB / Usage Day", format="%.2f MB"),
            },
        )
    else:
        st.info("No experiment-group usage records match the selected filters.")



# ========================= MONTH DETAIL TAB =========================
with detail_tab:
    st.subheader("Monthly Network Usage Detail")
    months = monthly_usage.month.astype(str).tolist() if not monthly_usage.empty else []

    if months:
        selected_month = st.selectbox(
            "Select Month",
            options=months,
            index=len(months) - 1,
            format_func=lambda month: pd.to_datetime(f"{month}-01").strftime("%B %Y"),
            key="detail_month_selector",
        )
    else:
        selected_month = None

    if selected_month:
        month_daily = q(f"""
            SELECT u.usage_date,
                   COUNT(DISTINCT u.customer_id) AS daily_users,
                   ROUND(SUM(u.data_mb) / 1024.0, 2) AS total_gb,
                   ROUND(AVG(u.data_mb), 2) AS avg_mb
            FROM usage_daily u
            JOIN customer_features c ON c.customer_id = u.customer_id
            WHERE strftime('%Y-%m', u.usage_date) = ? AND {filter_sql}
            GROUP BY u.usage_date ORDER BY u.usage_date
        """, [selected_month] + filter_params)
        month_device = q(f"""
            SELECT c.device_type, ROUND(SUM(u.data_mb) / 1024.0, 2) AS total_gb
            FROM usage_daily u
            JOIN customer_features c ON c.customer_id = u.customer_id
            WHERE strftime('%Y-%m', u.usage_date) = ? AND {filter_sql}
            GROUP BY c.device_type ORDER BY total_gb DESC
        """, [selected_month] + filter_params)
        month_weekday = q(f"""
            SELECT strftime('%w', u.usage_date) AS dow, COUNT(*) AS rows_,
                   ROUND(AVG(u.data_mb), 1) AS avg_mb
            FROM usage_daily u
            JOIN customer_features c ON c.customer_id = u.customer_id
            WHERE strftime('%Y-%m', u.usage_date) = ? AND {filter_sql}
            GROUP BY dow ORDER BY dow
        """, [selected_month] + filter_params)
        month_quartiles = q(f"""
            WITH n AS (
                SELECT mb_per_active_day AS mb,
                       NTILE(4) OVER (ORDER BY mb_per_active_day) AS q
                FROM customer_features c
                WHERE usage_days > 0 AND {filter_sql}
            )
            SELECT q, COUNT(*) AS subs, ROUND(MIN(mb), 0) AS min_mb, ROUND(MAX(mb), 0) AS max_mb
            FROM n GROUP BY q ORDER BY q
        """, filter_params)
        month_summary = q(f"""
            SELECT COUNT(DISTINCT u.customer_id) AS active_users,
                   ROUND(SUM(u.data_mb) / 1024.0, 2) AS total_gb,
                   ROUND(AVG(u.data_mb), 2) AS avg_mb
            FROM usage_daily u
            JOIN customer_features c ON c.customer_id = u.customer_id
            WHERE strftime('%Y-%m', u.usage_date) = ? AND {filter_sql}
        """, [selected_month] + filter_params)

        selected_month_label = pd.to_datetime(f"{selected_month}-01").strftime("%B %Y")
        active_users = int(month_summary.active_users.iloc[0]) if not month_summary.empty else 0
        total_gb = float(month_summary.total_gb.iloc[0]) if not month_summary.empty else 0
        avg_mb = float(month_summary.avg_mb.iloc[0]) if not month_summary.empty else 0
        c1, c2, c3, c4 = st.columns(4)
        with c1: metric_card("Active Subscribers", f"{active_users:,}", selected_month_label)
        with c2: metric_card("Total Data Carried", f"{total_gb:,.0f} GB", selected_month_label)
        with c3: metric_card("Average Daily Record Usage", f"{avg_mb:,.0f} MB", "Daily-row average")
        with c4:
            st.markdown("<div style='color:#BFB3C3;font-size:12px;font-weight:650'>Selected Month</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:#F0C5E6;font-size:25px;font-weight:750;margin-top:9px'>{selected_month_label}</div>", unsafe_allow_html=True)
        st.markdown("---")

        hero, side = st.columns([2, 1])
        with hero:
            if not month_daily.empty:
                fig = px.area(month_daily, x="usage_date", y="total_gb", title="Daily Network Data Carried",
                              labels={"usage_date": "Date", "total_gb": "Data Carried (GB)"})
                fig.update_traces(line=dict(width=3, color="#E58A3A"), fill="tozeroy")
                fig.add_hline(y=month_daily.total_gb.mean(), line_dash="dash",
                              annotation_text="Daily average", annotation_position="top left", annotation_font_color="#F0B66E")
                st.plotly_chart(style_chart(fig, 390), width="stretch")
        with side:
            if not month_daily.empty:
                fig = px.bar(month_daily, x="usage_date", y="daily_users", title="Daily Network Users",
                             labels={"usage_date": "Date", "daily_users": "Subscribers"})
                fig.update_layout(coloraxis_showscale=False)
                st.plotly_chart(style_chart(fig, 390), width="stretch")

        d1, d2, d3 = st.columns(3)
        with d1:
            if not month_device.empty:
                fig = px.pie(month_device, names="device_type", values="total_gb", hole=.55,
                             title="Data Usage by Device Type")
                st.plotly_chart(style_chart(fig, 280), width="stretch")
        with d2:
            if not month_weekday.empty:
                weekday_names = {"0": "Sun", "1": "Mon", "2": "Tue", "3": "Wed", "4": "Thu", "5": "Fri", "6": "Sat"}
                month_weekday["weekday"] = month_weekday.dow.map(weekday_names)
                fig = px.bar(month_weekday, x="weekday", y="avg_mb", title="Average Data Usage by Weekday",
                             labels={"weekday": "Day", "avg_mb": "Average MB"})
                st.plotly_chart(style_chart(fig, 280), width="stretch")
        with d3:
            if not month_quartiles.empty:
                fig = px.bar(month_quartiles, x="q", y="subs", title="Subscribers by Data Usage Quartile",
                             labels={"q": "Usage Quartile", "subs": "Subscribers"}, text="subs")
                fig.update_traces(textposition="outside")
                st.plotly_chart(style_chart(fig, 280), width="stretch")

        st.markdown("#### Daily Network Usage — Data Table")
        st.caption("SQL results for the selected month and active filters.")
        if not month_daily.empty:
            daily_table = month_daily.copy()
            daily_table["usage_date"] = pd.to_datetime(daily_table["usage_date"]).dt.strftime("%d %b %Y")
            daily_table = daily_table.rename(columns={
                "usage_date": "Date", "daily_users": "Active Subscribers",
                "total_gb": "Data Carried (GB)", "avg_mb": "Average Usage (MB)"
            })
            st.dataframe(
                daily_table, hide_index=True, width="stretch", height=310,
                column_config={
                    "Date": st.column_config.TextColumn("Date"),
                    "Active Subscribers": st.column_config.NumberColumn("Active Subscribers", format="%d"),
                    "Data Carried (GB)": st.column_config.NumberColumn("Data Carried (GB)", format="%.2f GB"),
                    "Average Usage (MB)": st.column_config.NumberColumn("Average Usage (MB)", format="%.2f MB"),
                },
            )
        else:
            st.info("No daily usage records are available for this month.")

    else:
        st.info("No monthly usage data available for the selected filters.")


st.markdown("---")
st.caption("Data provenance: Circle and plan structures are real; subscriber-level records are synthetic. Dashboard metrics are computed in SQL.")
