"""宝宝图像理解Agent节点：分析照片提取人物设定、视频脚本与音乐歌词"""
import json
import os
from typing import List, Dict, Any

from jinja2 import Template
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient

from graphs.state import AnalyzeInput, AnalyzeOutput


def get_text_content(content: Any) -> str:
    """安全提取 LLM content 文本"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        if content and isinstance(content[0], str):
            return " ".join(content)
        parts: List[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
        return " ".join(parts)
    return str(content)


def baby_analyze_node(
    state: AnalyzeInput,
    config: RunnableConfig,
    runtime: Runtime[Context],
) -> AnalyzeOutput:
    """
    title: 宝宝图像理解
    desc: 分析宝宝照片，生成统一人物设定、小短剧分镜脚本与背景音乐歌词
    integrations: 大语言模型
    """
    ctx = runtime.context
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH", ""), config["metadata"]["llm_cfg"])
    with open(cfg_file, "r", encoding="utf-8") as fd:
        _cfg = json.load(fd)

    llm_config: Dict[str, Any] = _cfg.get("config", {})
    sp: str = _cfg.get("sp", "")
    up: str = _cfg.get("up", "")

    model: str = llm_config.get("model", "doubao-seed-2-0-pro-260215")
    temperature: float = float(llm_config.get("temperature", 0.4))
    top_p: float = float(llm_config.get("top_p", 0.8))
    max_completion_tokens: int = int(llm_config.get("max_completion_tokens", 3000))
    thinking: str = llm_config.get("thinking", "disabled")

    up_tpl = Template(up)
    user_prompt: str = up_tpl.render()

    client = LLMClient(ctx=ctx)
    messages = [
        SystemMessage(content=sp),
        HumanMessage(
            content=[
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": {"url": state.baby_photo.url}},
            ]
        ),
    ]

    response = client.invoke(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p,
        max_completion_tokens=max_completion_tokens,
        thinking=thinking,
    )

    text = get_text_content(response.content).strip()
    if not text:
        raise Exception("宝宝图像理解模型未返回有效文本")

    # 提取 JSON 块
    text_l = text.strip()
    if text_l.startswith("```"):
        text_l = text_l.strip("`")
        if text_l.startswith("json"):
            text_l = text_l[4:]
    json_start = text_l.find("{")
    json_end = text_l.rfind("}")
    if json_start == -1 or json_end == -1:
        raise Exception(f"无法从模型输出中解析JSON: {text}")
    parsed: Dict[str, Any] = json.loads(text_l[json_start : json_end + 1])

    return AnalyzeOutput(
        baby_description=str(parsed.get("baby_description", "")).strip(),
        video_script=str(parsed.get("video_script", "")).strip(),
        music_lyrics=str(parsed.get("music_lyrics", "")).strip(),
    )