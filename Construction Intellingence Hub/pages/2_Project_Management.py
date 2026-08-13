# pages/2_Project_Management.py
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
from ollama import chat
from utils.helper import init_page, render_banner, render_metric_card

init_page("Project Management")

render_banner(
    "Project Database & Tracking",
    "Detailed list of active, completed, delayed, and planned construction sites."
)

# Fetch database
db = st.session_state["db"]
projects = db["projects"]

def ask_ai(prompt):

    try:

        response = chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI Construction Risk Analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return str(e)

# Filters Section
st.markdown("<h3 style='color: #1E3A8A;'>🔍 Search & Filters</h3>", unsafe_allow_html=True)
filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])

with filter_col1:
    search_query = st.text_input("Search Projects", placeholder="Type project name, client, or location...")
with filter_col2:
    status_filter = st.selectbox("Status Filter", ["All", "Active", "Completed", "Delayed", "Planning"])
with filter_col3:
    risk_filter = st.selectbox("Risk Filter", ["All", "High", "Medium", "Low"])

# Filter logic
filtered_df = projects.copy()

if search_query:
    filtered_df = filtered_df[
        filtered_df["Project Name"].str.contains(search_query, case=False) |
        filtered_df["Client"].str.contains(search_query, case=False) |
        filtered_df["Location"].str.contains(search_query, case=False) |
        filtered_df["Lead Engineer"].str.contains(search_query, case=False)
    ]

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

if risk_filter != "All":
    filtered_df = filtered_df[filtered_df["Risk Level"] == risk_filter]

# Display count and key metrics
st.markdown(f"**Found {len(filtered_df)} project(s)**")

# Metrics for filtered set
tot_budget = filtered_df["Budget"].sum()
tot_spend = filtered_df["Spend"].sum()
rem_budget = tot_budget - tot_spend

m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    render_metric_card("Total Budget (Filtered)", f"${tot_budget:,.2f}", "blue", "💵")
with m_col2:
    render_metric_card("Total Disbursed (Filtered)", f"${tot_spend:,.2f}", "yellow", "💸")
with m_col3:
    accent_type = "green" if rem_budget >= 0 else "red"
    render_metric_card("Remaining Capital", f"${rem_budget:,.2f}", accent_type, "⚖️")

st.markdown("<br>", unsafe_allow_html=True)

# Format the dataframe using Streamlit's st.column_config for interactive tables
st.dataframe(
    filtered_df,
    column_config={
        "Project ID": st.column_config.TextColumn("ID", width="small"),
        "Project Name": st.column_config.TextColumn("Project Title", width="medium"),
        "Client": st.column_config.TextColumn("Client Name", width="medium"),
        "Location": st.column_config.TextColumn("Location", width="small"),
        "Lead Engineer": st.column_config.TextColumn("Engineer-in-Charge", width="medium"),
        "Start Date": st.column_config.DateColumn("Start Date", format="YYYY-MM-DD"),
        "End Date": st.column_config.DateColumn("Estimated End", format="YYYY-MM-DD"),
        "Budget": st.column_config.NumberColumn("Budget ($)", format="$%,.0f"),
        "Spend": st.column_config.NumberColumn("Actual Spend ($)", format="$%,.0f"),
        "Progress": st.column_config.ProgressColumn("Completion Progress (%)", min_value=0, max_value=100, format="%d%%"),
        "Status": st.column_config.SelectboxColumn("Status", options=["Active", "Completed", "Delayed", "Planning"]),
        "Health Score": st.column_config.NumberColumn("Health Index", format="%d/100"),
        "Risk Level": st.column_config.SelectboxColumn("Risk Rating", options=["High", "Medium", "Low"])
    },
    width="stretch",
    hide_index=True
)

# Detailed Site Expanders
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>🔎 Granular Site Milestones</h3>", unsafe_allow_html=True)

for index, row in filtered_df.head(5).iterrows():
    with st.expander(f"📋 {row['Project Name']} — Lead: {row['Lead Engineer']}"):
        col_l, col_r = st.columns(2)
        with col_l:
            st.write(f"**Client:** {row['Client']}")
            st.write(f"**Location:** {row['Location']}")
            st.write(f"**Timeline:** {row['Start Date']} to {row['End Date']}")
            
            # Simple manual calculation of variances
            variance = row["Budget"] - row["Spend"]
            if variance < 0:
                st.markdown(f"**Financial Health:** <span style='color:red;'>Over budget by ${abs(variance):,.2f}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"**Financial Health:** <span style='color:green;'>Under budget by ${variance:,.2f}</span>", unsafe_allow_html=True)
        with col_r:
            st.markdown(f"**Completion Status:** `{row['Status']}`")
            st.markdown(f"**HSE Risk Profile:** `{row['Risk Level']}`")
            st.markdown(f"**Predictive AI Health Rating:** `{row['Health Score']}/100`")
            
            # Sub-tasks check
            st.markdown("**Core Project Milestones:**")
            if row['Status'] == "Completed":
                st.markdown("✅ Earthworks & Excavation (100%)\n\n✅ Concrete Framework & Foundation (100%)\n\n✅ Structural Steel & Masonry (100%)\n\n✅ Utilities, Finishes & Fit-outs (100%)")
            elif row['Status'] == "Planning":
                st.markdown("⬜ Earthworks & Excavation (0%)\n\n⬜ Concrete Framework & Foundation (0%)\n\n⬜ Structural Steel & Masonry (0%)\n\n⬜ Utilities, Finishes & Fit-outs (0%)")
            elif row['Status'] == "Delayed":
                st.markdown("✅ Earthworks & Excavation (100%)\n\n⚠️ Concrete Framework & Foundation (75%)\n\n⬜ Structural Steel & Masonry (0%)\n\n⬜ Utilities, Finishes & Fit-outs (0%)")
            else: # Active
                progress_val = row['Progress']
                task1 = "✅" if progress_val > 25 else "⏳"
                task2 = "✅" if progress_val > 50 else "⏳"
                task3 = "✅" if progress_val > 75 else "⏳"
                st.markdown(f"{task1} Earthworks & Excavation (100%)\n\n{task2} Concrete Framework & Foundation (80%)\n\n{task3} Structural Steel & Masonry (20%)\n\n⏳ Utilities, Finishes & Fit-outs (0%)")
st.markdown("---")

st.header("⚠ AI Risk Detection")

selected_project = st.selectbox(
    "Select Project for AI Analysis",
    projects["Project Name"]
)

project = projects[
    projects["Project Name"] == selected_project
].iloc[0]

st.write("### Selected Project")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Progress", f"{project['Progress']}%")
c2.metric("Budget", f"${project['Budget']:,.0f}")
c3.metric("Spend", f"${project['Spend']:,.0f}")
c4.metric("Health", project["Health Score"])

if st.button("🤖 Analyze Project Risk", width="stretch"):

    prompt=f"""
You are a Senior Construction Risk Consultant.

Analyze the following project.

Project Name:
{project['Project Name']}

Location:
{project['Location']}

Status:
{project['Status']}

Progress:
{project['Progress']}%

Budget:
{project['Budget']}

Current Spend:
{project['Spend']}

Health Score:
{project['Health Score']}

Risk Level:
{project['Risk Level']}

Generate

1 Executive Summary

2 Major Risks

3 Budget Analysis

4 Schedule Analysis

5 Risk Mitigation Plan

6 Final Recommendation
"""

    with st.spinner("AI is analyzing project..."):

        result=ask_ai(prompt)

    st.success("Risk Analysis Completed")

    st.markdown(result)
