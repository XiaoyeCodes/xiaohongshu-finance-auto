# OpenClaw 安装配置指南

📕 在 OpenClaw 中部署小红书财经自动化技能的完整流程

## 📋 前置检查

在开始之前，确保你已拥有：

- [ ] OpenClaw 运行环境
- [ ] 小红书账号（建议新号，已实名认证）
- [ ] Google Gemini API Key（用于 Nano Banana Pro 绘图）
- [ ] Node.js v18+
- [ ] Python 3.10+

---

## 🔧 安装步骤

### 步骤 1：克隆项目到 OpenClaw 工作区

```bash
cd C:\Users\你的用户名\.qclaw\workspace\skills
git clone https://github.com/你的用户名/xiaohongshu-finance-auto.git
```

或者手动下载：
1. 访问你的 GitHub 仓库
2. 点击 "Code" → "Download ZIP"
3. 解压到 `C:\Users\你的用户名\.qclaw\workspace\skills\xiaohongshu-finance-auto`

### 步骤 2：安装 Node.js 依赖

```bash
cd C:\Users\你的用户名\.qclaw\workspace\skills\xiaohongshu-finance-auto
npm install
```

### 步骤 3：安装 Python 依赖

```bash
pip install google-genai pillow
```

### 步骤 4：配置 API Key

在项目根目录创建 `.env` 文件：

```bash
# 创建 .env 文件
echo GEMINI_API_KEY=你的 API_KEY > .env
```

或者手动创建 `C:\Users\你的用户名\.qclaw\workspace\skills\xiaohongshu-finance-auto\.env`：

```
GEMINI_API_KEY=AIzaSy...你的完整 API_Key
```

**⚠️ 重要**：
- `.env` 文件已被 `.gitignore` 忽略，不会上传到 GitHub
- 不要分享你的 API Key
- 如果 API Key 泄露，立即在 Google Cloud Console 撤销

### 步骤 5：配置小红书 Cookies

#### 方法 1：浏览器扩展（推荐）

1. **安装扩展**
   - Chrome/Edge: 安装 [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)
   
2. **登录小红书**
   - 访问 https://www.xiaohongshu.com
   - 用手机小红书 APP 扫码登录

3. **导出 Cookies**
   - 点击浏览器工具栏的 EditThisCookie 图标
   - 点击 "导出" 按钮（向下箭头）
   - Cookies 已复制到剪贴板

4. **保存 Cookies 文件**
   - 打开记事本
   - 粘贴 JSON 内容
   - 保存为：`C:\Users\你的用户名\.local\bin\cookies.json`

#### 方法 2：开发者工具（无需扩展）

1. **登录小红书**
   - 访问 https://www.xiaohongshu.com 并登录

2. **打开开发者工具**
   - 按 `F12` 打开开发者工具
   - 切换到 **Application**（应用程序）标签

3. **复制 Cookies**
   - 左侧展开 **Cookies** → 选择 `https://www.xiaohongshu.com`
   - 右键点击任意 cookie → **复制所有为 JSON**

4. **保存文件**
   - 粘贴到记事本
   - 保存为：`C:\Users\你的用户名\.local\bin\cookies.json`

#### 验证 Cookies

```bash
# 检查 cookies 文件是否存在
dir C:\Users\你的用户名\.local\bin\cookies.json

# 查看 cookies 数量（应该 > 10 个）
Get-Content C:\Users\你的用户名\.local\bin\cookies.json | ConvertFrom-Json | Measure-Object | Select-Object -ExpandProperty Count
```

### 步骤 6：安装并启动 xiaohongshu-mcp

#### 下载 xiaohongshu-mcp

1. 访问 https://github.com/xpzouying/xiaohongshu-mcp/releases/latest
2. 下载对应系统的版本：
   - **Windows**: `xiaohongshu-mcp-windows-amd64.zip`
   - **macOS ARM**: `xiaohongshu-mcp-darwin-arm64.tar.gz`
   - **macOS Intel**: `xiaohongshu-mcp-darwin-amd64.tar.gz`
   - **Linux**: `xiaohongshu-mcp-linux-amd64.tar.gz`

#### 安装

**Windows**:
```powershell
# 创建目录
mkdir C:\Users\你的用户名\.local\bin -Force

# 解压（手动或使用命令）
# 将解压后的文件移动到 C:\Users\你的用户名\.local\bin\
```

**macOS/Linux**:
```bash
mkdir -p ~/.local/bin
tar -xzf xiaohongshu-mcp-*.tar.gz -C ~/.local/bin/
mv ~/.local/bin/xiaohongshu-mcp-* ~/.local/bin/xiaohongshu-mcp
chmod +x ~/.local/bin/xiaohongshu-mcp
```

#### 首次登录

```bash
# Windows
cd C:\Users\你的用户名\.local\bin
.\xiaohongshu-mcp-windows-amd64.exe login

# macOS/Linux
~/.local/bin/xiaohongshu-mcp login
```

会打开浏览器，用手机小红书扫码登录。

#### 启动 MCP 服务

```bash
# Windows（后台运行）
cd C:\Users\你的用户名\.local\bin
Start-Process -FilePath ".\xiaohongshu-mcp-windows-amd64.exe" -WindowStyle Hidden

# macOS/Linux（后台运行）
nohup ~/.local/bin/xiaohongshu-mcp > ~/.xiaohongshu/mcp.log 2>&1 &
```

