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

    # async with TikTokApi() as api:
    #     await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)

    #     await api.video(id='7041997751718137094').bytes()

    #     # Saving The Video
    #     with open('saved_video.mp4', 'wb') as output:
    #         output.write(video_bytes)

    #     async for related_video in video.related_videos(count=10):
    #         print(related_video)
    #         print(related_video.as_dict)

async def user_example():    
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(
            url="https://www.tiktok.com/@davidteathercodes/video/7074717081563942186"
        )

    
        video_bytes = api.video(id='7041997751718137094').bytes()
        print(video_bytes)
        # Saving The Video
        with open('saved_video.mp4', 'wb') as output:
            output.write(video_bytes)

        # async for related_video in video.related_videos(count=10):
        #     print(related_video)
        #     print(related_video.as_dict)

        # video_info = await video.info()  # is HTML request, so avoid using this too much
        # print(video_info)


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

async def user_example(name, video_count):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        user = api.user(name)
        user_data = await user.info()
        print(user_data)
        df = pd.DataFrame.from_dict(user_data)
        df.to_csv('./data/source/user-2023-09-14.csv')
        
        data = []
        async for video in user.videos(count=video_count):
            data.append(video.as_dict)
        
        df = pd.DataFrame.from_dict(data)
        print(df)
        df.to_json('./data/source/video-2023-09-14.json')
        df.to_json('./data/source/video-2023-09-14.csv')

if __name__ == "__main__":
    # bucket = s3_resource.Bucket(f'doc-example-bucket-{uuid.uuid4()}')

    conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
    for key in conn.list_objects(Bucket='frasercrichton-com-audio-transcription')['Contents']:
        print(key['Key'])
    # hello_s3()
    # start_job(job_name, media_uri, media_format, language_code, transcribe_client, vocabulary_name=None)
    
    # asyncio.run(user_example(name='giorgiameloni_ufficiale', video_count=400))
    # asyncio.run(download_video(id='x345', output_name='x.mp4'))

    

    # asyncio.run(get_hashtag_videos(name='meloni'))
    # asyncio.run(get_hashtag_videos(name='Glastonbury'))
    # asyncio.run(user_example())

