# import streamlit as st
# import pandas as pd
# from datetime import datetime
# from utils import load_data, filter_dataframe
# import streamlit.components.v1 as components

# from charts import (
#     executive_chart,
#     monthly_chart,
#     status_chart,
#     leaderboard_chart
# )

# # --------------------------------------------------
# # PAGE CONFIG
# # --------------------------------------------------

# st.set_page_config(
#     page_title="Collection Executive Dashboard",
#     page_icon="🏆",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --------------------------------------------------
# # LOAD CSS
# # --------------------------------------------------

# try:
#     with open("style.css") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# except:
#     pass

# # --------------------------------------------------
# # GOOGLE SHEET CSV
# # --------------------------------------------------

# CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT771wZ8ZcNJOh6odbwJRFjefSWNr8tI-ali3ivMq-4qymISZnnSsG3LZDsMr-wDiPZ7_5eRrNhBQ24/pub?output=csv"

# df = load_data(CSV_URL)

# # --------------------------------------------------
# # SIDEBAR
# # --------------------------------------------------

# st.sidebar.title("📊 EazyPaisa Collection Dashboard")

# if st.sidebar.button("🔄 Refresh Dashboard"):
#     st.cache_data.clear()
#     st.rerun()

# from datetime import datetime

# months = ["All"] + sorted(
#     df["Repay Month"].dropna().unique().tolist()
# )

# # Current month ka naam (July 2026 -> July)
# current_month = datetime.now().strftime("%B")

# # Agar sheet me current month hai to wahi default select hoga
# default_index = 0

# if current_month in months:
#     default_index = months.index(current_month)

# selected_month = st.sidebar.selectbox(
#     "Repay Month",
#     months,
#     index=default_index
# )

# executives = ["All"] + sorted(
#     df["Executive Name"].dropna().unique().tolist()
# )

# selected_executive = st.sidebar.selectbox(
#     "Collection Executive",
#     executives
# )

# status_list = ["All"] + sorted(
#     df["Current Status"].dropna().unique().tolist()
# )

# selected_status = st.sidebar.selectbox(
#     "Current Status",
#     status_list
# )

# from_date = st.sidebar.date_input(
#     "From Date",
#     value=df["Repay Date"].min()
# )

# to_date = st.sidebar.date_input(
#     "To Date",
#     value=df["Repay Date"].max()
# )

# filtered = filter_dataframe(
#     df,
#     selected_month,
#     selected_executive,
#     selected_status,
#     from_date,
#     to_date
# )

# # --------------------------------------------------
# # KPI VALUES
# # --------------------------------------------------

# loan_amount = filtered["Loan Amount"].sum()

# repay_amount = filtered["Loan Repay Amount"].sum()

# received_amount = filtered["Total Received"].sum()

# pending_amount = repay_amount - received_amount

# collection_percentage = 0

# if repay_amount > 0:
#     collection_percentage = (
#         received_amount / repay_amount
#     ) * 100

# executive_count = filtered["Executive Name"].nunique()

# account_count = len(filtered)

# closed_accounts = len(
#     filtered[
#         filtered["Current Status"]
#         .str.upper()
#         .str.contains("CLOSE", na=False)
#     ]
# )

# # --------------------------------------------------
# # HEADER
# # --------------------------------------------------

# st.title("🏆 Collection Executive Performance Dashboard")

# # st.caption(
# #     "Live Dashboard | Collection Executive Performance Dashboard"
# # )

# # --------------------------------------------------
# # KPI CARDS - FIXED VERSION
# # --------------------------------------------------

# # Create KPI data
# kpis = [
#     ("💰 Loan Amount", f"₹{loan_amount:,.0f}"),
#     ("💳 Repay Amount", f"₹{repay_amount:,.0f}"),
#     ("💵 Received", f"₹{received_amount:,.0f}"),
#     ("📉 Pending", f"₹{pending_amount:,.0f}"),
#     ("📈 Collection %", f"{collection_percentage:.2f}%"),
#     ("👨‍💼 Executives", f"{executive_count}"),
#     ("📄 Accounts", f"{account_count}"),
#     ("✅ Closed Accounts", f"{closed_accounts}")
# ]

# # Create HTML for all KPI cards at once
# kpi_html = """
# <div class="kpi-container">
# """

# for title, value in kpis:
#     kpi_html += f"""
#     <div class="kpi-card-new">
#         <div class="kpi-icon">{title.split()[0]}</div>
#         <div class="kpi-title-new">{title.split(' ', 1)[1]}</div>
#         <div class="kpi-value-new">{value}</div>
#     </div>
#     """

