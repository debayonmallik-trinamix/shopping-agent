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

request = youtube.search().list(
    part="snippet",
    q="Sony WH-1000XM5 review",
    type="video",
    maxResults=5
)

response = request.execute()

for item in response["items"]:
    print("Title:", item["snippet"]["title"])
    print("Channel:", item["snippet"]["channelTitle"])
    print("Video ID:", item["id"]["videoId"])
    print("-" * 60)