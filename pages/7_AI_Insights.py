# pages/7_AI_Insights.py
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
import numpy as np
import plotly.graph_objects as go
from ollama import chat
import requests
from utils.helper import init_page, render_banner, render_metric_card, style_plotly_chart

init_page("AI Insights")
def get_live_weather(city):

    try:
        url = f"https://wttr.in/{city}?format=j1"

        data = requests.get(url, timeout=5).json()

        current = data["current_condition"][0]

        return {
            "temp": current["temp_C"],
            "humidity": current["humidity"],
            "wind": current["windspeedKmph"],
            "condition": current["weatherDesc"][0]["value"]
        }

    except:
        return {
            "temp": "--",
            "humidity": "--",
            "wind": "--",
            "condition": "Unavailable"
        }
def ask_ai(prompt):
    try:
        response = chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": """
You are ConstructAI.

You are an AI assistant for a Construction Intelligence Hub.

Provide professional and concise recommendations.

Always answer in bullet points when possible.

Keep the answer under 150 words.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"❌ Ollama Error: {e}"

render_banner(
    "ConstructAI Predictive Insights",
    "Futuristic analytics engine: scheduling delay odds, cost overrun metrics, and weather risk maps."
)
db = st.session_state["db"]

projects = db["projects"]
employees = db["employees"]
materials = db["materials"]
budget = db["budget"]
safety = db["safety"]
activities = db["activities"]

st.markdown("<h3 style='color: #1E3A8A;'>🔮 Select Construction Site to Analyze</h3>", unsafe_allow_html=True)
selected_project_name = st.selectbox("Choose Project:", projects["Project Name"].tolist())

# Extract project row details
proj_row = projects[projects["Project Name"] == selected_project_name].iloc[0]
health = proj_row["Health Score"]
status = proj_row["Status"]
risk = proj_row["Risk Level"]
budget = proj_row["Budget"]
spend = proj_row["Spend"]
progress = proj_row["Progress"]
location = proj_row["Location"]
st.write("Selected Location:", location)
weather = get_live_weather(location)

weather_prompt = f"""
You are an AI construction weather advisor.

Location: {location}

Current Weather:
- Temperature: {weather['temp']}°C
- Condition: {weather['condition']}
- Humidity: {weather['humidity']}%
- Wind Speed: {weather['wind']} km/h

Give a short construction site advisory (2-3 lines).
"""

weather_advice = ask_ai(weather_prompt)
# Mock AI metrics based on project status and parameters
if status == "Delayed":
    delay_prob = 92
    overrun_prob = 84
    weather_risk = "Medium"
    reorder_urgency = "High"
    weather_msg = "Scattered rain expected. Outdoor concrete work must be rescheduled."
    rec_text = "Reallocate 5 scaffolders from Apex Tower; expedite steel delivery by utilizing air shipping; add safety inspectors on night shifts."
elif risk == "High" or spend > budget * (progress/100):
    delay_prob = 65
    overrun_prob = 78
    weather_risk = "High"
    reorder_urgency = "High"
    weather_msg = "Severe wind alerts (35mph) expected on Wednesday. Stop tower crane operations."
    rec_text = "Pause masonry work during winds; shift workforce to interior utility routing; pre-approve steel supplier billing variances."
elif status == "Completed":
    delay_prob = 0
    overrun_prob = 0
    weather_risk = "Low"
    reorder_urgency = "None"
    weather_msg = "Clear weather. Project successfully delivered."
    rec_text = "Perform final document handover; archive supplier ledger; dispatch workers to active projects."
else: # Active & Low Risk
    delay_prob = 12
    overrun_prob = 18
    weather_risk = "Low"
    reorder_urgency = "Low"
    weather_msg = "Sunny conditions. Optimal for structural framework construction."
    rec_text = "Maintain current workforce allocation; approve regular monthly invoices; prepare concrete formwork for next phase."

# Columns for AI KPIs
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1:
    h_color = "green" if health >= 85 else ("yellow" if health >= 70 else "red")
    render_metric_card("AI Project Health", f"{health}/100", h_color, "🔮", "Predicted stability index")
with c2:
    d_color = "red" if delay_prob >= 50 else ("yellow" if delay_prob >= 20 else "green")
    render_metric_card("Delay Probability", f"{delay_prob}%", d_color, "⏳", "AI scheduling hazard rating")
