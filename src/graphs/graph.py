"""宝宝照片创意影像生成器 主图编排"""
from langgraph.graph import StateGraph, END

from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput,
)
from graphs.nodes.baby_analyze_node import baby_analyze_node
from graphs.nodes.mario_image_node import mario_image_node
from graphs.nodes.pisa_image_node import pisa_image_node
from graphs.nodes.safari_image_node import safari_image_node
from graphs.nodes.harry_image_node import harry_image_node
from graphs.nodes.mcdonald_image_node import mcdonald_image_node
from graphs.nodes.baby_video_node import baby_video_node
from graphs.nodes.music_node import music_node
from graphs.nodes.photo_wall_node import photo_wall_node
from graphs.nodes.aggregate_node import aggregate_node

builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("baby_analyze", baby_analyze_node, metadata={"type": "agent", "llm_cfg": "config/baby_analyze_llm_cfg.json"})
builder.add_node("mario_image", mario_image_node)
builder.add_node("pisa_image", pisa_image_node)
builder.add_node("safari_image", safari_image_node)
builder.add_node("harry_image", harry_image_node)
builder.add_node("mcdonald_image", mcdonald_image_node)
builder.add_node("baby_video", baby_video_node)
builder.add_node("music", music_node)
builder.add_node("photo_wall", photo_wall_node)
builder.add_node("aggregate", aggregate_node)

# 设置入口点
builder.set_entry_point("baby_analyze")

# 图像理解后，并行开启5路主题生成 + 视频 + 音乐，共7路
builder.add_edge("baby_analyze", "mario_image")
builder.add_edge("baby_analyze", "pisa_image")
builder.add_edge("baby_analyze", "safari_image")
builder.add_edge("baby_analyze", "harry_image")
builder.add_edge("baby_analyze", "mcdonald_image")
builder.add_edge("baby_analyze", "baby_video")
builder.add_edge("baby_analyze", "music")

# 7路并行分支统一汇聚到照片墙（单一汇聚点），照片墙从全局状态取5张艺术照拼版
builder.add_edge(
    ["mario_image", "pisa_image", "safari_image", "harry_image", "mcdonald_image", "baby_video", "music"],
    "photo_wall",
)

builder.add_edge("photo_wall", "aggregate")

builder.add_edge("aggregate", END)

main_graph = builder.compile()