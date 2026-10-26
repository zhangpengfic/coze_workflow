"""宝宝小短剧视频生成节点"""
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk.video import VideoGenerationClient, TextContent, ImageURLContent, ImageURL

from graphs.state import VideoInput, VideoOutput
from utils.file.file import File


def baby_video_node(
    state: VideoInput,
    config: RunnableConfig,
    runtime: Runtime[Context],
) -> VideoOutput:
    """
    title: 宝宝小短剧视频生成
    desc: 以宝宝照片为首帧，根据分镜脚本生成一段宝宝小短剧视频
    integrations: 视频生成
    """
    ctx = runtime.context
    client = VideoGenerationClient(ctx=ctx)

    video_url, _resp, _last = client.video_generation(
        content_items=[
            TextContent(text=state.video_script),
            ImageURLContent(
                image_url=ImageURL(url=state.baby_photo.url),
                role="first_frame",
            ),
        ],
        model="doubao-seedance-2-0-260128",
        resolution="720p",
        ratio="9:16",
        duration=6,
        watermark=False,
        generate_audio=True,
    )
    if not video_url:
        raise Exception("宝宝小短剧视频生成失败")

    return VideoOutput(baby_video=File(url=video_url, file_type="video"))