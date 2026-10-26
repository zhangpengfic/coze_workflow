"""比萨斜塔主题艺术照生成节点"""
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import ImageGenerationClient

from graphs.state import ThemeImageInput, PisaOutput
from utils.file.file import File


def pisa_image_node(
    state: ThemeImageInput,
    config: RunnableConfig,
    runtime: Runtime[Context],
) -> PisaOutput:
    """
    title: 比萨斜塔主题艺术照
    desc: 将宝宝生成在意大利比萨斜塔前打卡的旅游风高清4K艺术照
    integrations: 图片生成
    """
    ctx = runtime.context
    theme = ("将照片中的宝宝置于意大利比萨斜塔前打卡，宝宝穿着轻便可爱的旅行装，"
             "倾斜的比萨斜塔作为背景，蓝天白云，旅游纪念照风格，"
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
        raise Exception(f"比萨斜塔主题图片生成失败: {response.error_messages}")

    return PisaOutput(pisa_image=File(url=response.image_urls[0], file_type="image"))