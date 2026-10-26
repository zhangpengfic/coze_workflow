"""麦当劳主题艺术照生成节点"""
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import ImageGenerationClient

from graphs.state import ThemeImageInput, McdonaldOutput
from utils.file.file import File


def mcdonald_image_node(
    state: ThemeImageInput,
    config: RunnableConfig,
    runtime: Runtime[Context],
) -> McdonaldOutput:
    """
    title: 麦当劳主题艺术照
    desc: 将宝宝生成在麦当劳欢乐餐厅场景中的高清4K艺术照
    integrations: 图片生成
    """
    ctx = runtime.context
    theme = ("将照片中的宝宝置于麦当劳欢乐餐厅场景，背景是麦当劳标志性金色拱门、"
             "汉堡、薯条与可乐元素，宝宝开心地吃着薯条，色彩鲜艳Q萌可爱，"
             "高清4K艺术照，保持宝宝面部特征一致。")
    prompt = f"{state.baby_description}。{theme}" if state.baby_description else theme

    client = ImageGenerationClient(ctx=ctx)
    response = client.generate(
        prompt=prompt,
        image=state.baby_photo.url,
        size="4K",
        watermark=False,
    )
    if not response.success or not response.image_urls:
        raise Exception(f"麦当劳主题图片生成失败: {response.error_messages}")

    return McdonaldOutput(mcdonald_image=File(url=response.image_urls[0], file_type="image"))