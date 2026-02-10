import os
import time
import asyncio
from typing import Literal, Optional, Union
import httpx
from .models import Text2VideoSubmit, Image2VideoSubmit, SubmitResponse, TaskResponse, TaskStatus
from .exceptions import raise_for_code

class SkyreelsClient:
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        polling_interval: float = 10.0,
        max_wait_time: float = 600.0,  # Default 10 minutes
    ):
        self.api_key = api_key or os.getenv("SKYREELS_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either via constructor or SKYREELS_API_KEY environment variable")
        
        self.base_url = (base_url or os.getenv("BASE_URL") or "https://infer.skyreels.ai").rstrip("/")
        self.timeout = timeout
        self.polling_interval = polling_interval
        self.max_wait_time = max_wait_time
        
        self._sync_client = httpx.Client(base_url=self.base_url, timeout=self.timeout)
        self._async_client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    def _handle_response(self, response: httpx.Response, response_model):
        data = response.json()
        code = data.get("code", response.status_code)
        msg = data.get("msg", "")
        trace_id = data.get("trace_id", "")
        
        raise_for_code(code, msg, trace_id)
        return response_model(**data)

    # Text2Video Sync
    def submit_text2video(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: Literal["16:9", "4:3", "1:1", "9:16", "3:4"] = "16:9",
        sound: bool = False,
        mode: Literal["std", "pro"] = "std"
    ) -> SubmitResponse:
        payload = Text2VideoSubmit(
            prompt=prompt,
            duration=duration,
            aspect_ratio=aspect_ratio,
            sound=sound,
            mode=mode,
            api_key=self.api_key
        )
        resp = self._sync_client.post("/api/v1/video/text2video/submit", json=payload.model_dump())
        return self._handle_response(resp, SubmitResponse)

    def get_text2video_task(self, task_id: str) -> TaskResponse:
        resp = self._sync_client.get(f"/api/v1/video/text2video/task/{task_id}")
        return self._handle_response(resp, TaskResponse)

    def generate_text2video(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: Literal["16:9", "4:3", "1:1", "9:16", "3:4"] = "16:9",
        sound: bool = False,
        mode: Literal["std", "pro"] = "std",
        polling_interval: Optional[float] = None,
        max_wait_time: Optional[float] = None
    ) -> TaskResponse:
        submit_resp = self.submit_text2video(
            prompt=prompt, duration=duration, aspect_ratio=aspect_ratio, 
            sound=sound, mode=mode
        )
        
        interval = polling_interval or self.polling_interval
        wait_time = max_wait_time or self.max_wait_time
        max_retries = int(wait_time / interval)
        print(f"task id: {submit_resp.task_id}, max retries: {max_retries}, max wait time: {wait_time}")

        for _ in range(max_retries):
            task_resp = self.get_text2video_task(submit_resp.task_id)
            if task_resp.status in [TaskStatus.SUCCESS, TaskStatus.FAILED]:
                return task_resp
            time.sleep(interval)
        return self.get_text2video_task(submit_resp.task_id)

    # Image2Video Sync
    def submit_image2video(
        self,
        prompt: str,
        image_url: str,
        duration: int = 5,
        sound: bool = False,
        mode: Literal["std", "pro"] = "std"
    ) -> SubmitResponse:
        payload = Image2VideoSubmit(
            prompt=prompt,
            first_frame_image=image_url,
            duration=duration,
            sound=sound,
            mode=mode,
            api_key=self.api_key
        )
        resp = self._sync_client.post("/api/v1/video/image2video/submit", json=payload.model_dump())
        return self._handle_response(resp, SubmitResponse)

    def get_image2video_task(self, task_id: str) -> TaskResponse:
        resp = self._sync_client.get(f"/api/v1/video/image2video/task/{task_id}")
        return self._handle_response(resp, TaskResponse)

    def generate_image2video(
        self,
        prompt: str,
        image_url: str,
        duration: int = 5,
        sound: bool = False,
        mode: Literal["std", "pro"] = "std",
        polling_interval: Optional[float] = None,
        max_wait_time: Optional[float] = None
    ) -> TaskResponse:
        submit_resp = self.submit_image2video(
            prompt=prompt, image_url=image_url, duration=duration, 
            sound=sound, mode=mode
        )
        
        interval = polling_interval or self.polling_interval
        wait_time = max_wait_time or self.max_wait_time
        max_retries = int(wait_time / interval)
        print(f"task id: {submit_resp.task_id}, max retries: {max_retries}, max wait time: {wait_time}")

        for _ in range(max_retries):
            task_resp = self.get_image2video_task(submit_resp.task_id)
            if task_resp.status in [TaskStatus.SUCCESS, TaskStatus.FAILED]:
                return task_resp
            time.sleep(interval)
        return self.get_image2video_task(submit_resp.task_id)

    # Text2Video Async
    async def asubmit_text2video(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: Literal["16:9", "4:3", "1:1", "9:16", "3:4"] = "16:9",
        sound: bool = False,
        mode: Literal["std", "pro"] = "std"
    ) -> SubmitResponse:
        payload = Text2VideoSubmit(
            prompt=prompt,
            duration=duration,
            aspect_ratio=aspect_ratio,
            sound=sound,
            mode=mode,
            api_key=self.api_key
        )
        resp = await self._async_client.post("/api/v1/video/text2video/submit", json=payload.model_dump())
        return self._handle_response(resp, SubmitResponse)

    async def aget_text2video_task(self, task_id: str) -> TaskResponse:
        resp = await self._async_client.get(f"/api/v1/video/text2video/task/{task_id}")
        return self._handle_response(resp, TaskResponse)

    async def agenerate_text2video(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: Literal["16:9", "4:3", "1:1", "9:16", "3:4"] = "16:9",
        sound: bool = False,
        mode: Literal["std", "pro"] = "std",
        polling_interval: Optional[float] = None,
        max_wait_time: Optional[float] = None
    ) -> TaskResponse:
        submit_resp = await self.asubmit_text2video(
            prompt=prompt, duration=duration, aspect_ratio=aspect_ratio, 
            sound=sound, mode=mode
        )
        
        interval = polling_interval or self.polling_interval
        wait_time = max_wait_time or self.max_wait_time
        max_retries = int(wait_time / interval)

        for _ in range(max_retries):
            task_resp = await self.aget_text2video_task(submit_resp.task_id)
            if task_resp.status in [TaskStatus.SUCCESS, TaskStatus.FAILED]:
                return task_resp
            await asyncio.sleep(interval)
        return await self.aget_text2video_task(submit_resp.task_id)

    # Image2Video Async
    async def asubmit_image2video(
        self,
        prompt: str,
        image_url: str,
        duration: int = 5,
        sound: bool = False,
        mode: Literal["std", "pro"] = "std"
    ) -> SubmitResponse:
        payload = Image2VideoSubmit(
            prompt=prompt,
            first_frame_image=image_url,
            duration=duration,
            sound=sound,
            mode=mode,
            api_key=self.api_key
        )
        resp = await self._async_client.post("/api/v1/video/image2video/submit", json=payload.model_dump())
        return self._handle_response(resp, SubmitResponse)

    async def aget_image2video_task(self, task_id: str) -> TaskResponse:
        resp = await self._async_client.get(f"/api/v1/video/image2video/task/{task_id}")
        return self._handle_response(resp, TaskResponse)

    async def agenerate_image2video(
        self,
        prompt: str,
        image_url: str,
        duration: int = 5,
        sound: bool = False,
        mode: Literal["std", "pro"] = "std",
        polling_interval: Optional[float] = None,
        max_wait_time: Optional[float] = None
    ) -> TaskResponse:
        submit_resp = await self.asubmit_image2video(
            prompt=prompt, image_url=image_url, duration=duration, 
            sound=sound, mode=mode
        )
        
        interval = polling_interval or self.polling_interval
        wait_time = max_wait_time or self.max_wait_time
        max_retries = int(wait_time / interval)

        for _ in range(max_retries):
            task_resp = await self.aget_image2video_task(submit_resp.task_id)
            if task_resp.status in [TaskStatus.SUCCESS, TaskStatus.FAILED]:
                return task_resp
            await asyncio.sleep(interval)
        return await self.aget_image2video_task(submit_resp.task_id)

    def close(self):
        self._sync_client.close()

    async def aclose(self):
        await self._async_client.aclose()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()
