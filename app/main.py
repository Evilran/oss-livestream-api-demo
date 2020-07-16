#!/usr/bin/env python3
# coding=utf-8

import time
from fastapi import Depends, FastAPI, HTTPException, status
from oss2 import *
from oss2.models import *

HOST = "[HOST]"
ACCESS_ID = "[ACCESS_ID]"
ACCESS_KEY = "[ACCESS_KEY]"
BUCKET_NAME = "[BUCKET_NAME]"
CHANNEL_NAME = "[CHANNEL_NAME]"

app = FastAPI(
    title="OSS Livestream",
    description="OSS Livestream Demo API",
    version="1.0",
    redoc_url=None,
)


@app.get("/")
def index():
    return {"OSS LIvestream": "Demo"}

@app.post("/livestream/create")
async def create_livestream_channel(playlist_name: str):
    try:
        auth = Auth(ACCESS_ID, ACCESS_KEY)
        bucket = Bucket(auth, HOST, BUCKET_NAME)
        channel_cfg = LiveChannelInfo(target=LiveChannelInfoTarget())
        channel = bucket.create_live_channel(CHANNEL_NAME, channel_cfg)
        publish_url = channel.publish_url
        play_url = channel.play_url
        signed_publish_url = bucket.sign_rtmp_url(
            CHANNEL_NAME, playlist_name + ".m3u8", 3600)
        return {"play_url": channel.play_url, "signed_publish_url": signed_publish_url}
    except:
        raise HTTPException(
            status_code=500, detail="livestream channel create failed")


@app.post("/livestream/delete")
async def delete_livestream_channel(playlist_name: str):
    auth = Auth(ACCESS_ID, ACCESS_KEY)
    bucket = Bucket(auth, HOST, BUCKET_NAME)
    deleted = False
    for info in LiveChannelIterator(bucket, prefix=CHANNEL_NAME):
        if info.name == CHANNEL_NAME:
            bucket.delete_live_channel(info.name)
            deleted = True
    end_time = int(time.time())
    start_time = end_time - 7200 # combine all ts files during two hours
    try:
        bucket.post_vod_playlist(
                CHANNEL_NAME,
                playlist_name + ".m3u8",
                start_time = start_time,
                end_time = end_time)
    except:
       raise HTTPException(
            status_code=500, detail="livestream channel delete failed")

    if deleted:
        return {"live_channel": info.name, "status": "success"}
    else:
        raise HTTPException(
            status_code=500, detail="livestream channel delete failed")

