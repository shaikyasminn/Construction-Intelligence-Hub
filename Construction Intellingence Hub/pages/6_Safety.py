# pages/6_Safety.py
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
from ollama import chat
from utils.helper import init_page, render_banner, render_metric_card, style_plotly_chart

init_page("Safety & Risk (HSE)")

render_banner(
    "Safety & Risk Dashboard (HSE)",
    "HSE incident-free tracking, safety audit checklist reviews, and compliance records."
)

db = st.session_state["db"]
safety = db["safety"]

def ask_ai(prompt):

    try:

        response = chat(
            model="llama3.2",
            messages=[
                {
                    "role":"system",
                    "content":"You are an AI Construction Safety Officer."
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        return f"❌ {e}"

# Portfolio Averages
avg_safety_score = safety["Safety Score (HSE)"].mean()
total_minor_incidents = safety["Minor Incidents"].sum()
total_major_incidents = safety["Major Incidents"].sum()
avg_compliance = safety["Compliance Index (%)"].mean()

# KPIs Row
s1, s2, s3, s4 = st.columns(4)
with s1:
    render_metric_card("Avg Safety Score", f"{avg_safety_score:.1f}/100", "green" if avg_safety_score >= 90 else "yellow", "🛡️", "HSE audit baseline")
with s2:
    render_metric_card("Days Since Last Incident", "342 Days", "green", "📅", "Continuous safe days")
with s3:
    render_metric_card("Total Minor Incidents", f"{total_minor_incidents}", "yellow" if total_minor_incidents > 0 else "green", "⚠️", "Minor on-site scrapes")
with s4:
    render_metric_card("OSHA Compliance Rating", f"{avg_compliance:.1f}%", "blue", "📄", "Federal safety index")

# Grid for checklist & charts
st.markdown("<br>", unsafe_allow_html=True)
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown("<h3 style='color: #1E3A8A;'>🏗️ Project Risk & Safety Analysis</h3>", unsafe_allow_html=True)
    
    # Scatter bubble plot or bar chart representing safety score by active project
    fig_safety_bar = px.bar(
        safety,
        x="Safety Score (HSE)",
        y="Project Name",
        orientation="h",
        color="Safety Score (HSE)",
        color_continuous_scale=px.colors.sequential.Teal,
        text="Safety Score (HSE)",
        labels={"Project Name": ""},
        height=380
    )
    style_plotly_chart(fig_safety_bar, x_title="Safety Score (HSE)")
    fig_safety_bar.update_layout(
        margin=dict(l=10, r=20, t=20, b=40),
        coloraxis_showscale=False
    )
    fig_safety_bar.update_traces(
        textposition="outside",
        textfont=dict(size=12, weight="bold"),
        marker_line_width=0
    )
    fig_safety_bar.update_yaxes(showgrid=False)
    st.plotly_chart(fig_safety_bar, use_container_width=True)

with right_col:
    st.markdown("<h3 style='color: #1E3A8A;'>✅ Daily HSE Supervisor Checklist</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color:#64748B;'>Interactive safety checklist for daily tool-box briefs:</p>", unsafe_allow_html=True)
    
    # Interactive checkboxes with session state storage so they persist while viewing
    ch1 = st.checkbox("👷 All on-site workers wearing Hard Hats, High-Vis, and Steel-Toe Boots.", value=True)
    ch2 = st.checkbox("🦺 Fall protection harnesses checked and anchored for high-elevation works.", value=True)
    ch3 = st.checkbox("🚧 Safety barricades and exclusion zones marked around heavy equipment operations.", value=True)
    ch4 = st.checkbox("🔌 Heavy electrical tools and generators inspected for grounded cables.", value=False)
    ch5 = st.checkbox("🔥 Fire extinguishers, first-aid kits, and emergency muster stations marked and clear.", value=True)
    ch6 = st.checkbox("🗣️ Pre-shift toolbox talk held with all site workers discussing hazards.", value=True)
    
    total_checks = sum([ch1, ch2, ch3, ch4, ch5, ch6])
    score_p = int((total_checks / 6) * 100)
    
    if score_p == 100:
        st.success(f"**Audit Score: {score_p}%** — Site is fully compliant to proceed! 🟢")
    elif score_p >= 75:
        st.warning(f"**Audit Score: {score_p}%** — Resolve unchecked hazards before midday. ⚠️")
    else:
        st.error(f"**Audit Score: {score_p}%** — CRITICAL HAZARD: Stop operations! 🚨")

# Table of Project Safety Audits
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>📋 Project Safety Audit Log</h3>", unsafe_allow_html=True)

def style_safety_risk(s):
    colors = []
    for val in s:
        if val == "High":
            colors.append("background-color: #FEE2E2; color: #DC2626; font-weight: 600; text-align: center; border-radius: 4px;")
        elif val == "Medium":
            colors.append("background-color: #FEF3C7; color: #D97706; font-weight: 600; text-align: center; border-radius: 4px;")
        else: # Low
            colors.append("background-color: #D1FAE5; color: #059669; font-weight: 600; text-align: center; border-radius: 4px;")
    return colors

styled_safety = safety.style.apply(style_safety_risk, subset=["Risk Rating"])

st.dataframe(
    styled_safety,
    column_config={
        "Project Name": st.column_config.TextColumn("Project Title", width="large"),
        "Total Safety Inspections": st.column_config.NumberColumn("Safety Checks", format="%d"),
        "Safety Score (HSE)": st.column_config.ProgressColumn("Safety Score (HSE)", min_value=0, max_value=100, format="%d%%"),
        "Minor Incidents": st.column_config.NumberColumn("Minor Incidents", format="%d"),
        "Major Incidents": st.column_config.NumberColumn("Major Incidents", format="%d"),
        "Unresolved Hazards": st.column_config.NumberColumn("Hazards Flagged", format="%d"),
        "Compliance Index (%)": st.column_config.NumberColumn("OSHA Rating (%)", format="%.1f%%"),
        "Risk Rating": st.column_config.TextColumn("Risk Profile", width="small"),
        "Last Audit Date": st.column_config.DateColumn("Last Audit", format="YYYY-MM-DD")
    },
    width="stretch",
    hide_index=True
)

# Emergency Contacts directory
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>📞 Emergency HSE Contacts Directory</h3>", unsafe_allow_html=True)

contacts = pd.DataFrame({
    "Project Location/Region": ["Midwest (Chicago, IL)", "Texas (Austin/Houston)", "West Coast (Seattle/San Fran)", "East Coast (New York, NY)"],
    "Lead HSE Officer": ["Marcus Vance, Safety Lead", "Patricia Gomez, HSE Mgr", "David Miller, Safety PE", "Brian Kelly, Safety Specialist"],
    "Direct Phone": ["+1 (312) 555-0192", "+1 (512) 555-8902", "+1 (206) 555-0144", "+1 (212) 555-0182"],
    "Corporate Email": ["m.vance@cihub-enterprise.com", "p.gomez@cihub-enterprise.com", "d.miller@cihub-enterprise.com", "b.kelly@cihub-enterprise.com"],
    "Nearest Level 1 Hospital": ["Chicago Memorial Hospital", "St. David's Medical Center", "Harborview Medical Center", "Bellevue Hospital Center"]
})

st.dataframe(contacts, width="stretch", hide_index=True)

st.markdown("---")

st.header("🦺 AI Site Safety Analyzer")

selected_project = st.selectbox(
    "Select Project",
    safety["Project Name"]
)

site = safety[
    safety["Project Name"] == selected_project
].iloc[0]

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Safety Score",
    f"{site['Safety Score (HSE)']}"
)

c2.metric(
    "Minor Incidents",
    site["Minor Incidents"]
)

c3.metric(
    "Major Incidents",
    site["Major Incidents"]
)

c4.metric(
    "Hazards",
    site["Unresolved Hazards"]
)

if st.button("🤖 Analyze Site Safety", width="stretch"):

    prompt=f"""
You are a Construction Site Safety Expert.

Analyze this project safety information.

Project

{site['Project Name']}

Safety Score

{site['Safety Score (HSE)']}

Minor Incidents

{site['Minor Incidents']}

Major Incidents

{site['Major Incidents']}

Unresolved Hazards

{site['Unresolved Hazards']}

Compliance

{site['Compliance Index (%)']}%

Risk Rating

{site['Risk Rating']}

Generate

1 Executive Summary

2 Safety Assessment

3 Critical Hazards

4 Compliance Review

5 Immediate Actions

6 Recommendations

7 Overall Safety Rating
"""

    with st.spinner("AI is analyzing site safety..."):

        result=ask_ai(prompt)

    st.success("Safety Analysis Completed")

    st.markdown(result)

    st.download_button(
        "📥 Download Safety Report",
        result,
        file_name="Safety_Report.txt",
        mime="text/plain",
        width="stretch"
    )