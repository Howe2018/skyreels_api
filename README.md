# Skyreels Python SDK

This library provides a simple and efficient way to integrate advanced AI video generation into your Python projects.

## Key Features
- **Text-to-Video (T2V)**: Create videos from text prompts, with or without audio.
- **Image-to-Video (I2V)**: Create video from an image and a text prompt, with or without audio.
- **Sync & Async Support**: Full support for both synchronous and asynchronous (`asyncio`) programming models.
- **Automatic Polling**: One-line methods to submit and wait for final video results.
- **1080P Support**: High-definition video generation via `pro` mode.
---

## Installation

### From Source
```bash
git clone https://github.com/Howe2018/skyreels_api.git
cd skyreels_api
pip install .
```

## Quick Start

### 1. Initialization
Set your API key and optionally the base URL via environment variables:
```bash
export SKYREELS_API_KEY="your_api_key"
```

### 2. Simple Video Generation (Automatic Polling)

#### 2.1 text2video without audio

```python
from skyreels import SkyreelsClient

client = SkyreelsClient()
task = client.generate_text2video(
    prompt="***",
    duration=5,
    mode="pro",
    sound=False,
    max_wait_time=600,
)
if task.status == "success":
    print(f"Video ready: {task.data.video_url}")
else:
    print(task)
```

#### 2.2 text2video with audio

```python
from skyreels import SkyreelsClient

client = SkyreelsClient()
task = client.generate_text2video(
    prompt="***",
    duration=5,
    mode="pro",
    sound=True,
    max_wait_time=600,
)
if task.status == "success":
    print(f"Video ready: {task.data.video_url}")
else:
    print(task)
```

#### 2.3 image2video without audio
```python
from skyreels import SkyreelsClient

client = SkyreelsClient()
task = client.generate_image2video(
    prompt="***",
    image_url="", # Must be a public image URL
    duration=5,
    mode="pro",
    sound=False,
    max_wait_time=600,
)
if task.status == "success":
    print(f"Video ready: {task.data.video_url}")
else:
    print(task)
```

#### 2.4 image2video with audio
```python
from skyreels import SkyreelsClient

client = SkyreelsClient()
task = client.generate_image2video(
    prompt="***",
    image_url="", # Must be a public image URL
    duration=5,
    mode="pro",
    sound=True,
    max_wait_time=600,
)
if task.status == "success":
    print(f"Video ready: {task.data.video_url}")
else:
    print(task)
```

---

## Documentation

For a full list of all parameters, **manual task management (submit/query)**, and detailed model schemas, please see our:

👉 **[Comprehensive API Reference & Guide](API_REFERENCE.md)**

## Error Handling

The SDK raises specific exceptions based on API error codes. All custom exceptions inherit from `SkyreelsError`.

| Code | Exception | Description |
| :--- | :--- | :--- |
| 401 | `InvalidAPIKeyError` | Invalid or missing API key. |
| 422 | `ParameterError` | Invalid parameters (e.g., duration out of range). |
| 429 | `ServiceBusyError` | Server is busy, retry later. |
| 480 | `InsufficientCreditsError` | Insufficient account credits. |
| 481 | `QuotaExceededError` | QPS/Concurrency limit reached. |
| 500 | `InternalError` | Internal server error. |
| 503 | `SecurityPolicyError` | Content blocked by safety policy. |

```python
from skyreels import SkyreelsClient, InsufficientCreditsError

client = SkyreelsClient()
try:
    client.generate_text2video(prompt="...")
except InsufficientCreditsError:
    print("Please top up your account.")
except Exception as e:
    print(f"Error: {e}")
```

## License
MIT
