from transformers import pipeline
import pandas as pd

# Load comments
df = pd.read_csv("comments.csv")
print(f"✅ Loaded {len(df)} comments!")

# Load sentiment analysis model
print("Loading sentiment model... (first time may take a few minutes)")
sentiment = pipeline("sentiment-analysis")

# Analyze sentiment for each comment
print("Analyzing sentiments...")
results = []
for comment in df["comment"]:
    try:
        result = sentiment(comment[:512])[0]  # limit to 512 characters
        results.append({
            "comment": comment,
            "sentiment": result["label"],
            "score": result["score"]
        })
    except Exception as e:
        print(f"⚠️ Skipped a comment: {e}")

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv("sentiment_results.csv", index=False)
print("✅ Sentiment analysis complete!")

# Summary
print("\n📊 Sentiment Summary:")
print(results_df["sentiment"].value_counts())