import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("trending_videos.csv")

# Convert types
df["views"] = pd.to_numeric(df["views"])
df["likes"] = pd.to_numeric(df["likes"])
df["comments"] = pd.to_numeric(df["comments"])
df["published_at"] = pd.to_datetime(df["published_at"])

# Engagement rate
df["engagement_rate"] = (df["likes"] + df["comments"]) / df["views"] * 100

# Hour of publish
df["publish_hour"] = df["published_at"].dt.hour

print("✅ Data cleaned successfully!")
print(df.head())

# 📊 Chart 1 - Which categories trend the most?
plt.figure(figsize=(10,5))
df["category_id"].value_counts().plot(kind="bar", color="skyblue")
plt.title("Most Trending Categories")
plt.xlabel("Category ID")
plt.ylabel("Number of Videos")
plt.tight_layout()
plt.savefig("chart1_categories.png")
plt.show()
print("✅ Chart 1 saved!")

# 📊 Chart 2 - Best time to post?
plt.figure(figsize=(10,5))
df["publish_hour"].value_counts().sort_index().plot(kind="bar", color="orange")
plt.title("Best Hour to Post")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Videos")
plt.tight_layout()
plt.savefig("chart2_best_hour.png")
plt.show()
print("✅ Chart 2 saved!")

# 📊 Chart 3 - Views vs Engagement?
plt.figure(figsize=(10,5))
sns.scatterplot(data=df, x="views", y="engagement_rate")
plt.title("Views vs Engagement Rate")
plt.xlabel("Views")
plt.ylabel("Engagement Rate (%)")
plt.tight_layout()
plt.savefig("chart3_views_engagement.png")
plt.show()
print("✅ Chart 3 saved!")

# 📊 Chart 4 - Top 10 channels
plt.figure(figsize=(10,5))
df["channel"].value_counts().head(10).plot(kind="barh", color="green")
plt.title("Top 10 Trending Channels")
plt.xlabel("Number of Videos")
plt.tight_layout()
plt.savefig("chart4_top_channels.png")
plt.show()
print("✅ Chart 4 saved!")

print("\n🎉 All charts generated successfully!")