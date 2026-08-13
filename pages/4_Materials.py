# pages/4_Materials.py
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
from ollama import chat
from utils.helper import init_page, render_banner, render_metric_card, style_plotly_chart

init_page("Material Management")

render_banner(
    "Inventory & Supply Chain",
    "Material stock levels, safety threshold alerts, supplier directory, and consumption trends."
)

db = st.session_state["db"]
materials = db["materials"]


def ask_ai(prompt):

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role":"system",
                "content":"You are an AI Construction Risk Analyst."
            },
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response["message"]["content"]
# Top KPIs Row
total_items = len(materials)
low_stock_df = materials[materials["Status"] == "Low Stock"]
low_stock_count = len(low_stock_df)
total_inv_value = materials["Total Value ($)"].sum()

m1, m2, m3, m4 = st.columns(4)
with m1:
    render_metric_card("Total SKUs Tracking", f"{total_items}", "blue", "📦", "Unique material items")
with m2:
    render_metric_card("Low Stock Alerts", f"{low_stock_count}", "red" if low_stock_count > 0 else "green", "⚠️", "Requires urgent ordering")
with m3:
    render_metric_card("Total Inventory Value", f"${total_inv_value:,.2f}", "yellow", "💵", "Assets valuation")
with m4:
    unique_suppliers = materials["Supplier"].nunique()
    render_metric_card("Partner Suppliers", f"{unique_suppliers}", "purple", "🤝", "Active vendor accounts")

