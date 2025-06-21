// src/app/static/js/constants.js

// 这个常量在 main.js 的 loadPromptContent 和 loadTextboxPromptContent 中用到了
export const DEFAULT_PROMPT_NAME = "默认提示词";

// 你可以根据需要将其他在前端 JS 中使用的常量添加到这里
// 例如，默认字号、字体等，如果它们在多个 JS 文件中需要共享的话
// export const DEFAULT_FRONTEND_FONT_SIZE = 25;

// 如果有其他在 script.js 中定义的、需要在多个新 JS 模块中使用的常量，也移到这里并导出

// 默认气泡填充颜色（白色）
export const DEFAULT_FILL_COLOR = '#FFFFFF';

// --- 新增：自动存档常量 ---
export const AUTO_SAVE_SLOT_NAME = "__autosave__"; // 内部使用的固定名称
export const AUTO_SAVE_DISPLAY_NAME = "自动存档"; // UI上显示的名称
// ------------------------

// 新增 AI 视觉 OCR 默认提示词
export const DEFAULT_AI_VISION_OCR_PROMPT = `你是一个ocr助手，你需要将我发送给你的图片中的文字提取出来并返回给我，要求：
1、完整识别：我发送给你的图片中的文字都是需要识别的内容
2、非贪婪输出：不要返回任何其他解释和说明。`;

// --- 新增 JSON 格式默认提示词 ---
export const DEFAULT_TRANSLATE_JSON_PROMPT = `You are a professional translation engine. Please translate the user-provided text into English.\nWhen the text contains special characters (such as braces {}, quotes "", backslashes \\\\ etc.), please retain them in the output but do not treat them as part of the JSON syntax.\nPlease strictly return the result in the following JSON format, without adding any additional explanations or conversation:\n{\n  "translated_text": "[Translated text goes here]"\n}`;
export const DEFAULT_AI_VISION_OCR_JSON_PROMPT = `你是一个OCR助手。请将我发送给你的图片中的所有文字提取出来。\n当文本中包含特殊字符（如大括号{}、引号""、反斜杠\等）时，请在输出中保留它们但不要将它们视为JSON语法的一部分。如果需要，你可以使用转义字符\\来表示这些特殊字符。\n请严格按照以下 JSON 格式返回结果，不要添加任何额外的解释或对话:\n{\n  "extracted_text": "[这里放入所有识别到的文字，可以包含换行符以大致保留原始分段，但不要包含任何其他非文本内容]"\n}`;
// ----------------------------

// --- 新增：高质量翻译模式默认提示词 ---
export const DEFAULT_HQ_TRANSLATE_PROMPT = `You are a comic book translation assistant. I will provide the original comic images and an exported JSON translation file containing only the original text without translations. Please help me translate the original text into English.
Translation requirements:
1. Only modify the "translated" text content in the JSON, keeping all other structures and fields unchanged
2. The "imagelndex" number in the json is the page number of each image. Before translating, first sort all the images I give you based on the original text content of each page in the json file and all comic images, and strictly compare according to the "imagelndex" number when comparing context. You should translate in the order of "imagelndex" to make each translation coherent and the context not abrupt
3. Identify the position of each sentence on which page through the "original" text content of each page in the json and all comic images, and combine the comic images and contextual context to make the translation more coherent and natural, conforming to the character's tone and scene
4. The "bubblelndex" number in the json may be incorrect. You need to judge the correct order of each sentence based on the images to output contextually coherent translations, but do not modify the original "bubblelndex" number when outputting translations
5. Preserve the original expression intent and emotion, but use more natural and fluent expressions
6. Pay attention to consistent translation of proper nouns and terms
7. When encountering humor, puns, or culture-specific content, try to find appropriate expressions in the target language
8. Do not add information or explanations that do not exist in the original text
9. Keep it concise and clear, conforming to bubble space limitations
10. Try not to exceed the original text in word count
11. You need to directly return the complete modified JSON file without explaining the reasons for each modification.`;

// AI校对的默认提示词
export const DEFAULT_PROOFREADING_PROMPT = `You are a professional comic proofreading assistant. Please help me proofread comic translation results. I will give you the original untranslated comic images and a JSON file composed of the original comic text and existing translation text. Please check and improve the translation quality based on the image content and contextual relationships.
Proofreading points:
1. The "imagelndex" number in the json is the page number of each image. Before proofreading, first sort all the images I give you based on the original text content of each page in the json file and all comic images, and strictly compare according to the "imagelndex" number when comparing context. You should proofread in the order of "imagelndex" to make each translation coherent and the context not abrupt
2. Identify the position of each sentence on which page through the "original" text content of each page in the json and all comic images, and combine the comic images and contextual context to make the translation more coherent and natural, conforming to the character's tone and scene
3. The "bubblelndex" number in the json may be incorrect. You need to judge the correct order of each sentence based on the images to output contextually coherent translations, but do not modify the original "bubblelndex" number when outputting translations
4. Unify translations for special terms or proper nouns
5. Focus on easily confused pronouns and tone words
6. Correct any grammatical or expression errors
Please directly return the modified JSON data, keeping the original format and only updating the content of the "translated" field.`;
// -----------------------------------------

// --- 新增 rpm 默认值 ---
export const DEFAULT_rpm_TRANSLATION = 0; // 0 表示无限制
export const DEFAULT_rpm_AI_VISION_OCR = 0;
// ------------------------

// --- 新增：自定义 AI 视觉 OCR 服务商 ID (前端使用) ---
export const CUSTOM_AI_VISION_PROVIDER_ID_FRONTEND = 'custom_openai_vision';
// ----------------------------------------------------
