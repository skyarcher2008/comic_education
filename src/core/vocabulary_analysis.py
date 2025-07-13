#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词汇分析模块 - 分析翻译结果中的生词
"""

import re
import logging
from typing import List, Dict, Set, Tuple
from collections import defaultdict
from pathlib import Path
import json

from cambridge_english import VOCABULARY, EnglishLevel

logger = logging.getLogger(__name__)

# 常见专有名词和人名模式
PROPER_NOUN_PATTERNS = [
    r'^[A-Z][a-z]+$',  # 首字母大写的单词
    r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$',  # 多个首字母大写的词组
]

# 常见人名前缀/后缀
NAME_INDICATORS = {
    'prefixes': ['mr', 'mrs', 'miss', 'ms', 'dr', 'prof', 'sir', 'lady'],
    'suffixes': ['jr', 'sr', 'ii', 'iii', 'iv']
}

# 需要忽略的词汇（标点符号、数字等）
IGNORE_PATTERNS = [
    r'^\d+$',  # 纯数字
    r'^[^\w\s]+$',  # 纯标点符号
    r'^[a-zA-Z]{1,2}$',  # 单个或两个字母（可能是缩写）
]

class VocabularyAnalyzer:
    """词汇分析器"""
    
    def __init__(self):
        self.cambridge_words = self._load_cambridge_vocabulary()
        self.analysis_results = {}
        
    def _load_cambridge_vocabulary(self) -> Set[str]:
        """加载剑桥少儿英语词汇表"""
        all_words = set()
        for level_words in VOCABULARY.values():
            for word in level_words:
                # 处理词组，将其拆分为单个单词
                words = re.findall(r'\b[a-zA-Z]+\b', word.lower())
                all_words.update(words)
        
        logger.info(f"加载剑桥少儿英语词汇表: {len(all_words)} 个单词")
        return all_words
    
    def _extract_words_from_text(self, text: str) -> List[str]:
        """从文本中提取单词"""
        # 使用正则表达式提取单词，保留原始大小写
        words = re.findall(r'\b[a-zA-Z]+(?:\'[a-zA-Z]+)?\b', text)
        return words
    
    def _is_proper_noun(self, word: str) -> bool:
        """判断是否为专有名词"""
        # 检查是否符合专有名词模式
        for pattern in PROPER_NOUN_PATTERNS:
            if re.match(pattern, word):
                return True
        return False
    
    def _is_name(self, word: str, context_words: List[str] = None) -> bool:
        """判断是否为人名"""
        word_lower = word.lower()
        
        # 检查是否有人名指示词
        if context_words:
            for i, ctx_word in enumerate(context_words):
                if ctx_word.lower() == word_lower:
                    # 检查前后是否有称谓
                    if i > 0 and context_words[i-1].lower() in NAME_INDICATORS['prefixes']:
                        return True
                    if i < len(context_words) - 1 and context_words[i+1].lower() in NAME_INDICATORS['suffixes']:
                        return True
        
        # 简单启发式：首字母大写且不在常见单词中
        if word[0].isupper() and word_lower not in self.cambridge_words:
            return True
        
        return False
    
    def _should_ignore(self, word: str) -> bool:
        """判断是否应该忽略该词"""
        for pattern in IGNORE_PATTERNS:
            if re.match(pattern, word):
                return True
        return False
    
    def analyze_text(self, text: str, source_info: str = "") -> Dict:
        """分析文本中的词汇"""
        words = self._extract_words_from_text(text)
        
        # 统计词汇
        word_counts = defaultdict(int)
        for word in words:
            if not self._should_ignore(word):
                word_counts[word.lower()] += 1
        
        # 分类词汇
        result = {
            'source': source_info,
            'total_words': len(words),
            'unique_words': len(word_counts),
            'cambridge_words': {},
            'new_words': {},
            'proper_nouns': {},
            'names': {},
            'statistics': {}
        }
        
        for word_lower, count in word_counts.items():
            # 找到原始大小写形式
            original_word = next((w for w in words if w.lower() == word_lower), word_lower)
            
            if word_lower in self.cambridge_words:
                result['cambridge_words'][original_word] = count
            else:
                if self._is_name(original_word, words):
                    result['names'][original_word] = count
                elif self._is_proper_noun(original_word):
                    result['proper_nouns'][original_word] = count
                else:
                    result['new_words'][original_word] = count
        
        # 统计信息
        result['statistics'] = {
            'cambridge_words_count': len(result['cambridge_words']),
            'new_words_count': len(result['new_words']),
            'proper_nouns_count': len(result['proper_nouns']),
            'names_count': len(result['names']),
            'new_words_ratio': len(result['new_words']) / len(word_counts) if word_counts else 0
        }
        
        return result
    
    def analyze_translation_batch(self, translations: List[Dict]) -> Dict:
        """批量分析翻译结果"""
        combined_results = {
            'total_sources': len(translations),
            'cambridge_words': defaultdict(int),
            'new_words': defaultdict(int),
            'proper_nouns': defaultdict(int),
            'names': defaultdict(int),
            'statistics': {},
            'sources': []
        }
        
        for translation in translations:
            text = translation.get('text', '')
            source = translation.get('source', 'unknown')
            
            if not text:
                continue
                
            result = self.analyze_text(text, source)
            combined_results['sources'].append(result)
            
            # 合并统计
            for word, count in result['cambridge_words'].items():
                combined_results['cambridge_words'][word] += count
            for word, count in result['new_words'].items():
                combined_results['new_words'][word] += count
            for word, count in result['proper_nouns'].items():
                combined_results['proper_nouns'][word] += count
            for word, count in result['names'].items():
                combined_results['names'][word] += count
        
        # 计算总体统计
        total_unique = (len(combined_results['cambridge_words']) + 
                       len(combined_results['new_words']) + 
                       len(combined_results['proper_nouns']) + 
                       len(combined_results['names']))
        
        combined_results['statistics'] = {
            'total_unique_words': total_unique,
            'cambridge_words_count': len(combined_results['cambridge_words']),
            'new_words_count': len(combined_results['new_words']),
            'proper_nouns_count': len(combined_results['proper_nouns']),
            'names_count': len(combined_results['names']),
            'new_words_ratio': len(combined_results['new_words']) / total_unique if total_unique > 0 else 0
        }
        
        return combined_results
    
    def generate_vocabulary_report(self, analysis_result: Dict, output_path: str = None) -> str:
        """生成词汇分析报告"""
        if output_path is None:
            output_path = "data/vocabulary_analysis_report.md"
        
        # 确保输出目录存在
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 生成Markdown报告
        report_lines = []
        
        # 标题和概述
        report_lines.append("# 漫画翻译词汇分析报告")
        report_lines.append("")
        report_lines.append("## 📊 分析概述")
        report_lines.append("")
        
        stats = analysis_result['statistics']
        report_lines.append(f"- **总词汇数量**: {stats['total_unique_words']}")
        report_lines.append(f"- **剑桥词汇**: {stats['cambridge_words_count']} 个")
        report_lines.append(f"- **生词**: {stats['new_words_count']} 个")
        report_lines.append(f"- **专有名词**: {stats['proper_nouns_count']} 个")
        report_lines.append(f"- **人名**: {stats['names_count']} 个")
        report_lines.append(f"- **生词比例**: {stats['new_words_ratio']:.1%}")
        report_lines.append("")
        
        # 需要学习的生词
        if analysis_result['new_words']:
            report_lines.append("## 📚 需要学习的生词")
            report_lines.append("")
            report_lines.append("以下单词不在剑桥少儿英语词汇表中，建议提前学习：")
            report_lines.append("")
            
            # 按字母顺序排序
            sorted_words = sorted(analysis_result['new_words'].items())
            for word, count in sorted_words:
                report_lines.append(f"- **{word}** (出现 {count} 次)")
            report_lines.append("")
        
        # 专有名词
        if analysis_result['proper_nouns']:
            report_lines.append("## 🏛️ 专有名词")
            report_lines.append("")
            report_lines.append("以下是地名、机构名等专有名词：")
            report_lines.append("")
            
            sorted_nouns = sorted(analysis_result['proper_nouns'].items())
            for noun, count in sorted_nouns:
                report_lines.append(f"- **{noun}** (出现 {count} 次)")
            report_lines.append("")
        
        # 人名
        if analysis_result['names']:
            report_lines.append("## 👤 人名")
            report_lines.append("")
            report_lines.append("以下是人物姓名：")
            report_lines.append("")
            
            sorted_names = sorted(analysis_result['names'].items())
            for name, count in sorted_names:
                report_lines.append(f"- **{name}** (出现 {count} 次)")
            report_lines.append("")
        
        # 已掌握词汇
        if analysis_result['cambridge_words']:
            report_lines.append("## ✅ 已掌握词汇")
            report_lines.append("")
            report_lines.append("以下单词在剑桥少儿英语词汇表中，应该已经掌握：")
            report_lines.append("")
            
            # 只显示前50个高频词
            sorted_cambridge = sorted(analysis_result['cambridge_words'].items(), 
                                    key=lambda x: x[1], reverse=True)[:50]
            for word, count in sorted_cambridge:
                report_lines.append(f"- {word} ({count} 次)")
            
            if len(analysis_result['cambridge_words']) > 50:
                report_lines.append(f"- ... 还有 {len(analysis_result['cambridge_words']) - 50} 个词汇")
            report_lines.append("")
        
        # 学习建议
        report_lines.append("## 💡 学习建议")
        report_lines.append("")
        
        new_words_count = stats['new_words_count']
        if new_words_count == 0:
            report_lines.append("🎉 太棒了！所有词汇都在剑桥少儿英语范围内，无需额外学习。")
        elif new_words_count <= 10:
            report_lines.append("📖 生词数量较少，建议在阅读前快速预习一下生词部分。")
        elif new_words_count <= 30:
            report_lines.append("📝 生词数量适中，建议制作单词卡片进行预习。")
        else:
            report_lines.append("📚 生词数量较多，建议分批学习，或考虑降低阅读难度。")
        
        report_lines.append("")
        report_lines.append("### 学习优先级")
        report_lines.append("1. **生词** - 重点学习，影响理解")
        report_lines.append("2. **专有名词** - 了解即可，不影响语法")
        report_lines.append("3. **人名** - 知道是人名即可")
        report_lines.append("")
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        logger.info(f"词汇分析报告已保存到: {output_path}")
        return output_path
    
    def generate_word_list(self, analysis_result: Dict, output_path: str = None) -> str:
        """生成简单的单词列表文件"""
        if output_path is None:
            output_path = "data/new_words_list.txt"
        
        # 确保输出目录存在
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        lines = []
        lines.append("=== 漫画翻译生词列表 ===")
        lines.append("")
        
        # 生词
        if analysis_result['new_words']:
            lines.append("需要学习的生词:")
            lines.append("-" * 20)
            for word in sorted(analysis_result['new_words'].keys()):
                lines.append(word)
            lines.append("")
        
        # 专有名词
        if analysis_result['proper_nouns']:
            lines.append("专有名词:")
            lines.append("-" * 20)
            for noun in sorted(analysis_result['proper_nouns'].keys()):
                lines.append(noun)
            lines.append("")
        
        # 人名
        if analysis_result['names']:
            lines.append("人名:")
            lines.append("-" * 20)
            for name in sorted(analysis_result['names'].keys()):
                lines.append(name)
            lines.append("")
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"单词列表已保存到: {output_path}")
        return output_path
    
    def get_learning_statistics(self, analysis_results: List[Dict]) -> Dict:
        """获取学习统计信息"""
        stats = {
            'total_sessions': len(analysis_results),
            'total_words': 0,
            'total_new_words': 0,
            'total_proper_nouns': 0,
            'total_names': 0,
            'difficulty_levels': {
                'easy': 0,    # 生词比例 < 10%
                'medium': 0,  # 生词比例 10-30%
                'hard': 0     # 生词比例 > 30%
            },
            'word_frequency': defaultdict(int),
            'learning_progress': {
                'mastered_words': set(),
                'new_words_encountered': set(),
                'total_exposure': 0
            }
        }
        
        for result in analysis_results:
            # 累计词汇统计
            stats['total_words'] += result['statistics']['total_unique_words']
            stats['total_new_words'] += result['statistics']['new_words_count']
            stats['total_proper_nouns'] += result['statistics']['proper_nouns_count']
            stats['total_names'] += result['statistics']['names_count']
            
            # 计算难度级别
            new_words_ratio = result['statistics']['new_words_ratio']
            if new_words_ratio < 0.1:
                stats['difficulty_levels']['easy'] += 1
            elif new_words_ratio < 0.3:
                stats['difficulty_levels']['medium'] += 1
            else:
                stats['difficulty_levels']['hard'] += 1
            
            # 词汇频率统计
            for word, count in result['new_words'].items():
                stats['word_frequency'][word] += count
                stats['learning_progress']['new_words_encountered'].add(word.lower())
            
            for word, count in result['cambridge_words'].items():
                stats['learning_progress']['mastered_words'].add(word.lower())
                stats['learning_progress']['total_exposure'] += count
        
        return stats

# 便捷函数
def analyze_translation_text(text: str, source: str = "") -> Dict:
    """分析单个翻译文本"""
    analyzer = VocabularyAnalyzer()
    return analyzer.analyze_text(text, source)

def analyze_translation_files(translations: List[Dict], output_dir: str = "data/vocabulary_analysis") -> Tuple[str, str]:
    """分析翻译文件并生成报告"""
    analyzer = VocabularyAnalyzer()
    
    # 批量分析
    result = analyzer.analyze_translation_batch(translations)
    
    # 生成报告
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    report_path = analyzer.generate_vocabulary_report(
        result, 
        f"{output_dir}/vocabulary_analysis_report.md"
    )
    
    word_list_path = analyzer.generate_word_list(
        result,
        f"{output_dir}/new_words_list.txt"
    )
    
    return report_path, word_list_path
