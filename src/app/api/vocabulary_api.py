#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词汇分析API端点
"""

import os
import json
from flask import Blueprint, request, jsonify, send_file
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

vocabulary_api = Blueprint('vocabulary_api', __name__)

@vocabulary_api.route('/api/vocabulary/reports', methods=['GET'])
def get_vocabulary_reports():
    """获取词汇分析报告列表"""
    try:
        reports_dir = Path("data/vocabulary_analysis")
        if not reports_dir.exists():
            return jsonify({
                'success': False,
                'message': '尚未生成词汇分析报告'
            })
        
        reports = []
        for file in reports_dir.glob("*.md"):
            stat = file.stat()
            reports.append({
                'filename': file.name,
                'path': str(file),
                'size': stat.st_size,
                'modified': stat.st_mtime
            })
        
        # 按修改时间排序
        reports.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({
            'success': True,
            'reports': reports
        })
    
    except Exception as e:
        logger.error(f"获取词汇分析报告失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取报告失败: {str(e)}'
        })

@vocabulary_api.route('/api/vocabulary/report/<filename>', methods=['GET'])
def get_vocabulary_report(filename):
    """获取单个词汇分析报告内容"""
    try:
        report_path = Path("data/vocabulary_analysis") / filename
        if not report_path.exists():
            return jsonify({
                'success': False,
                'message': '报告文件不存在'
            })
        
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'success': True,
            'filename': filename,
            'content': content
        })
    
    except Exception as e:
        logger.error(f"读取词汇分析报告失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'读取报告失败: {str(e)}'
        })

@vocabulary_api.route('/api/vocabulary/download/<filename>', methods=['GET'])
def download_vocabulary_report(filename):
    """下载词汇分析报告"""
    try:
        report_path = Path("data/vocabulary_analysis") / filename
        if not report_path.exists():
            return jsonify({
                'success': False,
                'message': '报告文件不存在'
            })
        
        return send_file(
            str(report_path),
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        logger.error(f"下载词汇分析报告失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'下载报告失败: {str(e)}'
        })

@vocabulary_api.route('/api/vocabulary/stats', methods=['GET'])
def get_vocabulary_stats():
    """获取词汇学习统计"""
    try:
        reports_dir = Path("data/vocabulary_analysis")
        if not reports_dir.exists():
            return jsonify({
                'success': False,
                'message': '尚未生成词汇分析报告'
            })
        
        stats = {
            'total_reports': 0,
            'total_words_analyzed': 0,
            'total_new_words': 0,
            'recent_reports': []
        }
        
        # 统计报告数量
        md_files = list(reports_dir.glob("*.md"))
        stats['total_reports'] = len(md_files)
        
        # 获取最近的报告
        recent_files = sorted(md_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
        for file in recent_files:
            stats['recent_reports'].append({
                'filename': file.name,
                'modified': file.stat().st_mtime
            })
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        logger.error(f"获取词汇统计失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取统计失败: {str(e)}'
        })
