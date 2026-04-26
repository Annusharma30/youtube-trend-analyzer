import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from googleapiclient.discovery import build
import os

st.set_page_config(page_title="YouTube Trend Analyzer", page_icon="🎬", layout="wide")
st.title("🎬 YouTube Trending Video Analyzer - India")
st.markdown("Analyzing trending YouTube videos using YouTube Data API + Sentiment Analysis")

# ── Load API Key ──
api_key = st.secrets.get("YOUTUBE_API_KEY", os.getenv("YOUTUBE_API_KEY"))

if not api_key:
    st.error("❌ YouTube API key not found!")
    st.stop()

# ── Fetch Live Data ──
@st.cache_data
def get_trending_videos():
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode="IN",
        maxResults=50
    )
    response = request.execute()
    videos = []
    for item in response["items"]:
        videos.append({
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "category_id": item["snippet"]["categoryId"],
            "published_at": item["snippet"]["publishedAt"],
            "views": item["statistics"].get("viewCount", 0),
            "likes": item["statistics"].get("likeCount", 0),
            "comments": item["statistics"].get("commentCount", 0),
        })
    return pd.DataFrame(videos)

with st.spinner("Fetching trending videos from YouTube..."):
    df = get_trending_videos()

# Convert types
df["views"] = pd.to_numeric(df["views"])
df["likes"] = pd.to_numeric(df["likes"])
df["comments"] = pd.to_numeric(df["comments"])
df["published_at"] = pd.to_datetime(df["published_at"])
df["engagement_rate"] = (df["likes"] + df["comments"]) / df["views"] * 100
df["publish_hour"] = df["published_at"].dt.hour

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

# ── Chart 1 ──
st.markdown("## 📊 Most Trending Categories")
fig1, ax1 = plt.subplots(figsize=(10, 4))
df["category_id"].value_counts().plot(kind="bar", color="skyblue", ax=ax1)
ax1.set_xlabel("Category ID")
ax1.set_ylabel("Number of Videos")
st.pyplot(fig1)

# ── Chart 2 ──
st.markdown("## ⏰ Best Hour to Post")
fig2, ax2 = plt.subplots(figsize=(10, 4))
df["publish_hour"].value_counts().sort_index().plot(kind="bar", color="orange", ax=ax2)
ax2.set_xlabel("Hour of Day")
ax2.set_ylabel("Number of Videos")
st.pyplot(fig2)

# ── Chart 3 ──
st.markdown("## 👀 Views vs Engagement Rate")
fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.scatterplot(data=df, x="views", y="engagement_rate", ax=ax3)
st.pyplot(fig3)

# ── Chart 4 ──
st.markdown("## 🏆 Top 10 Trending Channels")
fig4, ax4 = plt.subplots(figsize=(10, 4))
df["channel"].value_counts().head(10).plot(kind="barh", color="green", ax=ax4)
st.pyplot(fig4)

st.success("✅ Dashboard loaded successfully!")