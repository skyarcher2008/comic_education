#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Proofreading Module - LLM-based text capitalization correction

为翻译后的文本提供LLM校对功能，主要解决大小写格式问题
"""

import logging
from typing import List, Optional
from src.core.translation import translate_single_text
from src.shared import constants

logger = logging.getLogger(__name__)

# 校对专用的简化Prompt
PROOFREADING_PROMPT = """You are a text proofreading assistant. Your only task is to fix capitalization errors in English text for comic book speech bubbles.

RULES:
1. Capitalize the first letter of each sentence
2. Capitalize proper nouns (names, places, titles, brands, etc.)
3. Keep acronyms in uppercase (like "OK", "TV", "AI", etc.)
4. Keep interjections as they are (Oh!, Ah!, Hmm...)
5. Don't change any words, don't add or remove text
6. Only fix capitalization

INPUT: Text that may have incorrect capitalization
OUTPUT: The same text with correct capitalization

Examples:
Input: "hello world! this is JOHN speaking."
Output: "Hello world! This is John speaking."

Input: "OH NO! the TV is broken again!"
Output: "Oh no! The TV is broken again!"

Input: "i love NEW YORK city!"
Output: "I love New York City!"

Fix only capitalization, return the corrected text:"""

def proofread_text_capitalization(
    text: str,
    model_provider: str = constants.DEFAULT_MODEL_PROVIDER,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,
    custom_base_url: Optional[str] = None,
    rpm_limit: int = constants.DEFAULT_rpm_TRANSLATION
) -> str:
    """
    使用LLM校对单个文本的大小写格式
    
    Args:
        text: 需要校对的文本
        model_provider: 模型提供商
        api_key: API密钥
        model_name: 模型名称
        custom_base_url: 自定义API地址
        rpm_limit: 请求频率限制
        
    Returns:
        校对后的文本
    """
    if not text or not text.strip():
        return text
    
    # 如果文本很短（少于3个字符）或者全是标点符号，跳过校对
    if len(text.strip()) < 3 or not any(c.isalpha() for c in text):
        logger.debug(f"跳过校对短文本或无字母文本: '{text}'")
        return text
    
    # 如果文本已经是标准格式（首字母大写，无全大写单词），可能跳过
    words = text.split()
    if (text[0].isupper() and 
        not any(word.isupper() and len(word) > 2 and word.isalpha() for word in words) and
        not any(word.islower() and word[0].islower() for word in words[1:] if word and word[0].isalpha())):
        logger.debug(f"文本格式已正确，跳过校对: '{text}'")
        return text
    
    logger.info(f"开始校对文本大小写: '{text[:50]}...'")
    
    try:
        # 使用翻译接口进行校对，但目标语言设为英文，使用校对专用prompt
        corrected_text = translate_single_text(
            text=text,
            target_language="English", # 校对保持英文
            model_provider=model_provider,
            api_key=api_key,
            model_name=model_name,
            prompt_content=PROOFREADING_PROMPT,
            use_json_format=False,
            custom_base_url=custom_base_url,
            rpm_limit_translation=rpm_limit
        )
        
        # 检查校对结果是否有效
        if corrected_text and "翻译失败" not in corrected_text:
            # 简单验证：校对后的文本长度不应该变化太大
            if abs(len(corrected_text) - len(text)) / len(text) > 0.3:
                logger.warning(f"校对结果长度变化过大，使用原文: '{text}' -> '{corrected_text}'")
                return text
            
            logger.info(f"校对完成: '{text}' -> '{corrected_text}'")
            return corrected_text.strip()
        else:
            logger.warning(f"校对失败，使用原文: {corrected_text}")
            return text
            
    except Exception as e:
        logger.error(f"校对过程出错: {e}")
        return text

def proofread_text_list_capitalization(
    texts: List[str],
    model_provider: str = constants.DEFAULT_MODEL_PROVIDER,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,
    custom_base_url: Optional[str] = None,
    rpm_limit: int = constants.DEFAULT_rpm_TRANSLATION
) -> List[str]:
    """
    批量校对文本列表的大小写格式
    
    Args:
        texts: 需要校对的文本列表
        model_provider: 模型提供商
        api_key: API密钥
        model_name: 模型名称
        custom_base_url: 自定义API地址
        rpm_limit: 请求频率限制
        
    Returns:
        校对后的文本列表
    """
    if not texts:
        return texts
    
    logger.info(f"开始批量校对 {len(texts)} 个文本的大小写格式...")
    
    corrected_texts = []
    for i, text in enumerate(texts):
        logger.debug(f"校对文本 {i+1}/{len(texts)}: '{text[:30]}...'")
        corrected = proofread_text_capitalization(
            text, model_provider, api_key, model_name, custom_base_url, rpm_limit
        )
        corrected_texts.append(corrected)
    
    logger.info("批量校对完成")
    return corrected_texts

# 测试代码
if __name__ == "__main__":
    import os
    logging.basicConfig(level=logging.INFO)
    
    # 测试文本
    test_texts = [
        "hello world! this is JOHN speaking.",
        "OH NO! the TV is broken again!",
        "i love NEW YORK city!",
        "WAIT! don't GO there!",
        "hmm... that's INTERESTING.",
        "OK!",  # 短文本，应该跳过
        "..."   # 无字母文本，应该跳过
    ]
    
    # 如果有测试API密钥，可以测试
    test_api_key = os.environ.get("TEST_API_KEY")
    if test_api_key:
        print("=== 校对测试 ===")
        for text in test_texts:
            result = proofread_text_capitalization(
                text, 
                model_provider="siliconflow",
                api_key=test_api_key,
                model_name="alibaba/Qwen1.5-14B-Chat"
            )
            print(f"原文: '{text}'")
            print(f"校对: '{result}'")
            print()
    else:
        print("设置 TEST_API_KEY 环境变量以进行实际测试")
