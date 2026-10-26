"""结果汇总输出节点"""
from typing import List, Optional

from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context

from graphs.state import AggregateInput, AggregateOutput
from utils.file.file import File


def aggregate_node(
    state: AggregateInput,
    config: RunnableConfig,
    runtime: Runtime[Context],
) -> AggregateOutput:
    """
    title: 结果汇总输出
    desc: 汇总5张主题艺术照、照片墙、短视频与背景音乐作为最终交付结果
    """
    art_photos: List[File] = []
    required: List[Optional[File]] = [
        state.mario_image,
        state.pisa_image,
        state.safari_image,
        state.harry_image,
        state.mcdonald_image,
    ]
    for item in required:
        if item is None:
            raise Exception("结果汇总缺少主题艺术照：部分图片生成未完成")
        art_photos.append(item)

    if state.photo_wall is None or state.baby_video is None or state.background_music is None:
        raise Exception("结果汇总缺少照片墙或视频或背景音乐")

    return AggregateOutput(
        art_photos=art_photos,
        photo_wall=state.photo_wall,
        baby_video=state.baby_video,
        background_music=state.background_music,
    )