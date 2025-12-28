"""
彩票分析应用主窗口
彩票分析系统的主应用窗口。
"""

import sys
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QTabWidget, QLabel, QPushButton,
                              QTextEdit, QTableWidget, QTableWidgetItem, QFileDialog,
                              QMessageBox, QGridLayout, QGroupBox, QLineEdit, QSpinBox,
                              QHeaderView)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QPixmap

from ..config import ConfigManager
from ..core import DataAnalyzer, PredictionEngine, RecordManager
from ..data import DataHandler, DataVisualizer
from ..utils import PasswordGenerator, setup_logger, get_api_client, load_api_config, calculate_countdown
from .number_button import NumberButton
import json


class LotteryApp(QMainWindow):
    """彩票分析主应用窗口。"""
    
    def __init__(self):
        """初始化主应用程序。"""
        super().__init__()
        
        # Initialize components
        self.config_manager = ConfigManager()
        self.data_handler = DataHandler()
        self.data_analyzer = DataAnalyzer(self.config_manager.config.get('prediction', {}))
        self.prediction_engine = PredictionEngine(self.config_manager.config.get('prediction', {}))
        self.record_manager = RecordManager()
        self.password_generator = PasswordGenerator(self.config_manager.config.get('security', {}))
        self.visualizer = DataVisualizer()
        self.logger = setup_logger()
        
        # Initialize API client
        self.api_client = get_api_client()
        api_config_path = Path(__file__).parent.parent.parent / 'api_config.json'
        load_api_config(api_config_path, self.logger)
        
        # UI state
        self.selected_numbers = []
        self.current_data = None
        
        # Set up UI
        self.init_ui()
        
        self.logger.info("彩票分析系统已初始化")
    
    def init_ui(self):
        """初始化用户界面。"""
        # Window settings
        app_name = self.config_manager.get('system.app_name', '彩票分析系统')
        self.setWindowTitle(app_name)
        
        width = self.config_manager.get('ui.window_width', 1200)
        height = self.config_manager.get('ui.window_height', 800)
        self.setGeometry(100, 100, width, height)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Create tabs (Home first, then others)
        self.create_home_tab()
        self.create_analysis_tab()
        self.create_prediction_tab()
        self.create_data_management_tab()
        self.create_utilities_tab()
        
        # Start home page timer
        self.home_timer = QTimer()
        self.home_timer.timeout.connect(self.update_home_display)
        self.home_timer.start(1000)  # Update every second
        
        # Create menu bar
        self.create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage('就绪')
    
    def create_menu_bar(self):
        """创建应用程序菜单栏。"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('文件(&F)')
        
        import_action = file_menu.addAction('导入数据')
        import_action.triggered.connect(self.import_data)
        
        export_action = file_menu.addAction('导出数据')
        export_action.triggered.connect(self.export_data)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction('退出')
        exit_action.triggered.connect(self.close)
        
        # Tools menu
        tools_menu = menubar.addMenu('工具(&T)')
        
        password_action = tools_menu.addAction('生成密码')
        password_action.triggered.connect(self.show_password_generator)
        
        visualize_action = tools_menu.addAction('创建可视化')
        visualize_action.triggered.connect(self.create_visualization)
        
        # Help menu
        help_menu = menubar.addMenu('帮助(&H)')
        
        about_action = help_menu.addAction('关于')
        about_action.triggered.connect(self.show_about)
        
        faq_action = help_menu.addAction('常见问题')
        faq_action.triggered.connect(self.show_faq)
    
    def create_home_tab(self):
        """创建首页选项卡。"""
        home_tab = QWidget()
        layout = QVBoxLayout(home_tab)
        
        # Title
        title = QLabel("彩票分析系统 - 首页")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Current time label
        self.time_label = QLabel("🕐 当前时间: ")
        time_font = QFont()
        time_font.setPointSize(12)
        self.time_label.setFont(time_font)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)
        
        # Deadline info label (supports rich text for countdown)
        self.deadline_label = QLabel("⏰ 投注倒计时: ")
        deadline_font = QFont()
        deadline_font.setPointSize(11)
        self.deadline_label.setFont(deadline_font)
        self.deadline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.deadline_label.setTextFormat(Qt.TextFormat.RichText)  # Enable HTML rendering
        layout.addWidget(self.deadline_label)
        
        # Marquee/Announcement label
        self.marquee_label = QLabel("🎯 欢迎使用彩票分析系统")
        marquee_font = QFont()
        marquee_font.setPointSize(10)
        self.marquee_label.setFont(marquee_font)
        self.marquee_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.marquee_label.setStyleSheet("background-color: #ffe4b5; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.marquee_label)
        
        # Latest draw results table
        results_group = QGroupBox("最新开奖信息")
        results_layout = QVBoxLayout(results_group)
        
        self.home_results_table = QTableWidget()
        self.home_results_table.setColumnCount(5)
        self.home_results_table.setHorizontalHeaderLabels(["彩票类型", "期号", "开奖日期", "开奖号码", "状态"])
        self.home_results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.home_results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        results_layout.addWidget(self.home_results_table)
        
        layout.addWidget(results_group)
        
        # Quick action buttons
        actions_group = QGroupBox("快速操作")
        actions_layout = QHBoxLayout(actions_group)
        
        analyze_btn = QPushButton("数据分析")
        analyze_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        actions_layout.addWidget(analyze_btn)
        
        predict_btn = QPushButton("号码预测")
        predict_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(2))
        actions_layout.addWidget(predict_btn)
        
        data_btn = QPushButton("数据管理")
        data_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(3))
        actions_layout.addWidget(data_btn)
        
        layout.addWidget(actions_group)
        
        # Add tab
        self.tabs.addTab(home_tab, "首页")
        
        # Initial update
        self.update_home_display()
    
    def update_home_display(self):
        """更新首页显示"""
        # Update time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")
        self.time_label.setText(f"🕐 当前时间: {current_time}")
        
        # Update deadline info with countdown (HTML format)
        deadline_info = self.get_deadline_info()
        self.deadline_label.setText(f"⏰ 投注倒计时: {deadline_info}")
        
        # Update marquee
        self.update_marquee()
        
        # Update latest results table
        self.update_home_latest_table()
    
    
    def get_deadline_info(self):
        """获取截止时间信息（含倒计时）"""
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        
        countdown_items = []
        
        # 20:00 deadline lotteries
        if hour < 20 or (hour == 20 and minute == 0):
            countdown_20, urgent_20 = calculate_countdown(20, 0)
            if countdown_20 != "已截止":
                text = f"双色球、大乐透、快乐8 (20:00) 还剩 {countdown_20}"
                countdown_items.append((text, urgent_20))
        
        # 20:30 deadline lotteries
        if hour < 20 or (hour == 20 and minute < 30):
            countdown_2030, urgent_2030 = calculate_countdown(20, 30)
            if countdown_2030 != "已截止":
                text = f"福彩3D、排列三、排列五、七星彩、七乐彩 (20:30) 还剩 {countdown_2030}"
                countdown_items.append((text, urgent_2030))
        
        if countdown_items:
            # Format with HTML for red text on urgent items
            html_parts = []
            for text, is_urgent in countdown_items:
                if is_urgent:
                    html_parts.append(f'<span style="color: red; font-weight: bold;">{text}</span>')
                else:
                    html_parts.append(text)
            return " | ".join(html_parts)
        else:
            return "今日彩票销售已截止"
    
    def update_marquee(self):
        """更新滚动信息"""
        today = datetime.now().weekday()
        
        # 根据星期几确定开奖彩票
        if today in [0, 2, 4, 6]:  # 周一、三、五、日
            text = "🎯 今日开奖: 双色球、福彩3D、快乐8 | 祝您好运中大奖！"
        elif today in [1, 3, 5]:  # 周二、四、六
            text = "🎯 今日开奖: 大乐透、排列三、排列五、七星彩、七乐彩 | 祝您好运中大奖！"
        else:
            text = "🎯 今日开奖: 所有玩法 | 祝您好运中大奖！"
        
        self.marquee_label.setText(text)
    
    def update_home_latest_table(self):
        """更新最新开奖信息表"""
        # Try to fetch data from API
        results_data = []
        
        if self.api_client.is_configured():
            # Try to get real data from API
            lottery_types_to_fetch = ["双色球", "大乐透", "福彩3D"]
            for lottery_type in lottery_types_to_fetch:
                try:
                    draw_data = self.api_client.get_latest_draw(lottery_type)
                    if draw_data:
                        formatted = self.api_client.format_draw_result(lottery_type, draw_data)
                        if formatted:
                            # Format numbers for display
                            if lottery_type == "双色球":
                                red_nums = ", ".join([f"{n:02d}" for n in formatted['numbers']])
                                blue_num = f"{formatted['extra_numbers'][0]:02d}" if formatted['extra_numbers'] else "??"
                                numbers_str = f"{red_nums} + {blue_num}"
                            elif lottery_type == "大乐透":
                                main_nums = ", ".join([f"{n:02d}" for n in formatted['numbers']])
                                bonus_nums = ", ".join([f"{n:02d}" for n in formatted['extra_numbers']])
                                numbers_str = f"{main_nums} + {bonus_nums}"
                            else:
                                numbers_str = " ".join([str(n) for n in formatted['numbers']])
                            
                            date_str = formatted.get('draw_date', '').split()[0] if formatted.get('draw_date') else ''
                            results_data.append([
                                lottery_type,
                                f"{formatted.get('period', '')}期",
                                date_str,
                                numbers_str,
                                "已开奖"
                            ])
                except Exception as e:
                    self.logger.error(f"获取{lottery_type}数据失败: {e}")
                    continue
        
        # Fallback to sample data if API is not configured or failed
        if not results_data:
            results_data = [
                ["双色球", "2024XXX期", "2024-12-15", "03, 12, 18, 25, 28, 31 + 08", "示例数据"],
                ["大乐透", "2024XXX期", "2024-12-14", "05, 11, 19, 27, 33 + 02, 09", "示例数据"],
                ["福彩3D", "2024XXX期", "2024-12-15", "5 3 7", "示例数据"]
            ]
        
        # Update table
        self.home_results_table.setRowCount(len(results_data))
        for row, data in enumerate(results_data):
            for col, value in enumerate(data):
                self.home_results_table.setItem(row, col, QTableWidgetItem(value))
    
    def create_analysis_tab(self):
        """创建数据分析选项卡。"""
        analysis_tab = QWidget()
        layout = QVBoxLayout(analysis_tab)
        
        # Title
        title = QLabel("彩票数据分析")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Results display
        self.analysis_results = QTextEdit()
        self.analysis_results.setReadOnly(True)
        layout.addWidget(self.analysis_results)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        analyze_btn = QPushButton("运行分析")
        analyze_btn.clicked.connect(self.run_analysis)
        button_layout.addWidget(analyze_btn)
        
        clear_btn = QPushButton("清除结果")
        clear_btn.clicked.connect(lambda: self.analysis_results.clear())
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
        self.tabs.addTab(analysis_tab, "数据分析")
    
    def create_prediction_tab(self):
        """创建预测选项卡。"""
        prediction_tab = QWidget()
        layout = QVBoxLayout(prediction_tab)
        
        # Title
        title = QLabel("彩票号码预测")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Prediction settings
        settings_group = QGroupBox("预测设置")
        settings_layout = QHBoxLayout(settings_group)
        
        settings_layout.addWidget(QLabel("号码数量:"))
        self.pred_count_spin = QSpinBox()
        self.pred_count_spin.setMinimum(1)
        self.pred_count_spin.setMaximum(20)
        self.pred_count_spin.setValue(6)
        settings_layout.addWidget(self.pred_count_spin)
        
        settings_layout.addWidget(QLabel("最小号码:"))
        self.pred_min_spin = QSpinBox()
        self.pred_min_spin.setMinimum(1)
        self.pred_min_spin.setValue(1)
        settings_layout.addWidget(self.pred_min_spin)
        
        settings_layout.addWidget(QLabel("最大号码:"))
        self.pred_max_spin = QSpinBox()
        self.pred_max_spin.setMinimum(1)
        self.pred_max_spin.setMaximum(100)
        self.pred_max_spin.setValue(49)
        settings_layout.addWidget(self.pred_max_spin)
        
        settings_layout.addStretch()
        layout.addWidget(settings_group)
        
        # Prediction results
        self.prediction_results = QTextEdit()
        self.prediction_results.setReadOnly(True)
        layout.addWidget(self.prediction_results)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        predict_btn = QPushButton("生成预测")
        predict_btn.clicked.connect(self.generate_prediction)
        button_layout.addWidget(predict_btn)
        
        save_pred_btn = QPushButton("保存预测")
        save_pred_btn.clicked.connect(self.save_prediction)
        button_layout.addWidget(save_pred_btn)
        
        layout.addLayout(button_layout)
        
        # Zone-specific predictions
        zone_group = QGroupBox("🎯 专区预测")
        zone_layout = QHBoxLayout(zone_group)
        
        daletou_back_btn = QPushButton("大乐透后区预测")
        daletou_back_btn.clicked.connect(self.predict_daletou_back)
        zone_layout.addWidget(daletou_back_btn)
        
        shuangseqiu_blue_btn = QPushButton("双色球蓝球预测")
        shuangseqiu_blue_btn.clicked.connect(self.predict_shuangseqiu_blue)
        zone_layout.addWidget(shuangseqiu_blue_btn)
        
        layout.addWidget(zone_group)
        
        # Prize comparison section
        prize_group = QGroupBox("🏆 中奖对比")
        prize_layout = QVBoxLayout(prize_group)
        
        # Lottery type selector
        lottery_type_layout = QHBoxLayout()
        lottery_type_label = QLabel("彩票类型:")
        lottery_type_layout.addWidget(lottery_type_label)
        
        self.prize_lottery_type = QComboBox()
        self.prize_lottery_type.addItems(["双色球", "快乐8", "3D", "七乐彩"])
        self.prize_lottery_type.currentTextChanged.connect(self.update_prize_input_hint)
        lottery_type_layout.addWidget(self.prize_lottery_type)
        lottery_type_layout.addStretch()
        prize_layout.addLayout(lottery_type_layout)
        
        # Number selection info
        self.prize_info_label = QLabel("选择您的号码进行中奖对比 (双色球: 6个红球+1个蓝球)")
        prize_layout.addWidget(self.prize_info_label)
        
        # Number selection display
        self.prize_numbers_display = QLineEdit()
        self.prize_numbers_display.setPlaceholderText("示例: 3,9,12,13,26,32,9 (前6个红球，最后1个蓝球)")
        prize_layout.addWidget(self.prize_numbers_display)
        
        # Check button
        check_prize_btn = QPushButton("检查中奖")
        check_prize_btn.clicked.connect(self.check_prize_multi)
        prize_layout.addWidget(check_prize_btn)
        
        # Result display
        self.prize_result = QTextEdit()
        self.prize_result.setReadOnly(True)
        self.prize_result.setMaximumHeight(200)
        prize_layout.addWidget(self.prize_result)
        
        layout.addWidget(prize_group)
        
        self.tabs.addTab(prediction_tab, "号码预测")
    
    def create_data_management_tab(self):
        """创建数据管理选项卡。"""
        data_tab = QWidget()
        layout = QVBoxLayout(data_tab)
        
        # Title
        title = QLabel("数据管理")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Data table
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(3)
        self.data_table.setHorizontalHeaderLabels(['日期', '期数', '号码'])
        layout.addWidget(self.data_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        load_btn = QPushButton("加载数据")
        load_btn.clicked.connect(self.load_data_file)
        button_layout.addWidget(load_btn)
        
        sample_btn = QPushButton("生成示例数据")
        sample_btn.clicked.connect(self.generate_sample_data)
        button_layout.addWidget(sample_btn)
        
        export_btn = QPushButton("导出数据")
        export_btn.clicked.connect(self.export_data)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        self.tabs.addTab(data_tab, "数据管理")
    
    def create_utilities_tab(self):
        """创建实用工具选项卡。"""
        utils_tab = QWidget()
        layout = QVBoxLayout(utils_tab)
        
        # Title
        title = QLabel("实用工具")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Password Generator Section
        password_group = QGroupBox("密码生成器")
        password_layout = QVBoxLayout(password_group)
        
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        password_layout.addWidget(self.password_display)
        
        gen_password_btn = QPushButton("生成强密码")
        gen_password_btn.clicked.connect(self.generate_password)
        password_layout.addWidget(gen_password_btn)
        
        layout.addWidget(password_group)
        
        # Records Section
        records_group = QGroupBox("记录管理")
        records_layout = QVBoxLayout(records_group)
        
        self.records_table = QTableWidget()
        self.records_table.setColumnCount(3)
        self.records_table.setHorizontalHeaderLabels(['ID', '类型', '创建时间'])
        records_layout.addWidget(self.records_table)
        
        records_button_layout = QHBoxLayout()
        
        load_records_btn = QPushButton("加载记录")
        load_records_btn.clicked.connect(self.load_records)
        records_button_layout.addWidget(load_records_btn)
        
        export_records_btn = QPushButton("导出记录")
        export_records_btn.clicked.connect(self.export_records)
        records_button_layout.addWidget(export_records_btn)
        
        records_layout.addLayout(records_button_layout)
        
        layout.addWidget(records_group)
        
        layout.addStretch()
        
        self.tabs.addTab(utils_tab, "实用工具")
    
    def run_analysis(self):
        """对已加载的数据运行分析。"""
        if self.current_data is None or self.current_data.empty:
            QMessageBox.warning(self, "无数据", "请先加载数据。")
            return
        
        self.statusBar().showMessage('正在运行分析...')
        
        try:
            # Load data into analyzer
            self.data_analyzer.load_data(self.current_data)
            
            # Get statistics
            stats = self.data_analyzer.get_statistics_summary()
            
            # Format results
            results = "=== 彩票数据分析结果 ===\n\n"
            results += f"总期数: {stats.get('total_draws', 0)}\n\n"
            
            results += "热门号码 (最常出现):\n"
            hot_nums = stats.get('hot_numbers', [])
            results += f"{hot_nums}\n\n"
            
            results += "冷门号码 (最少出现):\n"
            cold_nums = stats.get('cold_numbers', [])
            results += f"{cold_nums}\n\n"
            
            results += "前 10 个最常见号码:\n"
            for num, freq in stats.get('most_common', []):
                results += f"  号码 {num}: {freq} 次\n"
            
            results += "\n模式分析:\n"
            patterns = stats.get('patterns', {})
            results += f"  发现的连续号码: {patterns.get('consecutive_numbers', 0)}\n"
            results += f"  奇偶比: {patterns.get('odd_even_ratio', 0):.2%}\n"
            results += f"  大小比: {patterns.get('high_low_ratio', 0):.2%}\n"
            
            self.analysis_results.setPlainText(results)
            self.statusBar().showMessage('分析完成')
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"分析失败: {str(e)}")
            self.statusBar().showMessage('分析失败')
    
    def generate_prediction(self):
        """生成彩票号码预测。"""
        if self.current_data is None or self.current_data.empty:
            QMessageBox.warning(self, "无数据", 
                              "请先加载历史数据以获得更好的预测。")
        
        self.statusBar().showMessage('正在生成预测...')
        
        try:
            # Get settings
            count = self.pred_count_spin.value()
            min_num = self.pred_min_spin.value()
            max_num = self.pred_max_spin.value()
            
            if min_num >= max_num:
                QMessageBox.warning(self, "无效范围", "最小号码必须小于最大号码。")
                return
            
            # Load data if available
            if self.current_data is not None:
                self.prediction_engine.load_historical_data(self.current_data)
            
            # Generate predictions
            result = self.prediction_engine.generate_prediction_with_confidence(
                count=count,
                number_range=(min_num, max_num)
            )
            
            # Format results
            output = "=== 彩票号码预测 ===\n\n"
            output += f"置信度: {result['confidence']:.1%}\n"
            output += f"使用数据点: {result['data_points_used']}\n"
            output += f"算法: {', '.join(result['algorithms_used'])}\n\n"
            
            output += "推荐预测 (集成):\n"
            output += f"  {result['recommended']}\n\n"
            
            output += "各算法预测:\n"
            for algo, numbers in result['predictions'].items():
                if algo != 'ensemble':
                    output += f"  {algo.title()}: {numbers}\n"
            
            self.prediction_results.setPlainText(output)
            self.statusBar().showMessage('预测已生成')
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"预测失败: {str(e)}")
            self.statusBar().showMessage('预测失败')
    
    def predict_daletou_back(self):
        """大乐透后区专用预测。"""
        if self.current_data is None or self.current_data.empty:
            QMessageBox.warning(self, "无数据", 
                              "请先加载历史数据以获得更好的预测。")
            return
        
        self.statusBar().showMessage('正在生成大乐透后区预测...')
        
        try:
            # Create engine for 大乐透
            engine = PredictionEngine(lottery_type="大乐透")
            engine.load_historical_data(self.current_data)
            
            # Generate back zone prediction
            result = engine.predict_daletou_back_zone()
            
            # Format results
            output = "=== 大乐透后区预测 ===\n\n"
            output += f"{result['description']}\n\n"
            output += f"预测结果: {result['formatted']}\n"
            output += f"号码: {result['bonus_numbers']}\n\n"
            output += f"置信度: {result['confidence']:.1%}\n"
            output += f"使用算法: {', '.join(result['algorithms_used'])}\n"
            
            self.prediction_results.setPlainText(output)
            self.statusBar().showMessage('大乐透后区预测已生成')
            
            QMessageBox.information(self, "预测完成", 
                                   f"大乐透后区预测: {result['formatted']}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"预测失败: {str(e)}")
            self.statusBar().showMessage('预测失败')
    
    def predict_shuangseqiu_blue(self):
        """双色球蓝球专用预测。"""
        if self.current_data is None or self.current_data.empty:
            QMessageBox.warning(self, "无数据", 
                              "请先加载历史数据以获得更好的预测。")
            return
        
        self.statusBar().showMessage('正在生成双色球蓝球预测...')
        
        try:
            # Create engine for 双色球
            engine = PredictionEngine(lottery_type="双色球")
            engine.load_historical_data(self.current_data)
            
            # Generate blue ball prediction
            result = engine.predict_shuangseqiu_blue_ball()
            
            # Format results
            output = "=== 双色球蓝球预测 ===\n\n"
            output += f"{result['description']}\n\n"
            output += f"预测结果: {result['formatted']}\n"
            output += f"号码: {result['blue_ball']}\n\n"
            output += f"置信度: {result['confidence']:.1%}\n"
            output += f"使用算法: {', '.join(result['algorithms_used'])}\n"
            
            self.prediction_results.setPlainText(output)
            self.statusBar().showMessage('双色球蓝球预测已生成')
            
            QMessageBox.information(self, "预测完成", 
                                   f"双色球蓝球预测: {result['formatted']}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"预测失败: {str(e)}")
            self.statusBar().showMessage('预测失败')
    
    def save_prediction(self):
        """保存当前预测到记录。"""
        prediction_text = self.prediction_results.toPlainText()
        
        if not prediction_text or prediction_text.strip() == "":
            QMessageBox.warning(self, "无预测", "请先生成预测。")
            return
        
        try:
            record = {
                'type': 'prediction',
                'title': f'预测 {len(self.record_manager.get_all_records()) + 1}',
                'description': '生成的预测',
                'data': {
                    'prediction_text': prediction_text,
                    'settings': {
                        'count': self.pred_count_spin.value(),
                        'min_num': self.pred_min_spin.value(),
                        'max_num': self.pred_max_spin.value()
                    }
                }
            }
            
            record_id = self.record_manager.add_record(record)
            QMessageBox.information(self, "成功", f"预测已保存，ID: {record_id}")
            self.statusBar().showMessage('预测已保存')
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存预测失败: {str(e)}")
    
    def import_data(self):
        """从文件导入彩票数据。"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "导入数据", "", 
            "CSV 文件 (*.csv);;JSON 文件 (*.json);;Excel 文件 (*.xlsx *.xls);;所有文件 (*)"
        )
        
        if filename:
            self.load_data_file(filename)
    
    def load_data_file(self, filename: str = None):
        """从文件加载数据。"""
        if filename is None:
            filename, _ = QFileDialog.getOpenFileName(
                self, "加载数据", "",
                "CSV 文件 (*.csv);;JSON 文件 (*.json);;Excel 文件 (*.xlsx *.xls);;所有文件 (*)"
            )
        
        if not filename:
            return
        
        self.statusBar().showMessage('正在加载数据...')
        
        try:
            file_path = Path(filename)
            
            if file_path.suffix == '.csv':
                data = self.data_handler.import_csv(filename)
            elif file_path.suffix == '.json':
                data = self.data_handler.import_json(filename)
            elif file_path.suffix in ['.xlsx', '.xls']:
                data = self.data_handler.import_excel(filename)
            else:
                QMessageBox.warning(self, "不支持的格式", 
                                  "请选择 CSV、JSON 或 Excel 文件。")
                return
            
            if data.empty:
                QMessageBox.warning(self, "无数据", "文件中没有有效数据。")
                return
            
            self.current_data = data
            self.update_data_table()
            
            QMessageBox.information(self, "成功", 
                                  f"从文件加载了 {len(data)} 条记录。")
            self.statusBar().showMessage('数据加载成功')
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载数据失败: {str(e)}")
            self.statusBar().showMessage('数据加载失败')
    
    def generate_sample_data(self):
        """生成测试用示例彩票数据。"""
        try:
            data = self.data_handler.create_sample_data(num_draws=100)
            self.current_data = data
            self.update_data_table()
            
            QMessageBox.information(self, "成功", "已生成 100 期示例彩票数据。")
            self.statusBar().showMessage('示例数据已生成')
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成示例数据失败: {str(e)}")
    
    def update_data_table(self):
        """用当前数据更新数据表。"""
        if self.current_data is None or self.current_data.empty:
            return
        
        self.data_table.setRowCount(len(self.current_data))
        
        for i, (idx, row) in enumerate(self.current_data.iterrows()):
            # Date
            date_item = QTableWidgetItem(str(row.get('date', '')))
            self.data_table.setItem(i, 0, date_item)
            
            # Draw number
            draw_item = QTableWidgetItem(str(row.get('draw_number', '')))
            self.data_table.setItem(i, 1, draw_item)
            
            # Numbers
            numbers = row.get('numbers', [])
            if isinstance(numbers, (list, tuple)):
                numbers_str = ', '.join(map(str, numbers))
            else:
                numbers_str = str(numbers)
            numbers_item = QTableWidgetItem(numbers_str)
            self.data_table.setItem(i, 2, numbers_item)
    
    def export_data(self):
        """将当前数据导出到文件。"""
        if self.current_data is None or self.current_data.empty:
            QMessageBox.warning(self, "无数据", "没有可导出的数据。")
            return
        
        filename, selected_filter = QFileDialog.getSaveFileName(
            self, "导出数据", "",
            "CSV 文件 (*.csv);;JSON 文件 (*.json);;Excel 文件 (*.xlsx);;所有文件 (*)"
        )
        
        if not filename:
            return
        
        self.statusBar().showMessage('正在导出数据...')
        
        try:
            file_path = Path(filename)
            
            if 'CSV' in selected_filter or file_path.suffix == '.csv':
                success = self.data_handler.export_csv(filename, self.current_data)
            elif 'JSON' in selected_filter or file_path.suffix == '.json':
                success = self.data_handler.export_json(filename, self.current_data)
            elif 'Excel' in selected_filter or file_path.suffix == '.xlsx':
                success = self.data_handler.export_excel(filename, self.current_data)
            else:
                success = self.data_handler.export_csv(filename + '.csv', self.current_data)
            
            if success:
                QMessageBox.information(self, "成功", "数据导出成功。")
                self.statusBar().showMessage('数据已导出')
            else:
                QMessageBox.warning(self, "导出失败", "无法导出数据。")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
            self.statusBar().showMessage('导出失败')
    
    def generate_password(self):
        """生成强密码。"""
        try:
            password = self.password_generator.generate()
            self.password_display.setText(password)
            self.statusBar().showMessage('密码已生成')
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成密码失败: {str(e)}")
    
    def show_password_generator(self):
        """显示密码生成器对话框。"""
        passwords = self.password_generator.generate_multiple(5)
        
        message = "生成的强密码:\n\n"
        for i, pwd in enumerate(passwords, 1):
            message += f"{i}. {pwd}\n"
        
        QMessageBox.information(self, "密码生成器", message)
    
    def create_visualization(self):
        """创建数据可视化。"""
        if self.current_data is None or self.current_data.empty:
            QMessageBox.warning(self, "无数据", "请先加载数据。")
            return
        
        try:
            # Load data into analyzer
            self.data_analyzer.load_data(self.current_data)
            
            # Get statistics
            frequency = self.data_analyzer.get_frequency_analysis()
            hot_nums, cold_nums = self.data_analyzer.get_hot_cold_numbers()
            
            # Create dashboard
            save_path = Path.home() / "lottery_dashboard.png"
            self.visualizer.create_analysis_dashboard(
                frequency, hot_nums, cold_nums, self.current_data, str(save_path)
            )
            
            QMessageBox.information(self, "成功", 
                                  f"仪表板已保存到:\n{save_path}")
            self.statusBar().showMessage('可视化已创建')
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"可视化失败: {str(e)}")
    
    def load_records(self):
        """加载并显示记录。"""
        try:
            records = self.record_manager.get_all_records()
            
            self.records_table.setRowCount(len(records))
            
            for i, record in enumerate(records):
                id_item = QTableWidgetItem(record.get('id', ''))
                self.records_table.setItem(i, 0, id_item)
                
                type_item = QTableWidgetItem(record.get('type', ''))
                self.records_table.setItem(i, 1, type_item)
                
                created_item = QTableWidgetItem(record.get('created_at', ''))
                self.records_table.setItem(i, 2, created_item)
            
            self.statusBar().showMessage(f'已加载 {len(records)} 条记录')
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载记录失败: {str(e)}")
    
    def export_records(self):
        """将记录导出到文件。"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出记录", "", "JSON 文件 (*.json);;所有文件 (*)"
        )
        
        if not filename:
            return
        
        try:
            success = self.record_manager.export_to_json(filename)
            
            if success:
                QMessageBox.information(self, "成功", "记录导出成功。")
            else:
                QMessageBox.warning(self, "导出失败", "无法导出记录。")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
    
    def show_about(self):
        """显示关于对话框。"""
        about_text = f"""
        <h2>{self.config_manager.get('system.app_name', '彩票分析系统')}</h2>
        <p>版本 {self.config_manager.get('system.version', '1.0.0')}</p>
        <p>一个跨平台的彩票分析和预测系统。</p>
        <p><b>功能:</b></p>
        <ul>
            <li>彩票数据的统计分析</li>
            <li>多算法预测引擎</li>
            <li>数据可视化工具</li>
            <li>记录管理</li>
            <li>密码生成</li>
        </ul>
        """
        QMessageBox.about(self, "关于", about_text)
    
    def show_faq(self):
        """显示常见问题对话框。"""
        faq_text = """
        <h3>常见问题</h3>
        
        <p><b>问: 如何导入数据?</b></p>
        <p>答: 转到 文件 > 导入数据 并选择 CSV、JSON 或 Excel 文件。</p>
        
        <p><b>问: 支持什么数据格式?</b></p>
        <p>答: 数据应该包含 'date'(日期)、'draw_number'(期数) 和 'numbers'(号码) 列。</p>
        
        <p><b>问: 预测的准确度如何?</b></p>
        <p>答: 预测基于统计分析。更多的历史数据可以提高准确度。</p>
        
        <p><b>问: 可以导出我的分析结果吗?</b></p>
        <p>答: 可以，使用导出数据或导出记录功能。</p>
        """
        QMessageBox.information(self, "常见问题", faq_text)
    
    def update_prize_input_hint(self, lottery_type):
        """更新中奖对比输入提示信息。"""
        hints = {
            "双色球": ("选择您的号码进行中奖对比 (双色球: 6个红球+1个蓝球)", 
                      "示例: 3,9,12,13,26,32,9 (前6个红球，最后1个蓝球)"),
            "快乐8": ("选择您的号码进行中奖对比 (快乐8: 10个号码)",
                     "示例: 4,7,11,17,20,22,27,29,32,34 (10个号码，1-80范围)"),
            "3D": ("选择您的号码进行中奖对比 (3D: 3个数字)",
                  "示例: 7,9,4 (3个数字，0-9范围)"),
            "七乐彩": ("选择您的号码进行中奖对比 (七乐彩: 7个号码)",
                      "示例: 5,10,14,15,16,18,23 (7个号码，1-30范围)")
        }
        
        if lottery_type in hints:
            self.prize_info_label.setText(hints[lottery_type][0])
            self.prize_numbers_display.setPlaceholderText(hints[lottery_type][1])
    
    def check_prize_multi(self):
        """检查多种彩票类型的中奖级别。"""
        lottery_type = self.prize_lottery_type.currentText()
        
        if lottery_type == "双色球":
            self.check_prize_ssq()
        elif lottery_type == "快乐8":
            self.check_prize_kl8()
        elif lottery_type == "3D":
            self.check_prize_3d()
        elif lottery_type == "七乐彩":
            self.check_prize_qlc()
    
    def check_prize_ssq(self):
        """检查双色球中奖级别。"""
        try:
            # Parse input numbers
            numbers_text = self.prize_numbers_display.text().strip()
            if not numbers_text:
                self.prize_result.setText("❌ 请输入您的号码")
                return
            
            # Parse numbers
            numbers = [int(x.strip()) for x in numbers_text.split(',')]
            
            if len(numbers) < 7:
                self.prize_result.setText("❌ 请输入至少7个号码 (6个红球 + 1个蓝球)")
                return
            
            # Split red and blue balls
            selected_red = numbers[:6]
            selected_blue = numbers[6] if len(numbers) > 6 else None
            
            # Validate red balls (1-33)
            if any(num < 1 or num > 33 for num in selected_red):
                self.prize_result.setText("❌ 红球号码必须在 1-33 之间")
                return
            
            # Validate blue ball (1-16)
            if selected_blue is None or selected_blue < 1 or selected_blue > 16:
                self.prize_result.setText("❌ 蓝球号码必须在 1-16 之间")
                return
            
            # Simulate draw numbers (in real app, these would come from actual draw data)
            draw_red = [3, 9, 12, 13, 26, 32]
            draw_blue = 9
            
            # Calculate matches
            red_match = len(set(selected_red) & set(draw_red))
            blue_match = 1 if selected_blue == draw_blue else 0
            
            # Determine prize level
            prize_info = ""
            prize_amount = ""
            
            if red_match == 6 and blue_match == 1:
                prize_info = "🎉 一等奖！6+1 匹配"
                prize_amount = "浮动奖金 (500万元起)"
            elif red_match == 6 and blue_match == 0:
                prize_info = "🥈 二等奖！6+0 匹配"
                prize_amount = "浮动奖金 (约20万元)"
            elif red_match == 5 and blue_match == 1:
                prize_info = "🥉 三等奖！5+1 匹配"
                prize_amount = "固定奖金: 3,000元"
            elif (red_match == 5 and blue_match == 0) or (red_match == 4 and blue_match == 1):
                prize_info = "4️⃣ 四等奖！5+0 或 4+1 匹配"
                prize_amount = "固定奖金: 200元"
            elif (red_match == 4 and blue_match == 0) or (red_match == 3 and blue_match == 1):
                prize_info = "5️⃣ 五等奖！4+0 或 3+1 匹配"
                prize_amount = "固定奖金: 10元"
            elif (red_match < 3 and blue_match == 1) or (red_match == 2 and blue_match == 1) or (red_match == 1 and blue_match == 1) or (red_match == 0 and blue_match == 1):
                prize_info = "6️⃣ 六等奖！仅蓝球匹配"
                prize_amount = "固定奖金: 5元"
            else:
                prize_info = "❌ 未中奖"
                prize_amount = "请继续努力！"
            
            # Display result
            result_text = f"""
