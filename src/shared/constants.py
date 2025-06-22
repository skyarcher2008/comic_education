"""
常量定义模块，用于存储应用程序中使用的各种常量
"""
import os

# --- 提示词相关 ---
DEFAULT_PROMPT = """You are an expert English teacher and My Little Pony comic translator. Your task is to rewrite English text from My Little Pony comics to make it suitable for Chinese elementary school students learning English.

IMPORTANT: If the input text is already simple, short, or consists of interjections/sound effects (like "ER...", "OH!", "AH!", "HMM...", "YEAH!", "NO!", etc.), return it exactly as provided. Do NOT add explanations or additional text.

VOCABULARY CONSTRAINTS:
- Use ONLY simple English words suitable for elementary students
- Keep sentences short and simple (maximum 10-12 words per sentence)
- Use present tense when possible, avoid complex grammar structures

PRESERVED TERMS (keep exactly as they are):
- CHARACTER NAMES: Twilight Sparkle, Rainbow Dash, Pinkie Pie, Applejack, Rarity, Fluttershy, Princess Celestia, Princess Luna, Spike, Starlight Glimmer
- PLACES: Equestria, Ponyville, Canterlot, Cloudsdale, Crystal Empire, Sweet Apple Acres, Carousel Boutique, Sugarcube Corner
- SPECIAL TERMS: cutie mark, unicorn, pegasus, earth pony, alicorn, magic, friendship, harmony, Elements of Harmony, Wonderbolts

REWRITING RULES:
1. For simple interjections or sounds (ER..., OH!, AH!, HMM..., YEAH!, NO!, etc.) - return exactly as provided
2. For already simple text suitable for elementary students - return exactly as provided
3. Keep all My Little Pony character names, place names, and special terms unchanged
4. Replace difficult vocabulary with simple words
5. Break long sentences into shorter, simpler ones
6. Use basic grammar suitable for elementary students
7. Avoid American slang and idioms
8. Use "said" instead of complex dialogue tags
9. Use simple conjunctions: "and", "but", "so", "because"
10. Use proper capitalization: Only capitalize the first letter of sentences and proper nouns. Do NOT output text in ALL CAPS
11. Rewrite sentences should not be longer than orignial sentences

EXAMPLES:
Original: "That's absolutely magnificent, darling!"
Rewritten: "That is very beautiful!"

Original: "I'm completely flabbergasted!"
Rewritten: "I am very surprised!"

Original: "ER..."
Rewritten: Er...

Original: "OH!"
Rewritten: Ohh!

Original: "HMM..."
Rewritten: Hmm...

OUTPUT: Return ONLY the rewritten English text. Never add explanations, comments, or additional guidance. For simple interjections, return them exactly as provided."""
DEFAULT_TEXTBOX_PROMPT = """You are an expert language teacher and translator. Please translate the provided non-English content into English and explain why you translated it that way, along with key language points to learn from the text."""
DEFAULT_PROMPT_NAME = "默认提示词"

# --- 模型与历史 ---
MAX_MODEL_HISTORY = 5
DEFAULT_MODEL_PROVIDER = 'siliconflow'
MODEL_HISTORY_FILE = 'model_history.json'
PROMPTS_FILE = 'prompts.json'
TEXTBOX_PROMPTS_FILE = 'textbox_prompts.json'

# --- 新增自定义OpenAI服务商ID ---
CUSTOM_OPENAI_PROVIDER_ID = 'custom_openai'
# ---------------------------------

# --- 翻译服务相关 ---
# 百度翻译API引擎ID
BAIDU_TRANSLATE_ENGINE_ID = 'baidu_translate'
# 有道翻译API引擎ID
YOUDAO_TRANSLATE_ENGINE_ID = 'youdao_translate'

