@echo off
REM 启动彩票分析预测系统 Web 服务器 (Windows)

echo ======================================
echo 彩票分析预测系统 - Web 服务器启动脚本
echo ======================================
echo.

REM 检查 Python 版本
echo 检查 Python...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖
echo.
echo 检查依赖...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask 未安装，正在安装依赖...
    pip install -r requirements.txt
) else (
    echo Flask 已安装
)

REM 获取本机 IP
echo.
echo 网络信息:
echo --------------------------------
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set local_ip=%%a
    goto :found
)
:found
set local_ip=%local_ip:~1%

echo 本机 IP: %local_ip%
echo.
echo 访问方式:
echo   电脑访问: http://localhost:5000
echo   手机访问: http://%local_ip%:5000
echo --------------------------------
echo.

REM 启动服务器
echo 正在启动 Web 服务器...
echo 按 Ctrl+C 停止服务器
echo.

python web_app.py

pause
