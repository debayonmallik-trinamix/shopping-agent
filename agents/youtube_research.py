import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

# Video we want to research
video_id = "6CsJZxfZsL0"

# -------------------------
# Get video information
# -------------------------

response = youtube.videos().list(
    part="snippet,statistics",
    id=video_id
).execute()

video = response["items"][0]

snippet = video["snippet"]
statistics = video["statistics"]

print("\nVIDEO INFORMATION")
print("=" * 60)

print("Title:", snippet["title"])
print("Channel:", snippet["channelTitle"])
print("Published:", snippet["publishedAt"])

print("Views:", statistics.get("viewCount"))
print("Likes:", statistics.get("likeCount"))
print("Comments:", statistics.get("commentCount"))

# -------------------------
# Get comments
# -------------------------

comments_response = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=20,
    textFormat="plainText"
).execute()

print("\nCOMMENTS")
print("=" * 60)

for item in comments_response["items"]:

    comment = item["snippet"]["topLevelComment"]["snippet"]

    author = comment["authorDisplayName"]
    text = comment["textDisplay"]
    likes = comment["likeCount"]

    print(f"\n{author} ({likes} likes)")
    print(text)