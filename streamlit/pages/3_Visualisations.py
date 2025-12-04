import streamlit as st
import pandas as pd
import plotly.express as px


# PAGE CONFIG

st.set_page_config(
    page_title="Visualisations",
    layout="wide"
)


# GLOBAL THEME STYLES

st.markdown("""
<style>

/* MULTIPAGE SIDEBAR NAV */
div[data-testid="stSidebarNav"] label {
    color: #ffc800 !important;
    font-size: 22px !important;
}

/* GLOBAL FONT */
html, body, [class*="st-"] {
    font-family: Verdana, Arial, sans-serif !important;
    color: #FFFFFF !important;
}

/* BASE FONT */
p, li, span, label, div {
    font-size: 20px !important;
}

/* HEADINGS */
h1 { font-size: 70px !important; color: #ffc800 !important; }
h2 { font-size: 50px !important; color: #ffc800 !important; }
h3 { font-size: 36px !important; color: #00A36C !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #4f5052ff !important;
}
section[data-testid="stSidebar"] label {
    color: #ffc800 !important;
    font-size: 22px !important;
}

/* SELECTED VALUE */
section[data-testid="stSelectbox"] span {
    color: #00A36C !important;
    font-size: 22px !important;
}

/* DROPDOWN PANEL */
div[data-baseweb="popover"],
ul[role="listbox"] {
    background-color: #4f5052ff !important;
}

li[role="option"] {
    background-color: #4f5052ff !important;
}

li[role="option"] span {
    color: #00A36C !important;
    font-size: 22px !important;
}

li[role="option"]:hover {
    background-color: rgba(0,163,108,0.35) !important;
}
li[role="option"]:hover span {
    color: #ffc800 !important;
}

li[aria-selected="true"] {
    background-color: rgba(255,200,0,0.30) !important;
}
li[aria-selected="true"] span {
    color: #ffc800 !important;
}

/* MAIN APP */
.stApp {
    background-color: #191a1dff !important;
}

/* CONTENT PANELS */
div[data-testid="stVerticalBlock"] > div {
    background-color: rgba(255,255,255,0.04);
    border-radius: 14px;
    padding: 1rem;
}

/* BUTTONS */
button {
    background-color: #00A36C !important;
    border-radius: 10px !important;
}

/* METRICS */
[data-testid="stMetricValue"] {
    font-size: 22px !important;
    color: #ffc800 !important;
}

/* EVEN TAB SPACING */
button[data-baseweb="tab"] {
    font-size: 20px !important;
    padding-left: 32px !important;
    padding-right: 32px !important;
}

/* ===== ADD FIX HERE ===== */
/* FIX FOR DROPDOWN SELECTED VALUE VISIBILITY */
div[data-baseweb="select"] > div {
    background-color: #4f5052ff !important;
}

div[data-baseweb="select"] span {
    color: #ffc800 !important;
}
/* ===== END OF FIX ===== */

</style>
""", unsafe_allow_html=True)


# PAGE HEADER

st.markdown("""
<h1 style="text-align:center;">ANALYTICS & VISUALISATIONS</h1>
<h3 style="text-align:center;margin-top:-10px;">OECD Electricity System Insights</h3>
<hr>
""", unsafe_allow_html=True)



# LOAD DATA

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/oecd_energy_fact.csv",
        low_memory=False
    )

df = load_data()


# DATE ENGINEERING

df["date"] = pd.to_datetime(df["Time"], format="%b-%y", errors="coerce")
df["Year"] = df["date"].dt.year


# SIDEBAR FILTERS

st.sidebar.header("Filters")

countries = sorted(df["Country"].dropna().unique())

primary_country = st.sidebar.selectbox(
    "Primary Country",
    countries,
    index=countries.index("Canada") if "Canada" in countries else 0
)

compare_country = st.sidebar.selectbox(
    "Compare With Country",
    ["None"] + countries,
    index=0
)

years = df["Year"].dropna()

year_start, year_end = st.sidebar.slider(
    "Year Range",
    min_value=int(years.min()),
    max_value=int(years.max()),
    value=(2015, int(years.max()))
)


# FILTERING FUNCTIONS

def filter_atomic(country):
    mask = (
        (df["Country"] == country) &
        (df["Year"].between(year_start, year_end))
    )
    out = df[mask]
    return out[out["is_atomic_fuel"]]


