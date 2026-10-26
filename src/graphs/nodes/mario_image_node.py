"""马里奥主题艺术照生成节点"""
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import ImageGenerationClient

from graphs.state import ThemeImageInput, MarioOutput
from utils.file.file import File


def mario_image_node(
    state: ThemeImageInput,
    config: RunnableConfig,
    runtime: Runtime[Context],
) -> MarioOutput:
    """
    title: 马里奥主题艺术照
    desc: 将宝宝生成在超级马里奥游戏世界中的高清4K艺术照
    integrations: 图片生成
    """
    ctx = runtime.context
    theme = ("将照片中的宝宝置身于超级马里奥游戏世界，宝宝身穿马里奥标志性红色工装与红色帽子，"
             "背景是蘑菇王国城堡、问号砖块、金币与彩旗，画面明亮欢快，游戏插画风格，"
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
        raise Exception(f"马里奥主题图片生成失败: {response.error_messages}")

    return MarioOutput(mario_image=File(url=response.image_urls[0], file_type="image"))