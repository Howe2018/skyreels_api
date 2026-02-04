import os
import asyncio
import argparse
from skyreels import SkyreelsClient, TaskStatus

# 6. Image2Video Async Submit/Query
# This test submits an image-to-video task and performs manual async polling until completion.

async def main():
    parser = argparse.ArgumentParser(description="Image2Video Async Submit/Query Test")
    parser.add_argument("--api-key", type=str, default=os.getenv("SKYREELS_API_KEY"), help="API Key")
    parser.add_argument("--base-url", type=str, default=os.getenv("BASE_URL", "https://apis.skyreels.ai"), help="Base URL")
    parser.add_argument("--prompt", type=str, default="Make clouds move", help="Video prompt")
    parser.add_argument("--image-url", type=str, default="https://picsum.photos/1280/720", help="First frame image URL")
    parser.add_argument("--duration", type=int, default=5, help="Video duration (1-8)")
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("Error: API Key is required. Set SKYREELS_API_KEY env var or use --api-key")
        return

    async with SkyreelsClient(api_key=args.api_key, base_url=args.base_url) as client:
        print(f"Submitting image2video task (async) with prompt: {args.prompt} and image: {args.image_url}")
        resp = await client.asubmit_image2video(
            prompt=args.prompt, 
            image_url=args.image_url,
            duration=args.duration
        )
        print(f"Submitted! Task ID: {resp.task_id}")
        
        # Manual polling loop until success or failed
        print("Polling task status...")
        while True:
            task = await client.aget_image2video_task(resp.task_id)
            print(f"Current Status: {task.status}")
            
            if task.status in [TaskStatus.SUCCESS, TaskStatus.FAILED]:
                if task.status == TaskStatus.SUCCESS:
                    print(f"Video URL: {task.data.video_url}")
                else:
                    print(f"Task failed: {task.msg}")
                break
            
            await asyncio.sleep(5)  # Wait for 5 seconds before next query

if __name__ == "__main__":
    asyncio.run(main())
