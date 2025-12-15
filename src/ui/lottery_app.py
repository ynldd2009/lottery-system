"""
Lottery App Main Window
Main application window for the lottery analysis system.
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QTabWidget, QLabel, QPushButton,
                              QTextEdit, QTableWidget, QTableWidgetItem, QFileDialog,
                              QMessageBox, QGridLayout, QGroupBox, QLineEdit, QSpinBox)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QPixmap

from ..config import ConfigManager
from ..core import DataAnalyzer, PredictionEngine, RecordManager
from ..data import DataHandler, DataVisualizer
from ..utils import PasswordGenerator, setup_logger
from .number_button import NumberButton


class LotteryApp(QMainWindow):
    """Main application window for lottery analysis."""
    
    def __init__(self):
        """Initialize the main application."""
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
        
        self.logger.info("Lottery Analysis System initialized")
    
    def init_ui(self):
        """Initialize the user interface."""
        # Window settings
        app_name = self.config_manager.get('system.app_name', 'Lottery Analysis System')
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
        
        # Create tabs
        self.create_analysis_tab()
        self.create_prediction_tab()
        self.create_data_management_tab()
        self.create_utilities_tab()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage('Ready')
    
    def create_menu_bar(self):
        """Create application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        import_action = file_menu.addAction('Import Data')
        import_action.triggered.connect(self.import_data)
        
        export_action = file_menu.addAction('Export Data')
        export_action.triggered.connect(self.export_data)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)
        
        # Tools menu
        tools_menu = menubar.addMenu('&Tools')
        
        password_action = tools_menu.addAction('Generate Password')
        password_action.triggered.connect(self.show_password_generator)
        
        visualize_action = tools_menu.addAction('Create Visualization')
        visualize_action.triggered.connect(self.create_visualization)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = help_menu.addAction('About')
        about_action.triggered.connect(self.show_about)
        
        faq_action = help_menu.addAction('FAQ')
        faq_action.triggered.connect(self.show_faq)
    
    def create_analysis_tab(self):
        """Create the data analysis tab."""
        analysis_tab = QWidget()
        layout = QVBoxLayout(analysis_tab)
        
        # Title
        title = QLabel("Lottery Data Analysis")
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
        
        analyze_btn = QPushButton("Run Analysis")
        analyze_btn.clicked.connect(self.run_analysis)
        button_layout.addWidget(analyze_btn)
        
        clear_btn = QPushButton("Clear Results")
        clear_btn.clicked.connect(lambda: self.analysis_results.clear())
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
        self.tabs.addTab(analysis_tab, "Analysis")
    
    def create_prediction_tab(self):
        """Create the prediction tab."""
        prediction_tab = QWidget()
        layout = QVBoxLayout(prediction_tab)
        
        # Title
        title = QLabel("Lottery Number Prediction")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Prediction settings
        settings_group = QGroupBox("Prediction Settings")
        settings_layout = QHBoxLayout(settings_group)
        
        settings_layout.addWidget(QLabel("Number Count:"))
        self.pred_count_spin = QSpinBox()
        self.pred_count_spin.setMinimum(1)
        self.pred_count_spin.setMaximum(20)
        self.pred_count_spin.setValue(6)
        settings_layout.addWidget(self.pred_count_spin)
        
        settings_layout.addWidget(QLabel("Min Number:"))
        self.pred_min_spin = QSpinBox()
        self.pred_min_spin.setMinimum(1)
        self.pred_min_spin.setValue(1)
        settings_layout.addWidget(self.pred_min_spin)
        
        settings_layout.addWidget(QLabel("Max Number:"))
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
        
        predict_btn = QPushButton("Generate Prediction")
        predict_btn.clicked.connect(self.generate_prediction)
        button_layout.addWidget(predict_btn)
        
        save_pred_btn = QPushButton("Save Prediction")
        save_pred_btn.clicked.connect(self.save_prediction)
        button_layout.addWidget(save_pred_btn)
        
        layout.addLayout(button_layout)
        
        self.tabs.addTab(prediction_tab, "Prediction")
    
    def create_data_management_tab(self):
        """Create the data management tab."""
        data_tab = QWidget()
        layout = QVBoxLayout(data_tab)
        
        # Title
        title = QLabel("Data Management")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Data table
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(3)
        self.data_table.setHorizontalHeaderLabels(['Date', 'Draw #', 'Numbers'])
        layout.addWidget(self.data_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        load_btn = QPushButton("Load Data")
        load_btn.clicked.connect(self.load_data_file)
        button_layout.addWidget(load_btn)
        
        sample_btn = QPushButton("Generate Sample Data")
        sample_btn.clicked.connect(self.generate_sample_data)
        button_layout.addWidget(sample_btn)
        
        export_btn = QPushButton("Export Data")
        export_btn.clicked.connect(self.export_data)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        self.tabs.addTab(data_tab, "Data Management")
    
    def create_utilities_tab(self):
        """Create the utilities tab."""
        utils_tab = QWidget()
        layout = QVBoxLayout(utils_tab)
        
        # Title
        title = QLabel("Utilities")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Password Generator Section
        password_group = QGroupBox("Password Generator")
        password_layout = QVBoxLayout(password_group)
        
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        password_layout.addWidget(self.password_display)
        
        gen_password_btn = QPushButton("Generate Strong Password")
        gen_password_btn.clicked.connect(self.generate_password)
        password_layout.addWidget(gen_password_btn)
        
        layout.addWidget(password_group)
        
        # Records Section
        records_group = QGroupBox("Records Management")
        records_layout = QVBoxLayout(records_group)
        
        self.records_table = QTableWidget()
        self.records_table.setColumnCount(3)
        self.records_table.setHorizontalHeaderLabels(['ID', 'Type', 'Created'])
        records_layout.addWidget(self.records_table)
        
        records_button_layout = QHBoxLayout()
        
        load_records_btn = QPushButton("Load Records")
        load_records_btn.clicked.connect(self.load_records)
        records_button_layout.addWidget(load_records_btn)
        
        export_records_btn = QPushButton("Export Records")
        export_records_btn.clicked.connect(self.export_records)
        records_button_layout.addWidget(export_records_btn)
        
        records_layout.addLayout(records_button_layout)
        
        layout.addWidget(records_group)
        
        layout.addStretch()
        
        self.tabs.addTab(utils_tab, "Utilities")
    
    def run_analysis(self):
        """Run data analysis on loaded data."""
        if self.current_data is None or self.current_data.empty:
            QMessageBox.warning(self, "No Data", "Please load data first.")
            return
        
        self.statusBar().showMessage('Running analysis...')
        
        try:
            # Load data into analyzer
            self.data_analyzer.load_data(self.current_data)
            
            # Get statistics
            stats = self.data_analyzer.get_statistics_summary()
            
            # Format results
            results = "=== Lottery Data Analysis Results ===\n\n"
            results += f"Total Draws: {stats.get('total_draws', 0)}\n\n"
            
            results += "Hot Numbers (Most Frequent):\n"
            hot_nums = stats.get('hot_numbers', [])
            results += f"{hot_nums}\n\n"
            
            results += "Cold Numbers (Least Frequent):\n"
            cold_nums = stats.get('cold_numbers', [])
            results += f"{cold_nums}\n\n"
            
            results += "Top 10 Most Common Numbers:\n"
            for num, freq in stats.get('most_common', []):
                results += f"  Number {num}: {freq} times\n"
            
            results += "\nPattern Analysis:\n"
            patterns = stats.get('patterns', {})
            results += f"  Consecutive numbers found: {patterns.get('consecutive_numbers', 0)}\n"
            results += f"  Odd/Even ratio: {patterns.get('odd_even_ratio', 0):.2%}\n"
            results += f"  High/Low ratio: {patterns.get('high_low_ratio', 0):.2%}\n"
            
            self.analysis_results.setPlainText(results)
            self.statusBar().showMessage('Analysis complete')
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Analysis failed: {str(e)}")
            self.statusBar().showMessage('Analysis failed')
    
    def generate_prediction(self):
        """Generate lottery number predictions."""
        if self.current_data is None or self.current_data.empty:
            QMessageBox.warning(self, "No Data", 
                              "Please load historical data first for better predictions.")
        
        self.statusBar().showMessage('Generating predictions...')
        
        try:
            # Get settings
            count = self.pred_count_spin.value()
            min_num = self.pred_min_spin.value()
            max_num = self.pred_max_spin.value()
            
            if min_num >= max_num:
                QMessageBox.warning(self, "Invalid Range", "Min number must be less than max number.")
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
            output = "=== Lottery Number Predictions ===\n\n"
            output += f"Confidence Level: {result['confidence']:.1%}\n"
            output += f"Data Points Used: {result['data_points_used']}\n"
            output += f"Algorithms: {', '.join(result['algorithms_used'])}\n\n"
            
            output += "Recommended Prediction (Ensemble):\n"
            output += f"  {result['recommended']}\n\n"
            
            output += "Algorithm-Specific Predictions:\n"
            for algo, numbers in result['predictions'].items():
                if algo != 'ensemble':
                    output += f"  {algo.title()}: {numbers}\n"
            
            self.prediction_results.setPlainText(output)
            self.statusBar().showMessage('Prediction generated')
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Prediction failed: {str(e)}")
            self.statusBar().showMessage('Prediction failed')
    
    def save_prediction(self):
        """Save current prediction to records."""
        prediction_text = self.prediction_results.toPlainText()
        
        if not prediction_text or prediction_text.strip() == "":
            QMessageBox.warning(self, "No Prediction", "Generate a prediction first.")
            return
        
        try:
            record = {
                'type': 'prediction',
                'title': f'Prediction {len(self.record_manager.get_all_records()) + 1}',
                'description': 'Generated prediction',
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
            QMessageBox.information(self, "Success", f"Prediction saved with ID: {record_id}")
            self.statusBar().showMessage('Prediction saved')
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save prediction: {str(e)}")
    
    def import_data(self):
        """Import lottery data from file."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Import Data", "", 
            "CSV Files (*.csv);;JSON Files (*.json);;Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        
        if filename:
            self.load_data_file(filename)
    
    def load_data_file(self, filename: str = None):
        """Load data from a file."""
        if filename is None:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Load Data", "",
                "CSV Files (*.csv);;JSON Files (*.json);;Excel Files (*.xlsx *.xls);;All Files (*)"
            )
        
        if not filename:
            return
        
        self.statusBar().showMessage('Loading data...')
        
        try:
            file_path = Path(filename)
            
            if file_path.suffix == '.csv':
                data = self.data_handler.import_csv(filename)
            elif file_path.suffix == '.json':
                data = self.data_handler.import_json(filename)
            elif file_path.suffix in ['.xlsx', '.xls']:
                data = self.data_handler.import_excel(filename)
            else:
                QMessageBox.warning(self, "Unsupported Format", 
                                  "Please select a CSV, JSON, or Excel file.")
                return
            
            if data.empty:
                QMessageBox.warning(self, "No Data", "The file contains no valid data.")
                return
            
            self.current_data = data
            self.update_data_table()
            
            QMessageBox.information(self, "Success", 
                                  f"Loaded {len(data)} records from file.")
            self.statusBar().showMessage('Data loaded successfully')
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
            self.statusBar().showMessage('Data loading failed')
    
    def generate_sample_data(self):
        """Generate sample lottery data for testing."""
        try:
            data = self.data_handler.create_sample_data(num_draws=100)
            self.current_data = data
            self.update_data_table()
            
            QMessageBox.information(self, "Success", "Generated 100 sample lottery draws.")
            self.statusBar().showMessage('Sample data generated')
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate sample data: {str(e)}")
    
    def update_data_table(self):
        """Update the data table with current data."""
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
        """Export current data to file."""
        if self.current_data is None or self.current_data.empty:
            QMessageBox.warning(self, "No Data", "No data to export.")
            return
        
        filename, selected_filter = QFileDialog.getSaveFileName(
            self, "Export Data", "",
            "CSV Files (*.csv);;JSON Files (*.json);;Excel Files (*.xlsx);;All Files (*)"
        )
        
        if not filename:
            return
        
        self.statusBar().showMessage('Exporting data...')
        
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
                QMessageBox.information(self, "Success", "Data exported successfully.")
                self.statusBar().showMessage('Data exported')
            else:
                QMessageBox.warning(self, "Export Failed", "Could not export data.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
            self.statusBar().showMessage('Export failed')
    
    def generate_password(self):
        """Generate a strong password."""
        try:
            password = self.password_generator.generate()
            self.password_display.setText(password)
            self.statusBar().showMessage('Password generated')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate password: {str(e)}")
    
    def show_password_generator(self):
        """Show password generator dialog."""
        passwords = self.password_generator.generate_multiple(5)
        
        message = "Generated Strong Passwords:\n\n"
        for i, pwd in enumerate(passwords, 1):
            message += f"{i}. {pwd}\n"
        
        QMessageBox.information(self, "Password Generator", message)
    
    def create_visualization(self):
        """Create data visualizations."""
        if self.current_data is None or self.current_data.empty:
            QMessageBox.warning(self, "No Data", "Please load data first.")
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
            
            QMessageBox.information(self, "Success", 
                                  f"Dashboard saved to:\n{save_path}")
            self.statusBar().showMessage('Visualization created')
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Visualization failed: {str(e)}")
    
    def load_records(self):
        """Load and display records."""
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
            
            self.statusBar().showMessage(f'Loaded {len(records)} records')
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load records: {str(e)}")
    
    def export_records(self):
        """Export records to file."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Records", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if not filename:
            return
        
        try:
            success = self.record_manager.export_to_json(filename)
            
            if success:
                QMessageBox.information(self, "Success", "Records exported successfully.")
            else:
                QMessageBox.warning(self, "Export Failed", "Could not export records.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def show_about(self):
        """Show about dialog."""
        about_text = f"""
        <h2>{self.config_manager.get('system.app_name')}</h2>
        <p>Version {self.config_manager.get('system.version')}</p>
        <p>A cross-platform lottery analysis and prediction system.</p>
        <p><b>Features:</b></p>
        <ul>
            <li>Statistical analysis of lottery data</li>
            <li>Multi-algorithm prediction engine</li>
            <li>Data visualization tools</li>
            <li>Record management</li>
            <li>Password generation</li>
        </ul>
        """
        QMessageBox.about(self, "About", about_text)
    
    def show_faq(self):
        """Show FAQ dialog."""
        faq_text = """
        <h3>Frequently Asked Questions</h3>
        
        <p><b>Q: How do I import data?</b></p>
        <p>A: Go to File > Import Data and select a CSV, JSON, or Excel file.</p>
        
        <p><b>Q: What data format is supported?</b></p>
        <p>A: The data should have 'date', 'draw_number', and 'numbers' columns.</p>
        
        <p><b>Q: How accurate are the predictions?</b></p>
        <p>A: Predictions are based on statistical analysis. More historical data improves accuracy.</p>
        
        <p><b>Q: Can I export my analysis results?</b></p>
        <p>A: Yes, use the Export Data or Export Records features.</p>
        """
        QMessageBox.information(self, "FAQ", faq_text)


def run_app():
    """Run the lottery application."""
    app = QApplication(sys.argv)
    window = LotteryApp()
    window.show()
    sys.exit(app.exec())