# kpi_html += """
# </div>
# """

# # Display KPI cards using components.html
# components.html(
#     f"""
#     <html>
#     <head>
#     <style>
#     .kpi-container {{
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
#         gap: 16px;
#         width: 100%;
#         margin: 20px 0;
#     }}

#     .kpi-card-new {{
#         background: linear-gradient(135deg, 
#             rgba(34, 197, 94, 0.15) 0%,
#             rgba(15, 23, 42, 0.8) 100%);
        
#         backdrop-filter: blur(20px);
#         border-radius: 20px;
#         padding: 20px;
#         border: 1px solid rgba(74, 222, 128, 0.3);
#         box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        
#         transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
#         text-align: center;
#         min-height: 140px;
#         display: flex;
#         flex-direction: column;
#         justify-content: space-between;
#     }}

#     .kpi-card-new:hover {{
#         transform: translateY(-8px);
#         border-color: #22c55e;
#         box-shadow: 0 25px 60px rgba(34, 197, 94, 0.25);
#     }}

#     .kpi-icon {{
#         font-size: 28px;
#         margin-bottom: 8px;
#     }}

#     .kpi-title-new {{
#         color: #cbd5e1;
#         font-size: 13px;
#         font-weight: 600;
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#         margin-bottom: 10px;
#     }}

#     .kpi-value-new {{
#         color: #ffffff;
#         font-size: 24px;
#         font-weight: 900;
#         letter-spacing: -0.5px;
#     }}

#     @media (max-width: 1200px) {{
#         .kpi-container {{
#             grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
#         }}
        
#         .kpi-value-new {{
#             font-size: 20px;
#         }}
#     }}

#     @media (max-width: 768px) {{
#         .kpi-container {{
#             grid-template-columns: repeat(2, 1fr);
#         }}
        
#         .kpi-card-new {{
#             padding: 15px;
#         }}
#     }}
#     </style>
#     </head>
#     <body style="background: transparent; margin: 0; padding: 0;">
#     {kpi_html}
#     </body>
#     </html>
#     """,
#     height=200
# )

# st.divider()

# # 👇 Collection Progress Bar yahan add karo
# import streamlit.components.v1 as components



# components.html(
#     f"""
# <!DOCTYPE html>
# <html>

# <head>

# <style>

# body{{
#     margin:0;
#     background:transparent;
#     font-family:Arial,sans-serif;
# }}

# .collection-progress-card{{

#     padding:22px;

#     border-radius:20px;

#     background:linear-gradient(
#         135deg,
#         #111827,
#         #1f2937
#     );

#     border:1px solid rgba(255,215,0,.20);

# }}

# .progress-title{{

#     display:flex;

#     justify-content:space-between;

#     align-items:center;

#     color:white;

#     font-size:22px;

#     font-weight:bold;

#     margin-bottom:15px;

# }}

# .progress-track{{

#     width:100%;

#     height:18px;

#     background:#2B2113;

#     border-radius:50px;

#     overflow:hidden;

# }}

# .progress-fill{{

#     width:{min(collection_percentage,100):.2f}%;

#     height:100%;

#     border-radius:50px;

#     background:linear-gradient(
#         90deg,
#         #7A4A00,
#         #C58A00,
#         #FFD700,
#         #FFF5B7,
#         #FFD700,
#         #C58A00,
#         #7A4A00
#     );

#     background-size:300% 100%;

#     animation:goldFlow 3s linear infinite;

# }}

# @keyframes goldFlow{{

# 0%{{background-position:0%;}}

# 100%{{background-position:300%;}}

# }}

# .progress-info{{

#     margin-top:18px;

#     display:flex;

#     justify-content:space-between;

#     text-align:center;

# }}

# .progress-info small{{

#     color:#BBBBBB;

#     font-size:12px;

# }}

# .progress-info b{{

#     color:#FFD700;

#     font-size:18px;

# }}

# </style>

# </head>

# <body>

# <div class="collection-progress-card">

# <div class="progress-title">

# <span>📈 Collection Performance</span>

# <span>{collection_percentage:.2f}%</span>

# </div>
# <div class="progress-track">

#     <div class="progress-fill" style="width:{min(collection_percentage,100):.2f}%">

#         <div class="progress-tooltip">

