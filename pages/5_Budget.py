# pages/5_Budget.py
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

init_page("Budget & Finance")

render_banner(
    "Budget & Financial Controls",
    "Track overall capital allocation, actual spend run-rates, invoice clearances, and S-Curves."
)

db = st.session_state["db"]
projects = db["projects"]
budget = db["budget"]

# Consolidated metrics
total_portfolio_budget = projects["Budget"].sum()
total_portfolio_spend = projects["Spend"].sum()
remaining_portfolio_capital = total_portfolio_budget - total_portfolio_spend

# Calculate cost categorizations from aggregate percentages across monthly data
# We can sum up columns from the budget dataframe
total_labor_cost = budget["Labor Costs ($M)"].sum() * 1e6
total_material_cost = budget["Material Costs ($M)"].sum() * 1e6
total_equipment_cost = budget["Equipment Costs ($M)"].sum() * 1e6
total_permit_cost = budget["Permits & Admin ($M)"].sum() * 1e6

# KPIs Row
b1, b2, b3 = st.columns(3)
with b1:
    render_metric_card("Authorized Portfolio Budget", f"${total_portfolio_budget:,.2f}", "blue", "💵", "Committed capital")
with b2:
    render_metric_card("Disbursed Expenses", f"${total_portfolio_spend:,.2f}", "yellow", "💸", "Total spending to date")
with b3:
    accent_t = "green" if remaining_portfolio_capital >= 0 else "red"
    render_metric_card("Remaining Balance", f"${remaining_portfolio_capital:,.2f}", accent_t, "⚖️", "Available buffer")

# Secondary Cost Category Metrics
st.markdown("<br>", unsafe_allow_html=True)
sc1, sc2, sc3, sc4 = st.columns(4)
with sc1:
    render_metric_card("Labor Expenditures", f"${total_labor_cost:,.0f}", "purple", "👥", "Wages & subcontractor costs")
with sc2:
    render_metric_card("Material Purchases", f"${total_material_cost:,.0f}", "green", "🧱", "Deliveries & supply contracts")
with sc3:
    render_metric_card("Equipment Leases", f"${total_equipment_cost:,.0f}", "blue", "🚜", "Machinery, logistics & fuel")
with sc4:
    render_metric_card("Permits & Regulatory", f"${total_permit_cost:,.0f}", "yellow", "📄", "Compliance, legal & admin")

# Grid for visual charts
st.markdown("<br>", unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns([1, 1])

with chart_col1:
    st.markdown("<h3 style='color: #1E3A8A;'>🍕 Allocation of Spent Capital</h3>", unsafe_allow_html=True)
    # Donut Chart for Expense Categories
    expense_cats = ["Labor Costs", "Material Costs", "Equipment Leases", "Permits & Admin"]
    expense_vals = [total_labor_cost, total_material_cost, total_equipment_cost, total_permit_cost]
    fig_donut = px.pie(
        names=expense_cats,
        values=expense_vals,
        hole=0.45,
        color_discrete_sequence=["#8B5CF6", "#10B981", "#3B82F6", "#F59E0B"],
        height=360
    )
    style_plotly_chart(fig_donut, is_pie_or_donut=True)
    st.plotly_chart(fig_donut, use_container_width=True)

with chart_col2:
    st.markdown("<h3 style='color: #1E3A8A;'>📈 Cumulative Spending Curve (S-Curve)</h3>", unsafe_allow_html=True)
    # Plotly S-Curve Chart (Cumulative planned vs cumulative actual)
    cum_planned = budget["Planned Budget ($M)"].cumsum()
    cum_actual = budget["Actual Spend ($M)"].cumsum()
    
    fig_scurve = go.Figure()
    fig_scurve.add_trace(go.Scatter(
        x=budget["Month"], y=cum_planned,
        mode='lines+markers', name='Planned Target (Cum. $M)',
        line=dict(color='#94A3B8', width=2, dash='dash')
    ))
    fig_scurve.add_trace(go.Scatter(
        x=budget["Month"], y=cum_actual,
        mode='lines+markers', name='Actual Performance (Cum. $M)',
        line=dict(color='#0F52BA', width=3),
        fill='tozeroy', fillcolor='rgba(15, 82, 186, 0.03)'
    ))
    style_plotly_chart(fig_scurve, x_title="Month", y_title="Cumulative Spend ($M)")
    fig_scurve.update_layout(
        margin=dict(l=10, r=10, t=30, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_scurve, use_container_width=True)

# Row 4: Transaction Ledger & Approvals
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>📜 Recent Invoices & Billing Log</h3>", unsafe_allow_html=True)

# Mock transaction logs
transactions = pd.DataFrame({
    "Invoice ID": ["INV-2026-901", "INV-2026-902", "INV-2026-903", "INV-2026-904", "INV-2026-905", "INV-2026-906", "INV-2026-907", "INV-2026-908"],
    "Vendor": ["Matrix Materials Inc.", "Titan Steel Works", "Pioneer Aggregates Co.", "Summit Health Group", 
               "Coastal Pipe & Fitting", "Giga Electrical Wholesalers", "Vulcan Building Solutions", "Sherwin Coating Solutions"],
    "Project Association": ["Apex Tower Phase 1", "Riverfront Condos", "Metro Highway Expansion", "Summit Ridge Hospital",
                           "Lakeside Water Plant", "Centennial Transit Hub", "Aura Luxury Suites", "Pinnacle Office Plaza"],
    "Disbursement Amount ($)": [42500.00, 112000.00, 32400.00, 142500.00, 18500.00, 64200.00, 52800.00, 24600.00],
    "Invoice Date": ["2026-07-02", "2026-07-02", "2026-07-01", "2026-07-01", "2026-06-30", "2026-06-30", "2026-06-29", "2026-06-28"],
    "Clearance Status": ["Approved", "Approved", "Approved", "Approved", "Approved", "Pending Review", "Approved", "Pending Review"]
})

def style_clearance_col(s):
    colors = []
    for val in s:
        if val == "Pending Review":
            colors.append("background-color: #FEF3C7; color: #D97706; font-weight: 600; text-align: center; border-radius: 4px;")
        else: # Approved
            colors.append("background-color: #D1FAE5; color: #059669; font-weight: 600; text-align: center; border-radius: 4px;")
    return colors

styled_transactions = transactions.style.apply(style_clearance_col, subset=["Clearance Status"])

st.dataframe(
    styled_transactions,
    column_config={
        "Invoice ID": st.column_config.TextColumn("Invoice ID", width="small"),
        "Vendor": st.column_config.TextColumn("Vendor Name", width="medium"),
        "Project Association": st.column_config.TextColumn("Associated Project", width="medium"),
        "Disbursement Amount ($)": st.column_config.NumberColumn("Amount ($)", format="$%,.2f"),
        "Invoice Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
        "Clearance Status": st.column_config.TextColumn("Clearance Status", width="small")
    },
    width="stretch",
    hide_index=True
)
