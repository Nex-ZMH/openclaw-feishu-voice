---
name: feishu-voice
description: 飞书语音消息发送。将文字转为语音条发送到飞书。
trigger: 系统消息包含"Feishu"或"飞书"，且满足以下任一条件时必须使用：(1) 用户发送语音消息（含[Audio]或file_key）→ 必须用语音回复；(2) 用户要求语音回复。飞书渠道禁止使用tts工具。
metadata: {"openclaw":{"emoji":"🎙️","requires":{"python":["ffmpeg-python"]},"depends":["voice-handle"]}}
---

## 核心规则

**飞书渠道语音回复规则**：
| 场景 | 动作 |
|------|------|
| 收到语音消息 | **必须**运行脚本语音回复 |
| 用户要求语音回复 | 运行脚本语音回复 |
| 用户说"文字回复" | 可以用文字回复 |

**禁止**：飞书渠道使用 `tts` 工具（飞书不支持 tts 生成的音频格式）

## 使用方法

运行 `feishu_voice.py` 脚本：

```bash
python "{{skill_path}}/feishu_voice.py" "要发送的文字" --voice "longwan"
```

| 参数 | 必需 | 说明 |
|------|------|------|
| 第一个参数 | ✅ | 要转为语音的文字 |
| --voice | 可选 | 音色代码，默认 longwan |

## 示例

```bash
python "{{skill_path}}/feishu_voice.py" "你好，我是小奈" --voice "longwan"
```

## 常用音色

| 音色代码 | 特点 |
|---------|------|
| longwan | 女声，优雅知性（默认） |
| longxiaocheng | 男声，成熟稳重 |
| zh-CN-XiaoxiaoNeural | 女声，温柔自然（Edge TTS） |
| zh-CN-YunxiNeural | 男声，阳光开朗（Edge TTS） |

完整音色列表见 [voice-handle 技能](../voice-handle/SKILL.md)。

## 注意事项

- 仅用于飞书渠道
- 自动将 MP3 转为 OPUS 格式
- 需要 FFmpeg 已安装
