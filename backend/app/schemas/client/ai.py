from typing import List, Optional
from pydantic import Field
from ..base import BaseSchema


class ChatMessage(BaseSchema):
    """历史对话消息"""
    role: str = Field(..., description="消息角色：system / user / assistant")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseSchema):
    """通用对话请求"""
    system_prompt: str = Field(..., description="系统提示词，定义模型角色与输出约束")
    user_prompt: str = Field(..., description="用户输入文本")
    model: Optional[str] = Field(None, description="可选模型名，缺省使用 settings.DEEPSEEK_MODEL")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="采样温度")
    max_tokens: int = Field(2000, ge=1, le=8192, description="最大输出 token 数")
    history: Optional[List[ChatMessage]] = Field(None, description="可选历史对话消息")


class ChatCompleteRequest(ChatRequest):
    """结构化 JSON 对话请求"""
    schema_hint: Optional[str] = Field(
        None,
        description="可选 JSON schema 提示，强制模型返回纯 JSON",
    )