#             <b>{collection_percentage:.2f}% Collection</b><br><br>

#             💰 Collected : ₹{received_amount / 10000000:.2f} Cr<br>

#             🎯 Target : ₹{received_amount / 10000000:.2f} Cr<br>

#             📉 Remaining : ₹{received_amount / 10000000:.2f} Cr

#         </div>

#     </div>

# </div>

# <div class="progress-info">

# <div>

# <small>Collected</small><br>

# <b>₹{received_amount / 10000000:.2f} Cr</b>

# </div>

# <div>

# <small>Remaining</small><br>

# <b>₹{received_amount / 10000000:.2f} Cr</b>

# </div>

# <div>

# <small>Target</small><br>

# <b>₹{received_amount / 10000000:.2f} Cr</b>

# </div>

# </div>

# </div>

# </body>

# </html>

# """,
#     height=170,
# )
# # # 👇 Iske baad ye code rahega
# # st.markdown("""
# # <div class="top-performer-header">
# #     🏆 Top Performers
# # </div>
# # """, unsafe_allow_html=True)

# # =====================================================
# # IMPROVED TOP 3 PERFORMANCE CARDS
# # =====================================================

# st.markdown("""
# <div class="top-performer-header">
#     🏆 Top Performers
# </div>
# """, unsafe_allow_html=True)

# leaders = (
#     filtered.groupby("Executive Name", as_index=False)
#     .agg({
#         "Loan Amount":"sum",
#         "Loan Repay Amount":"sum",
#         "Total Received":"sum"
#     })
# )

# leaders["Collection %"] = (
#     leaders["Total Received"] /
#     leaders["Loan Repay Amount"]
# ).fillna(0) * 100

# leaders = leaders.sort_values(
#     "Collection %",
#     ascending=False
# )

# top3 = leaders.head(3).reset_index(drop=True)

# if len(top3) >= 3:
#     left, second, first, third, right = st.columns([0.6, 1, 1, 1, 0.6])

#     # ================= SECOND PLACE (SILVER) =================
#     with second:
#         r = top3.iloc[1]
#         exec_name = r["Executive Name"]
#         received = r["Total Received"]
#         collection_pct = r["Collection %"]
#         repay_amt = r["Loan Repay Amount"]
        
#         st.markdown(
#             f"""
#             <div class="performance-card silver-card">
#                 <div class="medal-emoji">🥈</div>
#                 <div class="position-badge">2ND PLACE</div>
#                 <h3 class="exec-name">{exec_name}</h3>
#                 <div class="amount-box">₹{received:,.0f}</div>
#                 <div class="stats-row">
#                     <div class="stat-item">
#                         <div class="stat-label">Collection</div>
#                         <div class="stat-value">{collection_pct:.2f}%</div>
#                     </div>
#                     <div class="stat-divider"></div>
#                     <div class="stat-item">
#                         <div class="stat-label">Repay</div>
#                         <div class="stat-value">₹{repay_amt/100000:.1f}L</div>
#                     </div>
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#     # ================= FIRST PLACE (GOLD) =================
#     with first:
#         r = top3.iloc[0]
#         exec_name = r["Executive Name"]
#         received = r["Total Received"]
#         collection_pct = r["Collection %"]
#         repay_amt = r["Loan Repay Amount"]
#         loan_amt = r["Loan Amount"]
        
#         st.markdown(
#             f"""
#             <div class="performance-card gold-card">
#                 <div class="crown-emoji">👑</div>
#                 <div class="medal-emoji gold-medal">🥇</div>
#                 <div class="position-badge gold-badge">1ST PLACE</div>
#                 <h2 class="exec-name-gold">{exec_name}</h2>
#                 <div class="amount-box gold-amount">₹{received:,.0f}</div>
#                 <div class="stats-row gold-stats">
#                     <div class="stat-item">
#                         <div class="stat-label">Collection</div>
#                         <div class="stat-value">{collection_pct:.2f}%</div>
#                     </div>
#                     <div class="stat-divider"></div>
#                     <div class="stat-item">
#                         <div class="stat-label">Repay</div>
#                         <div class="stat-value">₹{repay_amt/100000:.1f}L</div>
#                     </div>
#                         <div class="stat-value gold-stat-val">{int(filtered[filtered['Executive Name']==exec_name].shape[0])}</div>
#                     </div>
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#     # ================= THIRD PLACE (BRONZE) =================
#     with third:
#         r = top3.iloc[2]

