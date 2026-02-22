---
name: voice-handle
description: 语音处理技能，包含本地 FunASR 语音识别 (ASR) 和 TTS 语音合成。
trigger: 需要语音识别或语音合成时触发。**飞书渠道需要语音回复时请使用 feishu-voice 技能**。
metadata: {"openclaw":{"emoji":"🎙️","requires":{"python":["funasr","torch","dashscope","ffmpeg-python","edge-tts"],"env":["DASHSCOPE_API_KEY"]},"tools":["tts"]}}
---

## 渠道区分

| 渠道 | 语音回复方式 |
|------|-------------|
| 飞书(Feishu) | 使用 `feishu-voice` 技能的 `send_feishu_voice` 工具 |
| 其他渠道 | 使用本技能的 `tts` 工具 |

## 功能

### ASR 语音识别
用户发送语音消息时，系统自动识别，结果在 Transcript 中显示。

### TTS 语音合成
调用 `tts` 工具将文字转为语音（飞书渠道除外）。

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| text | string | ✅ | 要合成的文字 |
| voice | string | 可选 | 音色代码，默认 longwan |

## 示例

```
调用 tts 工具:
- text: "你好，我是小奈"
- voice: "longwan"
```

## 音色列表

### Edge TTS（免费，需联网）
| 音色代码 | 特点 |
|---------|------|
| zh-CN-XiaoxiaoNeural | 女声，温柔自然 |
| zh-CN-XiaoyiNeural | 女声，年轻活泼 |
| zh-CN-YunjianNeural | 男声，沉稳有力 |
| zh-CN-YunxiNeural | 男声，阳光开朗 |
| zh-CN-YunyangNeural | 男声，新闻播报风格 |
| zh-CN-liaoning-XiaobeiNeural | 女声，东北口音 |
| zh-CN-shaanxi-XiaoniNeural | 女声，陕西口音 |

### 阿里 CosyVoice（需 DASHSCOPE_API_KEY）
| 音色代码 | 特点 |
|---------|------|
| longwan | 女声，优雅知性（默认） |
| longcheng | 女声，清新甜美 |
| longxiaochun | 女声，活泼可爱 |
| longxiaoxia | 女声，温柔亲切 |
| longxiaocheng | 男声，成熟稳重 |
| longxiaobai | 女声，清新自然 |
| longlaotie | 男声，东北口音 |
| longshu | 女声，知性优雅 |
| longshuo | 男声，沉稳专业 |
| longjing | 女声，干练利落 |
| longmiao | 女声，亲切温和 |
| longyue | 女声，悦耳动听 |
| longyuan | 女声，温婉柔和 |
| longfei | 男声，浑厚有力 |
| longjielidou | 男声，活泼有趣 |
| longtong | 女声，甜美可爱 |
| longxiang | 男声，阳光正气 |
| loongstella | 女声，国际范儿 |
| loongbella | 女声，亲和力强 |

## 注意事项

- ASR 使用本地模型，无需联网
- TTS 默认使用 Edge TTS（免费），配置 DASHSCOPE_API_KEY 后可用阿里 CosyVoice
