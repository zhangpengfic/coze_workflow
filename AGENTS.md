# 项目概述
- **名称**: 宝宝照片创意影像生成器（Baby Creative Studio）
- **功能**: 上传一张普通宝宝实景照片，自动生成5张主题艺术照、1张照片墙拼版、1段宝宝小短剧视频与1首配套背景音乐

## 工作流输入输出
- **输入**: `baby_photo`（宝宝实景照片 File）
- **输出**: `art_photos`（5张4K主题艺术照 List[File]）、`photo_wall`（照片墙 File）、`baby_video`（短视频 File）、`background_music`（背景音乐 File）

## 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| baby_analyze | `nodes/baby_analyze_node.py` | agent | 分析宝宝照片，产出人物设定/视频脚本/音乐歌词 | - | `config/baby_analyze_llm_cfg.json` |
| mario_image | `nodes/mario_image_node.py` | task | 生成马里奥主题4K艺术照 | - | - |
| pisa_image | `nodes/pisa_image_node.py` | task | 生成比萨斜塔主题4K艺术照 | - | - |
| safari_image | `nodes/safari_image_node.py` | task | 生成Safari主题4K艺术照 | - | - |
| harry_image | `nodes/harry_image_node.py` | task | 生成哈利波特主题4K艺术照 | - | - |
| mcdonald_image | `nodes/mcdonald_image_node.py` | task | 生成麦当劳主题4K艺术照 | - | - |
| photo_wall | `nodes/photo_wall_node.py` | task | 5张艺术照拼版为照片墙并上传对象存储 | - | - |
| baby_video | `nodes/baby_video_node.py` | task | 生成宝宝小短剧视频 | - | - |
| music | `nodes/music_node.py` | task | 生成配套背景音乐音频 | - | - |
| aggregate | `nodes/aggregate_node.py` | task | 汇总输出四类最终结果 | - | - |

**类型说明**: task(task节点) / agent(大模型)

## 并行编排
- baby_analyze 之后并行开启 7 路：5 个主题生成 + 视频 + 音乐
- 5 个主题生成汇聚到 photo_wall（add_edge 列表汇聚）
- photo_wall + baby_video + music 汇聚到 aggregate（add_edge 列表汇聚）

## 技能使用
- baby_analyze 使用大语言模型（doubao-seed-2-0-pro-260215，多模态）
- mario/pisa/safari/harry/mcdonald 使用图片生成（doubao-seedream-5-0-260128，4K）
- baby_video 使用视频生成（doubao-seedance-2-0-260128，图生视频）
- music 使用语音合成（TTS）
- photo_wall 使用对象存储（S3）