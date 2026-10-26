"""配套背景音乐生成节点"""
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import TTSClient

from graphs.state import MusicInput, MusicOutput
from utils.file.file import File


def music_node(
    state: MusicInput,
    config: RunnableConfig,
    runtime: Runtime[Context],
) -> MusicOutput:
    """
    title: 背景音乐生成
    desc: 根据歌曲歌词生成一段欢快活泼、适合宝宝的背景音乐音频
    integrations: 语音合成
    """
    ctx = runtime.context
    client = TTSClient(ctx=ctx)

    audio_url, _size = client.synthesize(
        uid="baby_studio",
        text=state.music_lyrics,
        speaker="saturn_zh_female_tiaopigongzhu_tob",
        audio_format="mp3",
        sample_rate=48000,
        speech_rate=10,
        loudness_rate=5,
    )
    if not audio_url:
        raise Exception("背景音乐生成失败")

    return MusicOutput(background_music=File(url=audio_url, file_type="audio"))