# --- 文件与目录 ---
# 默认字体路径现在指向 src/app/static/fonts/
DEFAULT_FONT_RELATIVE_PATH = os.path.join('src', 'app', 'static', 'fonts', 'msyh.ttc')
DEFAULT_FONT_PATH = "static/msyh.ttc"  # 保留旧变量以兼容现有代码
UPLOAD_FOLDER_NAME = 'uploads'
TEMP_FOLDER_NAME = 'temp'
UPLOAD_FOLDER = 'uploads'  # 保留旧变量以兼容现有代码
TEMP_FOLDER = 'temp'  # 保留旧变量以兼容现有代码

# --- 默认翻译与渲染参数 ---
DEFAULT_TARGET_LANG = 'en'
DEFAULT_SOURCE_LANG = 'japan'
DEFAULT_FONT_SIZE = 30
DEFAULT_TEXT_DIRECTION = 'vertical'
DEFAULT_TEXT_COLOR = '#231816'
DEFAULT_ROTATION_ANGLE = 0
DEFAULT_FILL_COLOR = '#FFFFFF'
DEFAULT_INPAINTING_STRENGTH = 1.0

# --- OCR 相关 ---
SUPPORTED_LANGUAGES_OCR = {
    "japan": "MangaOCR",
    "en": "PaddleOCR",
    "korean": "PaddleOCR",
    "chinese": "PaddleOCR",
    "chinese_cht": "PaddleOCR",
    "french": "PaddleOCR",
    "german": "PaddleOCR",
    "russian": "PaddleOCR",
    "italian": "PaddleOCR",
    "spanish": "PaddleOCR"
}
PADDLE_LANG_MAP = {
    "en": "en",
    "korean": "korean",
    "chinese": "ch",
    "chinese_cht": "chinese_cht",
    "french": "french",
    "german": "german",
    "russian": "ru",
    "italian": "italian",
    "spanish": "spanish"
}

# --- 百度OCR相关 ---
BAIDU_OCR_VERSIONS = {
    "standard": "标准版",
    "high_precision": "高精度版"
}

# 百度OCR语言映射使用大写编码
# 参考文档: https://cloud.baidu.com/doc/OCR/s/zk3h7xz52
BAIDU_LANG_MAP = {
    "japan": "japanese",
    "japanese": "japanese",
    "en": "english",
    "english": "english", 
    "korean": "korean",
    "chinese": "chinese",
    "chinese_cht": "chinese",
    "french": "french",
    "german": "german",
    "russian": "russian",
    "italian": "italian",
    "spanish": "spanish"
}

# --- 百度翻译相关 ---
# 百度翻译语言映射
# 参考文档: https://fanyi-api.baidu.com/doc/21
BAIDU_TRANSLATE_LANG_MAP = {
    'zh': 'zh',       # 中文
    'en': 'en',       # 英语
    'ja': 'jp',       # 日语 (百度API使用jp)
    'ko': 'kor',      # 韩语
    'fr': 'fra',      # 法语
    'es': 'spa',      # 西班牙语
    'it': 'it',       # 意大利语
    'de': 'de',       # 德语
    'ru': 'ru',       # 俄语
    'pt': 'pt',       # 葡萄牙语
    'vi': 'vie',      # 越南语
    'th': 'th',       # 泰语
    'auto': 'auto',   # 自动检测
}

# 项目内部语言代码到百度翻译语言代码的映射
PROJECT_TO_BAIDU_TRANSLATE_LANG_MAP = {
    'zh': 'zh',
    'en': 'en',
    'japan': 'jp',
    'korean': 'kor',
    'chinese': 'zh',
    'chinese_cht': 'zh',
    'french': 'fra',
    'german': 'de',
    'russian': 'ru',
    'italian': 'it',
    'spanish': 'spa'
}

# --- AI 视觉 OCR 相关 ---
AI_VISION_OCR_ENGINE_ID = 'ai_vision'  # 定义唯一标识符

# 新增自定义OpenAI兼容服务商ID (确保这个值是唯一的)
CUSTOM_AI_VISION_PROVIDER_ID = 'custom_openai_vision' # 与翻译的自定义ID区分

