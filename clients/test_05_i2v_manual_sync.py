import os
import argparse
import time
from skyreels import SkyreelsClient, TaskStatus

# 5. Image2Video Sync Submit/Query
# This test submits an image-to-video task and performs manual polling until completion.

def main():
    parser = argparse.ArgumentParser(description="Image2Video Sync Submit/Query Test")
    parser.add_argument("--api-key", type=str, default=os.getenv("SKYREELS_API_KEY"), help="API Key")
    parser.add_argument("--base-url", type=str, default=os.getenv("BASE_URL", "https://apis.skyreels.ai"), help="Base URL")
    parser.add_argument("--prompt", type=str, default="talking in a club", help="Video prompt")
    parser.add_argument("--image-url", type=str, default="https://skyreels-api.oss-accelerate.aliyuncs.com/examples/subject_reference/0_1.png", help="First frame image URL")
    parser.add_argument("--duration", type=int, default=5, help="Video duration (1-8)")
    parser.add_argument("--mode", type=str, choices=["std", "pro"], default="std", help="Generation mode (std or pro)")
    parser.add_argument("--sound", action="store_true", help="Enable sound generation")
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("Error: API Key is required. Set SKYREELS_API_KEY env var or use --api-key")
        return

    client = SkyreelsClient(api_key=args.api_key, base_url=args.base_url)
    try:
        print(f"Submitting image2video task (sync) with prompt: {args.prompt} (mode: {args.mode}, sound: {args.sound}) and image: {args.image_url}")
        resp = client.submit_image2video(
            prompt=args.prompt, 
            image_url=args.image_url,
            duration=args.duration,
            mode=args.mode,
            sound=args.sound
        )
        print(f"Submitted! Task ID: {resp.task_id}")
        
        # Manual polling loop until success or failed
        print("Polling task status...")
        while True:
            task = client.get_image2video_task(resp.task_id)
            print(f"Current Status: {task.status}")
            
            if task.status in [TaskStatus.SUCCESS, TaskStatus.FAILED]:
                if task.status == TaskStatus.SUCCESS:
                    print(f"Video URL: {task.data.video_url}")
                else:
                    print(f"Task failed: {task.msg}")
                break
            
            time.sleep(5)  # Wait for 5 seconds before next query
    finally:
        client.close()

if __name__ == "__main__":
    main()
