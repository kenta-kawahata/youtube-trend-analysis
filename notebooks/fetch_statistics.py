#!/usr/bin/env python
# coding: utf-8

# In[12]:


#ライブラリをimport
import os
import datetime
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
    return list(ids)

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
    return list(channel_ids)

def list_split(ex_list, n):
    for i in range(0, len(ex_list), n):
        yield ex_list[i:i+n]

#取得したidから動画の統計データを取得
def fetch_video_statistics():
    video_ids = get_ids()
    url = "https://www.googleapis.com/youtube/v3/videos"
    results=[]
    for video_id in list_split(video_ids, 50):
        params = {
            "part": "statistics",
            "id":video_id,
            "key": API_KEY
        }
        res = requests.get(url, params=params)
        data = res.json()
        results.extend(data.get("items",[]))
    timestamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d_%H%M%S")
    os.makedirs("data/raw/videos_statistics", exist_ok=True)
    path = f"data/raw/videos_statistics/video_statistics_{timestamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f)

#取得したchannel_idからチャンネルの統計データを取得
def fetch_channel_statistics():
    channel_ids = get_channel_ids()
    url = "https://www.googleapis.com/youtube/v3/channels"
    results=[]
    for channel_id in list_split(channel_ids, 50):
        params = {
            "part": "snippet,statistics",
            "id": channel_id,
            "key": API_KEY
        }
        res = requests.get(url, params=params)
        data = res.json()
        results.extend(data.get("items",[]))
    timestamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d_%H%M%S")
    os.makedirs("data/raw/channels_statistics", exist_ok=True)
    path = f"data/raw/channels_statistics/channel_statistics_{timestamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f)

if __name__ == "__main__":
    fetch_video_statistics()
    fetch_channel_statistics()
