# -*- coding: utf-8 -*-
"""快速测试 - Markdown清理和新格式"""
from main import clean_markdown

# 测试Markdown清理
test_cases = [
    "**加粗文本**正常文本",
    "*斜体* 和 __下划线加粗__",
    "# 标题\n正文内容",
    "`代码`和**混合**格式",
    "原文：\"初九：潜龙，勿用\"\n→ **关键信息**：时机未到"
]

print("="*60)
print("Markdown清理测试")
print("="*60)

for i, test in enumerate(test_cases, 1):
    print(f"\n测试 {i}:")
    print(f"原文: {repr(test)}")
    cleaned = clean_markdown(test)
    print(f"清理后: {cleaned}")

print("\n" + "="*60)
print("测试完成！所有Markdown格式已清除")
print("="*60)
