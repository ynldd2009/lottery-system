#!/bin/bash
# 启动彩票分析预测系统 Web 服务器

echo "======================================"
echo "彩票分析预测系统 - Web 服务器启动脚本"
echo "======================================"
echo ""

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python 版本: $python_version"

# 检查依赖
echo "检查依赖..."
if python3 -c "import flask" 2>/dev/null; then
    echo "✓ Flask 已安装"
else
    echo "✗ Flask 未安装"
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
fi

# 获取本机 IP
echo ""
echo "网络信息:"
echo "--------------------------------"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    local_ip=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    local_ip=$(hostname -I | awk '{print $1}')
else
    local_ip="无法自动检测"
fi

echo "本机 IP: $local_ip"
echo ""
echo "访问方式:"
echo "  电脑访问: http://localhost:5000"
echo "  手机访问: http://$local_ip:5000"
echo "--------------------------------"
echo ""

# 启动服务器
echo "正在启动 Web 服务器..."
echo "按 Ctrl+C 停止服务器"
echo ""

python3 web_app.py
