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
Install the SDK directly from the repository:
```bash
git clone https://github.com/Howe2018/skyreels_api.git
cd skyreels_api
pip install .
```

## Quick Start

### 1. Set Your API Key

The quickest way to get started is by setting your API key as an environment variable:

```bash
export SKYREELS_API_KEY="your_api_key_here"
```

### 2. Simple Video Generation (Automatic Polling)
The `generate_*` methods are high-level helpers that submit a task and automatically poll for the result until completion or until `max_wait_time` is reached.

#### 2.1 Text-to-Video (T2V) without Audio

```python
from skyreels import SkyreelsClient

client = SkyreelsClient()
task = client.generate_text2video(
    prompt="****",
    sound=False,
    max_wait_time=900,    # Max seconds to wait for completion
)

if task.status == "success":
    print(f"Video ready: {task.data.video_url}")
else:
    print(f"Task failed: {task}")
```

#### 2.2 Text-to-Video (T2V) with Audio

```python
from skyreels import SkyreelsClient

client = SkyreelsClient()
task = client.generate_text2video(
    prompt="****",
    sound=True,           # Enable AI-generated synchronized audio
    max_wait_time=900,
)

if task.status == "success":
    print(f"Video ready: {task.data.video_url}")
else:
    print(f"Task failed: {task}")
```

#### 2.3 Image-to-Video (I2V) without Audio
```python
from skyreels import SkyreelsClient

client = SkyreelsClient()
task = client.generate_image2video(
    prompt="****",
    image_url="***", # Must be a public image URL
    sound=False,
    max_wait_time=900,
)

if task.status == "success":
    print(f"Video ready: {task.data.video_url}")
else:
    print(f"Task failed: {task}")
```

#### 2.4 Image-to-Video (I2V) with Audio
```python
from skyreels import SkyreelsClient

client = SkyreelsClient()
task = client.generate_image2video(
    prompt="***",
    image_url="***", # Must be a public image URL
    sound=True,        # Enable AI-generated synchronized audio
    max_wait_time=900,
)

if task.status == "success":
    print(f"Video ready: {task.data.video_url}")
else:
    print(f"Task failed: {task}")
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
