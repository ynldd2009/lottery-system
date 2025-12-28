# Web Deployment Guide

## 彩票分析预测系统 - 网页版部署指南

本系统提供基于 Flask 的 Web 界面，支持从电脑和手机浏览器访问。

## 功能特性

### 🌐 多设备访问
- **电脑访问**: 通过桌面浏览器访问完整功能
- **手机访问**: 响应式设计，完美支持移动设备
- **平板访问**: 自适应布局，优化平板体验

### 📱 响应式界面
- 自动适配不同屏幕尺寸
- 触摸友好的交互设计
- 移动优先的用户体验

### 🔧 核心功能
1. **数据分析页面**: 生成样本数据，进行统计分析
2. **智能预测页面**: 7种算法预测，支持5种彩票类型
3. **数据管理页面**: 导入导出数据，查看数据信息
4. **实用工具页面**: 密码生成器，预测记录管理

## 快速启动

### 1. 安装依赖

```bash
# 确保已安装 Flask
pip install -r requirements.txt
```

### 2. 启动 Web 服务器

```bash
# 默认启动 (localhost:5000)
python web_app.py

# 自定义端口
python -c "from web_app import run_web_app; run_web_app(port=8080)"
```

### 3. 访问应用

#### 电脑访问
在浏览器中打开: `http://localhost:5000`

#### 手机访问
1. 确保手机和电脑在同一局域网
2. 查找电脑 IP 地址:
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig` 或 `ip addr`
3. 在手机浏览器中打开: `http://[电脑IP]:5000`
   例如: `http://192.168.1.100:5000`

## 详细配置

### 修改默认设置

编辑 `web_app.py`:

```python
if __name__ == "__main__":
    run_web_app(
        host='0.0.0.0',  # 允许外部访问
        port=5000,       # 端口号
        debug=False      # 生产环境设为 False
    )
```

### 启用调试模式

```python
run_web_app(debug=True)
```

调试模式特性:
- 代码更改自动重载
- 详细错误信息
- 交互式调试器

⚠️ **警告**: 生产环境请勿启用调试模式

## 生产部署

### 使用 Gunicorn (推荐)

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动应用 (4个工作进程)
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

### 使用 uWSGI

```bash
# 安装 uWSGI
pip install uwsgi

# 启动应用
uwsgi --http 0.0.0.0:5000 --wsgi-file web_app.py --callable app --processes 4
```

### 配置 Nginx 反向代理

创建 Nginx 配置文件 `/etc/nginx/sites-available/lottery-system`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/lottery-system/static;
    }
}
```

启用配置:
```bash
sudo ln -s /etc/nginx/sites-available/lottery-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 安全配置

### 1. 修改密钥

编辑 `web_app.py`:

```python
app.config['SECRET_KEY'] = 'your-secure-random-key-here'
```

生成安全密钥:
```python
import secrets
print(secrets.token_hex(32))
```

### 2. HTTPS 配置

使用 Let's Encrypt 获取免费 SSL 证书:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 3. 防火墙配置

```bash
# Ubuntu/Debian
sudo ufw allow 5000/tcp

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

## API 接口说明

### 数据管理 API

#### 生成样本数据
```
POST /api/generate-sample-data
Body: {"num_draws": 100}
```

#### 导入数据
```
POST /api/import-data
Form: file (CSV/JSON/Excel)
```

### 分析预测 API

#### 数据分析
```
POST /api/analyze
```

#### 生成预测
```
POST /api/predict
Body: {
    "lottery_type": "大乐透",
    "algorithm": "ensemble"
}
```

#### 所有算法预测
```
POST /api/predict-all-algorithms
Body: {"lottery_type": "大乐透"}
```

### 记录管理 API

#### 获取所有记录
```
GET /api/records
```

#### 添加记录
```
POST /api/records
Body: {
    "title": "预测标题",
    "numbers": [1, 5, 12, 23, 34],
    "notes": "备注信息"
}
```

#### 删除记录
```
DELETE /api/records/{record_id}
```

### 工具 API

#### 生成密码
```
POST /api/generate-password
Body: {
    "length": 16,
    "use_uppercase": true,
    "use_lowercase": true,
    "use_digits": true,
    "use_special": true
}
```

#### 获取彩票类型
```
GET /api/lottery-types
```

## 性能优化

### 1. 启用缓存

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/analyze', methods=['POST'])
@cache.cached(timeout=300)  # 缓存5分钟
def analyze_data():
    # ...
```

### 2. 数据库持久化

对于生产环境，建议使用数据库替代内存存储:

```python
# 使用 SQLite
import sqlite3

# 或使用 PostgreSQL/MySQL
from flask_sqlalchemy import SQLAlchemy
```

### 3. 异步处理

对于耗时操作，使用异步任务队列:

```bash
pip install celery redis
```

## 故障排除

### 问题: 无法从手机访问

**解决方案**:
1. 确保 `host='0.0.0.0'`
2. 检查防火墙设置
3. 确认手机和电脑在同一网络

### 问题: 端口被占用

**解决方案**:
```bash
# 查找占用端口的进程
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# 修改端口或终止进程
```

### 问题: 静态文件无法加载

**解决方案**:
1. 确认 `static/` 和 `templates/` 目录存在
2. 检查文件权限
3. 清除浏览器缓存

## 监控和日志

### 启用日志

```python
import logging

logging.basicConfig(
    filename='lottery_web.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 监控工具

推荐使用:
- **Prometheus + Grafana**: 性能监控
- **Sentry**: 错误追踪
- **New Relic**: 应用性能管理

## 系统要求

### 最低配置
- Python 3.8+
- 512MB RAM
- 100MB 磁盘空间

### 推荐配置
- Python 3.10+
- 2GB RAM
- 1GB 磁盘空间
- 多核 CPU

## 浏览器支持

✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+
✅ 移动浏览器 (iOS Safari, Chrome Mobile)

## 更新日志

### v1.0.0 (2024-12-15)
- ✨ 初始版本发布
- 🌐 支持电脑和手机访问
- 📊 完整的数据分析功能
- 🔮 7种预测算法
- 💾 数据导入导出
- 🛠️ 实用工具集成

## 获取帮助

- 查看完整文档: [README.md](README.md)
- 报告问题: GitHub Issues
- 贡献代码: [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
