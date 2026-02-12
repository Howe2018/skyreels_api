import os
import asyncio
import argparse
from skyreels import SkyreelsClient, TaskStatus

# 8. Image2Video Async Generate (Polling)
# This test uses the internal async polling mechanism for image-to-video generation.

async def main():
    parser = argparse.ArgumentParser(description="Image2Video Async Generate (Polling) Test")
    parser.add_argument("--api-key", type=str, default=os.getenv("SKYREELS_API_KEY"), help="API Key")
    parser.add_argument("--base-url", type=str, default=os.getenv("BASE_URL", "https://infer.skyreels.ai"), help="Base URL")
    parser.add_argument("--prompt", type=str, default="Forest movement", help="Video prompt")
    parser.add_argument("--image-url", type=str, default="https://picsum.photos/1280/720", help="First frame image URL")
    parser.add_argument("--duration", type=int, default=8, help="Video duration (1-8)")
    parser.add_argument("--interval", type=float, default=5.0, help="Polling interval in seconds")
    parser.add_argument("--mode", type=str, choices=["std", "pro"], default="std", help="Generation mode (std or pro)")
    parser.add_argument("--sound", action="store_true", help="Enable sound generation")
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("Error: API Key is required. Set SKYREELS_API_KEY env var or use --api-key")
        return

    async with SkyreelsClient(api_key=args.api_key, base_url=args.base_url, polling_interval=args.interval) as client:
        print(f"Generating image2video (async polling) with prompt: {args.prompt} (mode: {args.mode}, sound: {args.sound}) and image: {args.image_url}... This may take a few minutes.")
        task = await client.agenerate_image2video(
            prompt=args.prompt, 
            image_url=args.image_url,
            duration=args.duration,
            mode=args.mode,
            sound=args.sound
        )
        print(f"Final Status: {task.status}")
        
        if task.status == TaskStatus.SUCCESS:
            print(f"Video URL: {task.data.video_url}")
        else:
            print(f"Generation failed or timed out: {task.msg}")

if __name__ == "__main__":
    asyncio.run(main())
