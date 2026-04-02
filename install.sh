#!/bin/bash
# 一键安装脚本（macOS/Linux）
# 使用方法：chmod +x install.sh && ./install.sh

echo "====================================="
echo "小红书财经自动化技能 - 一键安装"
echo "====================================="
echo ""

# 检查 Node.js
echo "[1/5] 检查 Node.js..."
if command -v node &> /dev/null; then
    echo "✓ Node.js 已安装：$(node --version)"
else
    echo "✗ Node.js 未安装，请先安装：https://nodejs.org/"
    exit 1
fi

# 检查 Python
echo "[2/5] 检查 Python..."
if command -v python3 &> /dev/null; then
    echo "✓ Python 已安装：$(python3 --version)"
else
    echo "✗ Python 未安装，请先安装：https://www.python.org/"
    exit 1
fi

# 安装 Node.js 依赖
echo "[3/5] 安装 Node.js 依赖..."
npm install
if [ $? -eq 0 ]; then
    echo "✓ Node.js 依赖安装完成"
else
    echo "✗ Node.js 依赖安装失败"
    exit 1
fi

# 安装 Python 依赖
echo "[4/5] 安装 Python 依赖..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Python 依赖安装完成"
else
    echo "✗ Python 依赖安装失败"
    exit 1
fi

# 创建 .env 文件
echo "[5/5] 创建配置文件..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ 已创建 .env 文件"
    echo "⚠️ 请编辑 .env 文件，填入你的 GEMINI_API_KEY"
else
    echo "✓ .env 文件已存在"
fi

echo ""
echo "====================================="
echo "安装完成！"
echo "====================================="
echo ""
echo "下一步："
echo "1. 编辑 .env 文件，填入 GEMINI_API_KEY"
echo "2. 配置小红书 Cookies（见 INSTALL-OPENCLAW.md）"
echo "3. 启动 xiaohongshu-mcp 服务"
echo "4. 在 OpenClaw 中说：'发今天的小红书'"
echo ""