<h2>{prize_info}</h2>

<h3>📊 对比详情:</h3>
<table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
    <tr style="background-color: #f0f0f0;">
        <th>类型</th>
        <th>您的号码</th>
        <th>开奖号码</th>
        <th>匹配数</th>
    </tr>
    <tr>
        <td><b>红球</b></td>
        <td style="color: red;">{', '.join(map(str, selected_red))}</td>
        <td style="color: red;">{', '.join(map(str, draw_red))}</td>
        <td style="font-size: 16px; font-weight: bold;">{red_match}/6</td>
    </tr>
    <tr>
        <td><b>蓝球</b></td>
        <td style="color: blue;">{selected_blue}</td>
        <td style="color: blue;">{draw_blue}</td>
        <td style="font-size: 16px; font-weight: bold;">{blue_match}/1</td>
    </tr>
</table>

<h3>💰 奖金信息:</h3>
<p style="font-size: 14px; color: #006600;">{prize_amount}</p>

<p style="font-size: 12px; color: #666;">
<b>说明:</b> 开奖号码为模拟数据，实际中奖请以官方开奖结果为准。
</p>
            """
            
            self.prize_result.setHtml(result_text)
            
            # Update status bar
            self.statusBar().showMessage(f'中奖检查完成: {prize_info}')
            
        except ValueError:
            self.prize_result.setText("❌ 号码格式错误，请输入用逗号分隔的数字，例如: 3,9,12,13,26,32,9")
        except Exception as e:
            self.prize_result.setText(f"❌ 检查失败: {str(e)}")
    
    def check_prize_kl8(self):
        """检查快乐8中奖级别。"""
        try:
            numbers_text = self.prize_numbers_display.text().strip()
            if not numbers_text:
                self.prize_result.setText("❌ 请输入您的号码")
                return
            
            numbers = [int(x.strip()) for x in numbers_text.split(',')]
            
            if len(numbers) != 10:
                self.prize_result.setText("❌ 快乐8需要选择10个号码")
                return
            
            if any(num < 1 or num > 80 for num in numbers):
                self.prize_result.setText("❌ 号码必须在 1-80 之间")
                return
            
            # Simulate draw (20 numbers drawn)
            draw_numbers = [4, 7, 11, 17, 20, 22, 27, 29, 32, 34, 37, 48, 55, 64, 68, 69, 71, 73, 74, 78]
            
            match_count = len(set(numbers) & set(draw_numbers))
            
            # Determine prize
            prize_info = ""
            prize_amount = ""
            
            if match_count == 10:
                prize_info = "🎉 选十中十！"
                prize_amount = "500万元"
            elif match_count == 9:
                prize_info = "🥈 选十中九"
                prize_amount = "10,000元"
            elif match_count == 8:
                prize_info = "🥉 选十中八"
                prize_amount = "3,000元"
            elif match_count == 7:
                prize_info = "4️⃣ 选十中七"
                prize_amount = "300元"
            elif match_count == 6:
                prize_info = "5️⃣ 选十中六"
                prize_amount = "50元"
            elif match_count == 5:
                prize_info = "6️⃣ 选十中五"
                prize_amount = "5元"
            elif match_count == 0:
                prize_info = "7️⃣ 选十中零"
                prize_amount = "5元"
            else:
                prize_info = "❌ 未中奖"
                prize_amount = "请继续努力！"
            
            result_text = f"""