DEFAULT_AI_VISION_OCR_PROMPT = """你是一个ocr助手，你需要将我发送给你的图片中的文字提取出来并返回给我，要求：
1、完整识别：我发送给你的图片中的文字都是需要识别的内容
2、非贪婪输出：不要返回任何其他解释和说明。"""

# 新增支持的 AI 视觉服务商列表
SUPPORTED_AI_VISION_PROVIDERS = {
    'siliconflow': 'SiliconFlow (硅基流动)',
    'volcano': '火山引擎',
    'gemini': 'Google Gemini',
    CUSTOM_AI_VISION_PROVIDER_ID: '自定义 OpenAI 兼容视觉服务'
}

# --- 有道翻译相关 ---
# 有道翻译语言映射
# 参考文档: https://ai.youdao.com/DOCSIRMA/html/trans/api/wbfy/index.html
YOUDAO_TRANSLATE_LANG_MAP = {
    'zh': 'zh-CHS',    # 中文简体
    'en': 'en',        # 英语
    'ja': 'ja',        # 日语
    'ko': 'ko',        # 韩语
    'fr': 'fr',        # 法语
    'es': 'es',        # 西班牙语
    'it': 'it',        # 意大利语
    'de': 'de',        # 德语
    'ru': 'ru',        # 俄语
    'pt': 'pt',        # 葡萄牙语
    'vi': 'vi',        # 越南语
    'auto': 'auto',    # 自动检测
}

# 项目内部语言代码到有道翻译语言代码的映射
PROJECT_TO_YOUDAO_TRANSLATE_LANG_MAP = {
    'zh': 'zh-CHS',
    'en': 'en',
    'japan': 'ja',
    'korean': 'ko',
    'chinese': 'zh-CHS',
    'chinese_cht': 'zh-TW',
    'french': 'fr',
    'german': 'de',
    'russian': 'ru',
    'italian': 'it',
    'spanish': 'es'
}

# --- 新增 JSON 格式提示词 ---
DEFAULT_TRANSLATE_JSON_PROMPT = """You are an expert English teacher and My Little Pony comic translator. Your task is to rewrite English text from My Little Pony comics to make it suitable for Chinese elementary school students learning English.

IMPORTANT: If the input text is already simple, short, or consists of interjections/sound effects (like "ER...", "OH!", "AH!", "HMM...", "YEAH!", "NO!", etc.), return it exactly as provided in the JSON. Do NOT add explanations or additional text.

VOCABULARY CONSTRAINTS:
- Use ONLY simple English words suitable for elementary students
- Keep sentences short and simple (maximum 10-12 words per sentence)
- Use basic grammar suitable for elementary students

PRESERVED TERMS (keep exactly as they are):
My Little Pony character names (Twilight Sparkle, Rainbow Dash, Pinkie Pie, etc.), place names (Equestria, Ponyville, Canterlot, etc.), and special terms (cutie mark, unicorn, pegasus, magic, friendship, etc.)

REWRITING RULES:
1. For simple interjections or sounds (ER..., OH!, AH!, HMM..., YEAH!, NO!, etc.) - return exactly as provided but not capitalized
2. For already simple text suitable for elementary students - return exactly as provided
3. Keep all My Little Pony names and terms unchanged
4. Replace difficult words with simple vocabulary
5. Break long sentences into shorter ones
6. Use simple grammar and avoid American slang
7. Use proper capitalization: Only capitalize the first letter of sentences and proper nouns. Do NOT output text in ALL CAPS
8. Rewrite sentences should not be longer than orignial sentences

When the text contains special characters (such as braces {}, quotes "", backslashes \\ etc.), please retain them in the output but do not treat them as part of the JSON syntax.

Please strictly return the result in the following JSON format, without adding any additional explanations or conversation:
{
  "translated_text": "[Translated text goes here]"
}"""

