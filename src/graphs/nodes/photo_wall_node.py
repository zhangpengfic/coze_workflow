"""艺术照照片墙拼版节点"""
import io
import os
from typing import List, Optional, Tuple

import requests
from PIL import Image
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk.s3 import S3SyncStorage

from graphs.state import PhotoWallInput, PhotoWallOutput
from utils.file.file import File


def _download_image(url: str, cell: int) -> Image.Image:
    """下载图片并统一缩放为正方形"""
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    im: Image.Image = Image.open(io.BytesIO(resp.content)).convert("RGB")
    return im.resize((cell, cell))


def photo_wall_node(
    state: PhotoWallInput,
    config: RunnableConfig,
    runtime: Runtime[Context],
) -> PhotoWallOutput:
    """
    title: 艺术照照片墙拼版
    desc: 将5张主题艺术照拼版为一张照片墙并上传对象存储
    """
    ctx = runtime.context
    image_urls: List[Optional[str]] = [
        state.mario_image.url if state.mario_image else None,
        state.pisa_image.url if state.pisa_image else None,
        state.safari_image.url if state.safari_image else None,
        state.harry_image.url if state.harry_image else None,
        state.mcdonald_image.url if state.mcdonald_image else None,
    ]
    urls: List[str] = []
    for u in image_urls:
        if u:
            urls.append(u)
            continue
        raise Exception("照片墙拼版缺少主题艺术照：部分图片生成未完成")

    cell: int = 600
    gap: int = 20
    cols: int = 3
    rows: int = 2
    width: int = cols * cell + (cols + 1) * gap
    height: int = rows * cell + (rows + 1) * gap

    canvas: Image.Image = Image.new("RGB", (width, height), (245, 245, 245))
    imgs: List[Image.Image] = [_download_image(url, cell) for url in urls]

    # 布局：第一行3张，第二行2张居中
    positions: List[Tuple[int, int]] = []
    for i in range(3):
        positions.append((gap + i * (cell + gap), gap))
    bottom_start: int = (width - (2 * cell + gap)) // 2
    positions.append((bottom_start, cell + 2 * gap))
    positions.append((bottom_start + cell + gap, cell + 2 * gap))

    for (x, y), im in zip(positions, imgs):
        canvas.paste(im, (x, y))

    buf = io.BytesIO()
    canvas.save(buf, format="JPEG", quality=90)
    buf.seek(0)
    file_bytes: bytes = buf.read()

    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    key: str = storage.upload_file(
        file_content=file_bytes,
        file_name="photo_wall.jpg",
        content_type="image/jpeg",
    )
    photo_wall_url: str = storage.generate_presigned_url(
        key=key,
        expire_time=2592000,
    )
    return PhotoWallOutput(photo_wall=File(url=photo_wall_url, file_type="image"))