<h2>{prize_info}</h2>

<h3>📊 对比详情:</h3>
<table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
    <tr style="background-color: #f0f0f0;">
        <th>您的号码</th>
        <th>开奖号码</th>
        <th>匹配数</th>
    </tr>
    <tr>
        <td>{', '.join(map(str, sorted(numbers)))}</td>
        <td>{', '.join(map(str, sorted(draw_numbers)))}</td>
        <td style="font-size: 16px; font-weight: bold; color: red;">{match_count}/10</td>
    </tr>
</table>

<h3>💰 奖金信息:</h3>
<p style="font-size: 14px; color: #006600;">{prize_amount}</p>

<p style="font-size: 12px; color: #666;">
<b>说明:</b> 开奖号码为模拟数据，实际中奖请以官方开奖结果为准。
</p>
            """
            
            self.prize_result.setHtml(result_text)
            self.statusBar().showMessage(f'中奖检查完成: {prize_info}')
            
        except ValueError:
            self.prize_result.setText("❌ 号码格式错误，请输入用逗号分隔的10个数字")
        except Exception as e:
            self.prize_result.setText(f"❌ 检查失败: {str(e)}")
    
    def check_prize_3d(self):
        """检查3D中奖级别。"""
        try:
            numbers_text = self.prize_numbers_display.text().strip()
            if not numbers_text:
                self.prize_result.setText("❌ 请输入您的号码")
                return
            
            numbers = [int(x.strip()) for x in numbers_text.split(',')]
            
            if len(numbers) != 3:
                self.prize_result.setText("❌ 3D需要选择3个数字")
                return
            
            if any(num < 0 or num > 9 for num in numbers):
                self.prize_result.setText("❌ 数字必须在 0-9 之间")
                return
            
            # Simulate draw
            draw_numbers = [7, 9, 4]
            
            # Check matches
            prize_info = ""
            prize_amount = ""
            
            if numbers == draw_numbers:
                prize_info = "🎉 直选中奖！"
                prize_amount = "1,040元"
            elif sorted(numbers) == sorted(draw_numbers):
                prize_info = "🥈 组选中奖！"
                if len(set(numbers)) == 2:
                    prize_amount = "346元 (组选3)"
                else:
                    prize_amount = "173元 (组选6)"
            else:
                prize_info = "❌ 未中奖"
                prize_amount = "请继续努力！"
            
            result_text = f"""
