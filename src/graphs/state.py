"""
宝宝照片创意影像生成器 状态定义
全局状态、图出入参、以及各节点的独立出入参
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from utils.file.file import File


class GlobalState(BaseModel):
    """全局过程状态（LangGraph 自动合并各节点输出）"""
    baby_photo: File = Field(..., description="用户上传的宝宝实景照片")
    baby_description: str = Field(default="", description="宝宝统一人物设定描述")
    video_script: str = Field(default="", description="宝宝小短剧分镜脚本")
    music_lyrics: str = Field(default="", description="背景音乐配套歌词文本")
    mario_image: Optional[File] = Field(default=None, description="马里奥主题艺术照")
    pisa_image: Optional[File] = Field(default=None, description="比萨斜塔主题艺术照")
    safari_image: Optional[File] = Field(default=None, description="Safari主题艺术照")
    harry_image: Optional[File] = Field(default=None, description="哈利波特主题艺术照")
    mcdonald_image: Optional[File] = Field(default=None, description="麦当劳主题艺术照")
    photo_wall: Optional[File] = Field(default=None, description="艺术照拼版照片墙")
    baby_video: Optional[File] = Field(default=None, description="宝宝小短剧视频")
    background_music: Optional[File] = Field(default=None, description="背景音乐音频")
    art_photos: List[File] = Field(default=[], description="5张主题艺术照列表")


class GraphInput(BaseModel):
    """工作流的输入"""
    baby_photo: File = Field(..., description="用户上传的宝宝实景照片")


class GraphOutput(BaseModel):
    """工作流的输出"""
    art_photos: List[File] = Field(..., description="5张高清4K宝宝主题艺术照")
    photo_wall: File = Field(..., description="艺术照拼版照片墙")
    baby_video: File = Field(..., description="宝宝小短剧视频")
    background_music: File = Field(..., description="配套背景音乐")


# ---------- 节点出入参 ----------

class AnalyzeInput(BaseModel):
    """宝宝图像理解节点的输入"""
    baby_photo: File = Field(..., description="宝宝实景照片")


class AnalyzeOutput(BaseModel):
    """宝宝图像理解节点的输出"""
    baby_description: str = Field(..., description="宝宝统一人物设定描述")
    video_script: str = Field(..., description="宝宝小短剧分镜脚本")
    music_lyrics: str = Field(..., description="背景音乐配套歌词文本")


class ThemeImageInput(BaseModel):
    """主题艺术照生成节点的共用输入"""
    baby_photo: File = Field(..., description="宝宝实景照片（作为人物参考图）")
    baby_description: str = Field(..., description="宝宝统一人物设定描述")


class MarioOutput(BaseModel):
    """马里奥主题艺术照节点输出"""
    mario_image: File = Field(..., description="马里奥主题艺术照")


class PisaOutput(BaseModel):
    """比萨斜塔主题艺术照节点输出"""
    pisa_image: File = Field(..., description="比萨斜塔主题艺术照")


class SafariOutput(BaseModel):
    """Safari主题艺术照节点输出"""
    safari_image: File = Field(..., description="Safari主题艺术照")


class HarryOutput(BaseModel):
    """哈利波特主题艺术照节点输出"""
    harry_image: File = Field(..., description="哈利波特主题艺术照")


class McdonaldOutput(BaseModel):
    """麦当劳主题艺术照节点输出"""
    mcdonald_image: File = Field(..., description="麦当劳主题艺术照")


class VideoInput(BaseModel):
    """宝宝短视频生成节点的输入"""
    baby_photo: File = Field(..., description="宝宝实景照片（首帧起点）")
    video_script: str = Field(..., description="宝宝小短剧分镜脚本")


class VideoOutput(BaseModel):
    """宝宝短视频生成节点的输出"""
    baby_video: File = Field(..., description="宝宝小短剧视频")


class MusicInput(BaseModel):
    """背景音乐生成节点的输入"""
    music_lyrics: str = Field(..., description="背景音乐配套歌词文本")


class MusicOutput(BaseModel):
    """背景音乐生成节点的输出"""
    background_music: File = Field(..., description="背景音乐音频")


class PhotoWallInput(BaseModel):
    """照片墙拼版节点的输入（并行汇聚节点，字段可能在各自分支完成后才被赋值）"""
    mario_image: Optional[File] = Field(default=None, description="马里奥主题艺术照")
    pisa_image: Optional[File] = Field(default=None, description="比萨斜塔主题艺术照")
    safari_image: Optional[File] = Field(default=None, description="Safari主题艺术照")
    harry_image: Optional[File] = Field(default=None, description="哈利波特主题艺术照")
    mcdonald_image: Optional[File] = Field(default=None, description="麦当劳主题艺术照")


class PhotoWallOutput(BaseModel):
    """照片墙拼版节点的输出"""
    photo_wall: File = Field(..., description="艺术照拼版照片墙")


class AggregateInput(BaseModel):
    """结果汇总输出节点的输入（并行汇聚节点，字段可能在各自分支完成后才被赋值）"""
    mario_image: Optional[File] = Field(default=None, description="马里奥主题艺术照")
    pisa_image: Optional[File] = Field(default=None, description="比萨斜塔主题艺术照")
    safari_image: Optional[File] = Field(default=None, description="Safari主题艺术照")
    harry_image: Optional[File] = Field(default=None, description="哈利波特主题艺术照")
    mcdonald_image: Optional[File] = Field(default=None, description="麦当劳主题艺术照")
    photo_wall: Optional[File] = Field(default=None, description="艺术照拼版照片墙")
    baby_video: Optional[File] = Field(default=None, description="宝宝小短剧视频")
    background_music: Optional[File] = Field(default=None, description="背景音乐音频")


class AggregateOutput(BaseModel):
    """结果汇总输出节点的输出"""
    art_photos: List[File] = Field(..., description="5张主题艺术照列表")
    photo_wall: File = Field(..., description="艺术照拼版照片墙")
    baby_video: File = Field(..., description="宝宝小短剧视频")
    background_music: File = Field(..., description="背景音乐音频")