#!/usr/bin/env python3
"""
测试脚本：验证号码按钮显示
Test script to verify number button display
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QGridLayout
from PySide6.QtCore import Qt

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ui.number_button import NumberButton


class NumberButtonTestWindow(QMainWindow):
    """测试窗口用于验证号码按钮显示"""
    
    def __init__(self):
        super().__init__()
        self.selected_numbers = []
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("号码按钮显示测试 - Number Button Display Test")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("号码按钮显示测试")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Test Case 1: 双色球红球 (1-33)
        ssq_group = QGroupBox("测试1: 双色球红球 (1-33)")
        ssq_layout = QGridLayout(ssq_group)
        
        for i in range(1, 34):
            row = (i - 1) // 7
            col = (i - 1) % 7
            btn = NumberButton(i)
            btn.number_selected.connect(self.on_number_selected)
            ssq_layout.addWidget(btn, row, col)
        
        layout.addWidget(ssq_group)
        
        # Test Case 2: 双色球蓝球 (1-16)
        blue_group = QGroupBox("测试2: 双色球蓝球 (1-16)")
        blue_layout = QHBoxLayout(blue_group)
        
        for i in range(1, 17):
            btn = NumberButton(i)
            btn.number_selected.connect(self.on_number_selected)
            blue_layout.addWidget(btn)
        
        blue_layout.addStretch()
        layout.addWidget(blue_group)
        
        # Test Case 3: 大乐透前区 (1-35)
        dlt_group = QGroupBox("测试3: 大乐透前区 (1-35, 显示前14个)")
        dlt_layout = QGridLayout(dlt_group)
        
        for i in range(1, 15):
            row = (i - 1) // 7
            col = (i - 1) % 7
            btn = NumberButton(i)
            btn.number_selected.connect(self.on_number_selected)
            dlt_layout.addWidget(btn, row, col)
        
        layout.addWidget(dlt_group)
        
        # Selected numbers display
        self.selected_label = QLabel("已选号码: 无")
        self.selected_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.selected_label)
        
        # Status info
        status_label = QLabel("""
        ✅ 测试说明：
        - 点击号码按钮应该切换选中状态
        - 选中时应显示绿色背景
        - 未选中时应显示灰色背景
        - 鼠标悬停时应有视觉反馈
        - 所有号码应清晰可见，圆形按钮样式
        """)
        status_label.setStyleSheet("background-color: #e8f5e9; padding: 10px; border-left: 4px solid #4CAF50;")
        layout.addWidget(status_label)
    
    def on_number_selected(self, number, is_selected):
        """处理号码选择"""
        if is_selected:
            if number not in self.selected_numbers:
                self.selected_numbers.append(number)
        else:
            if number in self.selected_numbers:
                self.selected_numbers.remove(number)
        
        # Update display
        self.selected_numbers.sort()
        if self.selected_numbers:
            numbers_str = ", ".join([str(n) for n in self.selected_numbers])
            self.selected_label.setText(f"已选号码: {numbers_str} (共 {len(self.selected_numbers)} 个)")
        else:
            self.selected_label.setText("已选号码: 无")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = NumberButtonTestWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
