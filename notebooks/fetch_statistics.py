#!/usr/bin/env python
# coding: utf-8

# In[2]:


#ライブラリをimport
import os
from datetime import datetime
from glob import glob

import requests
import json

#envからAPI_KEYを取得
API_KEY = os.getenv("YOUTUBE_API_KEY")

#jsonファイルからidを取得する関数
def get_ids():
    files = glob("data/raw/popular_videos/*.json")
    ids=set()
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        items = data.get("items", [])
        for item in items:
            video_id = item.get("id")
            ids.add(video_id)
    return ",".join(list(ids))

#jsonファイルからchannel_idを取得する関数
def get_channel_ids():
    files = glob("data/raw/popular_videos/*.json")
    channel_ids=set()
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        items = data.get("items", [])
        for item in items:
            snippet=item.get("snippet", {})
            channel_id=snippet.get("channelId")
            channel_ids.add(channel_id)
    return ",".join(list(channel_ids))

#取得したidから動画の統計データを取得
def fetch_video_statistics():
    video_ids = get_ids()
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "statistics",
        "id":video_ids,
        "key": API_KEY
    }
    res = requests.get(url, params=params)
    data = res.json()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("data/raw/videos_statistics", exist_ok=True)
    path = f"data/raw/videos_statistics/video_statistics_{timestamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

#取得したchannel_idからチャンネルの統計データを取得
def fetch_channel_statistics():
    channel_ids = get_channel_ids()
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "snippet,statistics",
        "id": channel_ids,
        "key": API_KEY
    }
    res = requests.get(url, params=params)
    data = res.json()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("data/raw/channels_statistics", exist_ok=True)
    path = f"data/raw/channels_statistics/channel_statistics_{timestamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

if __name__ == "__main__":
    fetch_video_statistics()
    fetch_channel_statistics()
