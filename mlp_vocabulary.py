# My Little Pony 专有名词和改进的提示词

# 小马宝莉主要角色名字（需要保留的专有名词）
MLP_CHARACTER_NAMES = [
    # 主要角色 (Mane Six)
    "Twilight Sparkle", "Rainbow Dash", "Pinkie Pie", "Applejack", 
    "Rarity", "Fluttershy",
    
    # 公主
    "Princess Celestia", "Princess Luna", "Princess Cadance", 
    "Princess Flurry Heart",
    
    # 其他重要角色
    "Spike", "Starlight Glimmer", "Sunset Shimmer", "Trixie",
    "Shining Armor", "Big Macintosh", "Granny Smith", "Apple Bloom",
    "Sweetie Belle", "Scootaloo", "Diamond Tiara", "Silver Spoon",
    "Cheerilee", "Mayor Mare", "Derpy Hooves", "DJ Pon-3",
    "Octavia Melody", "Lyra Heartstrings", "Bon Bon",
    
    # 反派角色
    "Discord", "Queen Chrysalis", "King Sombra", "Nightmare Moon",
    "Lord Tirek", "Cozy Glow",
]

# 地名和专有名词
MLP_PLACE_NAMES = [
    "Equestria", "Ponyville", "Canterlot", "Cloudsdale", 
    "Crystal Empire", "Manehattan", "Las Pegasus",
    "Sweet Apple Acres", "Carousel Boutique", "Sugarcube Corner",
    "School of Friendship", "Castle of Friendship",
]

# 小马宝莉特有概念
MLP_SPECIAL_TERMS = [
    "cutie mark", "unicorn", "pegasus", "earth pony", "alicorn",
    "magic", "friendship", "harmony", "Elements of Harmony",
    "Wonderbolts", "Cutie Mark Crusaders", "School of Friendship",
    "Rainbow Power", "Tree of Harmony",
]

# 合并所有需要保留的专有名词
MLP_PROPER_NOUNS = MLP_CHARACTER_NAMES + MLP_PLACE_NAMES + MLP_SPECIAL_TERMS

# 小马宝莉专用提示词
MLP_SPECIALIZED_PROMPT = """You are an expert English teacher and My Little Pony comic translator. Your task is to rewrite English text from My Little Pony comics to make it suitable for Chinese elementary school students learning English.

VOCABULARY CONSTRAINTS:
- Use ONLY words from the Cambridge English A1 Movers and A2 Flyers vocabulary lists provided below
- If you must use a word not in these lists, choose the simplest possible alternative
- Keep sentences short and simple (maximum 10-12 words per sentence)
- Use present tense when possible, avoid complex grammar structures

PRESERVED TERMS:
The following My Little Pony proper nouns must be kept exactly as they are:
CHARACTERS: {character_names}
PLACES: {place_names} 
SPECIAL TERMS: {special_terms}

REWRITING RULES:
1. Keep all My Little Pony character names, place names, and special terms unchanged
2. Replace difficult vocabulary with Cambridge English vocabulary
3. Break long sentences into shorter, simpler ones
4. Use basic grammar suitable for elementary students
5. Avoid American slang and idioms
6. Use "said" instead of complex dialogue tags like "exclaimed", "whispered"
7. Use simple conjunctions: "and", "but", "so", "because"
8. Prefer active voice over passive voice

CAMBRIDGE ENGLISH VOCABULARY:
A1 MOVERS: {a1_vocabulary}

A2 FLYERS: {a2_vocabulary}

OUTPUT FORMAT:
- Return ONLY the rewritten English text
- No explanations or comments
- Maintain the emotional tone and meaning of the original
- Keep proper capitalization for proper nouns

Example:
Original: "That's absolutely magnificent, darling!"
Rewritten: "That is very beautiful!"

Original: "I'm completely flabbergasted by this revelation!"
Rewritten: "I am very surprised by this!"
"""

def get_mlp_prompt_with_vocabulary():
    """返回包含词汇表的完整小马宝莉提示词"""
    from cambridge_english import VOCABULARY, EnglishLevel
    
    # 获取词汇列表
    a1_words = list(VOCABULARY[EnglishLevel.A1_MOVERS])
    a2_words = list(VOCABULARY[EnglishLevel.A2_FLYERS])
    
    # 格式化提示词
    return MLP_SPECIALIZED_PROMPT.format(
        character_names=", ".join(MLP_CHARACTER_NAMES),
        place_names=", ".join(MLP_PLACE_NAMES),
        special_terms=", ".join(MLP_SPECIAL_TERMS),
        a1_vocabulary=", ".join(a1_words[:100]) + "...(truncated for space)",
        a2_vocabulary=", ".join(a2_words[:100]) + "...(truncated for space)"
    )

# JSON格式的小马宝莉提示词
MLP_JSON_PROMPT = """You are an expert English teacher and My Little Pony comic translator. Your task is to rewrite English text from My Little Pony comics to make it suitable for Chinese elementary school students learning English.

VOCABULARY CONSTRAINTS:
- Use ONLY words from Cambridge English A1 Movers and A2 Flyers vocabulary
- Keep sentences short and simple (maximum 10-12 words per sentence)
- Use basic grammar suitable for elementary students

PRESERVED TERMS:
Keep these My Little Pony proper nouns exactly as they are:
{proper_nouns}

REWRITING RULES:
1. Keep all My Little Pony names and terms unchanged
2. Replace difficult words with simple Cambridge English vocabulary
3. Break long sentences into shorter ones
4. Use simple grammar and avoid American slang
5. Use "said" for dialogue tags, "and/but/so/because" for connections

Return the result in this JSON format:
{{
  "translated_text": "[Your rewritten text here]"
}}
"""

def get_mlp_json_prompt():
    """返回JSON格式的小马宝莉提示词"""
    return MLP_JSON_PROMPT.format(
        proper_nouns=", ".join(MLP_PROPER_NOUNS[:30]) + "...(and others)"
    )
