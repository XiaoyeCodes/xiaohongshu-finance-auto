---
name: xiaohongshu-finance-auto
description: 小红书财经自动化发布技能。每日自动生成真人化财经文案 + 治愈系配图并发布到小红书。支持 8 个主题轮换、6 种文案结构、Nano Banana Pro 配图生成。
---

# 小红书财经自动化发布技能

## 触发场景

当用户说：
- "发今天的小红书"
- "发今日财经"
- "生成今天的小红书内容"
- "publish today's finance post"

## 核心能力

### 1. 每日主题轮换（8 个主题循环）

| 日期 | 主题 | 内容方向 |
|------|------|---------|
| 1/9/17... | 财商书籍推荐 | 《富爸爸穷爸爸》《小狗钱钱》等精华提炼 |
| 2/10/18... | 穷人变富思维 | 穷人思维 vs 富人思维对比 |
| 3/11/19... | 投资入门知识 | 基金/股票/理财基础知识 |
| 4/12/20... | 财务自由路径 | 被动收入构建、FIRE 运动 |
| 5/13/21... | 搞钱副业分享 | 副业项目、变现渠道 |
| 6/14/22... | 消费陷阱避坑 | 消费主义陷阱、省钱技巧 |
| 7/15/23... | 富人习惯解析 | 成功人士习惯、时间管理 |
| 8/16/24... | 投资心态建设 | 风险管理、长期投资心态 |

**计算公式**：`topic_id = (day_of_month % 8) + 1`

### 2. 文案结构轮换（6 种风格）

1. **问答式**：Q&A 互动，增强参与感
2. **误区式**：❌误区 vs✅真相，对比强烈
3. **清单式**：□ check items，清晰明了
4. **对比式**：Before/After，前后变化
5. **故事式**：时间线叙述，有情节
6. **分点式**：【1】【2】【3】，经典结构

### 3. 配图生成（Nano Banana Pro 优化）

**视觉规范**：
- 扁平化插画 + 矢量艺术
- 马卡龙色系 + 柔和背景
- 2D 极简风 + 结构化布局
- 可爱卡通人物（25-30 岁亚洲女性）
- 顶部文字占位栏
- 治愈系财经风

**Prompt 结构**：
```
An infographic poster for Xiaohongshu titled "[标题]" in large, clean Chinese characters.
The style is modern friendly flat vector art on a soft beige background.

顶部区域（核心问题）：[描述]
中部区域（核心内容）：[描述]
底部区域（数据/结果）：[描述]

All text in clean correct Chinese. Premium educational design with soft macaron colors. --ar 3:4
```

## 工作流程

### 步骤 1: 确定今日主题
```python
topic_id = (day_of_month % 8) + 1
topic_name = TOPICS[topic_id - 1]
```

### 步骤 2: 生成真人化文案
- 根据主题选择文案结构
- 生成标题（吸引力 + 不夸张）
- 生成正文（300-800 字，分段清晰）
- 添加标签（3-5 个热门财经标签）

### 步骤 3: 生成配图 Prompt
- 调用 `finance-prompt-generator.py`
- 根据文案结构匹配视觉方案
- 生成全中文 Prompt（Nano Banana 优化）

### 步骤 4: 生成配图
- 调用 `draw.py` 脚本
- 使用 Google Gemini API（Nano Banana Pro）
- 生成 2K 分辨率配图

### 步骤 5: 预览确认
- 发送文案 + 配图给用户
- 等待用户确认

### 步骤 6: 发布小红书
- 调用 xiaohongshu-mcp 发布接口
- 上传配图
- 发布文案

## 输出格式

### 文案示例
```markdown
标题：28 岁才明白，存不下钱真不是收入的问题

以前总觉得存不下钱是因为赚得少
现在回头看，完全是思维出了问题

【1. 等有钱了再理财】
这是我最后悔的事
工作前 3 年，总觉得钱少没必要理
结果就是钱一直少

后来强制自己每月存 20%
哪怕工资 5000 也存
现在回头看，那 3 年损失的不只是钱
是理财习惯和认知

【一些真实变化】
25 岁：月光，存款 0
26 岁：存款 5 万
27 岁：存款 12 万 + 副业收入
28 岁：存款 25 万 + 被动收入

共勉 🙏

#理财 #存钱 #富人思维 #个人成长 #搞钱
```

### 配图 Prompt 示例
```
An infographic poster for Xiaohongshu titled "28 岁才明白，存不下钱真不是收入的问题" in large, clean Chinese characters.
The style is modern friendly flat vector art on a soft beige background.

顶部区域（核心问题）：一个可爱的卡通人物看着空钱包思考，头顶有对话框"为什么存不下钱？"，旁边有工资条和账单图标。

中部区域（4 个思维转变）：四个方框展示：1."等有钱→先存钱"图标：存钱罐；2."省钱→会花钱"图标：购物袋；3."工资→多元收入"图标：多只手工作；4."消费→投资"图标：发芽的硬币。

底部区域（存款变化）：一个向上的柱状图展示"25 岁：0"→"26 岁：5 万"→"27 岁：12 万"→"28 岁：25 万"，末端有个开心的卡通人物举着"思维转变"的牌子。

All text in clean correct Chinese. Premium educational design with soft macaron colors. --ar 3:4
```

## 配置要求

### 环境变量
```bash
GEMINI_API_KEY=your_gemini_api_key
```

### 依赖服务
- xiaohongshu-mcp（小红书发布服务）
- Google Gemini API（Nano Banana Pro）

### 依赖包
```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "google-genai": "^1.0.0",
    "pillow": "^10.0.0"
  }
}
```

## 注意事项

### 内容规范
- ✅ 真人化语气（像朋友分享）
- ✅ 真实数据（具体金额/时间）
- ✅ 有价值（经验/方法/避坑）
- ❌ 避免 AI 味（工整分点、每段 emoji）
- ❌ 避免敏感词（保证收益、必赚等）
- ❌ 避免引流（微信号、公众号等）

### 发布频率
- 新号：一天 1-2 篇
- 老号：一天 2-3 篇
- 不要频繁发布（避免限流）

### 运营建议
- 多互动（回复评论、点赞别人）
- 保持垂直（专注财经领域）
- 持续输出（每天固定时间发布）
- 优化选题（根据数据调整）

## 文件结构

```
xiaohongshu-finance-auto/
├── README.md
├── SKILL.md
├── scripts/
│   ├── finance-prompt-generator.py  # 文案转绘图 prompt
│   ├── draw.py                       # 绘图脚本
│   └── publish.js                    # 发布脚本
├── examples/
│   ├── example-copy.md               # 文案示例
│   └── example-prompt.md             # Prompt 示例
└── package.json
```

## 常见问题

### Q: 文案 AI 味太重怎么办？
A: 轮换文案结构，用真人语气，加入真实经历和数据。

### Q: 配图生成失败？
A: 检查 API Key 是否有效，代理是否正常，prompt 是否全中文。

### Q: 发布后没流量？
A: 新号需要养号，多互动，内容要有价值，避免硬广。

### Q: 如何更换主题？
A: 主题根据日期自动轮换，也可手动指定主题编号。

---

**Happy Posting! 📕✨**
