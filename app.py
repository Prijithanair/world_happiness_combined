import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page setup
st.set_page_config(page_title="World Happiness Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("world_happiness_combined.csv")

df = load_data()

# Title
st.title("🌍 World Happiness Dashboard (2015–2019)")
st.markdown("Interactive exploration of global happiness trends and key factors.")

# Sidebar filters
st.sidebar.header("Filters")
year = st.sidebar.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    int(df["Year"].max())
)

filtered_df = df[df["Year"] == year]

# ===============================
# 1. Global happiness over time
# ===============================
st.subheader("📈 Global Happiness Over Time")

avg_happiness = df.groupby("Year")["Happiness Score"].mean()

fig, ax = plt.subplots()
ax.plot(avg_happiness.index, avg_happiness.values, marker="o")
ax.set_xlabel("Year")
ax.set_ylabel("Average Happiness Score")
st.pyplot(fig)

# ===============================
# 2. Top 10 happiest countries
# ===============================
st.subheader(f"🏆 Top 10 Happiest Countries ({year})")

top10 = (
    filtered_df
    .sort_values("Happiness Score", ascending=False)
    .head(10)
)

fig, ax = plt.subplots()
ax.barh(top10["Country"], top10["Happiness Score"])
ax.invert_yaxis()
ax.set_xlabel("Happiness Score")
st.pyplot(fig)

# ===============================
# 3. GDP vs Happiness
# ===============================
st.subheader("💰 GDP per Capita vs Happiness")

fig, ax = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x="GDP per capita",
    y="Happiness Score",
    ax=ax
)
ax.set_xlabel("GDP per Capita")
ax.set_ylabel("Happiness Score")
st.pyplot(fig)

# ===============================
# 4. Happiness Distribution
# ===============================
st.subheader("📊 Distribution of Happiness Scores")

fig, ax = plt.subplots()
ax.hist(filtered_df["Happiness Score"], bins=20)
ax.set_xlabel("Happiness Score")
ax.set_ylabel("Number of Countries")
st.pyplot(fig)

# ===============================
# 5. Correlation Heatmap
# ===============================
st.subheader("🔗 Correlation Between Happiness Factors")

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

fig, ax = plt.subplots()
sns.heatmap(corr_vars.corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("**Data Source:** World Happiness Report (2015–2019)")
