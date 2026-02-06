import os
import asyncio
import argparse
from skyreels import SkyreelsClient, TaskStatus

# 2. Text2Video Async Submit/Query
# This test submits a task and performs manual async polling until completion.

async def main():
    parser = argparse.ArgumentParser(description="Text2Video Async Submit/Query Test")
    parser.add_argument("--api-key", type=str, default=os.getenv("SKYREELS_API_KEY"), help="API Key")
    parser.add_argument("--base-url", type=str, default=os.getenv("BASE_URL", "https://infer.skyreels.ai"), help="Base URL")
    parser.add_argument("--prompt", type=str, default="A cute cat", help="Video prompt")
    parser.add_argument("--duration", type=int, default=5, help="Video duration (1-8)")
    parser.add_argument("--aspect-ratio", type=str, choices=["16:9", "4:3", "1:1", "9:16", "3:4"], default="16:9", help="Aspect ratio")
    parser.add_argument("--mode", type=str, choices=["std", "pro"], default="std", help="Generation mode (std or pro)")
    parser.add_argument("--sound", action="store_true", help="Enable sound generation")
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("Error: API Key is required. Set SKYREELS_API_KEY env var or use --api-key")
        return

    async with SkyreelsClient(api_key=args.api_key, base_url=args.base_url) as client:
        print(f"Submitting text2video task (async) with prompt: {args.prompt} (mode: {args.mode}, sound: {args.sound})")
        resp = await client.asubmit_text2video(
            prompt=args.prompt, 
            duration=args.duration,
            aspect_ratio=args.aspect_ratio,
            mode=args.mode,
            sound=args.sound
        )
        print(f"Submitted! Task ID: {resp.task_id}")
        
        # Manual polling loop until success or failed
        print("Polling task status...")
        while True:
            task = await client.aget_text2video_task(resp.task_id)
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
