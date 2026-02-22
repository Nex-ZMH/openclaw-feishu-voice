<h1 align="center">OpenClaw Feishu Voice 🎙️</h1>

<p align="center">
  <b>Zero Cost. Low Barrier. Voice Interaction for Feishu Bots Made Simple.</b>
</p>

<p align="center">
  <i>Free voice recognition & synthesis for Feishu chatbots — local ASR, Edge TTS, and seamless audio message delivery. No expensive APIs required.</i>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License: MIT">
  </a>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/Python-3.8%2B-green?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/Cost-FREE-success?style=flat-square" alt="Cost: Free">
</p>

<p align="center">
Built by <a href="https://github.com/Nex-ZMH">Minghao Zhao</a>, An Energy Industry AI Explorer from A Remote Mountain Village of China.
</p>

<p align="center">
  🌐 Languages:
  <a href="#english">English</a> ·
  <a href="#中文">简体中文</a>
</p>

<p align="center">
  ⚡️Quick Routes: 
  <a href="#getting-started">Getting Started</a> ·
  <a href="#features">Features</a> ·
  <a href="#installation">Installation</a> ·
  <a href="#voice-handle-skill">Voice-Handle</a> ·
  <a href="#feishu-voice-skill">Feishu-Voice</a>
</p>

---

## The Problem We Solve

### 🚫 Common Pain Points

| Issue | Description |
|------|------|
| 💰 **Expensive APIs** | Commercial voice APIs charge per request, costs add up quickly for active bots |
| 🔒 **High Barrier** | Setting up voice interaction requires complex integration with multiple services |
| 🌐 **Network Dependency** | Most ASR/TTS services require stable internet, problematic in restricted networks |
| 🎯 **Platform Lock-in** | Voice solutions often tied to specific platforms, hard to migrate |
| 📦 **Complex Setup** | Multiple dependencies, API keys, and configuration steps needed |

### ✅ Our Solution

- **100% Free ASR** — Local FunASR model for speech recognition, no API costs
- **Free TTS Options** — Edge TTS (Microsoft) completely free, optional DashScope for premium voices
- **Low Barrier** — Minimal setup, works out of the box with sensible defaults
- **Hybrid Architecture** — Local ASR for reliability, cloud TTS for quality (or fully local with Edge TTS)
- **Feishu-Ready** — Pre-built integration for Feishu audio messages, handles format conversion automatically

---

## English

### Getting Started

**OpenClaw Feishu Voice** is a dual-skill package designed for [OpenClaw] that enables seamless voice interaction in Feishu chatbots. It consists of two complementary skills:

1. **voice-handle** — Core voice processing engine with ASR (speech recognition) and TTS (speech synthesis)
2. **feishu-voice** — Feishu-specific adapter that converts TTS output to Feishu-compatible audio format

Perfect for developers building conversational AI bots on Feishu platform who want voice capabilities without breaking the bank.

### Features

#### 🎙️ Voice-Handle Skill

- 🔉 **Local ASR** — FunASR-based speech recognition running entirely on your machine
- 🗣️ **Multiple TTS Engines** — Edge TTS (free) + DashScope CosyVoice (premium)
- 🎭 **20+ Voice Options** — From professional news anchors to friendly assistants
- 🌍 **Accent Support** — Mandarin, Northeast dialect, Shaanxi dialect
- � **Dynamic Voice Switching** — Change voice on-the-fly via natural language, just tell OpenClaw "use a gentle female voice"
- � **Standalone API** — Can be used independently for any voice processing task

#### 📱 Feishu-Voice Skill

- 🔄 **Auto Format Conversion** — MP3 → OPUS for Feishu compatibility
- 📤 **Direct Upload** — Uploads to Feishu and sends as audio message
- ✂️ **Smart Segmentation** — Automatically splits long text into multiple voice messages
- ⚡ **One-Line Command** — Simple CLI for quick voice message sending
- 🔗 **Seamless Integration** — Works with OpenClaw's skill system

### Installation

```bash
# Clone the repository
git clone https://github.com/Nex-ZMH/openclaw-feishu-voice.git

# Navigate to directory
cd openclaw-feishu-voice

# Install Python dependencies
pip install funasr torch dashscope edge-tts ffmpeg-python
```

### Requirements

