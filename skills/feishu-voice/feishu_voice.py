#!/usr/bin/env python3
"""
Feishu Voice Skill - 飞书语音消息发送

功能：
1. 使用 voice-handle 的 TTS 生成语音
2. 将 MP3 转换为 OPUS 格式
3. 上传到飞书
4. 发送语音条消息

依赖：
- voice-handle (TTS)
- ffmpeg-python
"""

import os
import sys
import json
import re
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, List

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 导入 voice-handle 的 TTS 功能
sys.path.insert(0, str(Path(__file__).parent.parent / 'voice-handle'))
from tts_api import TTSAPI


try:
    import ffmpeg
    FFMPEG_AVAILABLE = True
except ImportError:
    FFMPEG_AVAILABLE = False


class FeishuVoice:
    """飞书语音消息发送器"""
    
    # 飞书 API 配置
    FEISHU_API_BASE = "https://open.feishu.cn/open-apis"
    
    # 默认音色
    DEFAULT_VOICE = "zh-CN-XiaoyiNeural"
    
    def __init__(self, app_id: Optional[str] = None, app_secret: Optional[str] = None, 
                 target_user: Optional[str] = None, api_key: Optional[str] = None):
        """
        初始化飞书语音发送器
        
        Args:
            app_id: 飞书应用 ID
            app_secret: 飞书应用密钥
            target_user: 默认目标用户 open_id
            api_key: DashScope API Key（可选）
        """
        self.app_id = app_id or os.getenv('FEISHU_APP_ID')
        self.app_secret = app_secret or os.getenv('FEISHU_APP_SECRET')
        self.target_user = target_user or os.getenv('FEISHU_TARGET_USER')
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
        
        # 尝试从 openclaw.json 读取配置
        if not self.app_id or not self.app_secret or not self.api_key:
            self._load_config_from_openclaw()
        
        # 初始化 TTS
        self.tts_api = TTSAPI(api_key=self.api_key)
    
    def _load_config_from_openclaw(self):
        """从 openclaw.json 加载配置"""
        config_paths = [
            Path.home() / '.openclaw' / 'openclaw.json',
            Path.cwd() / 'openclaw.json',
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    feishu_config = config.get('channels', {}).get('feishu', {})
                    if not self.app_id:
                        self.app_id = feishu_config.get('appId')
                    if not self.app_secret:
                        self.app_secret = feishu_config.get('appSecret')
                    if not self.target_user:
                        self.target_user = feishu_config.get('allowFrom', [None])[0]
                    if not self.api_key:
                        self.api_key = feishu_config.get('dashscopeApiKey')
                    
                    break
                except Exception as e:
                    print(f"Warning: Failed to load config from {config_path}: {e}")
    
    def _get_tenant_access_token(self) -> str:
        """获取飞书 Tenant Access Token"""
        import urllib.request
        import ssl
        
        url = f"{self.FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
        data = json.dumps({
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        # 禁用 SSL 验证（如果需要）
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, context=context) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return result['tenant_access_token']
            else:
                raise Exception(f"Failed to get token: {result.get('msg')}")
    
    def _convert_mp3_to_opus(self, mp3_path: str, opus_path: str) -> str:
        """
        将 MP3 转换为 OPUS 格式
        
        Args:
            mp3_path: MP3 文件路径
            opus_path: OPUS 输出路径
            
        Returns:
            OPUS 文件路径
        """
        if not FFMPEG_AVAILABLE:
            # 使用命令行 ffmpeg
            cmd = [
                'ffmpeg', '-y',
                '-i', mp3_path,
                '-c:a', 'libopus',
                '-b:a', '24k',
                '-application', 'voip',
                opus_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
        else:
            # 使用 ffmpeg-python
            (
                ffmpeg
                .input(mp3_path)
                .output(opus_path, **{
                    'c:a': 'libopus',
                    'b:a': '24k',
                    'application': 'voip'
                })
                .overwrite_output()
                .run(quiet=True)
            )
        
        return opus_path
    
    def _get_audio_duration(self, file_path: str) -> int:
        """获取音频时长（毫秒）"""
        try:
            cmd = [
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            duration_sec = float(result.stdout.strip())
            return int(duration_sec * 1000)
        except Exception:
            return 5000  # 默认 5 秒
    
    def _upload_file(self, token: str, file_path: str, duration: int) -> str:
        """
        上传文件到飞书
        
        Args:
            token: Tenant Access Token
            file_path: 文件路径
            duration: 音频时长（毫秒）
            
        Returns:
            file_key
        """
        import urllib.request
        import ssl
        
        url = f"{self.FEISHU_API_BASE}/im/v1/files"
        
        # 构建 multipart/form-data
        boundary = '----FormBoundary' + str(os.urandom(8).hex())
        
        file_data = open(file_path, 'rb').read()
        
        body = b''
        body += f'--{boundary}\r\n'.encode()
        body += b'Content-Disposition: form-data; name="file_type"\r\n\r\nopus\r\n'
        
        body += f'--{boundary}\r\n'.encode()
        body += b'Content-Disposition: form-data; name="file_name"\r\n\r\nvoice.opus\r\n'
        
        body += f'--{boundary}\r\n'.encode()
        body += f'Content-Disposition: form-data; name="duration"\r\n\r\n{duration}\r\n'.encode()
        
        body += f'--{boundary}\r\n'.encode()
        body += b'Content-Disposition: form-data; name="file"; filename="voice.opus"\r\n'
        body += b'Content-Type: audio/opus\r\n\r\n'
        body += file_data
        body += b'\r\n'
        body += f'--{boundary}--\r\n'.encode()
        
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Authorization': f'Bearer {token}'
            },
            method='POST'
        )
        
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, context=context) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return result['data']['file_key']
            else:
                raise Exception(f"Upload failed: {result.get('msg')}")
    
    def _send_voice_message(self, token: str, file_key: str, duration: int, 
                           target_user: Optional[str] = None) -> dict:
        """
        发送语音消息
        
        Args:
            token: Tenant Access Token
            file_key: 文件 key
            duration: 音频时长（毫秒）
            target_user: 目标用户 open_id
            
        Returns:
            发送结果
        """
        import urllib.request
        import ssl
        
        target = target_user or self.target_user
        if not target:
            raise ValueError("Target user not specified")
        
        url = f"{self.FEISHU_API_BASE}/im/v1/messages?receive_id_type=open_id"
        
        data = json.dumps({
            "receive_id": target,
            "content": json.dumps({
                "file_key": file_key,
                "duration": duration
            }),
            "msg_type": "audio"
        }).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            method='POST'
        )
        
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, context=context) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return result['data']
            else:
                raise Exception(f"Send failed: {result.get('msg')}")
    
    def _split_text(self, text: str, max_chars: int = 80) -> List[str]:
        """
        将长文本智能分段
        
        策略：
        1. 优先按句子结束符（。！？；）分割
        2. 如果单句过长，按逗号分割
        3. 确保每段不超过 max_chars 字符
        
        Args:
            text: 原始文本
            max_chars: 每段最大字符数
            
        Returns:
            分段后的文本列表
        """
        # 清理文本
        text = text.strip()
        if not text:
            return []
        
        segments = []
        current_segment = ""
        
        # 按句子分割（支持。！？；）
        sentences = re.split(r'([。！？；])', text)
        
        i = 0
        while i < len(sentences):
            sentence = sentences[i]
            # 添加标点符号到句子
            if i + 1 < len(sentences) and sentences[i + 1] in '。！？；':
                sentence += sentences[i + 1]
                i += 1
            
            sentence = sentence.strip()
            i += 1
            
            if not sentence:
                continue
            
            # 如果当前句子本身超过限制，需要进一步分割
            if len(sentence) > max_chars:
                # 先保存当前积累的段落
                if current_segment:
                    segments.append(current_segment.strip())
                    current_segment = ""
                
                # 按逗号、顿号分割长句
                sub_sentences = re.split(r'([，、])', sentence)
                j = 0
                while j < len(sub_sentences):
                    part = sub_sentences[j]
                    if j + 1 < len(sub_sentences) and sub_sentences[j + 1] in '，、':
                        part += sub_sentences[j + 1]
                        j += 1
                    
                    part = part.strip()
                    j += 1
                    
                    if not part:
                        continue
                    
                    # 如果分段后还是太长，强制截断
                    if len(part) > max_chars:
                        for k in range(0, len(part), max_chars):
                            segments.append(part[k:k + max_chars])
                    else:
                        segments.append(part)
            
            # 如果加入当前句子后超过限制，先保存当前段落
            elif len(current_segment) + len(sentence) > max_chars:
                if current_segment:
                    segments.append(current_segment.strip())
                current_segment = sentence
            else:
                current_segment += sentence
        
        # 保存最后一段
        if current_segment:
            segments.append(current_segment.strip())
        
        return [s for s in segments if s]

    def send_voice(self, text: str, voice: Optional[str] = None, 
                   target_user: Optional[str] = None, 
                   auto_split: bool = True,
                   max_segment_chars: int = 120) -> List[dict]:
        """
        发送语音消息到飞书（完整流程）
        
        Args:
            text: 要发送的文字
            voice: 音色，默认使用 DEFAULT_VOICE
            target_user: 目标用户 open_id
            auto_split: 是否自动分段长文本
            max_segment_chars: 每段最大字符数（建议60-100，对应约15-25秒语音）
            
        Returns:
            发送结果列表，每个元素包含 message_id
        """
        voice = voice or self.DEFAULT_VOICE
        
        # 判断是否需要分段
        if auto_split and len(text) > max_segment_chars:
            segments = self._split_text(text, max_segment_chars)
            print(f"文本已分段: {len(segments)} 段")
            for i, seg in enumerate(segments, 1):
                print(f"  段{i}: {seg[:40]}{'...' if len(seg) > 40 else ''}")
        else:
            segments = [text]
        
        results = []
        token = None
        
        for i, segment in enumerate(segments, 1):
            if len(segments) > 1:
                print(f"\n发送第 {i}/{len(segments)} 段...")
            
            # 创建临时目录
            with tempfile.TemporaryDirectory() as temp_dir:
                # 1. 生成 TTS
                mp3_path = os.path.join(temp_dir, 'voice.mp3')
                self.tts_api.tts(segment, mp3_path, voice)
                
                # 2. 获取音频时长
                duration = self._get_audio_duration(mp3_path)
                
                # 3. 转换为 OPUS
                opus_path = os.path.join(temp_dir, 'voice.opus')
                self._convert_mp3_to_opus(mp3_path, opus_path)
                
                # 4. 获取 Token（只获取一次）
                if token is None:
                    token = self._get_tenant_access_token()
                
                # 5. 上传文件
                file_key = self._upload_file(token, opus_path, duration)
                
                # 6. 发送消息
                result = self._send_voice_message(token, file_key, duration, target_user)
                results.append(result)
                
                if len(segments) > 1:
                    print(f"  ✅ 第 {i} 段发送成功")
        
        return results if len(results) > 1 else results[0]


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='发送语音消息到飞书')
    parser.add_argument('text', help='要发送的文字')
    parser.add_argument('--voice', '-v', default='zh-CN-XiaoyiNeural', help='音色')
    parser.add_argument('--user', '-u', help='目标用户 open_id')
    parser.add_argument('--no-split', action='store_true', help='禁用自动分段')
    parser.add_argument('--max-chars', type=int, default=80, help='每段最大字符数（默认80）')
    
    args = parser.parse_args()
    
    sender = FeishuVoice()
    results = sender.send_voice(
        args.text, 
        args.voice, 
        args.user,
        auto_split=not args.no_split,
        max_segment_chars=args.max_chars
    )
    
    if isinstance(results, list):
        print(f"\n✅ 成功发送 {len(results)} 条语音消息!")
        for i, result in enumerate(results, 1):
            print(f"   消息{i} ID: {result['message_id']}")
    else:
        print(f"\n✅ Voice message sent!")
        print(f"   Message ID: {results['message_id']}")
        print(f"   Chat ID: {results['chat_id']}")


if __name__ == '__main__':
    main()
