# 大写字母控制策略修改记录

## 修改时间
2025年6月21日

## 修改内容
将所有翻译prompt中的大写字母控制策略统一修改为更严格的版本：

### 修改前
```
Use proper capitalization: Only capitalize the first letter of sentences and proper nouns. Do NOT output text in ALL CAPS unless it's genuinely meant to represent shouting or emphasis in the original context.
```

### 修改后
```
Use proper capitalization: Only capitalize the first letter of sentences and proper nouns. Do NOT output text in ALL CAPS.
```

## 修改原因
- 更严格地控制大写字母的使用
- 即使原文表示大声喊叫或强调，也要转换成小写
- 确保输出文本更适合小学生阅读

## 影响的文件和位置

### 1. src/shared/constants.py
- `DEFAULT_PROMPT` (第31行)
- `DEFAULT_TRANSLATE_JSON_PROMPT` (第242行)
- `MLP_PROMPT` (第281行)  
- `MLP_JSON_PROMPT` (第307行)

### 2. src/core/translation.py
- `sakura_prompt` (第353行)

## 修改效果
所有翻译服务（包括SiliconFlow、DeepSeek、Ollama、Sakura等）现在都将：
1. 严格控制大写字母使用
2. 只在句子首字母和专有名词使用大写
3. 不输出任何全大写文本，即使原文是强调或喊叫

## 验证
已通过grep搜索确认所有相关位置都已正确修改。

## 注意事项
- 这个修改会影响所有新的翻译结果
- 已有的翻译结果不会改变
- 重新翻译时会使用新的规则
