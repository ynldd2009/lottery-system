# 号码按钮验证文档
# Number Button Validation Documentation

## 概述 Overview

本文档说明号码按钮组件 (NumberButton) 的验证结果。
This document describes the validation results for the NumberButton component.

## 组件位置 Component Location

- **源文件**: `src/ui/number_button.py`
- **测试脚本**: `test_number_buttons.py`

## 功能特性 Features

### 1. 视觉显示 Visual Display

- ✅ **圆形按钮样式**: 使用 `border-radius: 25px` 实现圆形外观
- ✅ **尺寸设置**: 最小 50x50px，最大 80x80px
- ✅ **字体**: 12pt 粗体，清晰可读
- ✅ **颜色方案**:
  - 未选中: 灰色背景 (#f0f0f0)，深灰文字 (#333)
  - 选中: 绿色背景 (#4CAF50)，白色文字
  - 悬停: 背景色加深

### 2. 交互功能 Interactive Features

- ✅ **点击切换**: 可通过点击切换选中/未选中状态
- ✅ **视觉反馈**: 选中状态有明显的颜色变化
- ✅ **信号发射**: 状态改变时发送 `number_selected` 信号
- ✅ **程序控制**: 支持通过 `set_selected()` 方法编程控制

### 3. 应用场景 Use Cases

号码按钮可用于以下彩票类型的号码选择：

1. **双色球 Double Color Ball**
   - 红球: 1-33
   - 蓝球: 1-16

2. **大乐透 Super Lotto**
   - 前区: 1-35
   - 后区: 1-12

3. **快乐8 Happy 8**
   - 号码: 1-80

4. **七乐彩 Seven Happy Lottery**
   - 号码: 1-30

5. **其他彩票类型** (可配置范围)

## 验证方法 Validation Method

### 运行测试脚本 Run Test Script

```bash
python test_number_buttons.py
```

### 测试内容 Test Content

测试脚本将显示三组号码按钮：

1. **测试1**: 双色球红球 (1-33) - 7列布局
2. **测试2**: 双色球蓝球 (1-16) - 水平布局
3. **测试3**: 大乐透前区 (1-35, 显示前14个) - 7列布局

### 验证检查项 Validation Checklist

- [x] 所有号码按钮正确显示
- [x] 圆形样式正确渲染
- [x] 点击可切换选中状态
- [x] 选中状态颜色变化正确 (灰 → 绿)
- [x] 未选中状态颜色正确
- [x] 鼠标悬停有视觉反馈
- [x] 已选号码列表正确更新
- [x] 信号正确发送和接收
- [x] 多个按钮可同时选中
- [x] 取消选中功能正常

## 代码实现 Implementation

### 核心功能 Core Features

```python
class NumberButton(QPushButton):
    """Custom button for lottery number selection."""
    
    number_selected = Signal(int, bool)  # 信号: 号码, 是否选中
    
    def __init__(self, number: int, parent=None):
        # 初始化按钮
        self.setCheckable(True)  # 可切换状态
        self.setMinimumSize(50, 50)  # 最小尺寸
        self.setMaximumSize(80, 80)  # 最大尺寸
        
    def _update_style(self):
        # 根据选中状态更新样式
        if self.is_selected:
            # 绿色背景，白色文字
        else:
            # 灰色背景，深色文字
```

### 样式定义 Style Definition

**未选中状态 Unselected:**
```css
background-color: #f0f0f0;
color: #333;
border: 2px solid #ccc;
border-radius: 25px;
```

**选中状态 Selected:**
```css
background-color: #4CAF50;
color: white;
border: 2px solid #45a049;
border-radius: 25px;
```

## 集成示例 Integration Example

```python
from src.ui.number_button import NumberButton

# 创建号码按钮
button = NumberButton(15)

# 连接信号
def on_selected(number, is_selected):
    print(f"号码 {number} {'选中' if is_selected else '取消选中'}")

button.number_selected.connect(on_selected)

# 程序化选中
button.set_selected(True)
```

## 验证结果 Validation Result

✅ **验证通过 PASSED**

号码按钮组件功能完整，显示正确，交互流畅。
所有功能特性按预期工作，适用于各种彩票类型的号码选择场景。

The NumberButton component is fully functional with correct display and smooth interaction.
All features work as expected and are suitable for number selection across various lottery types.

## 使用建议 Usage Recommendations

1. **布局建议**: 使用 QGridLayout 进行多行多列布局
2. **选择限制**: 根据彩票类型限制可选号码数量
3. **状态管理**: 保持已选号码列表的同步
4. **视觉提示**: 可添加已选数量显示
5. **验证逻辑**: 在提交前验证号码有效性

## 更新日志 Change Log

### 2024-12-16
- ✅ 创建验证文档
- ✅ 添加测试脚本
- ✅ 验证所有功能特性
- ✅ 确认显示正确性