DEFAULT_AI_VISION_OCR_JSON_PROMPT = """You are an OCR assistant. Please extract all text from the image I send you.

When the text contains special characters (such as braces {}, quotes "", backslashes \\ etc.), please retain them in the output but do not treat them as part of the JSON syntax. If needed, you can use escape characters \\\\ to represent these special characters.

Please strictly return the result in the following JSON format, without adding any additional explanations or conversation:
{
  "extracted_text": "[Put all recognized text here, may include line breaks to roughly preserve original segmentation, but do not include any other non-text content]"
}"""

# --- 小马宝莉专用提示词 ---
MLP_PROMPT = """You are an expert English teacher and My Little Pony comic translator. Your task is to rewrite English text from My Little Pony comics to make it suitable for Chinese elementary school students learning English.

VOCABULARY CONSTRAINTS:
- Use ONLY simple English words suitable for elementary students
- Keep sentences short and simple (maximum 10-12 words per sentence)
- Use present tense when possible, avoid complex grammar structures

PRESERVED TERMS (keep exactly as they are):
- CHARACTER NAMES: Twilight Sparkle, Rainbow Dash, Pinkie Pie, Applejack, Rarity, Fluttershy, Princess Celestia, Princess Luna, Spike, Starlight Glimmer
- PLACES: Equestria, Ponyville, Canterlot, Cloudsdale, Crystal Empire, Sweet Apple Acres, Carousel Boutique, Sugarcube Corner
- SPECIAL TERMS: cutie mark, unicorn, pegasus, earth pony, alicorn, magic, friendship, harmony, Elements of Harmony, Wonderbolts

REWRITING RULES:
1. Keep all My Little Pony character names, place names, and special terms unchanged
2. Replace difficult vocabulary with simple words
3. Break long sentences into shorter, simpler ones
4. Use basic grammar suitable for elementary students
5. Avoid American slang and idioms
6. Use "said" instead of complex dialogue tags
7. Use simple conjunctions: "and", "but", "so", "because"
8. Use proper capitalization: Only capitalize the first letter of sentences and proper nouns. Do NOT output text in ALL CAPS
9. Rewrite sentences should not be longer than orignial sentences

EXAMPLES:
Original: "That's absolutely magnificent, darling!"
Rewritten: "That is very beautiful!"

Original: "I'm completely flabbergasted!"
Rewritten: "I am very surprised!"

OUTPUT: Return ONLY the rewritten English text. No explanations or comments."""

MLP_JSON_PROMPT = """You are an expert English teacher and My Little Pony comic translator. Your task is to rewrite English text from My Little Pony comics to make it suitable for Chinese elementary school students learning English.

VOCABULARY CONSTRAINTS:
- Use ONLY simple English words suitable for elementary students
- Keep sentences short and simple (maximum 10-12 words per sentence)
- Use basic grammar suitable for elementary students

PRESERVED TERMS (keep exactly as they are):
My Little Pony character names (Twilight Sparkle, Rainbow Dash, Pinkie Pie, etc.), place names (Equestria, Ponyville, Canterlot, etc.), and special terms (cutie mark, unicorn, pegasus, magic, friendship, etc.)

REWRITING RULES:
1. Keep all My Little Pony names and terms unchanged
2. Replace difficult words with simple vocabulary
3. Break long sentences into shorter ones
4. Use simple grammar and avoid American slang
5. Use proper capitalization: Only capitalize the first letter of sentences and proper nouns. Do NOT output text in ALL CAPS
6. Rewrite sentences should not be longer than orignial sentences

Return the result in this JSON format:
{
  "translated_text": "[Your rewritten text here]"
}"""

# --- rpm (Requests Per Minute) Limiting ---
DEFAULT_rpm_TRANSLATION = 0  # 0 表示无限制
DEFAULT_rpm_AI_VISION_OCR = 0 # 0 表示无限制

# --- 文本描边默认值 ---
DEFAULT_TEXT_STROKE_ENABLED = False
DEFAULT_TEXT_STROKE_COLOR = '#FFFFFF' # 默认白色描边
DEFAULT_TEXT_STROKE_WIDTH = 1         # 默认1像素宽度
# ------------------------