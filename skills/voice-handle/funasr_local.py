#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FunASR 本地模型语音识别脚本
直接调用本地 FunASR模型，无需启动服务
"""

import sys
import os
from pathlib import Path
import logging
from contextlib import contextmanager

# 检查是否在正确的环境中运行
if "any4any" not in sys.executable.lower():
    # 如果不是 any4any 环境，尝试使用正确的 Python 重新执行
    import subprocess
    any4any_python = r"E:\conda\Anconda3\envs\any4any\python.exe"
    if os.path.exists(any4any_python):
        result = subprocess.run([any4any_python] + sys.argv)
        sys.exit(result.returncode)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

logging.getLogger("funasr").setLevel(logging.ERROR)
logging.getLogger("modelscope").setLevel(logging.ERROR)

MODEL_DIR = r"E:\A4A\A4A\FunASR-ctx"
VAD_MODEL_DIR = r"E:\A4A\A4A\modelscope\hub\models\iic\speech_fsmn_vad_zh-cn-16k-common-pytorch"

_model = None

def get_model():
    global _model
    if _model is None:
        from funasr import AutoModel
        import torch
        
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        
        try:
            _model = AutoModel(
                model=MODEL_DIR,
                vad_model=VAD_MODEL_DIR,
                vad_kwargs={"max_single_segment_time": 30000},
                device=device,
                hub="ms",
                disable_update=True,
                trust_remote_code=True,
            )
        except Exception as e:
            print(f"Model loading error: {e}", file=sys.stderr)
            raise
    return _model

def transcribe(audio_path: str) -> str:
    from funasr.utils.postprocess_utils import rich_transcription_postprocess
    import re
    
    model = get_model()
    
    res = model.generate(
        input=audio_path,
        cache={},
        language="auto",
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
        merge_length_s=15,
    )
    
    if not res or not res[0]:
        return ""
    
    raw_text = res[0]["text"]
    clean_text = re.sub(r"<\|.*?\|>", "", raw_text)
    final_text = rich_transcription_postprocess(clean_text)
    
    return final_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python funasr_local.py <audio_file>", file=sys.stderr)
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    if not Path(audio_file).exists():
        print(f"Error: File not found: {audio_file}", file=sys.stderr)
        sys.exit(1)
    
    # 检查模型目录是否存在
    if not Path(MODEL_DIR).exists():
        print(f"Error: Model directory not found: {MODEL_DIR}", file=sys.stderr)
        sys.exit(1)
    
    try:
        text = transcribe(audio_file)
        print(text)
    except Exception as e:
        import traceback
        print(f"Error during transcription: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
