from enum import Enum
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    SUCCESS = "success"
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    SUBMITTED = "submitted"
    UNKNOWN = "unknown"

    def __str__(self):
        return self.value

    @classmethod
    def _missing_(cls, value):
        """处理未知值，返回 UNKNOWN"""
        return cls.UNKNOWN

class TaskStatusCode(int, Enum):
    OK = 200
    FAILED = 500
    REQUEST_ERROR = 422
    # 添加其他可能出现的错误码
    UNAUTHORIZED = 401
    BUSY = 429
    INSUFFICIENT_CREDITS = 480
    QUOTA_EXCEEDED = 481
    SECURITY_POLICY = 503

class BaseRequest(BaseModel):
    api_key: str = Field(..., description="API key")

class Text2VideoSubmit(BaseRequest):
    prompt: str = Field(..., description="prompt")
    duration: int = Field(5, ge=1, le=8, description="Duration of the video")
    aspect_ratio: Literal["16:9", "4:3", "1:1", "9:16", "3:4"] = Field("16:9", description="Aspect ratio of the video")
    sound: bool = Field(False, description="Whether to create sound")
    mode: Literal["std", "pro"] = Field("std", description="mode")

class Image2VideoSubmit(BaseRequest):
    prompt: str = Field(..., description="prompt")
    first_frame_image: str = Field(..., description="first frame image url")
    duration: int = Field(5, ge=1, le=8, description="Duration of the video")
    sound: bool = Field(False, description="Whether to create sound")
    mode: Literal["std", "pro"] = Field("std", description="mode")

class VideoGenerateResponse(BaseModel):
    video_url: str = Field("", description="video url")
    resolution: str = Field("", description="Resolution of the video")
    duration: float = Field(0.0, description="time")
    cost_credits: float = Field(0.0, description="cost credits")

class TaskResponse(BaseModel):
    task_id: str = Field("", description="Task ID")
    msg: str = Field("", description="Message")
    code: TaskStatusCode = Field(TaskStatusCode.OK, description="Status code")
    status: TaskStatus = Field(TaskStatus.UNKNOWN, description="Status")
    data: Optional[VideoGenerateResponse] = Field(None, description="Data")
    trace_id: Optional[str] = Field(None, description="Trace ID")

class SubmitResponse(BaseModel):
    task_id: str = Field("", description="Task ID for subsequent queries")
    msg: str = Field("", description="Message description")
    code: TaskStatusCode = Field(TaskStatusCode.OK, description="Status code")
    status: str = Field("ok", description="Status identifier")
    data: Optional[Any] = Field(None, description="Return data, null on success")
    trace_id: Optional[str] = Field(None, description="Request tracking ID")
