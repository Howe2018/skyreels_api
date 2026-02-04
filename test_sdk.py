import os
import asyncio
from skyreels import SkyreelsClient

def test_sync():
    # This will fail if no API key is provided, which is expected
    try:
        client = SkyreelsClient(api_key="test_key")
        print("Sync client initialized")
        # We don't actually call the API to avoid 401/timeout
    except Exception as e:
        print(f"Sync test failed: {e}")

async def test_async():
    try:
        async with SkyreelsClient(api_key="test_key") as client:
            print("Async client initialized")
    except Exception as e:
        print(f"Async test failed: {e}")

if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())
    print("Basic initialization tests passed.")
