# pages/3_Workforce.py
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

init_page("Workforce Management")

render_banner(
    "Workforce Operations",
    "Employee rosters, site allocations, daily attendance logs, and productivity analytics."
)

db = st.session_state["db"]
employees = db["employees"]
projects = db["projects"]

# Metrics calculations
total_headcount = len(employees)
engineers_cnt = len(employees[employees["Role"] == "Engineer"])
supervisors_cnt = len(employees[employees["Role"] == "Supervisor"])
laborers_cnt = len(employees[employees["Role"] == "Laborer"])
others_cnt = total_headcount - (engineers_cnt + supervisors_cnt + laborers_cnt)

average_attendance = employees["Attendance Rate (%)"].mean()
average_productivity = employees["Productivity Index (%)"].mean()

# Metrics Row
w1, w2, w3, w4 = st.columns(4)
with w1:
    render_metric_card("Total Personnel", f"{total_headcount}", "blue", "👥", "Global payroll roster")
with w2:
    render_metric_card("Site Laborers", f"{laborers_cnt}", "green", "👷", "On-site tradesmen & workers")
with w3:
    render_metric_card("Avg. Attendance Rate", f"{average_attendance:.1f}%", "yellow", "📅", "Rolling 30-day index")
with w4:
    render_metric_card("Avg. Productivity Score", f"{average_productivity:.1f}%", "purple", "⚡", "Performance rating")

# Secondary Roles Metrics in sub-header
st.markdown(f"**Operational Breakdown:** Engineers: `{engineers_cnt}` | Supervisors: `{supervisors_cnt}` | Safety & Admins: `{others_cnt}`")

st.markdown("<br>", unsafe_allow_html=True)
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("<h3 style='color: #1E3A8A;'>🏗️ Workforce Allocation by Project</h3>", unsafe_allow_html=True)
    
    # Donut chart showing how workforce is split across projects
    # Filter out unassigned and count
    assigned_df = employees[employees["Assigned Project"] != "Unassigned"]
    allocation_counts = assigned_df["Assigned Project"].value_counts().reset_index()
    allocation_counts.columns = ["Project Name", "Staff Count"]
    
    fig_donut = px.pie(
        allocation_counts,
        values="Staff Count",
        names="Project Name",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        height=380
    )
    style_plotly_chart(fig_donut, is_pie_or_donut=True)
    st.plotly_chart(fig_donut, use_container_width=True)

with right_col:
    st.markdown("<h3 style='color: #1E3A8A;'>💼 Personnel Distribution by Role</h3>", unsafe_allow_html=True)
    
    # Bar chart for role distribution
    role_counts = employees["Role"].value_counts().reset_index()
    role_counts.columns = ["Role", "Count"]
    
    fig_role = px.bar(
        role_counts,
        x="Count",
        y="Role",
        orientation="h",
        color="Role",
        color_discrete_sequence=["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B", "#EF4444"],
        text="Count",
        height=380
    )
    style_plotly_chart(fig_role, x_title="Count")
    fig_role.update_layout(
        showlegend=False,
        margin=dict(l=10, r=20, t=20, b=40)
    )
    fig_role.update_traces(
        textposition="outside",
        textfont=dict(size=12, weight="bold"),
        marker_line_width=0,
        width=0.5
    )
    fig_role.update_yaxes(showgrid=False)
    st.plotly_chart(fig_role, use_container_width=True)

# Row 3: Filterable Employee Table
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>📋 Personnel Roster & Performance Records</h3>", unsafe_allow_html=True)

# Table controls
tbl_col1, tbl_col2, tbl_col3 = st.columns([2, 1, 1])
with tbl_col1:
    staff_search = st.text_input("Search Personnel", placeholder="Enter name, email, or ID...")
with tbl_col2:
    role_filter = st.selectbox("Role Filter", ["All"] + list(employees["Role"].unique()))
with tbl_col3:
    status_filter = st.selectbox("Status Filter", ["All", "Active", "On Leave", "Suspended"])

# Roster filter logic
roster_df = employees.copy()
if staff_search:
    roster_df = roster_df[
        roster_df["Name"].str.contains(staff_search, case=False) |
        roster_df["Contact"].str.contains(staff_search, case=False) |
        roster_df["Employee ID"].str.contains(staff_search, case=False)
    ]
if role_filter != "All":
    roster_df = roster_df[roster_df["Role"] == role_filter]
if status_filter != "All":
    roster_df = roster_df[roster_df["Status"] == status_filter]

# Render interactive dataframe
st.dataframe(
    roster_df,
    column_config={
        "Employee ID": st.column_config.TextColumn("ID", width="small"),
        "Name": st.column_config.TextColumn("Full Name", width="medium"),
        "Role": st.column_config.TextColumn("Designated Role", width="small"),
        "Assigned Project": st.column_config.TextColumn("Assigned Project Site", width="medium"),
        "Hourly Rate ($)": st.column_config.NumberColumn("Hourly Wage ($)", format="$%d"),
        "Attendance Rate (%)": st.column_config.ProgressColumn("Attendance Rate (%)", min_value=0, max_value=100, format="%.1f%%"),
        "Productivity Index (%)": st.column_config.ProgressColumn("Productivity Rating", min_value=0, max_value=100, format="%.1f%%"),
        "Status": st.column_config.SelectboxColumn("Status", options=["Active", "On Leave", "Suspended"]),
        "Contact": st.column_config.TextColumn("Corporate Email", width="medium")
    },
    width="stretch",
    hide_index=True
)
