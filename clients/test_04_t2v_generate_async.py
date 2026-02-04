import os
import asyncio
import argparse
from skyreels import SkyreelsClient, TaskStatus

# 4. Text2Video Async Generate (Polling)
# This test uses the internal async polling mechanism to wait for the final result.

async def main():
    parser = argparse.ArgumentParser(description="Text2Video Async Generate (Polling) Test")
    parser.add_argument("--api-key", type=str, default=os.getenv("SKYREELS_API_KEY"), help="API Key")
    parser.add_argument("--base-url", type=str, default=os.getenv("BASE_URL", "https://apis.skyreels.ai"), help="Base URL")
    parser.add_argument("--prompt", type=str, default="Ocean waves", help="Video prompt")
    parser.add_argument("--duration", type=int, default=5, help="Video duration (1-8)")
    parser.add_argument("--aspect-ratio", type=str, choices=["16:9", "4:3", "1:1", "9:16", "3:4"], default="16:9", help="Aspect ratio")
    parser.add_argument("--interval", type=float, default=5.0, help="Polling interval in seconds")
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("Error: API Key is required. Set SKYREELS_API_KEY env var or use --api-key")
        return

    async with SkyreelsClient(api_key=args.api_key, base_url=args.base_url, polling_interval=args.interval) as client:
        print(f"Generating text2video (async polling) with prompt: {args.prompt}... This may take a few minutes.")
        task = await client.agenerate_text2video(
            prompt=args.prompt, 
            duration=args.duration,
            aspect_ratio=args.aspect_ratio
        )
        print(f"Final Status: {task.status}")
        
        if task.status == TaskStatus.SUCCESS:
            print(f"Video URL: {task.data.video_url}")
        else:
            print(f"Generation failed or timed out: {task.msg}")

if __name__ == "__main__":
    asyncio.run(main())