<h2>{prize_info}</h2>

<h3>📊 对比详情:</h3>
<table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
    <tr style="background-color: #f0f0f0;">
        <th>您的号码</th>
        <th>开奖号码</th>
        <th>是否中奖</th>
    </tr>
    <tr>
        <td style="font-size: 18px; font-weight: bold;">{numbers[0]} {numbers[1]} {numbers[2]}</td>
        <td style="font-size: 18px; font-weight: bold; color: red;">{draw_numbers[0]} {draw_numbers[1]} {draw_numbers[2]}</td>
        <td style="font-size: 16px; font-weight: bold;">{'✓' if numbers == draw_numbers or sorted(numbers) == sorted(draw_numbers) else '✗'}</td>
    </tr>
</table>

<h3>💰 奖金信息:</h3>
<p style="font-size: 14px; color: #006600;">{prize_amount}</p>

<p style="font-size: 12px; color: #666;">
<b>说明:</b> 开奖号码为模拟数据，实际中奖请以官方开奖结果为准。
</p>
            """
            
            self.prize_result.setHtml(result_text)
            self.statusBar().showMessage(f'中奖检查完成: {prize_info}')
            
        except ValueError:
            self.prize_result.setText("❌ 号码格式错误，请输入用逗号分隔的3个数字")
        except Exception as e:
            self.prize_result.setText(f"❌ 检查失败: {str(e)}")
    
    def check_prize_qlc(self):
        """检查七乐彩中奖级别。"""
        try:
            numbers_text = self.prize_numbers_display.text().strip()
            if not numbers_text:
                self.prize_result.setText("❌ 请输入您的号码")
                return
            
            numbers = [int(x.strip()) for x in numbers_text.split(',')]
            
            if len(numbers) != 7:
                self.prize_result.setText("❌ 七乐彩需要选择7个号码")
                return
            
            if any(num < 1 or num > 30 for num in numbers):
                self.prize_result.setText("❌ 号码必须在 1-30 之间")
                return
            
            # Simulate draw (7 main + 1 special)
            draw_main = [5, 10, 14, 15, 16, 18, 23]
            draw_special = 28
            
            main_match = len(set(numbers) & set(draw_main))
            special_match = 1 if draw_special in numbers else 0
            
            # Determine prize
            prize_info = ""
            prize_amount = ""
            
            if main_match == 7:
                prize_info = "🎉 一等奖！7个基本号码全中"
                prize_amount = "浮动奖金 (约500万元)"
            elif main_match == 6 and special_match == 1:
                prize_info = "🥈 二等奖！6个基本号码+特别号"
                prize_amount = "浮动奖金 (约10万元)"
            elif main_match == 6:
                prize_info = "🥉 三等奖！6个基本号码"
                prize_amount = "固定奖金: 1,000元"
            elif main_match == 5 and special_match == 1:
                prize_info = "4️⃣ 四等奖！5个基本号码+特别号"
                prize_amount = "固定奖金: 200元"
            elif main_match == 5:
                prize_info = "5️⃣ 五等奖！5个基本号码"
                prize_amount = "固定奖金: 50元"
            elif main_match == 4 and special_match == 1:
                prize_info = "6️⃣ 六等奖！4个基本号码+特别号"
                prize_amount = "固定奖金: 10元"
            elif main_match == 4:
                prize_info = "7️⃣ 七等奖！4个基本号码"
                prize_amount = "固定奖金: 5元"
            else:
                prize_info = "❌ 未中奖"
                prize_amount = "请继续努力！"
            
            result_text = f"""
