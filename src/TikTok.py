from dotenv import dotenv_values

config = dotenv_values(".env")

from TikTokApi import TikTokApi
import asyncio
import os

ms_token = config["ms_token"]
# os.environ.get("ms_token", None) # get your own ms_token from your cookies on tiktok.com
print(ms_token)


async def trending_videos():
    print("start")
    async with TikTokApi() as api:
        print("about to")
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        print("awaiting", api.trending.videos(count=30))
        async for video in api.trending.videos(count=30):
            print(video)
            print(video.as_dict)

async def user_example():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        user = api.user('giorgiameloni_ufficiale')
        user_data = await user.info()
        print(user_data)

        # async for video in user.videos(count=30):
        #     print(video)
        #     print(video.as_dict)


if __name__ == "__main__":
    asyncio.run(user_example())
