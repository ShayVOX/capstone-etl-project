import streamlit as st
from PIL import Image


# PAGE CONFIG — MUST BE FIRST

st.set_page_config(
    page_title="Capstone Overview",
    layout="wide",
)


# GLOBAL STYLE OVERRIDES

st.markdown("""
<style>
/* HIDE STREAMLIT HEADER BAR */
header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0px;
}

div[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0px;
}
strea
/* CONTROL PAGE CONTENT WIDTH */
div[data-testid="stMainBlockContainer"] {
    max-width: 60% !important;   /* Try 60–85% here */
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}


/* ---------------------------------
   GLOBAL FONT
--------------------------------- */
html, body, [class*="st-"] {
    font-family: Verdana, Arial, sans-serif !important;
    color: #FFFFFF !important;
}

/* BASE FONT SIZE */
p, li, span, label, div {
    font-size: 20px !important;
}

/* ---------------------------------
   HEADINGS
--------------------------------- */
h1 {
    font-size: 80px !important;
    color: #ffc800 !important;
    font-weight: 700 !important;
}
h2 {
    font-size: 60px !important;
    color: #ffc800 !important;
    font-weight: 600 !important;
}
h3 {
    font-size: 40px !important;
    color: #00A36C !important;
}
h4 {
    font-size: 30px !important;
}

/* ---------------------------------
   SIDEBAR
--------------------------------- */
section[data-testid="stSidebar"] {
    background-color: #4f5052ff !important;
}
section[data-testid="stSidebar"] * {
    font-size: 25px !important;
    color: #ffc800 !important;
}

/* ---------------------------------
   MAIN APP BACKGROUND
--------------------------------- */
.stApp {
    background-color: #191a1dff !important;
}

/* ---------------------------------
   CONTENT CARDS / BLOCKS
--------------------------------- */
div[data-testid="stVerticalBlock"] > div {
    background-color: rgba(255,255,255,0.04);
    border-radius: 14px;
    padding: 1rem;
}

/* ---------------------------------
   BUTTONS
--------------------------------- */
button {
    background-color: #00A36C !important;
    color: white !important;
    border-radius: 10px !important;
}

/* ---------------------------------
   SLIDERS
--------------------------------- */
.stSlider > div {
    color: #E4D00A !important;
}

/* ---------------------------------
   METRICS
--------------------------------- */
[data-testid="stMetricValue"] {
    font-size: 22px !important;
    color: #E4D00A !important;
}
[data-testid="stMetricLabel"] {
    font-size: 16px !important;
    color: #C7D0D8 !important;
}

/* ---------------------------------
   IMAGES
--------------------------------- */
img {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# MAIN HEADER

st.markdown("""
<h1 style="text-align:center;">
CAPSTONE PROJECT — OECD ELECTRICITY DATA PIPELINE
</h1>

<h3 style="text-align:center; margin-top:-15px;">
Engineering-first end-to-end ETL pipeline and analytics platform
</h3>

<p style="text-align:center; font-size:26px; color:#00A36C;">
70% Data Engineering · 30% Analytics · consulting-style delivery
</p>
<hr>
""", unsafe_allow_html=True)


# PERSONAL STORY

st.subheader("Why Electricity?")

st.write("""
Growing up in parts of Africa where power cuts were routine, studying by candlelight
was often the norm rather than the exception.

That early experience stayed with me and developed a lasting curiosity about
electricity systems — how energy is generated, transported, and relied upon every
single day without most people noticing.

This capstone project stems directly from that personal connection, using real-world
electricity data to explore energy production, security of supply, and efficiency
across advanced economies.
""")


# DATA SOURCE

st.subheader("Data Source")

st.write("""
This project uses monthly production and electricity trade data from the  
**International Energy Agency (IEA)** — an organisation that provides trusted,
independent statistics to governments and institutions worldwide to inform
policy, investment, and energy security decisions.

The dataset focuses on **OECD member countries**, offering a consistent, comparable
view of mature electricity systems over the past decade.  
(OECD = Organisation for Economic Co-operation and Development)
""")

with st.expander("View 38 OECD Member Countries"):
    st.markdown("""
Australia, Austria, Belgium, Canada, Chile, Colombia, Czech Republic, Denmark,  
Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Japan,  
Korea, Latvia, Lithuania, Luxembourg, Mexico, Netherlands, New Zealand, Norway,  
Poland, Portugal, Slovak Republic, Slovenia, Spain, Sweden, Switzerland, Türkiye,  
United Kingdom, United States
""")


# STAKEHOLDERS

st.subheader("Stakeholders")

st.markdown("""
**Industry Context**
- Government energy analysts  
- National grid operators  
- Electricity market regulators  
- Policy planning agencies  

**Academy Delivery Context**
- Digital Futures tutors  
- Technical teammates  
- Digital Futures Senior Leadership Team (SLT)
""")

# DATA DISCLAIMER

st.subheader("Data Disclaimer")

st.write(
    "All data sourced directly from the **International Energy Agency Monthly Electricity Statistics tool — iea.org**."
)


# PROJECT AIMS

st.subheader("Project Aims")

st.markdown("""
**1.** Demonstrate the full 12-week Data Engineering curriculum — delivering a 
70% engineering / 30% analytics project enveloped by professional consulting skills
including communication, problem-solving, teamwork, critical thinking,
and stakeholder storytelling.

**2.** Design and build a production-style ETL pipeline transforming raw,
real-world datasets into a clean analytics-ready semantic layer.

**3.** Apply data validation and testing frameworks to ensure accuracy,
reconciliation integrity, and analytical confidence.

**4.** Deliver interactive dashboards exploring electricity generation mix,
import dependency, grid efficiency, and decarbonisation trends.

**5.** Use data storytelling to surface insights relating to  
energy security, sustainability, and infrastructure performance.
""")


# PRESENTER

st.divider()

col1, col2 = st.columns([1, 3])

with col1:
    photo = Image.open("streamlit/assets/sailesh.jpg")
    st.image(photo, width=180)

with col2:
    st.markdown("""
<h3 style='margin-bottom:4px;'>Sailesh Vyas</h3>
<p style='font-size:25px;'>Trainee Data Engineer</p>
<p style='font-size:25px;'>Digital Futures — Cohort 2509</p>
""", unsafe_allow_html=True)
