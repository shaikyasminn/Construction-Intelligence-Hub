# pages/1_Dashboard.py
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
import plotly.graph_objects as go
from utils.helper import init_page, render_banner, render_metric_card, style_plotly_chart

init_page("Dashboard")

render_banner(
    "Operations Dashboard",
    "Real-time operational overview, key milestones, financial trends, and event streams."
)

# Fetch Shared Database
db = st.session_state["db"]
projects = db["projects"]
employees = db["employees"]
materials = db["materials"]
budget = db["budget"]
activities = db["activities"]

# Row 1: KPI Metrics
total_projects = len(projects)
active_projects = len(projects[projects["Status"] == "Active"])
completed_projects = len(projects[projects["Status"] == "Completed"])
delayed_projects = len(projects[projects["Status"] == "Delayed"])

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    render_metric_card("Total Projects", f"{total_projects}", "blue", "📁", "Global portfolio size")
with kpi2:
    render_metric_card("Active Sites", f"{active_projects}", "green", "🏗️", "Currently under construction")
with kpi3:
    render_metric_card("Completed Sites", f"{completed_projects}", "purple", "✅", "Successfully delivered")
with kpi4:
    render_metric_card("Delayed Sites", f"{delayed_projects}", "red", "⚠️", "Requires immediate attention")

# Row 2: Secondary Operational Snapshot
st.markdown("<br>", unsafe_allow_html=True)
snap1, snap2, snap3, snap4 = st.columns(4)
with snap1:
    total_budget_val = f"${projects['Budget'].sum() / 1e6:.1f}M"
    render_metric_card("Total Portfolio Budget", total_budget_val, "blue", "💵", "Committed capital")
with snap2:
    total_spend_val = f"${projects['Spend'].sum() / 1e6:.1f}M"
    render_metric_card("Total Actual Spend", total_spend_val, "yellow", "💸", "Total funds disbursed")
with snap3:
    total_staff = len(employees[employees["Status"] == "Active"])
    render_metric_card("Active Workforce", f"{total_staff}", "green", "👥", "Personnel clocked-in today")
with snap4:
    low_stock = len(materials[materials["Status"] == "Low Stock"])
    render_metric_card("Material Alerts", f"{low_stock}", "red", "📦", "Items below safety threshold")

# Row 3: Charts Layout
st.markdown("<br>", unsafe_allow_html=True)
left_chart_col, right_chart_col = st.columns([3, 2])

with left_chart_col:
    st.markdown("<h3 style='color: #1E3A8A;'>📈 Portfolio Progress & Timelines</h3>", unsafe_allow_html=True)
    
    # Progress horizontal bar chart using Plotly
    active_delayed = projects[projects["Status"].isin(["Active", "Delayed"])].sort_values(by="Progress", ascending=True)
    fig_progress = px.bar(
        active_delayed,
        x="Progress",
        y="Project Name",
        orientation="h",
        color="Status",
        color_discrete_map={"Active": "#3B82F6", "Delayed": "#EF4444"},
        text="Progress",
        labels={"Progress": "Completion Percentage (%)", "Project Name": ""},
        height=380
    )
    style_plotly_chart(fig_progress, x_title="Completion Percentage (%)")
    fig_progress.update_layout(
        margin=dict(l=10, r=20, t=30, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_progress.update_traces(
        textposition="outside",
        textfont=dict(size=12, weight="bold"),
        texttemplate="%{text}%",
        marker_line_width=0,
        width=0.6
    )
    fig_progress.update_yaxes(showgrid=False)
    st.plotly_chart(fig_progress, use_container_width=True)

with right_chart_col:
    st.markdown("<h3 style='color: #1E3A8A;'>💰 Monthly Expenses Trend</h3>", unsafe_allow_html=True)
    
    # Monthly spending line chart
    fig_budget = go.Figure()
    fig_budget.add_trace(go.Scatter(
        x=budget["Month"], y=budget["Planned Budget ($M)"],
        mode='lines+markers', name='Planned ($M)',
        line=dict(color='#94A3B8', width=2, dash='dash')
    ))
    fig_budget.add_trace(go.Scatter(
        x=budget["Month"], y=budget["Actual Spend ($M)"],
        mode='lines+markers', name='Actual ($M)',
        line=dict(color='#0F52BA', width=3),
        fill='tozeroy', fillcolor='rgba(15, 82, 186, 0.05)'
    ))
    style_plotly_chart(fig_budget, x_title="Month", y_title="Spending ($M)")
    fig_budget.update_layout(
        margin=dict(l=10, r=10, t=30, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_budget, use_container_width=True)

# Row 4: Activities and Alerts
st.markdown("<br>", unsafe_allow_html=True)
activity_col, action_col = st.columns([3, 2])

with activity_col:
    st.markdown("<h3 style='color: #1E3A8A;'>📜 Recent Activity Feed</h3>", unsafe_allow_html=True)
    
    st.dataframe(
        activities[["Timestamp", "Project", "Activity", "Status"]],
        column_config={
            "Timestamp": st.column_config.TextColumn("Timestamp", width="medium"),
            "Project": st.column_config.TextColumn("Project", width="medium"),
            "Activity": st.column_config.TextColumn("Activity Details", width="large"),
            "Status": st.column_config.TextColumn("Status", width="small")
        },
        use_container_width=True,
        hide_index=True
    )

with action_col:
    st.markdown("<h3 style='color: #1E3A8A;'>⚡ Quick Portal Actions</h3>", unsafe_allow_html=True)
    
    act_col1, act_col2 = st.columns(2)
    with act_col1:
        if st.button("👥 Check Staff Attendance", width="stretch"):
            st.switch_page("pages/3_Workforce.py")
        if st.button("📦 Order Low Materials", width="stretch"):
            st.switch_page("pages/4_Materials.py")
        if st.button("🔮 Run Delay Predictor", width="stretch"):
            st.switch_page("pages/7_AI_Insights.py")
    with act_col2:
        if st.button("🗂️ Audit Active Sites", width="stretch"):
            st.switch_page("pages/2_Project_Management.py")
        if st.button("🛡️ Review HSE Incidents", width="stretch"):
            st.switch_page("pages/6_Safety.py")
        if st.button("📋 Download Excel Brief", width="stretch"):
            st.switch_page("pages/9_Reports.py")
            
    # System notifications box
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background-color: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 12px; padding: 1.25rem;'>
        <h4 style='margin: 0 0 0.5rem 0; color: #1E40AF; display: flex; align-items: center; gap: 0.5rem;'>
            🔔 System Notifications
        </h4>
        <ul style='margin: 0; padding-left: 1.25rem; font-size: 0.85rem; color: #1E3A8A; line-height: 1.6;'>
            <li>Weather forecast indicates Heavy Rain starting Tuesday. Ready concrete schedules should be adjusted.</li>
            <li>OSHA Inspector visit planned for <b>Lakeside Water Plant</b> on July 6th.</li>
            <li>Steel rebar shipment delayed by 2 days due to logistical issues.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
