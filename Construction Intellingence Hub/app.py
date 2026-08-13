# app.py
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

# =========================
# LOGIN AUTHENTICATION
# =========================

def login_page():

    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 10% 10%, rgba(30,58,138,0.10), transparent 30%),
                radial-gradient(circle at 90% 90%, rgba(249,115,22,0.10), transparent 30%),
                #f8fafc;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        .login-title {
            text-align: center;
            color: #1E3A8A;
            font-family: Georgia, serif;
            font-size: 30px;
            font-weight: 700;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        .login-subtitle {
            text-align: center;
            color: #64748B;
            font-size: 14px;
            margin-bottom: 5px;
        }

        .login-access {
            text-align: center;
            color: #F97316;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
            margin-bottom: 25px;
        }

        .security-text {
            text-align: center;
            color: #64748B;
            font-size: 12px;
            margin-top: 18px;
        }

        .footer-text {
            text-align: center;
            color: #94A3B8;
            font-size: 11px;
            margin-top: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Choose Login or Sign Up
    # =========================
    # PROFESSIONAL LOGIN HEADER
    # =========================

    # =========================
    # CIH LOGIN HEADER
    # =========================

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.image("assets/logo.png", width=85)

        st.markdown(
            "<h1 style='text-align:center; color:#1E3A8A;'>"
            "Construction Intelligence Hub"
            "</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align:center; color:#64748B;'>"
            "Enterprise AI Operations Portal"
            "</p>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align:center; color:#F97316; "
            "font-size:11px; font-weight:bold; letter-spacing:1.5px;'>"
            "SECURE ENTERPRISE ACCESS"
            "</p>",
            unsafe_allow_html=True
        )


    # =========================
    # LOGIN / SIGN UP
    # =========================

    tab_login, tab_signup = st.tabs([
        "🔐 Login",
        "📝 Create Account"
    ])


    with tab_login:

        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "🔐 Sign In to CIH",
            use_container_width=True
        ):

            users = st.session_state.get("users", {})

            if username in users and users[username] == password:

                st.session_state["logged_in"] = True
                st.session_state["username"] = username

                st.rerun()

            elif not username or not password:

                st.warning("Please enter both username and password.")

            else:

                st.error("Invalid username or password.")


    with tab_signup:

        new_name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
            key="signup_name"
        )

        new_username = st.text_input(
            "Username",
            placeholder="Choose a username",
            key="signup_username"
        )

        new_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="signup_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="signup_confirm"
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True
        ):

            if not new_name or not new_username or not new_email or not new_password:

                st.warning("Please fill in all fields.")

            elif new_password != confirm_password:

                st.error("Passwords do not match.")

            else:

                users = st.session_state.setdefault("users", {})

                if new_username in users:

                    st.error("Username already exists.")

                else:

                    users[new_username] = new_password

                    st.success(
                        "Account created successfully! You can now login."
                    )


    st.markdown("""
    <div style="
        text-align:center;
        color:#64748B;
        font-size:12px;
        margin-top:20px;
    ">
        🟢 Secure access to Construction Intelligence Hub
    </div>

    <div style="
        text-align:center;
        color:#94A3B8;
        font-size:11px;
        margin-top:10px;
    ">
        CIH Enterprise Portal • AI-Powered Construction Operations
    </div>
    """, unsafe_allow_html=True)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Store registered users
if "users" not in st.session_state:
    st.session_state["users"] = {
        "admin": "admin123"
    }

if not st.session_state["logged_in"]:
    login_page()
    st.stop()
# Logout button
with st.sidebar:
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state.pop("username", None)
        st.rerun()

from utils.helper import init_page, render_banner, render_metric_card

# Initialize page configuration
init_page("Enterprise Portal")

# Custom Welcome Hero
render_banner(
    "Construction Intelligence Hub",
    "Enterprise AI Operations Portal & Operational Command Center"
)

st.markdown("""
<div style='margin-bottom: 2rem;'>
    <p style='font-size: 1.15rem; color: #475569;'>
        Welcome to the <b>CI Hub Enterprise Portal</b>. This command center integrates real-time operations, material inventories, workforce logistics, budgeting controls, risk factors, and predictive AI modeling into a unified interface.
    </p>
</div>
""", unsafe_allow_html=True)

# Snapshots of Global Metrics
db = st.session_state["db"]
projects = db["projects"]
employees = db["employees"]
materials = db["materials"]

total_projects = len(projects)
active_projects = len(projects[projects["Status"] == "Active"])
delayed_projects = len(projects[projects["Status"] == "Delayed"])
total_workers = len(employees)
low_stock_count = len(materials[materials["Status"] == "Low Stock"])

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    render_metric_card("Total Projects", f"{total_projects}", "blue", "📁", "Global portfolio")
with col2:
    render_metric_card("Active Projects", f"{active_projects}", "green", "🏗️", "Currently building")
with col3:
    render_metric_card("Delayed Sites", f"{delayed_projects}", "red", "⚠️", "Requires attention")
with col4:
    render_metric_card("Active Roster", f"{total_workers}", "purple", "👥", "Personnel on duty")
