"""通用 AI 对话路由

参数化 prompt，不绑定任何具体业务（面试/简历等）。
- POST /ai/chat         非流式对话补全
- POST /ai/chat/complete 结构化 JSON 输出补全
- POST /ai/chat/stream   SSE 流式对话补全
"""
import json
import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.response import ApiResponse
from app.schemas.client.ai import ChatRequest, ChatCompleteRequest
from app.services.client.ai_service import ai_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest):
    """非流式对话补全"""
    content = await ai_service.chat(
        system_prompt=req.system_prompt,
        user_prompt=req.user_prompt,
        model=req.model,
        temperature=req.temperature,
        max_tokens=req.max_tokens,
        history=[m.model_dump() for m in req.history] if req.history else None,
    )
    return ApiResponse.success(data={"content": content})


@router.post("/chat/complete")
async def chat_complete(req: ChatCompleteRequest):
    """结构化 JSON 对话补全，自动解析为 dict"""
    data = await ai_service.complete(
        system_prompt=req.system_prompt,
        user_prompt=req.user_prompt,
        schema_hint=req.schema_hint,
        model=req.model,
        temperature=req.temperature,
        max_tokens=req.max_tokens,
        history=[m.model_dump() for m in req.history] if req.history else None,
    )
    return ApiResponse.success(data=data)


@router.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """SSE 流式对话补全

    每个 chunk 以 `data: {"content": "..."}` 形式推送，
    结束时推送 `data: [DONE]`，出错时推送 `data: {"error": "..."}`。
    """

    async def event_source():
        try:
            async for chunk in ai_service.chat_stream(
                system_prompt=req.system_prompt,
                user_prompt=req.user_prompt,
                model=req.model,
                temperature=req.temperature,
                max_tokens=req.max_tokens,
                history=[m.model_dump() for m in req.history] if req.history else None,
            ):
                yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:  # noqa: BLE001
            logger.error(f"AI 流式调用失败: {e}")
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_source(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 nginx 缓冲，保证 SSE 实时推送
        },
    )
