from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")

if not api_key:
    raise ValueError("❌ API key not found! Check your .env file.")

youtube = build("youtube", "v3", developerKey=api_key)

# ✅ FUNCTION 1 - Fetch trending videos
def get_trending_videos(region_code="IN", max_results=50):
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()
    
    videos = []
    for item in response["items"]:
        videos.append({
            "video_id": item["id"],              # ← ADDED THIS
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "category_id": item["snippet"]["categoryId"],
            "published_at": item["snippet"]["publishedAt"],
            "views": item["statistics"].get("viewCount", 0),
            "likes": item["statistics"].get("likeCount", 0),
            "comments": item["statistics"].get("commentCount", 0),
            "description": item["snippet"]["description"]
        })
    return pd.DataFrame(videos)

# ✅ FUNCTION 2 - Fetch comments
def get_comments(video_id, max_results=30):
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results
        )
        response = request.execute()
        comments = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    for item in response["items"]]
        return comments
    except Exception as e:
        print(f"⚠️ Could not fetch comments for {video_id}: {e}")
        return []

# ✅ RUN - Fetch trending videos
print("Fetching trending videos...")
df = get_trending_videos()
df.to_csv("trending_videos.csv", index=False)
print(f"✅ Saved {len(df)} videos to trending_videos.csv!")

# ✅ RUN - Fetch comments for top 10 videos
print("\nFetching comments for top 10 videos...")
all_comments = []
for video_id in df["video_id"].head(10):
    comments = get_comments(video_id)
    for comment in comments:
        all_comments.append({
            "video_id": video_id,
            "comment": comment
        })
    print(f"✅ Fetched {len(comments)} comments for video {video_id}")

comments_df = pd.DataFrame(all_comments)
comments_df.to_csv("comments.csv", index=False)
print(f"\n✅ Saved {len(comments_df)} comments to comments.csv!")