# Warning notifications for low stock items
if low_stock_count > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background-color: #FEE2E2; border: 1px solid #FCA5A5; border-radius: 12px; padding: 1.25rem;'>
        <h4 style='margin: 0 0 0.5rem 0; color: #991B1B; display: flex; align-items: center; gap: 0.5rem;'>
            🚨 Material Reorder Alerts (Stock Below Threshold)
        </h4>
        <div style='font-size: 0.85rem; color: #7F1D1D;'>
            The following materials have fallen below their safety threshold and require immediate reordering:
        </div>
        <div style='margin-top: 0.5rem; display: flex; flex-wrap: wrap; gap: 0.5rem;'>
    """ + "".join([f"<span style='background: #EF4444; color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.775rem; font-weight: 600;'>{row['Material Name']} ({row['Stock Quantity']} / {row['Minimum Stock']} {row['Unit']})</span>" for _, row in low_stock_df.iterrows()]) + """
        </div>
    </div>
    """, unsafe_allow_html=True)

# Grid for Charts
st.markdown("<br>", unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns([1, 1])

with chart_col1:
    st.markdown("<h3 style='color: #1E3A8A;'>🧱 Stock Distribution by Category</h3>", unsafe_allow_html=True)
    # Group and count by category
    cat_df = materials.groupby("Category")["Total Value ($)"].sum().reset_index()
    fig_cat = px.bar(
        cat_df,
        x="Total Value ($)",
        y="Category",
        orientation="h",
        color="Total Value ($)",
        color_continuous_scale=px.colors.sequential.Blues,
        labels={"Total Value ($)": "Inventory Value ($)"},
        height=360
    )
    style_plotly_chart(fig_cat, x_title="Inventory Value ($)")
    fig_cat.update_layout(
        margin=dict(l=10, r=10, t=20, b=40),
        coloraxis_showscale=False
    )
    fig_cat.update_yaxes(showgrid=False)
    st.plotly_chart(fig_cat, use_container_width=True)

with chart_col2:
    st.markdown("<h3 style='color: #1E3A8A;'>🚛 Material Usage Trend (Last 6 Months)</h3>", unsafe_allow_html=True)
    # Mock usage data for chart
    usage_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    usage_data = pd.DataFrame({
        "Month": usage_months * 3,
        "Quantity (Tons)": [120, 150, 170, 140, 210, 230,   # Cement
                             45, 60, 55, 75, 90, 85,        # Steel
                             90, 100, 110, 95, 130, 140],   # Aggregates
        "Material": ["Cement"]*6 + ["Steel"]*6 + ["Aggregates"]*6
    })
    fig_usage = px.bar(
        usage_data,
        x="Month",
        y="Quantity (Tons)",
        color="Material",
        color_discrete_map={"Cement": "#1E3A8A", "Steel": "#3B82F6", "Aggregates": "#94A3B8"},
        height=360
    )
    style_plotly_chart(fig_usage, x_title="Month", y_title="Quantity (Tons)")
    fig_usage.update_layout(
        margin=dict(l=10, r=10, t=30, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_usage.update_xaxes(showgrid=False)
    st.plotly_chart(fig_usage, use_container_width=True)

# Main Inventory Roster Table
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>📋 Full Inventory Ledger</h3>", unsafe_allow_html=True)

# Table controls
filter_c1, filter_c2, filter_c3 = st.columns([2, 1, 1])
with filter_c1:
    mat_search = st.text_input("Search Materials", placeholder="Search material title or ID...")
with filter_c2:
    cat_filter = st.selectbox("Category Filter", ["All"] + list(materials["Category"].unique()))
with filter_c3:
    status_filter = st.selectbox("Stock Status Filter", ["All", "In Stock", "Low Stock", "Out of Stock"])

# Filter logic
inv_df = materials.copy()
if mat_search:
    inv_df = inv_df[
        inv_df["Material Name"].str.contains(mat_search, case=False) |
        inv_df["Material ID"].str.contains(mat_search, case=False)
    ]
if cat_filter != "All":
    inv_df = inv_df[inv_df["Category"] == cat_filter]
if status_filter != "All":
    inv_df = inv_df[inv_df["Status"] == status_filter]

# Pandas color mapping function for clean badge presentation
def style_status_col(s):
    colors = []
    for val in s:
        if val == "Low Stock":
            colors.append("background-color: #FEF3C7; color: #D97706; font-weight: 600; text-align: center; border-radius: 4px;")
        elif val == "Out of Stock":
            colors.append("background-color: #FEE2E2; color: #DC2626; font-weight: 600; text-align: center; border-radius: 4px;")
        else: # In Stock
            colors.append("background-color: #D1FAE5; color: #059669; font-weight: 600; text-align: center; border-radius: 4px;")
    return colors

styled_inv_df = inv_df.style.apply(style_status_col, subset=["Status"])

# Streamlit Dataframe display
st.dataframe(
    styled_inv_df,
    column_config={
        "Material ID": st.column_config.TextColumn("ID", width="small"),
        "Material Name": st.column_config.TextColumn("Material Title", width="large"),
        "Category": st.column_config.TextColumn("Category", width="medium"),
        "Stock Quantity": st.column_config.NumberColumn("Current Stock", format="%d"),
        "Minimum Stock": st.column_config.NumberColumn("Min. Threshold", format="%d"),
        "Unit": st.column_config.TextColumn("Unit Type", width="small"),
        "Unit Price ($)": st.column_config.NumberColumn("Unit Cost ($)", format="$%,.2f"),
        "Total Value ($)": st.column_config.NumberColumn("Total Asset Value ($)", format="$%,.2f"),
        "Supplier": st.column_config.TextColumn("Preferred Supplier", width="medium"),
        "Status": st.column_config.TextColumn("Stock Status", width="small")
    },
    width="stretch",
    hide_index=True
)

# Row 4: Suppliers Directory list
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #1E3A8A;'>🤝 Primary Supplier Contact Directory</h3>", unsafe_allow_html=True)

# Static Supplier List for aesthetics
supplier_data = pd.DataFrame({
    "Supplier Name": ["Matrix Materials Inc.", "Vulcan Building Solutions", "Pioneer Aggregates Co.", 
                       "Titan Steel Works", "Apex Build & Logistics", "Coastal Pipe & Fitting", 
                       "Giga Electrical Wholesalers", "Sherwin Coating Solutions"],
    "Supplied Materials": ["Cement & Concrete Mixes", "Concrete Blocks, Sand, Bricks", "Aggregates, Road Gravel",
                          "Structural Steel & Rebar", "Logistics & general builder lines", "Pipes, Fittings & Plumbing",
                          "Industrial Panels & Wires", "Exterior Acrylic & Paint Coatings"],
    "Contact Person": ["Charles Matrix", "Janet Vulcan", "Robert Pioneer", "Stanislas Titan", 
                      "Peter Apex", "David Coast", "Greta Giga", "Sarah Sherwin"],
    "Email": ["sales@matrixmaterials.com", "orders@vulcanbuild.com", "delivery@pioneeragg.com", "contracts@titansteel.com",
              "peter.h@apexlogistics.com", "info@coastalpipe.com", "supply@gigaelectrical.com", "commercial@sherwincoatings.com"],
    "Reliability Rating": ["⭐⭐⭐⭐⭐ (4.9)", "⭐⭐⭐⭐ (4.4)", "⭐⭐⭐⭐⭐ (4.8)", "⭐⭐⭐⭐ (4.3)", 
                          "⭐⭐⭐⭐⭐ (4.7)", "⭐⭐⭐⭐ (4.1)", "⭐⭐⭐⭐⭐ (4.9)", "⭐⭐⭐⭐ (4.5)"]
})

st.dataframe(supplier_data, width="stretch", hide_index=True)
st.markdown("---")

st.header("🧱 AI Material Estimator")

st.write("Estimate construction materials using AI based on project specifications.")

col1, col2 = st.columns(2)

with col1:
    area = st.number_input(
        "Project Area (sq ft)",
        min_value=500,
        value=5000,
        step=100
    )

    floors = st.number_input(
        "Number of Floors",
        min_value=1,
        value=5
    )

with col2:
    building_type = st.selectbox(
        "Building Type",
        [
            "Residential",
            "Commercial",
            "Hospital",
            "School",
            "Industrial"
        ]
    )

    structure = st.selectbox(
        "Structure Type",
        [
            "RCC",
            "Steel",
            "Composite"
        ]
    )

if st.button("🤖 Estimate Materials", width="stretch"):

    low_stock = materials[
        materials["Status"]=="Low Stock"
    ][["Material Name","Stock Quantity"]].to_string(index=False)

    prompt=f"""
You are a Construction Quantity Surveyor.

Estimate the construction materials.

Project Details

Building Type:
{building_type}

Structure:
{structure}

Area:
{area} sq ft

Floors:
{floors}

Current Inventory

{low_stock}

Generate

1 Executive Summary

2 Estimated Cement

3 Estimated Steel

4 Estimated Bricks

5 Estimated Sand

6 Estimated Aggregate

7 Inventory Check

8 Procurement Recommendations

Present the output in a professional report.
"""

    with st.spinner("AI is estimating materials..."):

        result=ask_ai(prompt)

    st.success("Material Estimation Completed")

    st.markdown(result)

    st.download_button(
        "📥 Download Material Report",
        result,
        file_name="Material_Estimation.txt",
        mime="text/plain",
        width="stretch"
    )