def filter_trade(country):
    subset = df[
        (df["Country"] == country) &
        (df["Year"].between(year_start, year_end))
    ]

    imports = subset[subset["Balance"] == "Total Imports"].groupby("Year")["Value"].sum()
    exports = subset[subset["Balance"] == "Total Exports"].groupby("Year")["Value"].sum()
    production = subset[subset["Balance"] == "Net Electricity Production"].groupby("Year")["Value"].sum()

    trade = pd.concat(
        [imports, exports, production],
        axis=1,
        keys=["Imports", "Exports", "Production"]
    ).dropna()

    trade["Net Imports"] = trade["Imports"] - trade["Exports"]

    trade["Bubble Size"] = trade["Net Imports"].abs().clip(lower=1)

    trade["Import Dependency %"] = (
        trade["Net Imports"] /
        (trade["Imports"] + trade["Production"])
    ) * 100

    trade["Country"] = country

    return trade.reset_index()


atomic_main = filter_atomic(primary_country)
trade_frames = [filter_trade(primary_country)]

if compare_country != "None":
    atomic_compare = filter_atomic(compare_country)
    trade_frames.append(filter_trade(compare_country))
else:
    atomic_compare = None

trade_combined = pd.concat(trade_frames)


# TABS

tab1, tab2, tab3, tab4 = st.tabs([
    "ENERGY MIX",
    "RENEWABLE TRENDS",
    "IMPORT DEPENDENCY",
    "GRID LOSSES"
])



# TAB 1 — ENERGY MIX

with tab1:
    st.subheader("Energy Mix by Carbon Group")

    mix = atomic_main.groupby("fuel_group")["Value"].sum().reset_index()

    fig = px.pie(
        mix,
        names="fuel_group",
        values="Value",
        hole=0.35,
        title=f"{primary_country} — Electricity Generation Mix",
        color="fuel_group",
        color_discrete_map={
            "LOW_CARBON": "#00A36C",
            "NUCLEAR": "#ffc800",
            "FOSSIL": "#808B96"
        }
    )

    fig.update_layout(
        title_font_size=34,
        legend=dict(
            orientation="v",
            x=-0.15,
            y=0.5,
            font=dict(size=26)
        )
    )

    st.plotly_chart(fig, width="stretch")



# TAB 2 — RENEWABLE TRENDS

with tab2:
    st.subheader("Renewable Electricity Production Trend")

    def calc_renewables(atomic, name):
        t = atomic[atomic["fuel_group"] == "LOW_CARBON"]
        t = t.groupby("Year")["Value"].sum().reset_index()
        t["Country"] = name
        return t

    frames = [calc_renewables(atomic_main, primary_country)]

    if atomic_compare is not None:
        frames.append(calc_renewables(atomic_compare, compare_country))

    trend = pd.concat(frames)

    fig = px.line(
        trend,
        x="Year",
        y="Value",
        color="Country",
        markers=True,
        title="Renewable Generation Comparison",
        labels={"Value": "GWh"},
        color_discrete_map={
            primary_country: "#00A36C",
            compare_country: "#ffc800" if compare_country != "None" else "#00A36C"
        }
    )

    fig.update_layout(
        title_font_size=30,
        legend=dict(font=dict(size=24))
    )

    st.plotly_chart(fig, width="stretch")



# TAB 3 — IMPORT DEPENDENCY (BUBBLES)

with tab3:
    st.subheader("Electricity Import Dependency Comparison")

    fig = px.scatter(
        trade_combined,
        x="Year",
        y="Import Dependency %",
        size="Bubble Size",
        color="Country",
        labels={
            "Import Dependency %": "% of supply imported"
        },
        title="Import Dependency Comparison",
        color_discrete_map={
            primary_country: "#00A36C",
            compare_country: "#ffc800"
        }
    )

    fig.update_layout(
        title_font_size=30,
        legend=dict(font=dict(size=24))
    )

    st.plotly_chart(fig, width="stretch")



# TAB 4 — GRID LOSSES

with tab4:
    st.subheader("Electricity Grid Loss Percentage")

    losses = df[(df["Country"] == primary_country) & (df["Balance"] == "Distribution Losses")].groupby("Year")["Value"].sum()
    prod = df[(df["Country"] == primary_country) & (df["Balance"] == "Net Electricity Production")].groupby("Year")["Value"].sum()

    grid = pd.concat(
        [losses, prod],
        axis=1,
        keys=["Losses", "Production"]
    ).dropna()

    grid["Grid Loss %"] = (grid["Losses"] / grid["Production"]) * 100

    fig = px.bar(
        grid,
        x=grid.index,
        y="Grid Loss %",
        title=f"{primary_country} — Grid Loss Percentage",
        labels={"x": "Year", "Grid Loss %": "% lost"},
        color_discrete_sequence=["#00A36C"]
    )

    fig.update_layout(
        title_font_size=30,
        legend=dict(font=dict(size=24))
    )

    st.plotly_chart(fig, width="stretch")
