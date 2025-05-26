#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超星学习通题目提取工具 - Chaoxing Quiz Extractor

此脚本用于从超星学习通导出的 HTML 文件中批量提取题目、选项及正确答案，生成对应的 TXT 文件，文件名与 HTML 文件名一致。

使用说明：
    1. 将脚本放置于含有 HTML 文件的目录下。
    2. 安装依赖：pip install beautifulsoup4
    3. 运行：python chaoxing_quiz_extractor.py

Author: Jiayvyv
Date: 2025-05-26
"""
import os
import glob
from bs4 import BeautifulSoup
import re

def extract_questions(html_path):
    """
    从单个 HTML 文件中提取题目、选项及正确答案，返回格式化字符串列表
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    questions = soup.select('.questionLi')
    results = []

    for q in questions:
        # 提取题干
        qt = q.find('h3', class_='mark_name')
        if not qt:
            continue
        content = ''.join(qt.stripped_strings)
        match = re.match(r"\d+\.?\s*(?:\(单选题\))?(.*)", content)
        question_text = match.group(1).strip() if match else content

        # 提取选项
        options = {}
        for li in q.select('ul.mark_letter li'):
            text = ''.join(li.stripped_strings)
            m = re.match(r"([A-D])\.?\s*(.*)", text)
            if m and m.group(2).strip():
                options[m.group(1)] = m.group(2).strip()

        # 提取正确答案
        ans_span = q.find('span', class_='rightAnswerContent')
        answer = ans_span.get_text(strip=True) if ans_span else ''

        # 组织输出
        formatted = question_text + '\n'
        for opt in sorted(options.keys()):
            formatted += f"{opt}. {options[opt]}\n"
        formatted += f"答案：{answer}\n"
        results.append(formatted)

    return results


def main():
    """
    遍历当前目录下所有 HTML 文件，处理后输出同名 TXT 文件
    """
    html_files = glob.glob('*.html')
    if not html_files:
        print("当前目录下未找到任何 HTML 文件。")
        return

    for html_file in html_files:
        txt_file = os.path.splitext(html_file)[0] + '.txt'
        try:
            questions = extract_questions(html_file)
            if questions:
                with open(txt_file, 'w', encoding='utf-8') as f:
                    for item in questions:
                        f.write(item + '\n')
                print(f"已生成 {txt_file}")
            else:
                print(f"未在 {html_file} 中提取到任何题目。")
        except Exception as e:
            print(f"处理 {html_file} 时出错: {e}")

if __name__ == '__main__':
    main()
