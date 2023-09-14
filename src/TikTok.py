from dotenv import dotenv_values

config = dotenv_values(".env")

from TikTokApi import TikTokApi
import asyncio
import os
import pandas as pd
import logging

ms_token = config["ms_token"]

async def get_hashtag_videos(name=None, id=None):
    async with TikTokApi(logging_level=logging.DEBUG) as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        tag = api.hashtag(name=name, id=id)

        hashtag_data = await tag.info()
        print(hashtag_data)
        print(tag)
        async for video in tag.videos(count=30):
            print(video)
            print(video.as_dict)
            df = pd.DataFrame.from_dict(video.as_dict)
            df.to_csv('./hashtag.csv')

async def trending_videos():
    print("start")
    async with TikTokApi() as api:
        print("about to")
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        print("awaiting", api.trending.videos(count=30))
        async for video in api.trending.videos(count=30):
            print(video)
            print(video.as_dict)

videos_df = pd.DataFrame()

async def user_example(name):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        user = api.user(name)
        user_data = await user.info()
        print(user_data)
        df = pd.DataFrame.from_dict(user_data)
        df.to_csv('./user.csv')
        
        data = []
        async for video in user.videos(count=200):
            data.append(video.as_dict)
        
        df = pd.DataFrame.from_dict(data)
        print(df)
        df.to_json('./source/video.json')
       
if __name__ == "__main__":
    asyncio.run(user_example(name='giorgiameloni_ufficiale'))
    

    # asyncio.run(get_hashtag_videos(name='meloni'))
    # asyncio.run(get_hashtag_videos(name='Glastonbury'))
    # asyncio.run(user_example())

