# Skyreels Python SDK

Python SDK for [Skyreels API](https://apis.skyreels.ai).

## Installation

```bash
pip install skyreels-sdk
```

## Usage

### Initialization

You can provide the API key via the constructor or the `SKYREELS_API_KEY` environment variable.
The base URL can be provided via the constructor or the `BASE_URL` environment variable, defaulting to `https://apis.skyreels.ai`.

```python
from skyreels import SkyreelsClient

# Method 1: Pass via constructor
client = SkyreelsClient(api_key="your_api_key", base_url="https://apis.skyreels.ai")

# Method 2: Environment variables
# export SKYREELS_API_KEY=your_api_key
# export BASE_URL=https://apis.skyreels.ai
client = SkyreelsClient()
```

### 1. Manual Task Management (Submit & Query)

This mode gives you full control over the task lifecycle. You submit a task, get a `task_id`, and query the status later.

#### Synchronous

```python
# Text to Video
response = client.submit_text2video(prompt="A beautiful sunset", duration=5)
task = client.get_text2video_task(response.task_id)

# Image to Video
response = client.submit_image2video(prompt="Move water", image_url="https://...")
task = client.get_image2video_task(response.task_id)

if task.status == "success":
    print(f"Video URL: {task.data.video_url}")
```

#### Asynchronous

```python
async def main():
    async with SkyreelsClient() as client:
        # Text to Video
        resp = await client.asubmit_text2video(prompt="A beautiful sunset")
        task = await client.aget_text2video_task(resp.task_id)
        
        # Image to Video
        resp = await client.asubmit_image2video(prompt="Move water", image_url="https://...")
        task = await client.aget_image2video_task(resp.task_id)
```

### 2. Automatic Polling (One-Step Generation)

This mode is simpler for scripts. The SDK handles polling internally and returns only when the task is finished (success or failed).

#### Synchronous

```python
# Text to Video
task = client.generate_text2video(prompt="A beautiful sunset")

# Image to Video
task = client.generate_image2video(prompt="Move water", image_url="https://...")

if task.status == "success":
    print(f"Video URL: {task.data.video_url}")
```

#### Asynchronous

```python
async def main():
    async with SkyreelsClient() as client:
        # Text to Video
        task = await client.agenerate_text2video(prompt="A beautiful sunset")
        
        # Image to Video
        task = await client.agenerate_image2video(prompt="Move water", image_url="https://...")
```

## Error Handling

The SDK raises specific exceptions based on the API error codes:

- `InvalidAPIKeyError` (401)
- `ParameterError` (422)
- `ServiceBusyError` (429)
- `InsufficientCreditsError` (480)
- `QuotaExceededError` (481)
- `InternalError` (500)
- `SecurityPolicyError` (503)

```python
from skyreels import SkyreelsClient, InsufficientCreditsError

try:
    client.generate_text2video(prompt="...")
except InsufficientCreditsError:
    print("Please recharge your credits.")
except Exception as e:
    print(f"An error occurred: {e}")
```
