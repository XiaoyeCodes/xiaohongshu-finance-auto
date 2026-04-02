# 小红书财经自动化发布技能

📕 自动化的"小红书财经博主"技能 - 每天自动生成真人化文案 + 配图并发布

## ✨ 核心功能

- **每日主题轮换**：8 个财经主题自动循环（理财书籍/富人思维/投资入门/财务自由/副业/消费陷阱/富人习惯/投资心态）
- **文案结构轮换**：6 种文案风格避免审美疲劳（问答式/误区式/清单式/对比式/故事式/分点式）
- **AI 配图生成**：根据文案自动生成 Nano Banana Pro 优化的绘图 prompt，生成治愈系财经风配图
- **真人化文案**：避免 AI 味，像朋友分享一样自然
- **一键发布**：预览确认后自动发布到小红书

## 📁 项目结构

```
xiaohongshu-finance-auto/
├── README.md                      # 本文件
├── SKILL.md                       # 技能描述文件
├── scripts/
│   ├── finance-prompt-generator.py  # 文案转绘图 prompt 工具
│   ├── draw.py                      # 绘图脚本（来自 quick-draw 技能）
│   └── publish.js                   # 小红书发布脚本
├── examples/
│   ├── example-c文案.md             # 文案示例
│   └── example-prompt.md            # 配图 prompt 示例
└── package.json                     # Node.js 依赖
```

## 🚀 快速开始

### 📋 前置要求

1. **小红书账号**：已登录小红书网页版（建议新号，已实名认证）
2. **Node.js**：v18+
3. **Python 3.10+**：用于绘图 prompt 生成
4. **MCP 服务**：已部署 xiaohongshu-mcp
5. **绘图 API**：Google Gemini API Key（用于 Nano Banana Pro）
6. **绘图脚本**：已包含在 `scripts/draw.py`（无需额外安装）

### 📖 OpenClaw 专用安装指南

**⚠️ 重要**：如果你使用 OpenClaw，请查看详细安装教程：

👉 **[INSTALL-OPENCLAW.md](INSTALL-OPENCLAW.md)**

包含：
- ✅ 完整的 OpenClaw 配置流程
- ✅ Cookies 导出教程（2 种方法）
- ✅ xiaohongshu-mcp 安装步骤
- ✅ API Key 配置说明
- ✅ 故障排查指南

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/YOUR_USERNAME/xiaohongshu-finance-auto.git
cd xiaohongshu-finance-auto
```

2. **安装依赖**
```bash
npm install
pip install google-genai pillow
```

3. **配置 API Key**
在 `.env` 文件中添加：
```
GEMINI_API_KEY=your_api_key_here
```

4. **配置小红书 Cookies**
- 登录 https://www.xiaohongshu.com
- 导出 cookies 到 `~/.local/bin/cookies.json`

5. **启动 MCP 服务**
```bash
xiaohongshu-mcp-windows-amd64.exe
```

### 使用方法

**最简单指令**：
```
发今天的小红书
```

**完整流程**：
1. 生成今日文案（根据日期自动轮换主题）
2. 生成配图 prompt（根据文案结构匹配视觉方案）
3. 调用绘图 API 生成配图
4. 发送预览给用户
5. 用户确认后发布到小红书

## 📊 主题轮换机制

| 日期 | 主题编号 | 主题类型 |
|------|---------|---------|
| 1 日 | 1 | 财商书籍推荐 |
| 2 日 | 2 | 穷人变富思维 |
| 3 日 | 3 | 投资入门知识 |
| 4 日 | 4 | 财务自由路径 |
| 5 日 | 5 | 搞钱副业分享 |
| 6 日 | 6 | 消费陷阱避坑 |
| 7 日 | 7 | 富人习惯解析 |
| 8 日 | 8 | 投资心态建设 |
| 9 日 | 1 | 财商书籍推荐（循环） |

计算公式：`主题编号 = (日期数 % 8) + 1`

## 🎨 文案结构轮换

为避免 AI 味和审美疲劳，每天轮换不同文案结构：

1. **问答式**：Q&A 互动，增强参与感
2. **误区式**：❌误区 vs✅真相，对比强烈
3. **清单式**：□ check items，清晰明了
4. **对比式**：Before/After，前后变化
5. **故事式**：时间线叙述，有情节
6. **分点式**：【1】【2】【3】，经典结构

## 🖼️ 配图规范

**视觉风格**：
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

## 📝 文案示例

### 示例 1：问答式（副业主题）
```
标题：下班后做什么能多赚 3000？这 5 个副业靠谱

Q：上班族有什么副业推荐？
A：这是我被问最多的问题

先说结论：
别碰刷单、点赞、打字员
那些都是割韭菜的

我做过的 5 个靠谱副业：
1️⃣ 知识付费（最推荐）...
2️⃣ 自媒体写作...
3️⃣ 技能接单...
...
```

### 示例 2：误区式（投资主题）
```
标题：关于基金定投，90% 的人都搞错了

❌ 误区 1：定投越多越好
✅ 真相：用闲钱定投，不影响生活

❌ 误区 2：下跌就停止
✅ 真相：下跌更要坚持，摊低成本

❌ 误区 3：随时可以取出
✅ 真相：至少坚持 3 年，享受复利
...
```

## ⚠️ 注意事项

### 新号运营建议
- **发布频率**：一天 1-2 篇（不要太多）
- **内容质量**：真人化文案，避免 AI 味
- **互动维护**：多回复评论，增加活跃度
- **配图质量**：高清、原创、符合调性
- **标签使用**：3-5 个热门标签即可

### 避免封号
- ❌ 不要发硬广/引流内容
- ❌ 不要抄袭/搬运
- ❌ 不要频繁发布（一天超过 5 篇）
- ❌ 不要用敏感词（保证收益、必赚等）
- ✅ 多互动（点赞、评论别人）
- ✅ 内容有价值（真实经验/数据）

## 🛠️ 技术栈

- **Node.js**：MCP 客户端
- **Python**：绘图 prompt 生成
- **Google Gemini API**：图片生成（Nano Banana Pro）
- **xiaohongshu-mcp**：小红书发布服务
- **@modelcontextprotocol/sdk**：MCP 协议

## 📄 License

MIT License

## 🙏 致谢

- [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) - 小红书 MCP 服务
- [google-genai](https://github.com/google/generative-ai-js) - Google Gemini API

---

**Made with ❤️ for 小红书财经博主们**
