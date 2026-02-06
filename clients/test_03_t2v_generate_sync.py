import os
import argparse
from skyreels import SkyreelsClient, TaskStatus

# 3. Text2Video Sync Generate (Polling)
# This test uses the internal polling mechanism to wait for the final result.

def main():
    parser = argparse.ArgumentParser(description="Text2Video Sync Generate (Polling) Test")
    parser.add_argument("--api-key", type=str, default=os.getenv("SKYREELS_API_KEY"), help="API Key")
    parser.add_argument("--base-url", type=str, default=os.getenv("BASE_URL", "https://apis.skyreels.ai"), help="Base URL")
    parser.add_argument("--prompt", type=str, default="Snowy mountains", help="Video prompt")
    parser.add_argument("--duration", type=int, default=5, help="Video duration (1-8)")
    parser.add_argument("--aspect-ratio", type=str, choices=["16:9", "4:3", "1:1", "9:16", "3:4"], default="16:9", help="Aspect ratio")
    parser.add_argument("--interval", type=float, default=5.0, help="Polling interval in seconds")
    parser.add_argument("--mode", type=str, choices=["std", "pro"], default="std", help="Generation mode (std or pro)")
    parser.add_argument("--sound", action="store_true", help="Enable sound generation")
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("Error: API Key is required. Set SKYREELS_API_KEY env var or use --api-key")
        return

    client = SkyreelsClient(api_key=args.api_key, base_url=args.base_url, polling_interval=args.interval)
    try:
        print(f"Generating text2video (sync polling) with prompt: {args.prompt} (mode: {args.mode}, sound: {args.sound})... This may take a few minutes.")
        task = client.generate_text2video(
            prompt=args.prompt, 
            duration=args.duration,
            aspect_ratio=args.aspect_ratio,
            mode=args.mode,
            sound=args.sound
        )
        print(f"Final Status: {task.status}")
        
        if task.status == TaskStatus.SUCCESS:
            print(f"Video URL: {task.data.video_url}")
        else:
            print(f"Generation failed or timed out: {task.msg}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
