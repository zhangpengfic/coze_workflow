"""哈利波特魔法主题艺术照生成节点"""
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import ImageGenerationClient

from graphs.state import ThemeImageInput, HarryOutput
from utils.file.file import File


def harry_image_node(
    state: ThemeImageInput,
    config: RunnableConfig,
    runtime: Runtime[Context],
) -> HarryOutput:
    """
    title: 哈利波特魔法主题艺术照
    desc: 将宝宝装扮成哈利波特魔法师的高清4K艺术照
    integrations: 图片生成
    """
    ctx = runtime.context
    theme = ("将照片中的宝宝装扮成一名小哈利波特魔法师，身穿霍格沃茨魔法袍、头戴小魔杖、"
             "戴着圆框眼镜，背景为魔法学院古堡、漂浮的蜡烛与闪耀的魔法光芒，"
             "奇幻魔法风格，高清4K艺术照，保持宝宝面部特征一致。")
    prompt = f"{state.baby_description}。{theme}" if state.baby_description else theme

    client = ImageGenerationClient(ctx=ctx)
    response = client.generate(
        prompt=prompt,
        image=state.baby_photo.url,
        size="4K",
        watermark=False,
    )
    if not response.success or not response.image_urls:
        raise Exception(f"哈利波特主题图片生成失败: {response.error_messages}")

    return HarryOutput(harry_image=File(url=response.image_urls[0], file_type="image"))