#         exec_name = r["Executive Name"]
#         received = r["Total Received"]
#         collection_pct = r["Collection %"]
#         repay_amt = r["Loan Repay Amount"]
        
#         st.markdown(
#             f"""
#             <div class="performance-card bronze-card">
#                 <div class="medal-emoji">🥉</div>
#                 <div class="position-badge">3RD PLACE</div>
#                 <h3 class="exec-name">{exec_name}</h3>
#                 <div class="amount-box">₹{received:,.0f}</div>
#                 <div class="stats-row">
#                     <div class="stat-item">
#                         <div class="stat-label">Collection</div>
#                         <div class="stat-value">{collection_pct:.2f}%</div>
#                     </div>
#                     <div class="stat-divider"></div>
#                     <div class="stat-item">
#                         <div class="stat-label">Repay</div>
#                         <div class="stat-value">₹{repay_amt/100000:.1f}L</div>
#                     </div>
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

# elif len(top3) > 0:
#     cols = st.columns(len(top3))
#     for idx, col in enumerate(cols):
#         with col:
#             r = top3.iloc[idx]
#             exec_name = r["Executive Name"]
#             received = r["Total Received"]
#             collection_pct = r["Collection %"]
            
#             st.markdown(
#                 f"""
#                 <div class="performance-card simple-card">
#                     <div class="simple-rank">#{idx+1}</div>
#                     <div class="exec-name-simple">{exec_name}</div>
#                     <div class="amount-simple">₹{received:,.0f}</div>
#                     <div class="percentage-simple">{collection_pct:.2f}%</div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

# st.markdown("<br>", unsafe_allow_html=True)

# # =====================================================
# # EXECUTIVE SUMMARY
# # =====================================================

# st.subheader("📋 Executive Summary")

# summary = (
#     filtered.groupby("Executive Name", as_index=False)
#     .agg({
#         "Loan Amount": "sum",
#         "Loan Repay Amount": "sum",
#         "Total Received": "sum",
#         "Pending Amount": "sum"
#     })
# )

# summary["Collection %"] = (
#     summary["Total Received"] /
#     summary["Loan Repay Amount"]
# ).fillna(0) * 100

# summary["Accounts"] = (
#     filtered.groupby("Executive Name")
#     .size()
#     .values
# )

# summary = summary.sort_values(
#     "Collection %",
#     ascending=False
# )

# summary.insert(
#     0,
#     "Rank",
#     range(1, len(summary) + 1)
# )

# summary = summary.reset_index(drop=True)

# table_html = """
# <div class="leaderboard-table">
# <table>

# <thead>
# <tr>
# <th>Rank</th>
# <th>Executive Name</th>
# <th>Loan Amount</th>
# <th>Repay Amount</th>
# <th>Total Received</th>
# <th>Pending Amount</th>
# <th>Collection %</th>
# <th>Accounts</th>
# </tr>
# </thead>

# <tbody>
# """

# for _, row in summary.iterrows():

#     medal = ""

#     if row["Rank"] == 1:
#         medal = "🥇"

#     elif row["Rank"] == 2:
#         medal = "🥈"

#     elif row["Rank"] == 3:
#         medal = "🥉"

#     pct = row["Collection %"]

#     if pct >= 95:
#         color = "#00ff88"

#     elif pct >= 85:
#         color = "#ffd54f"

#     else:
#         color = "#ff5252"

#     table_html += f"""
#     <tr>

#         <td class="rank">
#             {medal} {row['Rank']}
#         </td>

#         <td class="name">
#             {row['Executive Name']}
#         </td>

#         <td>
#             ₹{row['Loan Amount']:,.0f}
#         </td>

#         <td>
#             ₹{row['Loan Repay Amount']:,.0f}
#         </td>

#         <td>
#             ₹{row['Total Received']:,.0f}
#         </td>

#         <td>
#             ₹{row['Pending Amount']:,.0f}
#         </td>

#         <td style="color:{color};font-weight:900;">
#             {pct:.2f}%
#         </td>

#         <td>
#             {row['Accounts']}
#         </td>

#     </tr>
#     """

# table_html += """
# </tbody>
# </table>
# </div>
# """

# with open("style.css", "r", encoding="utf-8") as f:
#     css = f.read()

# components.html(
#     f"""
# <!DOCTYPE html>
# <html>

# <head>

# <style>

# {css}

# body{{
#     margin:0;
#     padding:10px;
#     background:#052e1b;
# }}

# </style>

