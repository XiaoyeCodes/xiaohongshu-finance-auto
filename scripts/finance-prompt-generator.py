#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书财经文案 → 绘图 Prompt 生成器
专为 Nano Banana Pro 优化的视觉指令生成工具
"""

import json
import re
from pathlib import Path

class FinanceVisualPlanner:
    """财经文案视觉规划器"""
    
    # 核心视觉规范（必须包含在每个 Prompt 中）
    VISUAL_SPECS = """扁平化插画，矢量艺术，2D 极简风，结构化布局，清晰的分割区域，顶部带有文字占位栏，圆润线条，简化的图标，统一的可爱卡通人物，马卡龙色系，柔和色调，干净的浅米色或奶油色背景，无明暗，无渐变，干净的色块，极简阴影，轻松治愈教育正能量"""
    
    # 文案结构类型
    STRUCTURE_TYPES = {
        "list": "清单式",  # 【1】【2】【3】或 1.2.3.
        "qa": "问答式",    # Q: A: 或 问：答：
        "myth": "误区式",  # ❌✅ 对比
        "checklist": "清单打勾式",  # □ items
        "contrast": "对比式",  # Before/After 或 之前/之后
        "story": "故事式",  # 时间线/转折点
        "default": "分点式"  # 默认分段
    }
    
    # 财经概念视觉转译词典
    CONCEPT_MAP = {
        "存钱": "存钱罐 + 金币种子",
        "理财": "发芽的硬币树",
        "副业": "多只手同时工作",
        "工资": "工资条/银行卡",
        "消费": "购物袋/钱包",
        "省钱": "小猪存钱罐",
        "投资": "向上增长的图表",
        "财务自由": "沙滩椅 + 阳光",
        "穷人思维": "灰色封闭圆圈",
        "富人思维": "金色开放光圈",
        "月光": "空钱包 + 月亮",
        "存款": "堆叠的金币",
        "被动收入": "睡觉时钱流入",
        "复利": "雪球越滚越大",
        "预算": "分类信封",
        "债务": "沉重的石头",
        "资产": "下金蛋的鹅",
        "负债": "漏水的桶",
        "收入": "流入的水流",
        "支出": "流出的水滴",
        "储蓄": "水位上升的容器",
    }
    
    def __init__(self):
        self.cashier_mascot = "25-30 岁亚洲女性，简约短发，温暖微笑，穿着柔和的针织衫"
    
    def analyze_content(self, text: str) -> dict:
        """分析文案，识别结构并提取核心观点"""
        # 提取标题
        title_match = re.search(r'标题 [：:]\s*(.+)', text)
        title = title_match.group(1) if title_match else text.split('\n')[0].strip()[:30]
        
        # 识别文案结构类型
        structure_type = self._detect_structure(text)
        
        # 根据结构类型提取内容
        if structure_type == "qa":
            sections = self._extract_qa_pairs(text)
        elif structure_type == "myth":
            sections = self._extract_myths(text)
        elif structure_type == "checklist":
            sections = self._extract_checklist(text)
        elif structure_type == "contrast":
            sections = self._extract_contrast(text)
        elif structure_type == "story":
            sections = self._extract_story_points(text)
        else:
            sections = self._extract_list(text)
        
        # 提取数据/对比
        data_points = re.findall(r'(\d+.*?(?:岁 | 万 | %|千|百|元 | 月))', text)
        
        return {
            "title": title,
            "structure": structure_type,
            "sections": sections[:4],
            "data_points": data_points[:5],
            "tone": self._detect_tone(text)
        }
    
    def _detect_structure(self, text: str) -> str:
        """识别文案结构类型"""
        if re.search(r'Q[：:\s]|问 [：:\s]|❌.*✅', text):
            return "qa" if re.search(r'Q[：:\s]|问 [：:\s]', text) else "myth"
        elif re.search(r'□|Before.*After|之前.*之后', text):
            return "checklist" if '□' in text else "contrast"
        elif re.search(r'那年 | 今天 | 后来 | 上周', text):
            return "story"
        elif re.search(r'[【\(](\d+)[】\)]', text):
            return "list"
        else:
            return "default"
    
    def plan_structure(self, analysis: dict) -> list:
        """根据文案结构类型规划图片结构"""
        structure = analysis["structure"]
        
        # 根据结构类型匹配配图方案
        if structure == "qa":
            return self._plan_qa_structure(analysis)
        elif structure == "myth":
            return self._plan_myth_structure(analysis)
        elif structure == "checklist":
            return self._plan_checklist_structure(analysis)
        elif structure == "contrast":
            return self._plan_contrast_structure(analysis)
        elif structure == "story":
            return self._plan_story_structure(analysis)
        else:
            return self._plan_default_structure(analysis)
    
    def _plan_qa_structure(self, analysis: dict) -> list:
        """问答式配图方案"""
        return [
            {"type": "question", "title": "核心问题", "focus": analysis["title"]},
            {"type": "qa_pairs", "title": "问答展示", "focus": "2-3 个核心 Q&A"},
            {"type": "answer", "title": "关键答案", "focus": analysis["sections"][0] if analysis["sections"] else "解决方案"},
        ]
    
    def _plan_myth_structure(self, analysis: dict) -> list:
        """误区式配图方案"""
        return [
            {"type": "myth_title", "title": "主题", "focus": "90% 的人都搞错了"},
            {"type": "myths", "title": "误区对比", "focus": "❌误区 vs✅真相"},
            {"type": "truth", "title": "真相总结", "focus": "正确做法"},
        ]
    
    def _plan_checklist_structure(self, analysis: dict) -> list:
        """清单式配图方案"""
        return [
            {"type": "checklist_title", "title": analysis["title"], "focus": "checklist"},
            {"type": "items", "title": "清单项目", "focus": "□ items 展示"},
            {"type": "progress", "title": "完成进度", "focus": "已完成 X/Y"},
        ]
    
    def _plan_contrast_structure(self, analysis: dict) -> list:
        """对比式配图方案"""
        return [
            {"type": "contrast_title", "title": analysis["title"], "focus": "对比主题"},
            {"type": "before_after", "title": "前后对比", "focus": "Before vs After"},
            {"type": "change", "title": "变化总结", "focus": "核心变化"},
        ]
    
    def _plan_story_structure(self, analysis: dict) -> list:
        """故事式配图方案"""
        return [
            {"type": "story_start", "title": "故事开头", "focus": "时间/人物/场景"},
            {"type": "turning_point", "title": "关键转折", "focus": "转折点事件"},
            {"type": "ending", "title": "结局/感悟", "focus": "现在的状态"},
        ]
    
    def _plan_default_structure(self, analysis: dict) -> list:
        """默认分点式配图方案"""
        return [
            {"type": "cover", "title": analysis["title"], "focus": "主题吸引"},
            {"type": "points", "title": "核心观点", "focus": "分点展示"},
            {"type": "data", "title": "数据支撑", "focus": "真实数据"},
        ]
    
    def _extract_qa_pairs(self, text: str) -> list:
        """提取问答对"""
        pairs = []
        for match in re.finditer(r'(Q[：:\s]|问 [：:\s])(.+?)(A[：:\s]|答 [：:\s])(.+?)(?=Q[：:\s]|问 [：:\s]|$)', text, re.DOTALL):
            pairs.append(f"Q:{match.group(2).strip()} | A:{match.group(4).strip()}")
        return pairs if pairs else ["问答内容"]
    
    def _extract_myths(self, text: str) -> list:
        """提取误区对比"""
        myths = []
        for match in re.finditer(r'❌(.+?)✅(.+?)(?=❌|✅|$)', text, re.DOTALL):
            myths.append(f"❌{match.group(1).strip()} | ✅{match.group(2).strip()}")
        return myths if myths else ["误区对比"]
    
    def _extract_checklist(self, text: str) -> list:
        """提取清单项目"""
        items = re.findall(r'□\s*(.+?)(?=\n□|$)', text)
        return items if items else ["清单项目"]
    
    def _extract_contrast(self, text: str) -> list:
        """提取对比内容"""
        contrasts = []
        for match in re.finditer(r'(Before|之前)(.+?)(After|之后)(.+?)(?=Before|之前|$)', text, re.DOTALL):
            contrasts.append(f"Before:{match.group(2).strip()} | After:{match.group(4).strip()}")
        return contrasts if contrasts else ["前后对比"]
    
    def _extract_story_points(self, text: str) -> list:
        """提取故事关键点"""
        points = []
        for marker in ['那年', '今天', '后来', '上周', '现在']:
            match = re.search(rf'{marker}[^。.!？!?]*[。.!？!?]?', text)
            if match:
                points.append(f"{marker}:{match.group(0)}")
        return points if points else ["故事内容"]
    
    def _extract_list(self, text: str) -> list:
        """提取分点内容"""
        sections = []
        for pattern in [r'[【\(](\d+)[】\)]\s*(.+?)(?=[【\(]\d|共勉|$)', r'(\d+)\.\s*(.+?)(?=\d\.|共勉|$)']:
            matches = re.findall(pattern, text, re.DOTALL)
            for _, content in matches:
                sections.append(content.strip())
        if not sections:
            paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 20]
            sections = paragraphs[:4]
        return sections if sections else ["分点内容"]
    
    def _detect_tone(self, text: str) -> str:
        """检测文案语气"""
        if re.search(r'共勉 | 加油 | 你可以', text):
            return "治愈鼓励"
        elif re.search(r'❌|误区 | 真相', text):
            return "专业揭秘"
        elif re.search(r'Q[：:\s]|问 [：:\s]', text):
            return "互动问答"
        else:
            return "专业教育"
    
    def translate_to_visual(self, text: str) -> str:
        """将文字概念转译为视觉元素"""
        visual_elements = []
        
        for concept, visual in self.CONCEPT_MAP.items():
            if concept in text:
                visual_elements.append(visual)
        
        return "，".join(visual_elements) if visual_elements else "理财相关元素"
    
    def generate_prompt(self, image_plan: dict, index: int, total: int) -> str:
        """生成单张图片的完整 Prompt"""
        
        # 根据图片类型定制描述
        type_descriptions = {
            "cover": f"封面设计，醒目的大标题区域，{self.cashier_mascot}站在画面中央，周围环绕金币和理财图标，吸引眼球",
            "pain_point": f"痛点场景，{self.cashier_mascot}困惑的表情，面前是空钱包和账单，表达烦恼但不过度负面",
            "solution": f"解决方案展示，{self.cashier_mascot}自信微笑，手持理财工具/图表，展示方法步骤",
            "result": f"结果对比，左右分割构图，左侧灰色调（之前），右侧金色调（之后），{self.cashier_mascot}从困惑到开心的转变",
            "concept": f"概念解释，{self.cashier_mascot}指向核心视觉元素，清晰的信息层级",
        }
        
        base_desc = type_descriptions.get(image_plan["type"], image_plan["focus"])
        
        # 构建完整 Prompt
        prompt = f"""一张{base_desc}，{self.translate_to_visual(image_plan["focus"])},顶部有横幅占位空间，结构化布局，马卡龙配色，柔和的粉色/绿色/米色背景，干净色块，无渐变，治愈系财经风，专业且充满正能量，{self.VISUAL_SPECS}"""
        
        return prompt
    
    def generate_all(self, content: str) -> list:
        """完整流程：分析→规划→生成所有图片的 Prompt"""
        analysis = self.analyze_content(content)
        structure = self.plan_structure(analysis)
        
        results = []
        for i, plan in enumerate(structure):
            prompt = self.generate_prompt(plan, i+1, len(structure))
            results.append({
                "index": i + 1,
                "total": len(structure),
                "type": plan["type"],
                "title": plan["title"],
                "focus": plan["focus"],
                "visual_logic": f"{plan['type']}类型图，用于展示{plan['focus']}",
                "prompt": prompt
            })
        
        return results


def main():
    # 今天的财经文案
    content = """
    标题：28 岁才明白，存不下钱真不是收入的问题
    
    以前总觉得存不下钱是因为赚得少
    现在回头看，完全是思维出了问题
    
    【1. 等有钱了再理财】
    这是我最后悔的事
    工作前 3 年，总觉得钱少没必要理
    结果就是钱一直少
    
    【2. 省钱=不花钱】
    有段时间特别极端
    奶茶不喝、外卖不点、衣服不买
    结果呢？报复性消费了
    
    【3. 工资=全部收入】
    工作了 5 年才意识到
    只靠工资很难富起来
    
    【4. 先消费后储蓄】
    以前是：收入 - 支出 = 储蓄
    现在是：收入 - 储蓄 = 支出
    """
    
    planner = FinanceVisualPlanner()
    results = planner.generate_all(content)
    
    print("=" * 80)
    print("📸 小红书财经文案 - 视觉规划方案")
    print("=" * 80)
    
    for img in results:
        print(f"\n📸 图片 {img['index']}/{img['total']}：{img['title']}")
        print(f"   类型：{img['type']}")
        print(f"   视觉逻辑：{img['visual_logic']}")
        print(f"\n   🎨 Nano Banana Prompt:")
        print(f"   {img['prompt']}")
        print("   " + "-" * 70)
    
    # 输出 JSON 格式供脚本使用
    print("\n\n📋 JSON 格式（供程序调用）:")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    main()
