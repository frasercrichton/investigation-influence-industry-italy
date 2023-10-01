from dotenv import dotenv_values

config = dotenv_values(".env")

from TikTokApi import TikTokApi
import asyncio
import os
import pandas as pd
import logging
import yt_dlp
from yt_dlp.utils import ExtractorError, DownloadError

ms_token = config["ms_token"]


# warnings.filterwarnings("ignore", message="Glyph (.*) missing from current font")
# sns.set_theme(style="darkgrid")

logger = logging.getLogger(__name__)

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

videos_df = pd.DataFrame()

async def get_user_data(user_name, video_count=0):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        user = api.user(user_name)
        user_data = await user.info()
        print(user_data)
        df = pd.DataFrame.from_dict(user_data)
        df.to_csv('./data/source/user-2023-09-22.json')
        
        if (video_count != 0):
            print('getting videos')
        
        # df = pd.DataFrame.from_dict(data)
        # print(df)
        # df.to_json('./data/source/video-2023-09-14.json')

        likes = api.user(username=user_name).liked()
        likes_df = pd.DataFrame.from_dict(likes)
        print(likes_df)
        likes_df.to_json('./data/source/likes.json')
     
if __name__ == "__main__":
    user_name = 'giorgiameloni_ufficiale'
    
    # , video_count=400
    asyncio.run(get_user_data(user_name=user_name))
    # asyncio.run(get_hashtag_videos(name='meloni'))
    # asyncio.run(get_hashtag_videos(name='Glastonbury'))
    # asyncio.run(user_example())

