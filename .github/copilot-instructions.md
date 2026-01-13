# Copilot 使用说明（彩票分析系统）

## 项目概览
**彩票分析与预测系统** - Python 构建的中文彩票数据分析平台，支持多个彩票类型（8种）、多端访问（Web、桌面GUI、CLI）、7种预测算法、数据导入导出。

完整实现位于 `origin/copilot/develop-lottery-analysis-system` 分支。当前 main 分支为开发骨架。

## 核心架构

### 三层架构 + 配置层
```
User Interface (Web/Desktop/CLI)
    ↓
Business Logic (PredictionEngine, DataAnalyzer, RecordManager)
    ↓
Data Handling (DataHandler, LotteryTypes config)
    ↓
External (API, CSV/JSON/Excel files)
```

### 关键目录结构
- `src/core/` - 核心业务逻辑：`prediction_engine.py`（7种算法）、`data_analyzer.py`（统计分析）、`record_manager.py`（记录管理）
- `src/ui/` - UI 层：`lottery_app.py`（PySide6 桌面应用）、`number_button.py`（自定义按钮）
- `src/config/` - 配置管理：`lottery_types.py`（8 种彩票定义）、`config_manager.py`（JSON 配置）
- `src/data/` - 数据处理：`data_handler.py`（导入/导出 CSV/JSON/Excel）、`visualizer.py`（图表生成）
- `src/utils/` - 工具：`api_client.py`（API 调用）、`password_generator.py`（密码生成）
- `static/` + `templates/` - Flask Web 前端（响应式设计）
- `main.py` - 桌面应用入口 | `web_app.py` - Web 服务器 | `demo_cli.py` - CLI 演示

### 支持的彩票类型 (8 种)
- **中国体彩**：大乐透、七星彩、排列三、排列五
- **中国福彩**：双色球、快乐8、七乐彩、福彩3D

每种彩票在 `config.json` 中定义：`red_count`、`blue_count`、`number_range`、`price`、`deadline`

## 关键代码模式

### 预测算法
`PredictionEngine` 实现 7 种算法，返回 `List[int]`：
1. `predict_by_frequency()` - 历史频率排序
2. `predict_hot_cold()` - 热号/冷号分析
3. `predict_pattern_balanced()` - 模式平衡预测
4. `predict_weighted_frequency()` - 近期数据加权
5. `predict_gap_analysis()` - "债位"预测（缺失号码）
6. `predict_moving_average()` - 趋势平均
7. `predict_cyclic()` - 周期模式检测

集成预测：`predict_ensemble()` 组合所有算法并评分置信度

### 典型工作流
```python
# 数据导入与预测
1. DataHandler.load_data(file_path) → DataFrame
2. DataAnalyzer.load_data(df) → 构建统计缓存
3. PredictionEngine.predict_ensemble() → [(num, confidence), ...]
4. RecordManager.save_record(prediction) → 保存到 JSON
5. DataHandler.export_data('csv'|'json'|'excel') → 导出文件
```

### 彩票配置查询模式
```python
from src.config.lottery_types import get_lottery_type
lottery = get_lottery_type("大乐透")
# 返回对象属性：red_count, blue_count, number_range, price, deadline
```

## 技术栈与依赖
- **框架**：Flask 2.3+（Web）、PySide6 6.5+（桌面 GUI）
- **数据**：Pandas 2.0+、NumPy 1.24+、SciPy 1.11+
- **存储**：JSON（配置/记录）、CSV/Excel（数据导入导出）
- **可视化**：Matplotlib、Pillow（二维码）
- **通信**：Requests、Flask-CORS

## 启动和测试

### Web 界面（推荐 - 支持移动访问）
```bash
pip install -r requirements.txt
python web_app.py
# 访问 http://localhost:5000（本地）或 http://<IP>:5000（移动设备）
```

### 桌面应用
```bash
pip install -r requirements.txt
python main.py
```

### CLI 演示
```bash
python demo_cli.py
```

### 单元测试
```bash
python test_number_buttons.py  # 按钮验证测试
```

## 项目特有约定

### 1. 中文路径处理
路径包含中文和空格，需要妥善编码：
```bash
cd "./完整原型：前端 + 后端 — auth"
# 或在脚本中使用: import urllib.parse; urllib.parse.quote(path)
```

### 2. 模块导入规范
- 使用相对导入：`from ..config import lottery_types`
- 所有模块目录都有 `__init__.py` 初始化

### 3. 配置驱动开发
彩票参数（号码范围、球数、价格、截止时间）必须定义在 `config.json` 中，通过 `get_lottery_type()` 统一查询。硬编码参数需要立即重构。

### 4. 错误处理策略
数据分析异常不中断流程，返回空值或默认随机数，保证系统可用性。

## 常见问题排查

| 问题 | 排查位置 |
|------|--------|
| 未识别彩票类型 | `config.json` 定义 + `src/config/lottery_types.py` |
| 预测结果不合理 | `src/core/prediction_engine.py` 算法逻辑 + `DataAnalyzer.get_frequency_analysis()` |
| Web 界面空白 | `templates/` 模板文件、`static/css/style.css`、`web_app.py` API 路由 |
| 桌面应用崩溃 | `src/ui/lottery_app.py` 信号连接、`number_button.py` 绘制逻辑 |

## 修改前检查清单
- ✅ 修改在 `copilot/develop-*` 或 `feature/*` 分支进行（不在 main）
- ✅ 彩票类型修改需同时更新 `config.json` 和 `lottery_types.py`
- ✅ 算法修改后运行 `test_number_buttons.py` 和 `demo_cli.py` 验证
- ✅ Web 前端修改需测试多种屏幕尺寸（响应式规则在 `static/css/style.css`）
- ✅ 提交信息清晰简洁，中英双语都可

## 相关文档
- [WEB_DEPLOYMENT.md](https://github.com/ynldd2009/lottery-system/blob/copilot/develop-lottery-analysis-system/WEB_DEPLOYMENT.md) - Web 部署指南
- [STATISTICAL_MODELS.md](https://github.com/ynldd2009/lottery-system/blob/copilot/develop-lottery-analysis-system/STATISTICAL_MODELS.md) - 算法原理详解
- [LOTTERY_TYPES.md](https://github.com/ynldd2009/lottery-system/blob/copilot/develop-lottery-analysis-system/LOTTERY_TYPES.md) - 8 种彩票参数表
- [WEB_INTERFACE_GUIDE.md](https://github.com/ynldd2009/lottery-system/blob/copilot/develop-lottery-analysis-system/WEB_INTERFACE_GUIDE.md) - Web UI 用户操作指南
