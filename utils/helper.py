# utils/helper.py
import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import datetime

# Ensure assets directory exists and generate logo if missing
def ensure_logo_exists():
    logo_dir = "assets"
    if not os.path.exists(logo_dir):
        os.makedirs(logo_dir)
    logo_path = os.path.join(logo_dir, "logo.png")
    if not os.path.exists(logo_path):
        # Create a professional construction themed placeholder logo
        img = Image.new("RGBA", (240, 240), color=(15, 82, 186, 255)) # Sapphire Blue
        draw = ImageDraw.Draw(img)
        
        # Draw a building/construction accent shape
        # Draw a house/tower outline
        draw.polygon([(120, 40), (190, 110), (160, 110), (160, 200), (80, 200), (80, 110), (50, 110)], 
                     fill=(255, 255, 255, 255), outline=None)
        
        # Add details - windows/girders
        draw.rectangle([(95, 120), (115, 150)], fill=(30, 58, 138, 255))
        draw.rectangle([(125, 120), (145, 150)], fill=(30, 58, 138, 255))
        draw.rectangle([(95, 160), (115, 190)], fill=(30, 58, 138, 255))
        draw.rectangle([(125, 160), (145, 190)], fill=(30, 58, 138, 255))
        
        # Draw gear/helmet motif at the top or simple text below
        # For simplicity, text "CIH" can be overlayed
        try:
            # Try to load a default font
            font = ImageFont.load_default()
            draw.text((105, 210), "CIH", fill=(255, 255, 255, 255), font=font)
        except Exception:
            pass
            
        img.save(logo_path, "PNG")

def load_css():
    css_path = os.path.join("assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        st.warning("CSS stylesheet missing from assets directory.")

def init_page(page_title):
    """Initializes standard page layout, custom styles, and sidebar content."""
    st.set_page_config(
        page_title=f"{page_title} | Construction Intelligence Hub",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Generate assets if needed
    ensure_logo_exists()
    
    # Load stylesheet
    load_css()
    
    # Initalize Session State for Shared Sample Data if not exists
    from utils.sample_data import get_all_data
    if "db" not in st.session_state:
        st.session_state["db"] = get_all_data()
        
    # Standard Sidebar Brand Banner
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=120)
        
    st.sidebar.markdown("""
    <div style='margin-bottom: 20px;'>
        <h2 style='margin: 0; font-size: 1.35rem; color: #1E3A8A;'>CI Hub Enterprise</h2>
        <p style='margin: 0; font-size: 0.8rem; color: #64748B;'>AI-Powered Operations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar footer metadata
    st.sidebar.divider()
    st.sidebar.markdown(f"""
    <div style='font-size: 0.75rem; color: #94A3B8;'>
        <p><b>User Role:</b> Project Admin</p>
        <p><b>System Date:</b> {datetime.date.today().strftime('%B %d, %Y')}</p>
        <p><b>Status:</b> Connected 🟢</p>
    </div>
    """, unsafe_allow_html=True)

def render_banner(title, subtitle):
    """Renders a gorgeous custom CSS gradient banner."""
    banner_html = f"""
    <div class="banner-container">
        <h1 class="banner-title">🏗️ {title}</h1>
        <p class="banner-subtitle">{subtitle}</p>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)

def render_metric_card(title, value, accent_type="blue", meta_icon="📈", meta_text=""):
    """Renders a beautiful premium card using HTML/CSS."""
    accent_class = f"card-accent-{accent_type}"
    meta_html = f"""
    <div class="card-meta">
        <span>{meta_icon}</span>
        <span>{meta_text}</span>
    </div>
    """ if meta_text else ""
    
    card_html = f"""
    <div class="card-container {accent_class}">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
        {meta_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def style_plotly_chart(fig, title_text="", x_title="", y_title="", is_pie_or_donut=False, is_gauge=False):
    """Applies premium, high-contrast styling to a Plotly chart for Light & Dark mode readability."""
    layout_update = {
        "plot_bgcolor": "rgba(0,0,0,0)",
        "paper_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family="'Inter', -apple-system, sans-serif", size=13),
    }
    
    if title_text:
        layout_update["title"] = dict(
            text=title_text,
            font=dict(size=16, family="'Inter', -apple-system, sans-serif", weight="bold"),
            x=0.0,
            y=0.98
        )
        
    if is_pie_or_donut:
        layout_update["margin"] = dict(l=30, r=30, t=60 if title_text else 30, b=60)
        layout_update["legend"] = dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        )
    elif is_gauge:
        layout_update["margin"] = dict(l=30, r=30, t=60 if title_text else 30, b=30)
    else:
        layout_update["margin"] = dict(l=50, r=30, t=60 if title_text else 30, b=50)
        layout_update["legend"] = dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        )
        
    fig.update_layout(**layout_update)
    
    if not is_pie_or_donut and not is_gauge:
        fig.update_xaxes(
            title=dict(text=x_title, font=dict(size=12, family="'Inter', -apple-system, sans-serif", weight="bold")) if x_title else None,
            tickfont=dict(size=11),
            gridcolor="rgba(148, 163, 184, 0.15)",
            showgrid=True
        )
        fig.update_yaxes(
            title=dict(text=y_title, font=dict(size=12, family="'Inter', -apple-system, sans-serif", weight="bold")) if y_title else None,
            tickfont=dict(size=11),
            gridcolor="rgba(148, 163, 184, 0.15)",
            showgrid=True
        )
    return fig