**验证服务是否启动**：
```bash
# 检查进程
Get-Process | Where-Object {$_.ProcessName -like "*xiaohongshu*"}

# 检查端口（应该监听 18060）
netstat -ano | findstr "18060"
```

### 步骤 7：在 OpenClaw 中注册技能

编辑 OpenClaw 配置文件：

```bash
# 编辑配置文件
notepad C:\Users\你的用户名\.qclaw\openclaw.json
```

添加技能路径：

```json
{
  "skills": {
    "load": {
      "extraDirs": [
        "C:\\Users\\你的用户名\\.qclaw\\workspace\\skills\\xiaohongshu-finance-auto"
      ]
    }
  }
}
```

或者在 OpenClaw 设置界面中添加技能目录。

### 步骤 8：重启 OpenClaw

```bash
# 重启 OpenClaw 网关
openclaw gateway restart
```

或者在 OpenClaw 界面中点击重启。

---

## 🚀 使用方法

### 最简单指令

在 OpenClaw 聊天中输入：

```
发今天的小红书
```

或

```
发今日财经
```

### 完整流程

1. **生成文案**：根据日期自动选择今日主题（8 个主题轮换）
2. **生成配图 prompt**：根据文案结构匹配视觉方案（6 种结构轮换）
3. **生成配图**：调用 Nano Banana Pro 生成 2K 分辨率配图
4. **预览确认**：发送文案 + 配图给你预览
5. **发布**：你说"可以发"后，发布到小红书

### 自定义指令

```bash
# 指定文案结构
发今天的小红书，用问答式

# 指定主题
发今天的小红书，主题是副业

# 指定配图风格
发今日财经，配图要简洁点
```

---

## 🔍 故障排查

### 问题 1：发布失败，提示超时

**可能原因**：
- MCP 服务未启动
- Cookies 过期
- 网络问题

**解决方案**：
```bash
# 重启 MCP 服务
Get-Process | Where-Object {$_.ProcessName -like "*xiaohongshu*"} | Stop-Process -Force
Start-Sleep 3
cd C:\Users\你的用户名\.local\bin
Start-Process -FilePath ".\xiaohongshu-mcp-windows-amd64.exe" -WindowStyle Hidden

# 重新登录
.\xiaohongshu-login-windows-amd64.exe
```

### 问题 2：配图生成失败

**可能原因**：
- API Key 无效
- 代理问题
- Prompt 编码问题

**解决方案**：
```bash
# 检查 API Key
Get-Content .env

# 测试 API
python3 -c "from google import genai; print('OK')"

# 检查代理（如果使用）
echo $env:HTTP_PROXY
```

### 问题 3：Cookies 无效

**症状**：
- 发布时提示登录过期
- MCP 服务无法连接

**解决方案**：
1. 重新导出 cookies（参考步骤 5）
2. 确保 cookies.json 格式正确（JSON 数组）
3. 重启 MCP 服务

### 问题 4：文案 AI 味太重

**解决方案**：
- 手动编辑文案，加入个人经历
- 使用真实数据（金额、时间、百分比）
- 用口语化表达（"说实话"、"共勉"）
- 减少 emoji 使用（1-2 个即可）

---

## 📊 主题轮换表

| 日期 | 主题 | 文案结构建议 |
|------|------|-------------|
| 1/9/17... | 财商书籍推荐 | 清单式 |
| 2/10/18... | 穷人变富思维 | 对比式 |
| 3/11/19... | 投资入门知识 | 问答式 |
| 4/12/20... | 财务自由路径 | 误区式 |
| 5/13/21... | 搞钱副业分享 | 问答式 |
| 6/14/22... | 消费陷阱避坑 | 误区式 |
| 7/15/23... | 富人习惯解析 | 清单式 |
| 8/16/24... | 投资心态建设 | 故事式 |

**计算公式**：`主题编号 = (日期数 % 8) + 1`

---

## ⚠️ 注意事项

### 新号运营建议

- **发布频率**：一天 1-2 篇（不要超过 3 篇）
- **养号期**：前 7 天多发优质内容，多互动
- **内容垂直**：专注财经领域，不要发其他内容
- **互动维护**：回复每一条评论，增加活跃度

### 避免封号

- ❌ 不要发硬广/引流内容（微信号、公众号）
- ❌ 不要抄袭/搬运（会被限流）
- ❌ 不要频繁发布（一天超过 5 篇）
- ❌ 不要用敏感词（保证收益、必赚、稳赚不赔）
- ✅ 多互动（点赞、评论别人的笔记）
- ✅ 内容有价值（真实经验、数据、方法）

### API Key 安全

- ✅ 不要分享 `.env` 文件
- ✅ 不要上传 API Key 到 GitHub
- ✅ 定期更换 API Key
- ✅ 设置 API Key 使用限额

---

## 📞 获取帮助

### 常见问题

查看 [FAQ.md](FAQ.md) 或 [Issues](https://github.com/你的用户名/xiaohongshu-finance-auto/issues)

### 社区支持

- OpenClaw Discord: https://discord.gg/clawd
- 项目 Issues: https://github.com/你的用户名/xiaohongshu-finance-auto/issues

### 付费咨询

如需一对一部署指导，请联系：[你的联系方式]

---

**Happy Posting! 📕✨**

最后更新：2026-04-02
