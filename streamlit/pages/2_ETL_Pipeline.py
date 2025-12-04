import streamlit as st
from PIL import Image
from pathlib import Path


# PAGE CONFIG

st.set_page_config(
    page_title="ETL Project Pipeline",
    layout="wide"
)

ASSETS = Path("streamlit/assets")


# GLOBAL STYLE — MATCH app.py

st.markdown("""
<style>

/* MATCH PAGE WIDTH CONTROL */
div[data-testid="stAppViewContainer"] > .main > .block-container {
    max-width: 70% !important;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* GLOBAL FONT */
html, body, [class*="st-"] {
    font-family: Verdana, Arial, sans-serif !important;
    color: #FFFFFF !important;
}

/* BASE FONT SIZE */
p, li, span, label, div {
    font-size: 20px !important;
}

/* HEADINGS */
h1 { font-size: 80px !important; color: #ffc800 !important; font-weight: 700 !important; }
h2 { font-size: 60px !important; color: #ffc800 !important; font-weight: 600 !important; }
h3 { font-size: 40px !important; color: #00A36C !important; }
h4 { font-size: 30px !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #4f5052ff !important;
}
section[data-testid="stSidebar"] * {
    font-size: 25px !important;
    color: #ffc800 !important;
}

/* MAIN BACKGROUND */
.stApp {
    background-color: #191a1dff !important;
}

/* CONTENT CARDS */
div[data-testid="stVerticalBlock"] > div {
    background-color: rgba(255,255,255,0.04);
    border-radius: 14px;
    padding: 1.2rem;
}

/* GLOW EFFECT FOR HERO IMAGE */
.hero-glow img {
    box-shadow: 0px 0px 40px rgba(255,200,0,0.45);
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)


# MAIN PAGE HEADER

st.markdown("""
<h1 style="text-align:center;">
ETL PROJECT PIPELINE
</h1>

<p style="text-align:center; font-size:26px; color:#00A36C;">
Engineering-first deep dive into pipeline architecture and data processing
</p>
<hr>
""", unsafe_allow_html=True)


# HERO IMAGE WITH GLOW

hero_img = Image.open(ASSETS / "ETL-pipeline-image.png")

st.markdown("<div class='hero-glow'>", unsafe_allow_html=True)
st.image(hero_img, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# PROJECT PLANNING — FULL WIDTH

pp_img = Image.open(ASSETS / "ProjectPlanning.png")

st.markdown("<h3>PROJECT PLANNING</h3>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.image(pp_img, use_container_width=True)

with col2:
    st.write("""
This phase defined the entire structure of delivery before any code was written.

Core activities:

• Virtual environments & dependency management  
• GitHub repository & branching workflows  
• Agile Kanban planning and sprint tracking  
• Dataset profiling & schema discovery  
• Domain research (electricity production & energy flows)  
• KPI identification & testing strategy design  
• Data governance & documentation standards  

This stage ensured the project followed a professional consulting-style delivery model.
""")

st.divider()


# EXTRACTION & TRANSFORMATION

c1, c2 = st.columns(2)

with c1:
    ext_img = Image.open(ASSETS / "Extraction.png")

    st.markdown("<h3>EXTRACTION</h3>", unsafe_allow_html=True)
    st.image(ext_img, use_container_width=True)

    st.write("""
Two IEA datasets were ingested containing:

• Monthly energy production by fuel type  
• Electricity imports and exports  

Engineering work included:

• CSV parsing & metadata cleanup  
• Temporal conversions and data type coercion  
• OECD country filtering  
• Structural consistency verification  
• Raw-layer data validation

Result: stable raw ingestion sources with minimal transformation.
""")

with c2:
    transform_img = Image.open(ASSETS / "Transform.png")

    st.markdown("<h3>TRANSFORMATION</h3>", unsafe_allow_html=True)
    st.image(transform_img, use_container_width=True)

    st.write("""
This stage delivered most of the engineering complexity.

Key transformations included:

• Fuel label normalisation (Coal / Oil / Solar / etc.)  
• Carbon grouping (LOW_CARBON / FOSSIL / NUCLEAR)  
• Atomic vs validation row classification  
• Feature engineering for KPI-ready metrics  
• Aggregation pipelines producing:
   - total_generation_gwh  
   - renewable_share_pct  
   - nuclear_share_pct  
   - fossil_share_pct  
   - import_dependency_pct  
   - grid_losses_pct  

The output of this step is a clean semantic layer designed specifically for analytics.
""")

st.divider()


# LOAD & ANALYTICS

c3, c4 = st.columns(2)
with c3:
    load_img = Image.open(ASSETS / "Load.png")

    st.markdown("<h3>LOAD</h3>", unsafe_allow_html=True)
    st.image(load_img, use_container_width=True)

    st.write("""
Final datasets were persisted into structured processed tables:

• Versioned CSV fact outputs  
• Row-level completeness & reconciliation testing  
• KPI integrity verification vs IEA totals  
• Replayable pipeline builds

These datasets act as the **single source of truth** for reporting.
""")

with c4:
    analytics_img = Image.open(ASSETS / "Analytics.png")

    st.markdown("<h3>ANALYTICS</h3>", unsafe_allow_html=True)
    st.image(analytics_img, use_container_width=True)

    st.write("""
Plotly dashboards and KPI views were developed in Streamlit to present:

• Energy generation mix  
• Renewable transition trajectories  
• Import dependency risk indicators  
• Grid efficiency & loss metrics

All visuals consume the **processed dataset outputs only**, maintaining
clear separation between engineering and analytics layers.
""")

st.divider()


# FOOTER

st.markdown("""
<p style="text-align:center; font-size:18px; color:#C7D0D8;">
This engineering pipeline demonstrates a full end-to-end data delivery lifecycle,
from raw ingestion to tested analytics deployment.
</p>
""", unsafe_allow_html=True)
