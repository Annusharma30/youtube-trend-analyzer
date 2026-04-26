import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="YouTube Trend Analyzer", page_icon="🎬", layout="wide")

st.title("🎬 YouTube Trending Video Analyzer - India")
st.markdown("Analyzing trending YouTube videos using YouTube Data API + Sentiment Analysis")

# ── Load Data ──
df = pd.read_csv("trending_videos.csv")
df["views"] = pd.to_numeric(df["views"])
df["likes"] = pd.to_numeric(df["likes"])
df["comments"] = pd.to_numeric(df["comments"])
df["published_at"] = pd.to_datetime(df["published_at"])
df["engagement_rate"] = (df["likes"] + df["comments"]) / df["views"] * 100
df["publish_hour"] = df["published_at"].dt.hour

sentiment_df = pd.read_csv("sentiment_results.csv")

# ── Metrics Row ──
st.markdown("## 📊 Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Videos", len(df))
col2.metric("Avg Views", f"{df['views'].mean():,.0f}")
col3.metric("Avg Likes", f"{df['likes'].mean():,.0f}")
col4.metric("Avg Engagement", f"{df['engagement_rate'].mean():.2f}%")

# ── Raw Data ──
st.markdown("## 📋 Trending Videos Data")
st.dataframe(df[["title", "channel", "views", "likes", "comments", "engagement_rate"]])

# ── Chart 1 - Categories ──
st.markdown("## 📊 Most Trending Categories")
fig1, ax1 = plt.subplots(figsize=(10, 4))
df["category_id"].value_counts().plot(kind="bar", color="skyblue", ax=ax1)
ax1.set_xlabel("Category ID")
ax1.set_ylabel("Number of Videos")
st.pyplot(fig1)

# ── Chart 2 - Best Hour ──
st.markdown("## ⏰ Best Hour to Post")
fig2, ax2 = plt.subplots(figsize=(10, 4))
df["publish_hour"].value_counts().sort_index().plot(kind="bar", color="orange", ax=ax2)
ax2.set_xlabel("Hour of Day")
ax2.set_ylabel("Number of Videos")
st.pyplot(fig2)

# ── Chart 3 - Views vs Engagement ──
st.markdown("## 👀 Views vs Engagement Rate")
fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.scatterplot(data=df, x="views", y="engagement_rate", ax=ax3)
st.pyplot(fig3)

# ── Chart 4 - Top Channels ──
st.markdown("## 🏆 Top 10 Trending Channels")
fig4, ax4 = plt.subplots(figsize=(10, 4))
df["channel"].value_counts().head(10).plot(kind="barh", color="green", ax=ax4)
st.pyplot(fig4)

# ── Sentiment ──
st.markdown("## 💬 Comment Sentiment Analysis")
col1, col2 = st.columns(2)
with col1:
    st.dataframe(sentiment_df.head(20))
with col2:
    fig5, ax5 = plt.subplots()
    sentiment_df["sentiment"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax5)
    ax5.set_ylabel("")
    st.pyplot(fig5)

st.success("✅ Dashboard loaded successfully!")