# </head>

# <body>

# {table_html}

# </body>

# </html>

# """,
# height=650,
# scrolling=True
# )
# st.divider()

# # =====================================================
# # DOWNLOAD REPORTS
# # =====================================================

# st.subheader("📥 Export Reports")

# download_col1, download_col2 = st.columns(2)

# with download_col1:

#     csv = summary.to_csv(index=False).encode("utf-8")

#     st.download_button(
#         label="📄 Download CSV",
#         data=csv,
#         file_name="Collection_Executive_Report.csv",
#         mime="text/csv",
#         use_container_width=True
#     )

# with download_col2:

#     from io import BytesIO

#     output = BytesIO()

#     with pd.ExcelWriter(output, engine="openpyxl") as writer:
#         summary.to_excel(
#             writer,
#             sheet_name="Executive Report",
#             index=False
#         )

#     st.download_button(
#         label="📊 Download Excel",
#         data=output.getvalue(),
#         file_name="Collection_Executive_Report.xlsx",
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         use_container_width=True
#     )

# st.divider()

# # =====================================================
# # FOOTER
# # =====================================================

# # st.markdown(
# #     """
# #     <div style="text-align:center;padding:20px;border-top:1px solid #ddd;">
# #         <h4>🏆 Collection Executive Performance Dashboard</h4>
# #         <p>Live Google Sheet • Streamlit • Plotly • Pandas</p>
# #         <p>Developed for Collection Team</p>
# #     </div>
# #     """,
# #     unsafe_allow_html=True
# # )




import streamlit as st
import pandas as pd
from datetime import datetime
from utils import load_data, filter_dataframe
import streamlit.components.v1 as components

