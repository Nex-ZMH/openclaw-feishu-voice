#!/usr/bin/env python3
"""
TTS API - 语音合成接口
支持 CosyVoice (阿里 DashScope) 和 Edge TTS (微软)
"""

import os
import sys
import asyncio
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# CosyVoice (DashScope)
try:
    import dashscope
    from dashscope.audio.tts_v2 import SpeechSynthesizer
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False

# Edge TTS
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False


class TTSAPI:
    """TTS 语音合成接口"""
    
    VOICES = {
        'longwan': {'name': '龙婉', 'gender': '女', 'style': '优雅知性', 'scene': '语音助手、导航播报、聊天数字人'},
        'longcheng': {'name': '龙橙', 'gender': '女', 'style': '清新甜美', 'scene': '语音助手、导航播报、聊天数字人'},
        'longhua': {'name': '龙华', 'gender': '女', 'style': '温柔大方', 'scene': '语音助手、导航播报、聊天数字人'},
        'longxiaochun': {'name': '龙小淳', 'gender': '女', 'style': '活泼可爱', 'scene': '语音助手、聊天数字人（中英文）'},
        'longxiaoxia': {'name': '龙小夏', 'gender': '女', 'style': '温柔亲切', 'scene': '语音助手、聊天数字人'},
        'longxiaocheng': {'name': '龙小诚', 'gender': '男', 'style': '成熟稳重', 'scene': '语音助手、导航播报（中英文）'},
        'longxiaobai': {'name': '龙小白', 'gender': '女', 'style': '清新自然', 'scene': '聊天数字人、有声书、语音助手'},
        'longlaotie': {'name': '龙老铁', 'gender': '男', 'style': '东北口音', 'scene': '新闻播报、有声书、直播带货'},
        'longshu': {'name': '龙书', 'gender': '女', 'style': '知性优雅', 'scene': '有声书、新闻播报、智能客服'},
        'longshuo': {'name': '龙硕', 'gender': '男', 'style': '沉稳专业', 'scene': '新闻播报、客服催收'},
        'longjing': {'name': '龙婧', 'gender': '女', 'style': '干练利落', 'scene': '新闻播报、客服催收'},
        'longmiao': {'name': '龙妙', 'gender': '女', 'style': '亲切温和', 'scene': '客服催收、有声书、语音助手'},
        'longyue': {'name': '龙悦', 'gender': '女', 'style': '悦耳动听', 'scene': '诗词朗诵、有声书、新闻播报'},
        'longyuan': {'name': '龙媛', 'gender': '女', 'style': '温婉柔和', 'scene': '有声书、语音助手、聊天数字人'},
        'longfei': {'name': '龙飞', 'gender': '男', 'style': '浑厚有力', 'scene': '会议播报、新闻播报、有声书'},
        'longjielidou': {'name': '龙杰力豆', 'gender': '男', 'style': '活泼有趣', 'scene': '新闻播报、有声书、聊天助手（中英文）'},
        'longtong': {'name': '龙彤', 'gender': '女', 'style': '甜美可爱', 'scene': '有声书、导航播报、聊天数字人'},
        'longxiang': {'name': '龙祥', 'gender': '男', 'style': '阳光正气', 'scene': '新闻播报、有声书、导航播报'},
        'loongstella': {'name': 'Stella', 'gender': '女', 'style': '国际范儿', 'scene': '语音助手、直播带货（中英文）'},
        'loongbella': {'name': 'Bella', 'gender': '女', 'style': '亲和力强', 'scene': '智能客服、新闻播报、对话闲聊'},
    }
    
    DEFAULT_VOICE = 'longwan'
    TTS_MODEL = 'cosyvoice-v1'
    
    # Edge TTS 音色列表
    EDGE_VOICES = {
        'zh-CN-XiaoxiaoNeural': {'name': '晓晓', 'gender': '女', 'style': '温柔自然', 'engine': 'edge'},
        'zh-CN-XiaoyiNeural': {'name': '晓伊', 'gender': '女', 'style': '年轻活泼', 'engine': 'edge'},
        'zh-CN-YunjianNeural': {'name': '云健', 'gender': '男', 'style': '沉稳有力', 'engine': 'edge'},
        'zh-CN-YunxiNeural': {'name': '云希', 'gender': '男', 'style': '阳光开朗', 'engine': 'edge'},
        'zh-CN-YunxiaNeural': {'name': '云夏', 'gender': '男', 'style': '年轻清新', 'engine': 'edge'},
        'zh-CN-YunyangNeural': {'name': '云扬', 'gender': '男', 'style': '新闻播报', 'engine': 'edge'},
        'zh-CN-liaoning-XiaobeiNeural': {'name': '晓北', 'gender': '女', 'style': '东北口音', 'engine': 'edge'},
        'zh-CN-shaanxi-XiaoniNeural': {'name': '晓妮', 'gender': '女', 'style': '陕西口音', 'engine': 'edge'},
    }
    
    VOICE_KEYWORDS = {
        '男': ['longxiaocheng', 'longlaotie', 'longshuo', 'longfei', 'longjielidou', 'longxiang'],
        '女': ['longwan', 'longcheng', 'longhua', 'longxiaochun', 'longxiaoxia', 'longxiaobai', 'longshu', 'longjing', 'longmiao', 'longyue', 'longyuan', 'longtong', 'loongstella', 'loongbella'],
        '温柔': ['longwan', 'longxiaoxia', 'longhua', 'longyuan'],
        '活泼': ['longxiaochun', 'longtong', 'longjielidou'],
        '成熟': ['longxiaocheng', 'longshuo', 'longfei'],
        '年轻': ['longxiaobai', 'longxiaochun', 'longtong'],
        '新闻': ['longshuo', 'longfei', 'longxiang', 'longjing'],
        '有声书': ['longshu', 'longyue', 'longyuan', 'longfei'],
        '客服': ['longshu', 'longmiao', 'loongbella'],
        '东北': ['longlaotie'],
        '知性': ['longwan', 'longshu'],
        '甜美': ['longcheng', 'longtong'],
        '专业': ['longxiaocheng', 'longshuo'],
    }
    
    def __init__(self, api_key=None, prefer_engine=None):
        """
        初始化 TTS
        
        Args:
            api_key: DashScope API Key（可选，Edge TTS 不需要）
            prefer_engine: 优先使用的引擎 'cosyvoice' 或 'edge'，None 表示自动选择
        """
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
        self.prefer_engine = prefer_engine
        
        # 初始化 DashScope
        if DASHSCOPE_AVAILABLE and self.api_key:
            dashscope.api_key = self.api_key
        
        # 确定可用的引擎
        self._check_engines()
    
    def _check_engines(self):
        """检查可用的 TTS 引擎"""
        self.cosyvoice_available = DASHSCOPE_AVAILABLE and self.api_key
        self.edge_tts_available = EDGE_TTS_AVAILABLE
        
        if not self.cosyvoice_available and not self.edge_tts_available:
            raise ImportError("没有可用的 TTS 引擎，请安装 dashscope 或 edge-tts")
    
    def _is_edge_voice(self, voice: str) -> bool:
        """判断是否为 Edge TTS 音色"""
        return voice in self.EDGE_VOICES
    
    def _tts_cosyvoice(self, text: str, voice: str, output_file: str) -> str:
        """使用 CosyVoice 合成语音"""
        synthesizer = SpeechSynthesizer(model=self.TTS_MODEL, voice=voice)
        audio_data = synthesizer.call(text)
        
        if audio_data:
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            return output_file
        return None
    
    def _tts_edge(self, text: str, voice: str, output_file: str) -> str:
        """使用 Edge TTS 合成语音"""
        async def _generate():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
        
        asyncio.run(_generate())
        return output_file
    
    def match_voice(self, description: str) -> str:
        """根据语义描述匹配音色
        
        Args:
            description: 用户描述，如"温柔的女声"、"像新闻主播"
            
        Returns:
            str: 匹配的音色代码
        """
        description = description.lower()
        
        for voice_id, info in self.VOICES.items():
            if info['name'] in description or voice_id in description:
                return voice_id
        
        matches = {}
        for keyword, voices in self.VOICE_KEYWORDS.items():
            if keyword in description:
                for v in voices:
                    matches[v] = matches.get(v, 0) + 1
        
        if matches:
            return max(matches, key=matches.get)
        
        return self.DEFAULT_VOICE
    
    def list_voices(self, filter_gender=None, filter_style=None, engine=None):
        """列出可用音色
        
        Args:
            filter_gender: 按性别筛选 ('男' 或 '女')
            filter_style: 按风格筛选
            engine: 按引擎筛选 ('cosyvoice' 或 'edge')
            
        Returns:
            list: 音色信息列表
        """
        result = []
        
        # CosyVoice 音色
        if engine is None or engine == 'cosyvoice':
            for voice_id, info in self.VOICES.items():
                if filter_gender and info['gender'] != filter_gender:
                    continue
                if filter_style and filter_style not in info['style']:
                    continue
                result.append({
                    'id': voice_id,
                    'name': info['name'],
                    'gender': info['gender'],
                    'style': info['style'],
                    'scene': info['scene'],
                    'engine': 'cosyvoice'
                })
        
        # Edge TTS 音色
        if engine is None or engine == 'edge':
            for voice_id, info in self.EDGE_VOICES.items():
                if filter_gender and info['gender'] != filter_gender:
                    continue
                if filter_style and filter_style not in info['style']:
                    continue
                result.append({
                    'id': voice_id,
                    'name': info['name'],
                    'gender': info['gender'],
                    'style': info['style'],
                    'engine': 'edge'
                })
        
        return result
    
    def tts(self, text, output_file="output.wav", voice=None):
        """语音合成（文字转语音）
        
        自动根据音色选择引擎：
        - CosyVoice 音色：使用 DashScope API
        - Edge TTS 音色：使用 Edge TTS
        
        Args:
            text: 要合成的文字
            output_file: 输出文件路径
            voice: 音色代码或语义描述
            
        Returns:
            str: 输出文件路径
        """
        try:
            # 确定音色
            if voice is None:
                # 根据优先引擎选择默认音色
                if self.prefer_engine == 'edge' and self.edge_tts_available:
                    voice = 'zh-CN-XiaoxiaoNeural'
                else:
                    voice = self.DEFAULT_VOICE
            elif voice not in self.VOICES and voice not in self.EDGE_VOICES:
                # 尝试匹配 CosyVoice 音色
                voice = self.match_voice(voice)
            
            # 判断使用哪个引擎
            use_edge = self._is_edge_voice(voice)
            
            if use_edge:
                if not self.edge_tts_available:
                    print(f"Edge TTS 不可用，尝试使用 CosyVoice")
                    return None
                return self._tts_edge(text, voice, output_file)
            else:
                if not self.cosyvoice_available:
                    print(f"CosyVoice 不可用，尝试使用 Edge TTS")
                    if self.edge_tts_available:
                        return self._tts_edge(text, 'zh-CN-XiaoxiaoNeural', output_file)
                    return None
                return self._tts_cosyvoice(text, voice, output_file)
                
        except Exception as e:
            print(f"合成出错: {e}")
            return None


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='TTS API - 语音合成')
    parser.add_argument('action', choices=['tts', 'list', 'match'], help='操作')
    parser.add_argument('input', nargs='?', help='输入文字')
    parser.add_argument('-o', '--output', default='output.mp3', help='输出文件')
    parser.add_argument('-v', '--voice', default=None, help='音色或语义描述')
    parser.add_argument('-g', '--gender', choices=['男', '女'], help='按性别筛选')
    
    args = parser.parse_args()
    
    tts = TTSAPI()
    
    if args.action == 'tts':
        if not args.input:
            print("请提供要合成的文字")
            sys.exit(1)
        output = tts.tts(args.input, args.output, args.voice)
        print(f"已生成: {output}" if output else "合成失败")
    elif args.action == 'list':
        voices = tts.list_voices(filter_gender=args.gender)
        for v in voices:
            print(f"{v['id']}: {v['name']} ({v['gender']}) - {v['style']}")
    elif args.action == 'match':
        if not args.input:
            print("请提供语义描述")
            sys.exit(1)
        matched = tts.match_voice(args.input)
        info = tts.VOICES[matched]
        print(f"匹配音色: {info['name']} ({matched}) - {info['style']}")
