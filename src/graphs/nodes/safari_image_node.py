"""Safari主题艺术照生成节点"""
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import ImageGenerationClient

from graphs.state import ThemeImageInput, SafariOutput
from utils.file.file import File


def safari_image_node(
    state: ThemeImageInput,
    config: RunnableConfig,
    runtime: Runtime[Context],
) -> SafariOutput:
    """
    title: Safari主题艺术照
    desc: 将宝宝生成在非洲草原Safari探险场景中的高清4K艺术照
    integrations: 图片生成
    """
    ctx = runtime.context
    theme = ("将照片中的宝宝置于非洲草原Safari探险场景，周围有长颈鹿、大象等野生动物，"
             "宝宝坐在安全的小吉普车中或由向导抱着，夕阳金辉下的草原，"
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
        raise Exception(f"Safari主题图片生成失败: {response.error_messages}")

    return SafariOutput(safari_image=File(url=response.image_urls[0], file_type="image"))