from charts import (
    executive_chart,
    monthly_chart,
    status_chart,
    leaderboard_chart
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Collection Executive Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# --------------------------------------------------
# GOOGLE SHEET CSV
# --------------------------------------------------

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT771wZ8ZcNJOh6odbwJRFjefSWNr8tI-ali3ivMq-4qymISZnnSsG3LZDsMr-wDiPZ7_5eRrNhBQ24/pub?output=csv"

df = load_data(CSV_URL)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📊 EazyPaisa Collection Dashboard")

if st.sidebar.button("🔄 Refresh Dashboard"):
    st.cache_data.clear()
    st.rerun()

from datetime import datetime

months = ["All"] + sorted(
    df["Repay Month"].dropna().unique().tolist()
)

# Current month ka naam (July 2026 -> July)
current_month = datetime.now().strftime("%B")

# Agar sheet me current month hai to wahi default select hoga
default_index = 0

if current_month in months:
    default_index = months.index(current_month)

selected_month = st.sidebar.selectbox(
    "Repay Month",
    months,
    index=default_index
)

executives = ["All"] + sorted(
    df["Executive Name"].dropna().unique().tolist()
)

selected_executive = st.sidebar.selectbox(
    "Collection Executive",
    executives
)

status_list = ["All"] + sorted(
    df["Current Status"].dropna().unique().tolist()
)

selected_status = st.sidebar.selectbox(
    "Current Status",
    status_list
)

from_date = st.sidebar.date_input(
    "From Date",
    value=df["Repay Date"].min()
)

to_date = st.sidebar.date_input(
    "To Date",
    value=df["Repay Date"].max()
)

filtered = filter_dataframe(
    df,
    selected_month,
    selected_executive,
    selected_status,
    from_date,
    to_date
)

# --------------------------------------------------
# KPI VALUES
# --------------------------------------------------

loan_amount = filtered["Loan Amount"].sum()

repay_amount = filtered["Loan Repay Amount"].sum()

received_amount = filtered["Total Received"].sum()

pending_amount = repay_amount - received_amount

collection_percentage = 0

if repay_amount > 0:
    collection_percentage = (
        received_amount / repay_amount
    ) * 100

executive_count = filtered["Executive Name"].nunique()

account_count = len(filtered)

closed_accounts = len(
    filtered[
        filtered["Current Status"]
        .str.upper()
        .str.contains("CLOSE", na=False)
    ]
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🏆 Collection Executive Performance Dashboard")

# st.caption(
#     "Live Dashboard | Collection Executive Performance Dashboard"
# )

# --------------------------------------------------
# KPI CARDS - FIXED VERSION
# --------------------------------------------------

# Create KPI data
kpis = [
    ("💰 Loan Amount", f"₹{loan_amount:,.0f}"),
    ("💳 Repay Amount", f"₹{repay_amount:,.0f}"),
    ("💵 Received", f"₹{received_amount:,.0f}"),
    ("📉 Pending", f"₹{pending_amount:,.0f}"),
    ("📈 Collection %", f"{collection_percentage:.2f}%"),
    ("👨‍💼 Executives", f"{executive_count}"),
    ("📄 Accounts", f"{account_count}"),
    ("✅ Closed Accounts", f"{closed_accounts}")
]

# Create HTML for all KPI cards at once
kpi_html = """
<div class="kpi-container">
"""

for title, value in kpis:
    kpi_html += f"""
    <div class="kpi-card-new">
        <div class="kpi-icon">{title.split()[0]}</div>
        <div class="kpi-title-new">{title.split(' ', 1)[1]}</div>
        <div class="kpi-value-new">{value}</div>
    </div>
    """

kpi_html += """
</div>
"""

# Display KPI cards using components.html
components.html(
    f"""
    <html>
    <head>
    <style>
    .kpi-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        width: 100%;
        margin: 20px 0;
    }}

    .kpi-card-new {{
        background: linear-gradient(135deg, 
            rgba(34, 197, 94, 0.15) 0%,
            rgba(15, 23, 42, 0.8) 100%);
        
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(74, 222, 128, 0.3);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        text-align: center;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}

    .kpi-card-new:hover {{
        transform: translateY(-8px);
        border-color: #22c55e;
        box-shadow: 0 25px 60px rgba(34, 197, 94, 0.25);
    }}

    .kpi-icon {{
        font-size: 28px;
        margin-bottom: 8px;
    }}

    .kpi-title-new {{
        color: #cbd5e1;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }}

    .kpi-value-new {{
        color: #ffffff;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -0.5px;
    }}

    @media (max-width: 1200px) {{
        .kpi-container {{
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        }}
        
        .kpi-value-new {{
            font-size: 20px;
        }}
    }}

    @media (max-width: 768px) {{
        .kpi-container {{
            grid-template-columns: repeat(2, 1fr);
        }}
        
        .kpi-card-new {{
            padding: 15px;
        }}
    }}
    </style>
    </head>
    <body style="background: transparent; margin: 0; padding: 0;">
    {kpi_html}
    </body>
    </html>
    """,
    height=200
)

st.divider()

# 👇 Collection Progress Bar yahan add karo
import streamlit.components.v1 as components

# ⭐ FIXED: Calculate Crore values correctly
collected_cr = received_amount / 10000000
remaining_cr = pending_amount / 10000000
target_cr = repay_amount / 10000000

components.html(
    f"""
<!DOCTYPE html>
<html>

<head>

<style>

body{{
    margin:0;
    background:transparent;
    font-family:Arial,sans-serif;
}}

.collection-progress-card{{

    padding:22px;

    border-radius:20px;

    background:linear-gradient(
        135deg,
        #111827,
        #1f2937
    );

    border:1px solid rgba(255,215,0,.20);

}}

.progress-title{{

    color:white;

    font-size:22px;

    font-weight:bold;

    margin-bottom:15px;

}}

.progress-track{{

    width:100%;

    height:18px;

    background:#2B2113;

    border-radius:50px;

    overflow:hidden;

}}

.progress-fill{{

    width:{min(collection_percentage,100):.2f}%;

    height:100%;

    border-radius:50px;

    background:linear-gradient(
        90deg,
        #7A4A00,
        #C58A00,
        #FFD700,
        #FFF5B7,
        #FFD700,
        #C58A00,
        #7A4A00
    );

    background-size:300% 100%;

    animation:goldFlow 3s linear infinite;

}}

@keyframes goldFlow{{

0%{{background-position:0%;}}

100%{{background-position:300%;}}

}}

.progress-info{{

    margin-top:18px;

    display:flex;

    justify-content:space-between;

    text-align:center;

}}

.progress-info small{{

    color:#BBBBBB;

    font-size:12px;

}}

.progress-info b{{

    color:#FFD700;

    font-size:18px;

}}

</style>

</head>

<body>

<div class="collection-progress-card">

<div class="progress-title">
📈 Collection Performance
</div>

<div class="progress-track">

    <div class="progress-fill" style="width:{min(collection_percentage,100):.2f}%">

        <div class="progress-tooltip">

            <b>{collection_percentage:.2f}% Collection</b><br><br>

            💰 Collected : ₹{collected_cr:.2f} Cr<br>

            🎯 Target : ₹{target_cr:.2f} Cr<br>

            📉 Remaining : ₹{remaining_cr:.2f} Cr

        </div>

    </div>

</div>

<div class="progress-info">

<div>

<small>Collected</small><br>

<b>₹0 to ₹{collected_cr:.2f} Cr</b>

</div>

<div>

<small>Remaining</small><br>

<b>₹0 to ₹{remaining_cr:.2f} Cr</b>

</div>

<div>

<small>Target</small><br>

<b>₹0 to ₹{target_cr:.2f} Cr</b>

</div>

</div>

</div>

</body>

</html>

""",
    height=170,
)
# # 👇 Iske baad ye code rahega
# st.markdown("""
# <div class="top-performer-header">
#     🏆 Top Performers
# </div>
# """, unsafe_allow_html=True)

# =====================================================
# IMPROVED TOP 3 PERFORMANCE CARDS
# =====================================================

st.markdown("""
<div class="top-performer-header">
    🏆 Top Performers
</div>
""", unsafe_allow_html=True)

leaders = (
    filtered.groupby("Executive Name", as_index=False)
    .agg({
        "Loan Amount":"sum",
        "Loan Repay Amount":"sum",
        "Total Received":"sum"
    })
)

leaders["Collection %"] = (
    leaders["Total Received"] /
    leaders["Loan Repay Amount"]
).fillna(0) * 100

leaders = leaders.sort_values(
    "Collection %",
    ascending=False
)

top3 = leaders.head(3).reset_index(drop=True)

if len(top3) >= 3:
    left, second, first, third, right = st.columns([0.6, 1, 1, 1, 0.6])

    # ================= SECOND PLACE (SILVER) =================
    with second:
        r = top3.iloc[1]
        exec_name = r["Executive Name"]
        received = r["Total Received"]
        collection_pct = r["Collection %"]
        repay_amt = r["Loan Repay Amount"]
        
        st.markdown(
            f"""
            <div class="performance-card silver-card">
                <div class="medal-emoji">🥈</div>
                <div class="position-badge">2ND PLACE</div>
                <h3 class="exec-name">{exec_name}</h3>
                <div class="amount-box">₹{received:,.0f}</div>
                <div class="stats-row">
                    <div class="stat-item">
                        <div class="stat-label">Collection</div>
                        <div class="stat-value">{collection_pct:.2f}%</div>
                    </div>
                    <div class="stat-divider"></div>
                    <div class="stat-item">
                        <div class="stat-label">Repay</div>
                        <div class="stat-value">₹{repay_amt/100000:.1f}L</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ================= FIRST PLACE (GOLD) =================
    with first:
        r = top3.iloc[0]
        exec_name = r["Executive Name"]
        received = r["Total Received"]
        collection_pct = r["Collection %"]
        repay_amt = r["Loan Repay Amount"]
        loan_amt = r["Loan Amount"]
        
        st.markdown(
            f"""
            <div class="performance-card gold-card">
                <div class="crown-emoji">👑</div>
                <div class="medal-emoji gold-medal">🥇</div>
                <div class="position-badge gold-badge">1ST PLACE</div>
                <h2 class="exec-name-gold">{exec_name}</h2>
                <div class="amount-box gold-amount">₹{received:,.0f}</div>
                <div class="stats-row gold-stats">
                    <div class="stat-item">
                        <div class="stat-label">Collection</div>
                        <div class="stat-value">{collection_pct:.2f}%</div>
                    </div>
                    <div class="stat-divider"></div>
                    <div class="stat-item">
                        <div class="stat-label">Repay</div>
                        <div class="stat-value">₹{repay_amt/100000:.1f}L</div>
                    </div>
                        <div class="stat-value gold-stat-val">{int(filtered[filtered['Executive Name']==exec_name].shape[0])}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ================= THIRD PLACE (BRONZE) =================
    with third:
        r = top3.iloc[2]

        exec_name = r["Executive Name"]
        received = r["Total Received"]
        collection_pct = r["Collection %"]
        repay_amt = r["Loan Repay Amount"]
        
        st.markdown(
            f"""
            <div class="performance-card bronze-card">
                <div class="medal-emoji">🥉</div>
                <div class="position-badge">3RD PLACE</div>
                <h3 class="exec-name">{exec_name}</h3>
                <div class="amount-box">₹{received:,.0f}</div>
                <div class="stats-row">
                    <div class="stat-item">
                        <div class="stat-label">Collection</div>
                        <div class="stat-value">{collection_pct:.2f}%</div>
                    </div>
                    <div class="stat-divider"></div>
                    <div class="stat-item">
                        <div class="stat-label">Repay</div>
                        <div class="stat-value">₹{repay_amt/100000:.1f}L</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

elif len(top3) > 0:
    cols = st.columns(len(top3))
    for idx, col in enumerate(cols):
        with col:
            r = top3.iloc[idx]
            exec_name = r["Executive Name"]
            received = r["Total Received"]
            collection_pct = r["Collection %"]
            
            st.markdown(
                f"""
                <div class="performance-card simple-card">
                    <div class="simple-rank">#{idx+1}</div>
                    <div class="exec-name-simple">{exec_name}</div>
                    <div class="amount-simple">₹{received:,.0f}</div>
                    <div class="percentage-simple">{collection_pct:.2f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.subheader("📋 Executive Summary")

summary = (
    filtered.groupby("Executive Name", as_index=False)
    .agg({
        "Loan Amount": "sum",
        "Loan Repay Amount": "sum",
        "Total Received": "sum",
        "Pending Amount": "sum"
    })
)

summary["Collection %"] = (
    summary["Total Received"] /
    summary["Loan Repay Amount"]
).fillna(0) * 100

summary["Accounts"] = (
    filtered.groupby("Executive Name")
    .size()
    .values
)

summary = summary.sort_values(
    "Collection %",
    ascending=False
)

summary.insert(
    0,
    "Rank",
    range(1, len(summary) + 1)
)

summary = summary.reset_index(drop=True)

table_html = """
<div class="leaderboard-table">
<table>

<thead>
<tr>
<th>Rank</th>
<th>Executive Name</th>
<th>Loan Amount</th>
<th>Repay Amount</th>
<th>Total Received</th>
<th>Pending Amount</th>
<th>Collection %</th>
<th>Accounts</th>
</tr>
</thead>

<tbody>
"""

for _, row in summary.iterrows():

    medal = ""

    if row["Rank"] == 1:
        medal = "🥇"

    elif row["Rank"] == 2:
        medal = "🥈"

    elif row["Rank"] == 3:
        medal = "🥉"

    pct = row["Collection %"]

    if pct >= 95:
        color = "#00ff88"

    elif pct >= 85:
        color = "#ffd54f"

    else:
        color = "#ff5252"

    table_html += f"""
    <tr>

        <td class="rank">
            {medal} {row['Rank']}
        </td>

        <td class="name">
            {row['Executive Name']}
        </td>

        <td>
            ₹{row['Loan Amount']:,.0f}
        </td>

        <td>
            ₹{row['Loan Repay Amount']:,.0f}
        </td>

        <td>
            ₹{row['Total Received']:,.0f}
        </td>

        <td>
            ₹{row['Pending Amount']:,.0f}
        </td>

        <td style="color:{color};font-weight:900;">
            {pct:.2f}%
        </td>

        <td>
            {row['Accounts']}
        </td>

    </tr>
    """

table_html += """
</tbody>
</table>
</div>
"""

with open("style.css", "r", encoding="utf-8") as f:
    css = f.read()

components.html(
    f"""
<!DOCTYPE html>
<html>

<head>

<style>

{css}

body{{
    margin:0;
    padding:10px;
    background:#052e1b;
}}

</style>

</head>

<body>

{table_html}

</body>

</html>

""",
height=650,
scrolling=True
)
st.divider()

# =====================================================
# DOWNLOAD REPORTS
# =====================================================

st.subheader("📥 Export Reports")

download_col1, download_col2 = st.columns(2)

with download_col1:

    csv = summary.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name="Collection_Executive_Report.csv",
        mime="text/csv",
        use_container_width=True
    )

with download_col2:

    from io import BytesIO

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        summary.to_excel(
            writer,
            sheet_name="Executive Report",
            index=False
        )

    st.download_button(
        label="📊 Download Excel",
        data=output.getvalue(),
        file_name="Collection_Executive_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.divider()

# =====================================================
# FOOTER
# =====================================================

# st.markdown(
#     """
#     <div style="text-align:center;padding:20px;border-top:1px solid #ddd;">
#         <h4>🏆 Collection Executive Performance Dashboard</h4>
#         <p>Live Google Sheet • Streamlit • Plotly • Pandas</p>
#         <p>Developed for Collection Team</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )
