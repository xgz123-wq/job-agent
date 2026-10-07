"""通用 AI 服务封装

基于 DeepSeek（OpenAI 兼容协议）实现，提供与业务无关的对话/补全能力。
- chat()        非流式对话补全，返回完整文本
- chat_stream() 流式对话补全，逐块产出文本（用于 SSE）
- complete()    结构化 JSON 输出补全，自动剥离 markdown 代码块并解析为 dict

业务侧（面试、简历解析等）请勿在此文件硬编码 prompt，
应通过参数传入 system_prompt / user_prompt / schema_hint。
"""
import json
import logging
from typing import AsyncGenerator, Dict, List, Optional

from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

# DeepSeek 使用 OpenAI 兼容 API
client = AsyncOpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url=settings.DEEPSEEK_BASE_URL,
)


class AIService:
    """通用 AI 对话服务（DeepSeek / OpenAI 兼容）"""

    # ------------------------------------------------------------------ #
    # 基础调用
    # ------------------------------------------------------------------ #
    @staticmethod
    async def chat(
        system_prompt: str,
        user_prompt: str,
        *,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """非流式对话补全，返回完整响应文本。

        Args:
            system_prompt: 系统提示词，定义模型角色与输出约束。
            user_prompt:    用户输入文本。
            model:          可选模型名，缺省使用 settings.DEEPSEEK_MODEL。
            temperature:    采样温度。
            max_tokens:     最大输出 token 数。
            history:        可选历史对话消息，按顺序插入到 system 和当前 user 之间。
        """
        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_prompt})

        try:
            response = await client.chat.completions.create(
                model=model or settings.DEEPSEEK_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"DeepSeek API 调用失败: {e}")
            raise

    @staticmethod
    async def chat_stream(
        system_prompt: str,
        user_prompt: str,
        *,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> AsyncGenerator[str, None]:
        """流式对话补全，逐块产出文本，适用于 SSE 推流场景。"""
        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_prompt})

        try:
            stream = await client.chat.completions.create(
                model=model or settings.DEEPSEEK_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"DeepSeek 流式 API 调用失败: {e}")
            raise

    # ------------------------------------------------------------------ #
    # 结构化 JSON 输出
    # ------------------------------------------------------------------ #
    @staticmethod
    async def complete(
        system_prompt: str,
        user_prompt: str,
        *,
        schema_hint: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2000,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> dict:
        """要求模型输出 JSON 并解析为 dict。

        在 system_prompt 末尾追加 schema_hint（若提供），强制模型返回纯 JSON
        （不允许 markdown 代码块包裹），并自动剥离可能的 ```json 围栏。
        """
        full_system = system_prompt
        if schema_hint:
            full_system = f"{system_prompt}\n\n必须返回纯JSON格式（不要markdown代码块），结构如下：\n{schema_hint}"

        text = await AIService.chat(
            full_system,
            user_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            history=history,
        )
        return AIService._extract_json(text)

    @staticmethod
    def _extract_json(text: str) -> dict:
        """从 AI 响应中提取 JSON，兼容 markdown 代码块包裹的情况。"""
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            lines = lines[1:]  # 移除开头的 ```json 行
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        return json.loads(text)


ai_service = AIService()
