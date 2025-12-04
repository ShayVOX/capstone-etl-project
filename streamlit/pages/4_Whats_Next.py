import streamlit as st


# PAGE CONFIG — MUST BE FIRST

st.set_page_config(
    page_title="What's Next",
    layout="wide",
)


# GLOBAL STYLES (MATCH OTHER PAGES)

st.markdown(
    """
<style>

/* CONTROL PAGE CONTENT WIDTH */
div[data-testid="stAppViewContainer"] > .main > .block-container {
    max-width: 70% !important;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* MULTIPAGE SIDEBAR NAV LABELS */
div[data-testid="stSidebarNav"] label {
    font-size: 22px !important;
    color: #ffc800 !important;
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
h1 {
    font-size: 70px !important;
    color: #ffc800 !important;
    font-weight: 700 !important;
}
h2 {
    font-size: 50px !important;
    color: #ffc800 !important;
    font-weight: 600 !important;
}
h3 {
    font-size: 36px !important;
    color: #00A36C !important;
}
h4 {
    font-size: 30px !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #4f5052ff !important;
}
section[data-testid="stSidebar"] * {
    font-size: 22px !important;
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
    padding: 1rem;
}

/* BUTTONS */
button {
    background-color: #00A36C !important;
    color: white !important;
    border-radius: 10px !important;
}

/* METRICS */
[data-testid="stMetricValue"] {
    font-size: 22px !important;
    color: #ffc800 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 16px !important;
    color: #C7D0D8 !important;
}

/* IMAGES */
img {
    border-radius: 10px;
}

</style>
""",
    unsafe_allow_html=True,
)


# PAGE HEADER

st.markdown(
    """
<h1 style="text-align:center;">
WHAT'S NEXT — SCALABILITY AND ROADMAP
</h1>
<h3 style="text-align:center; margin-top:-10px;">
From single laptop prototype to production-grade data product
</h3>
<hr>
""",
    unsafe_allow_html=True,
)


# CHALLENGES ENCOUNTERED

st.subheader("Challenges Encountered")

st.write(
    """
This capstone was my first time bringing many moving parts together:
project planning, engineering, testing, visualisation and presentation.
Several practical challenges emerged along the way.

Key areas of difficulty:

- Limited prior experience with Streamlit and custom CSS for UI design,
  which made styling and layout surprisingly time-consuming.
- Needing to understand how Streamlit components, HTML markup and injected CSS
  interact, and occasionally conflict.
- Working with a large IEA dataset that mixes atomic fuel rows, pre-aggregated
  totals and metadata rows in the same file.
- Discovering that some “Electricity” total rows do not always reconcile cleanly
  with the sum of underlying fuels, which complicates automated validation.
- Balancing time between engineering depth, dashboard usability and
  presentation preparation within the academy timeframe.

These were addressed through iterative experiments, reading Streamlit documentation,
and using generative AI as a pair-programmer to discuss options, refactor code,
and debug layout issues more quickly.
"""
)

st.divider()


# DATA QUALITY AND LIMITATIONS

st.subheader("Data Quality and Limitations")

st.write(
    """
While the IEA is a premium data source, the raw extract still comes with real-world
complexity and constraints.

Main limitations and observations:

- The file combines raw fuels, calculated totals, electricity system balances and
  free-text flags such as “Data is estimated for this month”.
- Some “Electricity” rows behave more like accounting totals or quality checks
  and do not always equal the simple sum of atomic fuels such as Coal, Oil,
  Natural Gas, Nuclear and Renewables.
- The project focuses on OECD member countries only, which is excellent for
  comparability but excludes many emerging economies.
- Because of the timebox, one reconciliation test around electricity totals
  has been deliberately left as a known issue and a future improvement rather
  than fully solved in this iteration.

In the presentation, this can be positioned as realistic data work:
you rarely get perfect data, but you design your pipeline so that limitations
are explicit, documented and testable.
"""
)

st.divider()


# FUTURE DEVELOPMENT ROADMAP

st.subheader("Future Development Roadmap")

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Data Platform and Engineering")

    st.write(
        """
        - Lift-and-shift the pipeline from local CSV processing into a cloud environment
          with object storage, for example landing data in an S3-style bucket.
        - Replace ad-hoc scripts with a small, versioned Python package exposing clear
          extract, transform and load entry points.
        - Introduce an orchestrator (for example a scheduler or workflow tool)
          to run the pipeline incrementally and on a fixed timetable.
        - Strengthen observability with structured logging, row-level counts and
          more granular validation rules around electricity totals.
        - Evolve the current semantic layer into a documented contract
          so that upstream changes can be detected safely.
        """
    )

with col2:
    st.markdown("##### Analytics, Product and UX")

    st.write(
        """
        - Extend KPIs beyond electricity mix, import dependency and grid losses to include
          indicators such as peak demand coverage or volatility in imports.
        - Add richer comparison modes: for example benchmarking each country against
          OECD averages or peer groups.
        - Prototype alternative front-ends alongside Streamlit using AI-integrated tools
          such as Base44 and Justinmind to explore different user journeys, wireframes
          and stakeholder-specific dashboards.
        - Package the dashboard as a repeatable “energy insights” product that could be
          adapted for non-OECD markets or other energy carriers such as gas or heat.
        """
    )

st.divider()


# PERSONAL LEARNING NEXT STEPS

st.subheader("Personal Learning and Next Steps")

st.write(
    """
Looking ahead, there are several areas where I plan to deepen my skills:

- Formalising pipeline orchestration by evolving a new run_pipeline runner into a
  more production-style job controller, including enhanced logging, failure handling,
  and the foundations of scheduling workflows.
- Consolidating my testing practice by expanding the current pytest suite, especially
  around data reconciliation and edge cases.
- Becoming more fluent with Streamlit layout, theming and component composition so
  that future dashboards can be built faster and styled more cleanly.
- Continuing my broader data engineering learning path, including cloud services,
  orchestration tools and infrastructure-as-code.
- Building a small portfolio of end-to-end projects, using this capstone as the first
  example of how I combine engineering, analytics and stakeholder-focused storytelling.

I am proud to have creatyed a "template" for a solid, working prototype,
and there is a clear roadmap to turn it into a production-grade data product.

My journey for the last 12 weeks has been nothing short of a rollercoaster ride but I know this:
"I BELONG" in technology and data will be the language I speak. 
Thank you to everyone who has made it possible for me to reach this far. 

"""
)