| Requirement | Description |
|-------------|-------------|
| Python 3.8+ | Core runtime |
| FFmpeg | Audio format conversion |
| FunASR Models | Downloaded automatically on first run (~1GB), low disk footprint |
| DashScope API Key | Optional, for premium CosyVoice TTS with generous free tier |
| Feishu Bot | Configure via [Feishu Docs](https://open.feishu.cn) or [OpenClaw Docs]

> 💡 **Tips:**
> - **FunASR** runs locally with minimal resource usage — no need to worry about device performance
> - **DashScope API** offers generous free quota for CosyVoice TTS — premium voices at zero cost for most users

### Configuration

#### DashScope API Key (Optional)

For premium CosyVoice TTS voices, configure your DashScope API key:

**Method 1: Environment Variable (Recommended)**
```bash
# Linux/macOS
export DASHSCOPE_API_KEY="your-api-key-here"

# Windows PowerShell
$env:DASHSCOPE_API_KEY="your-api-key-here"

# Windows CMD
set DASHSCOPE_API_KEY=your-api-key-here
```

**Method 2: OpenClaw Config File**

Add to your `~/.openclaw/openclaw.json`:
```json
{
  "channels": {
    "feishu": {
      "appId": "your-feishu-app-id",
      "appSecret": "your-feishu-app-secret",
      "dashscopeApiKey": "your-dashscope-api-key"
    }
  }
}
```

> 📍 **Get DashScope API Key:** [Alibaba Cloud DashScope Console](https://dashscope.console.aliyun.com/)

#### Feishu Bot Configuration

For Feishu bot setup, refer to:
- [Feishu Open Platform Docs](https://open.feishu.cn/document/home/introduction-to-feishu-open-platform/)
- [OpenClaw Documentation](https://github.com/Nex-ZMH/openclaw)

### Usage

#### Voice-Handle (TTS)

```python
from voice_handle.tts_api import TTSAPI

# Initialize with optional DashScope API key
tts = TTSAPI(api_key="your-dashscope-key")  # or None for Edge TTS only

# Generate speech
tts.tts("Hello, I am your voice assistant", "output.mp3", voice="longwan")

# List available voices
voices = tts.list_voices(filter_gender="女")

# Match voice by description
voice = tts.match_voice("温柔的女声")
```

#### Feishu-Voice

```bash
# Send voice message to Feishu
python feishu-voice/feishu_voice.py "你好，这是一条语音消息" --voice "longwan"

# With custom target user
python feishu-voice/feishu_voice.py "Hello" --user "ou_xxxxxx"
```

### Voice Options

#### Free Edge TTS Voices

| Voice ID | Name | Gender | Style |
|----------|------|--------|-------|
| zh-CN-XiaoxiaoNeural | 晓晓 | Female | Gentle, natural |
| zh-CN-XiaoyiNeural | 晓伊 | Female | Young, lively |
| zh-CN-YunxiNeural | 云希 | Male | Sunny, cheerful |
| zh-CN-YunjianNeural | 云健 | Male | Steady, powerful |
| zh-CN-liaoning-XiaobeiNeural | 晓北 | Female | Northeast accent |

#### Premium CosyVoice Voices (Requires DashScope API Key)

| Voice ID | Name | Gender | Style |
|----------|------|--------|-------|
| longwan | 龙婉 | Female | Elegant, intellectual |
| longxiaocheng | 龙小诚 | Male | Mature, steady |
| longlaotie | 龙老铁 | Male | Northeast accent |
| longshu | 龙书 | Female | Intellectual, elegant |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Feishu Voice                     │
├─────────────────────────┬───────────────────────────────────┤
│      voice-handle       │          feishu-voice             │
├─────────────────────────┼───────────────────────────────────┤
│  ┌─────────────────┐    │    ┌─────────────────────────┐    │
│  │   FunASR ASR    │    │    │   MP3 → OPUS Convert    │    │
│  │   (Local)       │    │    │   (FFmpeg)              │    │
│  └─────────────────┘    │    └─────────────────────────┘    │
│  ┌─────────────────┐    │    ┌─────────────────────────┐    │
│  │   Edge TTS      │    │    │   Feishu File Upload    │    │
│  │   (Free)        │───▶│───▶│   (API)                 │    │
│  └─────────────────┘    │    └─────────────────────────┘    │
│  ┌─────────────────┐    │    ┌─────────────────────────┐    │
│  │   CosyVoice TTS │    │    │   Send Audio Message    │    │
│  │   (Premium)     │    │    │   (API)                 │    │
│  └─────────────────┘    │    └─────────────────────────┘    │
└─────────────────────────┴───────────────────────────────────┘
```

### Roadmap

- [ ] WebSocket streaming for real-time voice interaction
- [ ] Voice activity detection (VAD) improvements
- [ ] Multi-language support (English, Japanese)
- [ ] Custom voice cloning integration

---

## 中文

### 简介

**OpenClaw Feishu Voice** 是为 [OpenClaw]设计的双技能包，让飞书机器人轻松实现语音交互能力。包含两个互补技能：

1. **voice-handle** — 核心语音处理引擎，包含 ASR（语音识别）和 TTS（语音合成）
2. **feishu-voice** — 飞书专用适配器，将 TTS 输出转换为飞书兼容的音频格式

专为在飞书平台构建对话 AI 机器人的开发者设计，零成本实现语音能力。

### 核心亮点

- 💰 **完全免费** — Edge TTS + 本地 FunASR，无需付费 API
- 🚀 **低门槛** — 最小化配置，开箱即用
- 🎭 **丰富音色** — 20+ 种音色可选，支持方言
- 🔄 **动态切换** — 自然语言换音色，说"换个温柔女声"即可
- 📱 **自动转换** — 自动处理音频格式，适配飞书要求
- ✂️ **智能分段** — 长文本自动拆分为多条语音消息

### 功能特性

#### 🎙️ Voice-Handle 技能

- 🔉 **本地 ASR** — 基于 FunASR 的语音识别，完全本地运行
- 🗣️ **多引擎 TTS** — Edge TTS（免费）+ DashScope CosyVoice（高级）
- 🎭 **20+ 音色** — 从专业新闻主播到亲切助手
- 🌍 **方言支持** — 普通话、东北话、陕西话
- 🔄 **动态音色切换** — 自然语言换音色，直接告诉 OpenClaw"换个温柔的女声"即可
- 🔌 **独立 API** — 可单独用于任何语音处理任务

#### 📱 Feishu-Voice 技能

- 🔄 **自动格式转换** — MP3 → OPUS，适配飞书
- 📤 **直接上传** — 上传到飞书并发送为语音消息
- ✂️ **智能分段** — 长文本自动拆分为多条语音
- ⚡ **一行命令** — 简单 CLI 快速发送语音消息
- 🔗 **无缝集成** — 与 OpenClaw 技能系统完美配合

### 安装方法

```bash
# 克隆仓库
git clone https://github.com/Nex-ZMH/openclaw-feishu-voice.git

# 进入目录
cd openclaw-feishu-voice

# 安装 Python 依赖
pip install funasr torch dashscope edge-tts ffmpeg-python
```

### 系统要求

| 要求 | 说明 |
|------|------|
| Python 3.8+ | 核心运行环境 |
| FFmpeg | 音频格式转换 |
| FunASR 模型 | 首次运行自动下载（约 1GB），占用空间小 |
| DashScope API Key | 可选，用于高级 CosyVoice TTS，有可观的免费额度 |
| 飞书机器人 | 配置请参照 [飞书开放平台](https://open.feishu.cn) 或 [OpenClaw 文档] |

> 💡 **温馨提示：**
> - **FunASR** 本地运行资源占用极低，无需担心设备性能问题
> - **DashScope API** 提供可观的免费额度，大多数用户可零成本使用高级音色

### 配置说明

#### DashScope API Key 配置（可选）

如需使用高级 CosyVoice 音色，请配置 DashScope API Key：

**方式一：环境变量（推荐）**
```bash
# Linux/macOS
export DASHSCOPE_API_KEY="your-api-key-here"

# Windows PowerShell
$env:DASHSCOPE_API_KEY="your-api-key-here"

# Windows CMD
set DASHSCOPE_API_KEY=your-api-key-here
```

**方式二：OpenClaw 配置文件**

在 `~/.openclaw/openclaw.json` 中添加：
```json
{
  "channels": {
    "feishu": {
      "appId": "你的飞书应用ID",
      "appSecret": "你的飞书应用密钥",
      "dashscopeApiKey": "你的DashScope API Key"
    }
  }
}
```

> 📍 **获取 DashScope API Key：** [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)

#### 飞书机器人配置

飞书机器人配置请参考：
- [飞书开放平台文档](https://open.feishu.cn/document/home/introduction-to-feishu-open-platform/)
- [OpenClaw 文档](https://github.com/Nex-ZMH/openclaw)

### 使用方法

#### Voice-Handle（TTS）

```python
from voice_handle.tts_api import TTSAPI

# 初始化（可选 DashScope API Key）
tts = TTSAPI(api_key="your-dashscope-key")  # 或 None 仅使用 Edge TTS

# 生成语音
tts.tts("你好，我是你的语音助手", "output.mp3", voice="longwan")

# 列出可用音色
voices = tts.list_voices(filter_gender="女")

# 根据描述匹配音色
voice = tts.match_voice("温柔的女声")
```

#### Feishu-Voice

```bash
# 发送语音消息到飞书
python feishu-voice/feishu_voice.py "你好，这是一条语音消息" --voice "longwan"

# 指定目标用户
python feishu-voice/feishu_voice.py "Hello" --user "ou_xxxxxx"
```

### 常用音色

#### 免费 Edge TTS 音色

| 音色代码 | 名称 | 性别 | 风格 |
|----------|------|------|------|
| zh-CN-XiaoxiaoNeural | 晓晓 | 女 | 温柔自然 |
| zh-CN-XiaoyiNeural | 晓伊 | 女 | 年轻活泼 |
| zh-CN-YunxiNeural | 云希 | 男 | 阳光开朗 |
| zh-CN-YunjianNeural | 云健 | 男 | 沉稳有力 |
| zh-CN-liaoning-XiaobeiNeural | 晓北 | 女 | 东北口音 |

#### 高级 CosyVoice 音色（需 DashScope API Key）

| 音色代码 | 名称 | 性别 | 风格 |
|----------|------|------|------|
| longwan | 龙婉 | 女 | 优雅知性 |
| longxiaocheng | 龙小诚 | 男 | 成熟稳重 |
| longlaotie | 龙老铁 | 男 | 东北口音 |
| longshu | 龙书 | 女 | 知性优雅 |

### 开发计划

- [ ] WebSocket 流式传输，实现实时语音交互
- [ ] 语音活动检测（VAD）优化
- [ ] 多语言支持（英语、日语）
- [ ] 自定义声音克隆集成

---

## Author

[Minghao Zhao](https://github.com/Nex-ZMH)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
