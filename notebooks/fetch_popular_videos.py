#!/usr/bin/env python
# coding: utf-8

# In[1]:


#ライブラリをimport
import os
import datetime

import requests
import json

#envからAPI_KEYを取得
API_KEY = os.getenv("YOUTUBE_API_KEY")

#日本で人気の動画50個のデータを取得
def fetch_popular_videos():
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": "JP",
        "maxResults": 50,
        "key": API_KEY
    }
    res = requests.get(url, params=params)
    data = res.json()
    timestamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d_%H%M%S")
    os.makedirs("data/raw/popular_videos", exist_ok=True)
    path = f"data/raw/popular_videos/popular_videos_{timestamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
if __name__ == "__main__":
    fetch_popular_videos()
