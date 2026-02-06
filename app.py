import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="🌍",
    layout="wide"
)

sns.set_style("whitegrid")

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("world_happiness_combined.csv")

df = load_data()

# -----------------------------
# Title & description
# -----------------------------
st.title("🌍 World Happiness Dashboard (2015–2019)")
st.markdown(
    "This interactive dashboard explores global happiness trends and the key factors "
    "that influence well-being across countries and years."
)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.markdown("## 🎛 Dashboard Controls")
st.sidebar.markdown("Use the slider to explore different years.")

year = st.sidebar.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    int(df["Year"].max())
)

filtered_df = df[df["Year"] == year]

# -----------------------------
# KPI Metrics
# -----------------------------
st.markdown("## 🌟 Key Indicators")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    label="Average Happiness Score",
    value=round(filtered_df["Happiness Score"].mean(), 2)
)

kpi2.metric(
    label="Happiest Country",
    value=filtered_df.sort_values(
        "Happiness Score", ascending=False
    ).iloc[0]["Country"]
)

kpi3.metric(
    label="Countries Analyzed",
    value=filtered_df["Country"].nunique()
)

st.markdown("---")

# -----------------------------
# Global happiness over time
# -----------------------------
st.markdown("## 📈 Global Happiness Trend")

avg_happiness = df.groupby("Year")["Happiness Score"].mean()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(avg_happiness.index, avg_happiness.values, marker="o", color="#2E86C1")
ax.set_xlabel("Year")
ax.set_ylabel("Average Happiness Score")
st.pyplot(fig)

st.markdown("---")

# -----------------------------
# Top 10 + Distribution (side by side)
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"## 🏆 Top 10 Happiest Countries ({year})")
    top10 = (
        filtered_df
        .sort_values("Happiness Score", ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(top10["Country"], top10["Happiness Score"], color="#28B463")
    ax.invert_yaxis()
    ax.set_xlabel("Happiness Score")
    st.pyplot(fig)

with col2:
    st.markdown("## 📊 Happiness Score Distribution")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(filtered_df["Happiness Score"], bins=20, color="#F5B041")
    ax.set_xlabel("Happiness Score")
    ax.set_ylabel("Number of Countries")
    st.pyplot(fig)

st.markdown("---")

# -----------------------------
# GDP vs Happiness
# -----------------------------
st.markdown("## 💰 GDP per Capita vs Happiness")
st.caption("Each point represents a country for the selected year.")

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=filtered_df,
    x="GDP per capita",
    y="Happiness Score",
    color="#2E86C1",
    ax=ax
)
ax.set_xlabel("GDP per Capita")
ax.set_ylabel("Happiness Score")
st.pyplot(fig)

st.markdown("---")

# -----------------------------
# Correlation Heatmap
# -----------------------------
st.markdown("## 🔗 Correlation Between Happiness Factors")

corr_vars = filtered_df[
    [
        "Happiness Score",
        "GDP per capita",
        "Social support",
        "Healthy life expectancy",
        "Freedom",
        "Perceptions of corruption"
    ]
]

fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(
    corr_vars.corr(),
    annot=True,
    cmap="coolwarm",
    ax=ax
)
st.pyplot(fig)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "ℹ️ **How to use this dashboard:** "
    "Adjust the year using the slider to explore how happiness levels and "
    "contributing factors change over time."
)

st.markdown(
    "**Data Source:** World Happiness Report (2015–2019)"
)