with col5:
    render_metric_card("Supply Alerts", f"{low_stock_count}", "yellow", "📦", "Low inventory items")

st.markdown("<h2 style='margin-top: 2.5rem; margin-bottom: 1.5rem; color: #1E3A8A;'>Operational Modules Launchpad</h2>", unsafe_allow_html=True)

# Grid layout for navigation
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2, row2_col3 = st.columns(3)
row3_col1, row3_col2, row3_col3 = st.columns(3)

# Row 1 Module Launchers
with row1_col1:
    st.markdown("""
    <div style='border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; background: #FFFFFF; min-height: 170px;'>
        <h4 style='margin: 0; color: #0F52BA;'>📊 Operational Dashboard</h4>
        <p style='color: #64748B; font-size: 0.85rem; margin: 0.5rem 0 1.25rem 0;'>Real-time metrics, project milestones, expense run-rates, and live notifications.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Dashboard", key="btn_dashboard", width="stretch"):
        st.switch_page("pages/1_Dashboard.py")

with row1_col2:
    st.markdown("""
    <div style='border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; background: #FFFFFF; min-height: 170px;'>
        <h4 style='margin: 0; color: #0F52BA;'>🗂️ Project Management</h4>
        <p style='color: #64748B; font-size: 0.85rem; margin: 0.5rem 0 1.25rem 0;'>Interactive tracking database, project progress metrics, and location mapping.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Projects Control", key="btn_projects", width="stretch"):
        st.switch_page("pages/2_Project_Management.py")

with row1_col3:
    st.markdown("""
    <div style='border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; background: #FFFFFF; min-height: 170px;'>
        <h4 style='margin: 0; color: #0F52BA;'>👥 Workforce Logistics</h4>
        <p style='color: #64748B; font-size: 0.85rem; margin: 0.5rem 0 1.25rem 0;'>Employee rosters, job roles allocation statistics, and attendance tracker.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Workforce Portal", key="btn_workforce", width="stretch"):
        st.switch_page("pages/3_Workforce.py")

# Row 2 Module Launchers
with row2_col1:
    st.markdown("""
    <div style='border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; background: #FFFFFF; min-height: 170px;'>
        <h4 style='margin: 0; color: #0F52BA;'>📦 Material & Stock</h4>
        <p style='color: #64748B; font-size: 0.85rem; margin: 0.5rem 0 1.25rem 0;'>Inventory list, safety threshold triggers, supplier list, and usage analytics.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Materials Portal", key="btn_materials", width="stretch"):
        st.switch_page("pages/4_Materials.py")

with row2_col2:
    st.markdown("""
    <div style='border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; background: #FFFFFF; min-height: 170px;'>
        <h4 style='margin: 0; color: #0F52BA;'>💳 Budget & Finance</h4>
        <p style='color: #64748B; font-size: 0.85rem; margin: 0.5rem 0 1.25rem 0;'>Expense breakdowns, actual versus planned budgets, and monthly cost curves.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Finance Hub", key="btn_budget", width="stretch"):
        st.switch_page("pages/5_Budget.py")

with row2_col3:
    st.markdown("""
    <div style='border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; background: #FFFFFF; min-height: 170px;'>
        <h4 style='margin: 0; color: #0F52BA;'>🛡️ Safety & Risk (HSE)</h4>
        <p style='color: #64748B; font-size: 0.85rem; margin: 0.5rem 0 1.25rem 0;'>HSE audits, incident counts, PPE compliance checks, and emergency contacts.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Safety Center", key="btn_safety", width="stretch"):
        st.switch_page("pages/6_Safety.py")

# Row 3 Module Launchers
with row3_col1:
    st.markdown("""
    <div style='border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; background: #FFFFFF; min-height: 170px;'>
        <h4 style='margin: 0; color: #0F52BA;'>🔮 AI Insights & Forecasts</h4>
        <p style='color: #64748B; font-size: 0.85rem; margin: 0.5rem 0 1.25rem 0;'>Predictive health scores, schedule delay odds, and weather impact projections.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch AI Engine", key="btn_ai", width="stretch"):
        st.switch_page("pages/7_AI_Insights.py")

with row3_col2:
    st.markdown("""
    <div style='border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; background: #FFFFFF; min-height: 170px;'>
        <h4 style='margin: 0; color: #0F52BA;'>💬 ConstructAI Assistant</h4>
        <p style='color: #64748B; font-size: 0.85rem; margin: 0.5rem 0 1.25rem 0;'>Interactive project operations AI chat assistant with pre-programmed queries.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Chat Agent", key="btn_assistant", width="stretch"):
        st.switch_page("pages/8_AI_Assistant.py")

with row3_col3:
    st.markdown("""
    <div style='border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; background: #FFFFFF; min-height: 170px;'>
        <h4 style='margin: 0; color: #0F52BA;'>📋 Executive Reports</h4>
        <p style='color: #64748B; font-size: 0.85rem; margin: 0.5rem 0 1.25rem 0;'>Generate consolidated CSV/PDF/Excel executive briefs and site analytics reports.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Reports Generator", key="btn_reports", width="stretch"):
        st.switch_page("pages/9_Reports.py")
