# pages/9_Reports.py
import sys
import os

# Ensure search path includes the project root and current working directory
root_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(root_dir) == "pages":
    root_dir = os.path.dirname(root_dir)
root_dir = os.path.normpath(root_dir)
if root_dir not in sys.path or sys.path[0] != root_dir:
    if root_dir in sys.path:
        sys.path.remove(root_dir)
    sys.path.insert(0, root_dir)

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helper import init_page, render_banner, render_metric_card, style_plotly_chart

init_page("Executive Reports")

render_banner(
    "Analytical Reports Center",
    "Customize operational metrics, draft executive briefs, and export project audit logs."
)

db = st.session_state["db"]
projects = db["projects"]
employees = db["employees"]
materials = db["materials"]

# Sidebar configurations specific to report building
st.sidebar.markdown("### ⚙️ Report Builder")
rpt_project = st.sidebar.selectbox("Scope Project:", ["All Portfolio"] + projects["Project Name"].tolist())
rpt_format = st.sidebar.radio("Export Format:", ["PDF Report", "Excel Spreadsheet", "CSV Datafile"])

st.sidebar.markdown("#### Include Modules:")
inc_fin = st.sidebar.checkbox("Financial Ledgers", value=True)
inc_wrk = st.sidebar.checkbox("Workforce Distribution", value=True)
inc_mat = st.sidebar.checkbox("Inventory Audits", value=True)
inc_saf = st.sidebar.checkbox("HSE Compliance Logs", value=True)

# Main Report Layout
st.markdown("<h3 style='color: #1E3A8A;'>📄 Consolidated Executive Summary</h3>", unsafe_allow_html=True)

scope_desc = f"all projects in the global portfolio" if rpt_project == "All Portfolio" else f"the **{rpt_project}** construction site"

st.markdown(f"""
<div style='background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; color: #334155; line-height: 1.6;'>
    <h4 style='margin: 0 0 0.5rem 0; color: #1E3A8A;'>Enterprise Audit Brief</h4>
    <p style='margin: 0;'>
        This document represents the official performance report generated on <b>July 03, 2026</b>. 
        The scope includes <b>{scope_desc}</b>. 
        All data compiled within this ledger represents real-time operational status including expenditures, staff log-ins, safety audits, and predictive AI variances.
    </p>
</div>
""", unsafe_allow_html=True)

# KPI Summary Row
st.markdown("<br>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

# Filter database based on report selection
if rpt_project == "All Portfolio":
    rep_proj_df = projects
else:
    rep_proj_df = projects[projects["Project Name"] == rpt_project]

tot_proj_num = len(rep_proj_df)
tot_proj_budget = rep_proj_df["Budget"].sum()
tot_proj_spend = rep_proj_df["Spend"].sum()
avg_health = rep_proj_df["Health Score"].mean()

with k1:
    render_metric_card("Projects Scoped", f"{tot_proj_num}", "blue", "📁")
with k2:
    render_metric_card("Scoped Budget", f"${tot_proj_budget / 1e6:.2f}M", "blue", "💵")
with k3:
    render_metric_card("Actual Expenditures", f"${tot_proj_spend / 1e6:.2f}M", "yellow", "💸")
with k4:
    render_metric_card("Average AI Health", f"{avg_health:.1f}/100", "green" if avg_health >= 85 else "yellow", "🔮")

# Export Buttons Row
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>📥 Download Generated Report Files</h3>", unsafe_allow_html=True)

exp_col1, exp_col2, exp_col3 = st.columns(3)

# Real CSV file converter for immediate download functionality!
csv_data = rep_proj_df.to_csv(index=False).encode('utf-8')

with exp_col1:
    # Dummy PDF downloader
    st.markdown("""
    <div style='text-align: center; border: 1px solid #E2E8F0; padding: 1rem; border-radius: 12px; background: white;'>
        <span style='font-size: 2.5rem;'>📄</span>
        <h5 style='margin: 0.5rem 0;'>Corporate Brief (PDF)</h5>
    </div>
    """, unsafe_allow_html=True)
    st.download_button(
        label="Download PDF Report",
        data="Dummy PDF File Content - Construction Intelligence Hub Report Summary",
        file_name=f"CIH_Executive_Report_{rpt_project.replace(' ', '_')}.pdf",
        mime="application/pdf",
        width="stretch"
    )

with exp_col2:
    # Dummy Excel downloader
    st.markdown("""
    <div style='text-align: center; border: 1px solid #E2E8F0; padding: 1rem; border-radius: 12px; background: white;'>
        <span style='font-size: 2.5rem;'>📊</span>
        <h5 style='margin: 0.5rem 0;'>Financials Ledger (XLSX)</h5>
    </div>
    """, unsafe_allow_html=True)
    st.download_button(
        label="Download Excel Ledger",
        data="Dummy Excel Binary Data - Construction Intelligence Hub Financial Table",
        file_name=f"CIH_Finance_Ledger_{rpt_project.replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width="stretch"
    )

with exp_col3:
    # Real CSV downloader
    st.markdown("""
    <div style='text-align: center; border: 1px solid #E2E8F0; padding: 1rem; border-radius: 12px; background: white;'>
        <span style='font-size: 2.5rem;'>📝</span>
        <h5 style='margin: 0.5rem 0;'>Database CSV File</h5>
    </div>
    """, unsafe_allow_html=True)
    st.download_button(
        label="Download Database (CSV)",
        data=csv_data,
        file_name=f"CIH_Data_Export_{rpt_project.replace(' ', '_')}.csv",
        mime="text/csv",
        width="stretch"
    )

# Report Section Content Preview based on selections
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>👁️ Scoped Data Preview</h3>", unsafe_allow_html=True)

if inc_fin:
    with st.container():
        st.markdown("#### 💵 Financial Transactions Preview")
        st.dataframe(rep_proj_df[["Project Name", "Budget", "Spend"]], width="stretch", hide_index=True)

if inc_wrk:
    with st.container():
        st.markdown("#### 👥 Active Site Personnel Preview")
        if rpt_project == "All Portfolio":
            active_staff_preview = employees.head(10)
        else:
            active_staff_preview = employees[employees["Assigned Project"] == rpt_project]
        st.dataframe(active_staff_preview[["Employee ID", "Name", "Role", "Assigned Project", "Status"]], width="stretch", hide_index=True)

if inc_mat:
    with st.container():
        st.markdown("#### 🧱 Low Stock Material Warnings")
        st.dataframe(materials[materials["Status"] == "Low Stock"][["Material Name", "Stock Quantity", "Minimum Stock", "Supplier"]], width="stretch", hide_index=True)

# Charts section for exporting
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>📊 Analytical Preview Chart</h3>", unsafe_allow_html=True)

fig_rep = px.scatter(
    rep_proj_df,
    x="Budget",
    y="Spend",
    size="Progress",
    color="Status",
    hover_name="Project Name",
    labels={"Budget": "Project Budget ($)", "Spend": "Actual Spend ($)"},
    title="Financial Performance Variance Plot (Bubble Size indicates Completion %)",
    height=400
)
style_plotly_chart(fig_rep, title_text="Financial Performance Variance Plot", x_title="Project Budget ($)", y_title="Actual Spend ($)")
fig_rep.update_layout(
    margin=dict(l=50, r=20, t=60, b=50)
)
st.plotly_chart(fig_rep, use_container_width=True)