with c3:
    o_color = "red" if overrun_prob >= 50 else ("yellow" if overrun_prob >= 20 else "green")
    render_metric_card("Budget Overrun Risk", f"{overrun_prob}%", o_color, "💵", "Variance cost alert odds")
with c4:
    w_color = "red" if weather_risk == "High" else ("yellow" if weather_risk == "Medium" else "green")
    render_metric_card("Weather Hazard Risk", weather_risk, w_color, "🌦️", "Local site conditions risk")

# Detailed AI Predictions Layout
st.markdown("<br>", unsafe_allow_html=True)
left_panel, right_panel = st.columns([1, 1])

with left_panel:
    st.markdown("<h3 style='color: #1E3A8A;'>⚡ Predictive Health Gauge</h3>", unsafe_allow_html=True)
    
    # Plotly Gauge Chart for Health Score
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = health,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Predicted Health Index", 'font': {'size': 16, 'color': '#1E3A8A'}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': "#0F52BA"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#CBD5E1",
            'steps': [
                {'range': [0, 50], 'color': '#FEE2E2'},
                {'range': [50, 80], 'color': '#FEF3C7'},
                {'range': [80, 100], 'color': '#D1FAE5'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    style_plotly_chart(fig_gauge, is_gauge=True)
    fig_gauge.update_layout(
        margin=dict(l=20, r=20, t=30, b=10),
        height=280
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with right_panel:
    st.markdown("<h3 style='color: #1E3A8A;'>🌦️ Weather Impact & Hazard Level</h3>", unsafe_allow_html=True)
    
    # Beautiful Custom HTML Container for Weather Predictor
    weather_card_html = f"""
    <div style='background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; min-height: 200px;'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
            <span style='font-size: 1.1rem; font-weight: 700; color: #1E3A8A;'>📍 Site Location: {location}</span>
            <span style='font-size: 0.775rem; background: #EFF6FF; color: #1E40AF; padding: 4px 10px; border-radius: 12px; font-weight: 600;'>LIVE METEOROLOGY</span>
        </div>
        <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
            <span style='font-size: 2.5rem;'>🌦️</span>
            <div>
                <div style='font-size: 1.5rem; font-weight: 800; color: #0F172A;'>{weather['temp']}°C | {weather['condition']}</div>
                <div style='font-size: 0.85rem; color: #64748B;'>Humidity: {weather['humidity']}% | Wind: {weather['wind']} km/h</div>
            </div>
        </div>
        <div style='background-color: #FEF3C7; border-left: 4px solid #D97706; padding: 0.75rem; border-radius: 4px; font-size: 0.85rem; color: #92400E;'>
            <b>AI Advisory:</b> {weather_advice}
        </div>
    </div>
    """
    st.markdown(weather_card_html, unsafe_allow_html=True)

# Row 3: AI Recommendations & Scheduling Optimization
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>💡 AI Operational Recommendations</h3>", unsafe_allow_html=True)

st.info(f"**Optimization Proposal for {selected_project_name}:** \n\n{rec_text}")

# Grid of Predictive Analytics Details
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>🧠 Portfolio Health Predictions</h3>", unsafe_allow_html=True)

# Format project dataframe with AI insights
insights_df = projects[["Project Name", "Health Score", "Status", "Risk Level"]].copy()

# Add mock predictions based on actual health score
insights_df["AI Health Score"] = insights_df["Health Score"]
insights_df["AI Risk Assessment"] = insights_df["Risk Level"]
insights_df["Predicted Delay (Days)"] = insights_df["Health Score"].apply(lambda x: int((100 - x) * np.random.uniform(0.3, 0.6)))
insights_df["Efficiency Rating"] = insights_df["Health Score"].apply(lambda x: f"{x + np.random.randint(-3, 3)}%")

def style_ai_risk(s):
    colors = []
    for val in s:
        if val == "High":
            colors.append("background-color: #FEE2E2; color: #DC2626; font-weight: 600; text-align: center; border-radius: 4px;")
        elif val == "Medium":
            colors.append("background-color: #FEF3C7; color: #D97706; font-weight: 600; text-align: center; border-radius: 4px;")
        else: # Low
            colors.append("background-color: #D1FAE5; color: #059669; font-weight: 600; text-align: center; border-radius: 4px;")
    return colors

styled_insights = insights_df[["Project Name", "AI Health Score", "AI Risk Assessment", "Predicted Delay (Days)", "Efficiency Rating"]].style.apply(style_ai_risk, subset=["AI Risk Assessment"])

st.dataframe(
    styled_insights,
    column_config={
        "Project Name": st.column_config.TextColumn("Project Title", width="large"),
        "AI Health Score": st.column_config.ProgressColumn("AI Health Index", min_value=0, max_value=100, format="%d%%"),
        "AI Risk Assessment": st.column_config.TextColumn("AI Risk Assessment", width="small"),
        "Predicted Delay (Days)": st.column_config.NumberColumn("Est. Delay Variance", format="%d days"),
        "Efficiency Rating": st.column_config.TextColumn("Personnel Efficiency", width="small")
    },
    width="stretch",
    hide_index=True
)
st.markdown("---")
st.markdown("## 🤖 AI Decision Center")
st.write("Generate AI-powered insights using Ollama.")
col1, col2 = st.columns(2)

with col1:
    summary_btn = st.button("📊 AI Project Summary",width="stretch")

with col2:
    risk_btn = st.button("⚠ AI Risk Analysis", width="stretch")

col3, col4 = st.columns(2)

with col3:
    budget_btn = st.button("💰 Budget Advisor", width="stretch")

with col4:
    safety_btn = st.button("🛡 Safety Advisor", width="stretch")

col5, col6 = st.columns(2)

with col5:
    material_btn = st.button("📦 Material Advisor",width="stretch")

with col6:
    report_btn = st.button("📄 Executive Report", width="stretch")
if "ai_result" not in st.session_state:
    st.session_state["ai_result"] = ""
output = st.container()
# ---------------- AI Button Actions ---------------- #

if summary_btn:
    prompt = f"""
Generate a professional executive summary.

Projects: {len(projects)}
Active: {len(projects[projects['Status']=="Active"])}
Delayed: {len(projects[projects['Status']=="Delayed"])}
Completed: {len(projects[projects['Status']=="Completed"])}

Budget:
{projects['Budget'].sum():,.0f}

Spend:
{projects['Spend'].sum():,.0f}
"""
    with output:
        st.markdown("### 📊 AI Project Summary")
        result = ask_ai(prompt)
        st.session_state["ai_result"] = result
        st.write(result)


if risk_btn:
    prompt = f"""
Analyze project risks.

{projects[['Project Name','Risk Level','Status']].to_string(index=False)}

Give recommendations.
"""
    with output:
        st.markdown("### ⚠ AI Risk Analysis")
        result = ask_ai(prompt)
        st.session_state["ai_result"] = result
        st.write(result)


if budget_btn:
    prompt = f"""
Analyze the current budget.

Budget:
{projects['Budget'].sum():,.0f}

Spend:
{projects['Spend'].sum():,.0f}

Give financial recommendations.
"""
    with output:
        st.markdown("### 💰 Budget Advisor")
        result = ask_ai(prompt)
        st.session_state["ai_result"] = result
        st.write(result)    


if safety_btn:
    prompt = f"""
Average Safety Score:
{safety['Safety Score (HSE)'].mean()}

Unresolved Hazards:
{safety['Unresolved Hazards'].sum()}

Give safety recommendations.
"""
    with output:
        st.markdown("### 🛡 Safety Advisor")
        result = ask_ai(prompt)
        st.session_state["ai_result"] = result
        st.write(result)


if material_btn:
    prompt = f"""
Low Stock Materials

{materials[materials['Status']=="Low Stock"][['Material Name','Stock Quantity']].to_string(index=False)}

Suggest procurement actions.
"""
    with output:
        st.markdown("### 📦 Material Advisor")
        result = ask_ai(prompt)
        st.session_state["ai_result"] = result
        st.write(result)


if report_btn:
    prompt = f"""
Create an Executive Report.

Include

Project Summary
Budget
Safety
Risks
Materials
Recommendations

Projects:
{len(projects)}
"""
    with output:
        st.markdown("### 📄 Executive Report")
        result = ask_ai(prompt)
        st.session_state["ai_result"] = result
        st.write(result)

if st.session_state["ai_result"]:

    st.download_button(
        "📥 Download Report",
        data=st.session_state["ai_result"],
        file_name="AI_Report.txt",
        mime="text/plain"
    )