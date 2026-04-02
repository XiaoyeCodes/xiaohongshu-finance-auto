# 一键安装脚本（Windows）
# 使用方法：右键 → 以管理员身份运行

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "小红书财经自动化技能 - 一键安装" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Node.js
Write-Host "[1/5] 检查 Node.js..." -ForegroundColor Yellow
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version
    Write-Host "✓ Node.js 已安装：$nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Node.js 未安装，请先安装：https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# 检查 Python
Write-Host "[2/5] 检查 Python..." -ForegroundColor Yellow
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host "✓ Python 已安装：$pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python 未安装，请先安装：https://www.python.org/" -ForegroundColor Red
    exit 1
}

# 安装 Node.js 依赖
Write-Host "[3/5] 安装 Node.js 依赖..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Node.js 依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "✗ Node.js 依赖安装失败" -ForegroundColor Red
    exit 1
}

# 安装 Python 依赖
Write-Host "[4/5] 安装 Python 依赖..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python 依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "✗ Python 依赖安装失败" -ForegroundColor Red
    exit 1
}

# 创建 .env 文件
Write-Host "[5/5] 创建配置文件..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ 已创建 .env 文件" -ForegroundColor Green
    Write-Host "⚠️ 请编辑 .env 文件，填入你的 GEMINI_API_KEY" -ForegroundColor Yellow
} else {
    Write-Host "✓ .env 文件已存在" -ForegroundColor Green
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "安装完成！" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "1. 编辑 .env 文件，填入 GEMINI_API_KEY" -ForegroundColor White
Write-Host "2. 配置小红书 Cookies（见 INSTALL-OPENCLAW.md）" -ForegroundColor White
Write-Host "3. 启动 xiaohongshu-mcp 服务" -ForegroundColor White
Write-Host "4. 在 OpenClaw 中说：'发今天的小红书'" -ForegroundColor White
Write-Host ""