<h2>{prize_info}</h2>

<h3>📊 对比详情:</h3>
<table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
    <tr style="background-color: #f0f0f0;">
        <th>类型</th>
        <th>您的号码</th>
        <th>开奖号码</th>
        <th>匹配数</th>
    </tr>
    <tr>
        <td><b>基本号码</b></td>
        <td>{', '.join(map(str, sorted(numbers)))}</td>
        <td style="color: red;">{', '.join(map(str, sorted(draw_main)))}</td>
        <td style="font-size: 16px; font-weight: bold;">{main_match}/7</td>
    </tr>
    <tr>
        <td><b>特别号码</b></td>
        <td>{draw_special if special_match else '-'}</td>
        <td style="color: blue;">{draw_special}</td>
        <td style="font-size: 16px; font-weight: bold;">{special_match}/1</td>
    </tr>
</table>

<h3>💰 奖金信息:</h3>
<p style="font-size: 14px; color: #006600;">{prize_amount}</p>

<p style="font-size: 12px; color: #666;">
<b>说明:</b> 开奖号码为模拟数据，实际中奖请以官方开奖结果为准。
</p>
            """
            
            self.prize_result.setHtml(result_text)
            self.statusBar().showMessage(f'中奖检查完成: {prize_info}')
            
        except ValueError:
            self.prize_result.setText("❌ 号码格式错误，请输入用逗号分隔的7个数字")
        except Exception as e:
            self.prize_result.setText(f"❌ 检查失败: {str(e)}")


def run_app():
    """运行彩票应用程序。"""
    app = QApplication(sys.argv)
    window = LotteryApp()
    window.show()
    sys.exit(app.exec())
