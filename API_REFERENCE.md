# Skyreels SDK Full API Reference & Guide

Welcome to the Skyreels Python SDK documentation. This guide provides a comprehensive overview of all available interfaces, parameters, and usage patterns for integrating Skyreels AI video generation into your Python applications.

---

## 1. Installation & Initialization

### Installation (From Source)
```bash
git clone https://github.com/skyreels/skyreels_api.git
cd skyreels_api
pip install .
```

### Initialization
The `SkyreelsClient` supports both synchronous and asynchronous operations. You can configure it via the constructor or environment variables.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `api_key` | `str` | `os.getenv("SKYREELS_API_KEY")` | Your Skyreels API Key. |
| `base_url` | `str` | `"https://infer.skyreels.ai"` | The API endpoint. Can be set via `BASE_URL` env var. |
| `timeout` | `float` | `60.0` | HTTP request timeout. |
| `polling_interval` | `float` | `10.0` | Default interval for internal polling methods. |
| `max_wait_time` | `float` | `900.0` | Default timeout (15 mins) for internal polling methods. |
| `mode` | `str` | `"std"` | Default generation mode (`"std"` or `"pro"`), the "std" mode generates 720P output, whereas the "pro" mode provides higher-quality results with 1080P resolution and increased fps.|

---

## 2. Text to Video (T2V)

### 2.1 Key Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `prompt` | `str` | **Required** | Text description for video generation. |
| `duration` | `int` | `5` | Duration of the generated video in seconds. |
| `aspect_ratio` | `str` | `"16:9"` | Aspect ratio of the video. Options: `"16:9"`, `"4:3"`, `"1:1"`, `"9:16"`, `"3:4"`. |
| `sound` | `bool` | `False` | **Important:** Determines whether the output video has audio. |
| `mode` | `str` | `"std"` | **Important:** Generation mode. `"std"` results in 720P, while `"pro"` provides 1080P high-definition. |

### 2.2 One-Step Generation (Automatic Polling)
The `generate_text2video` method handles task submission and internal polling. It blocks (or awaits) until the video is ready or fails.

**Example:**
```python
task = client.generate_text2video(prompt="A futuristic city", mode="pro")
if task.status == "success":
    print(task.data.video_url)
```

### 2.3 Manual Task Management
For more complex workflows, such as batch processing or custom polling logic, use the manual submission and query methods.

#### Submit a Task
- `submit_text2video(...)` (Sync)
- `asubmit_text2video(...)` (Async)

Returns a `SubmitResponse` containing the `task_id`.

#### Query Task Status
- `get_text2video_task(task_id: str)` (Sync)
- `aget_text2video_task(task_id: str)` (Async)

Returns a `TaskResponse`.

**Manual Workflow Example (Sync):**
```python
import time
from skyreels import SkyreelsClient, TaskStatus

client = SkyreelsClient()
# 1. Submit with sound enabled
resp = client.submit_text2video(
    prompt="A beautiful sunset", 
    sound=True
)
task_id = resp.task_id

# 2. Custom Polling Loop
while True:
    task = client.get_text2video_task(task_id)
    print(f"Current status: {task.status}")
    if task.status in [TaskStatus.SUCCESS, TaskStatus.FAILED]:
        break
    time.sleep(10)

if task.status == TaskStatus.SUCCESS:
    print(f"Video URL: {task.data.video_url}")
```

---

## 3. Image to Video (I2V)

### 3.1 Key Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `prompt` | `str` | **Required** | Text description for video generation. |
| `image_url` | `str` | **Required** | URL of the source image|
| `duration` | `int` | `5` | Duration of the generated video in seconds. |
| `sound` | `bool` | `False` | **Important:** Determines whether the output video has audio. |
| `mode` | `str` | `"std"` | **Important:** Generation mode. `"std"` results in 720P, while `"pro"` provides 1080P high-definition. |

### 3.2 One-Step Generation (Automatic Polling)
The `generate_image2video` method handles task submission and internal polling.

**Example:**
```python
task = client.generate_image2video(
    prompt="Make ripples", 
    image_url="https://example.com/lake.jpg"
)
```

### 3.3 Manual Task Management (Non-One-Step)

#### Submit a Task
- `submit_image2video(...)` (Sync)
- `asubmit_image2video(...)` (Async)

#### Query Task Status
- `get_image2video_task(task_id: str)` (Sync)
- `aget_image2video_task(task_id: str)` (Async)

**Manual Workflow Example (Async):**
```python
import asyncio
from skyreels import SkyreelsClient, TaskStatus

async def main():
    async with SkyreelsClient() as client:
        # 1. Submit
        resp = await client.asubmit_image2video(
            prompt="Make clouds move", 
            image_url="https://..."
        )
        task_id = resp.task_id
        
        # 2. Async Polling
        while True:
            task = await client.aget_image2video_task(task_id)
            if task.status in [TaskStatus.SUCCESS, TaskStatus.FAILED]:
                break
            await asyncio.sleep(10)
            
        if task.status == TaskStatus.SUCCESS:
            print(f"Result: {task.data.video_url}")

asyncio.run(main())
```

---

## 4. Models & Response Schema

### SubmitResponse
Returned by all `submit_*` methods.
- `task_id`: String ID used for queries.
- `msg`: Status message.
- `code`: Status code (200 for success).

### TaskResponse
- `task_id`: String ID.
- `status`: `TaskStatus` enum.
- `msg`: Status message.
- `data`: `VideoData` object (only on `SUCCESS`).

### VideoData
- `video_url`: The link to the result.
- `duration`: Video length.
- `resolution`: e.g., "1920x1080".
- `cost_credits`: Credits consumed.

---

## 5. Error Handling & Exceptions

The Skyreels SDK maps API error codes to specific Python exceptions. All custom exceptions inherit from `SkyreelsError`.

### Exception Reference Table

| HTTP/API Code | Exception Class | Description | Recommended Action |
| :--- | :--- | :--- | :--- |
| 401 | `InvalidAPIKeyError` | The provided API key is incorrect or expired. | Check and update your API key. |
| 422 | `ParameterError` | One or more input parameters are invalid. | Review the API docs and check parameter constraints (e.g., duration 1-8). |
| 429 | `ServiceBusyError` | The server is currently under high load. | Retry the request after a short delay. |
| 480 | `InsufficientCreditsError` | Your account balance is too low for this task. | Recharge your account credits. |
| 481 | `QuotaExceededError` | Your Concurrency or QPS limit has been reached. | Reduce request frequency or contact support to increase quota. |
| 500 | `InternalError` | An unexpected error occurred on the server side. | Retry later or contact technical support. |
| 503 | `SecurityPolicyError` | The input prompt or image triggered safety filters. | Modify the input content and try again. |

### Example Usage

```python
from skyreels import SkyreelsClient, SkyreelsError, InsufficientCreditsError

client = SkyreelsClient()

try:
    task = client.generate_text2video(prompt="...")
except InsufficientCreditsError:
    print("Insufficient credits, please recharge.")
except SkyreelsError as e:
    print(f"API Error: {e.message} (Code: {e.code}, Trace ID: {e.trace_id})")
except Exception as e:
    print(f"Unexpected error: {e}")
```
