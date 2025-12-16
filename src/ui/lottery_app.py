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
from ..utils import PasswordGenerator, setup_logger
from .number_button import NumberButton


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
        
        # Deadline info label
        self.deadline_label = QLabel("⏰ 购买截止: ")
        deadline_font = QFont()
        deadline_font.setPointSize(11)
        self.deadline_label.setFont(deadline_font)
        self.deadline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.home_results_table.setColumnCount(4)
        self.home_results_table.setHorizontalHeaderLabels(["彩票类型", "开奖日期", "开奖号码", "状态"])
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
        
        # Update deadline info
        deadline_info = self.get_deadline_info()
        self.deadline_label.setText(f"⏰ 购买截止: {deadline_info}")
        
        # Update marquee
        self.update_marquee()
        
        # Update latest results table
        self.update_home_latest_table()
    
    def get_deadline_info(self):
        """获取截止时间信息"""
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        
        deadlines = []
        
        if hour < 20 or (hour == 20 and minute == 0):
            if hour < 19:
                deadlines.append("双色球 20:00")
                deadlines.append("大乐透 20:00")
                deadlines.append("快乐8 20:00")
            if hour < 20:
                deadlines.append("福彩3D 20:30")
                deadlines.append("排列三 20:30")
                deadlines.append("排列五 20:30")
                deadlines.append("七星彩 20:30")
                deadlines.append("七乐彩 20:30")
        
        return " | ".join(deadlines) if deadlines else "今日彩票销售已截止"
    
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
        # Populate with sample data or latest results
        self.home_results_table.setRowCount(3)
        
        # Sample data - in real app, this would come from actual data
        sample_data = [
            ["双色球", "2024-12-15", "03, 12, 18, 25, 28, 31 + 08", "已开奖"],
            ["大乐透", "2024-12-14", "05, 11, 19, 27, 33 + 02, 09", "已开奖"],
            ["福彩3D", "2024-12-15", "5 3 7", "已开奖"]
        ]
        
        for row, data in enumerate(sample_data):
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


def run_app():
    """运行彩票应用程序。"""
    app = QApplication(sys.argv)
    window = LotteryApp()
    window.show()
    sys.exit(app.exec())
