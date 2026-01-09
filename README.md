# Lottery Analysis and Prediction System

A comprehensive lottery analysis and prediction system built with Python. **Now accessible from both computers and mobile phones via Web interface!**

## ✨ Features

### 🌐 Multi-Platform Access
- **Web Interface**: Access from any device - computer, phone, tablet
- **Desktop GUI**: Full-featured PySide6 application for Windows/macOS/Linux  
- **Mobile Optimized**: Responsive design for smartphones
- **Cross-Device**: Seamless experience across all platforms

### 🎰 Lottery Support
- **Chinese Sports Lottery**: 大乐透, 七星彩, 排列三, 排列五
- **General Lottery**: Configurable for any lottery type
- **Type-Specific Predictions**: Optimized for each lottery format

### 📊 Core Functionalities
- **Data Analysis**: Frequency analysis, hot/cold numbers, pattern detection
- **7 Prediction Algorithms**: 
  - Frequency-based prediction
  - Hot/cold number analysis
  - Pattern-balanced prediction
  - Weighted frequency (recent data weighted)
  - Gap analysis (predict "due" numbers)
  - Moving average (trend-based)
  - Cyclic pattern detection
- **Ensemble Prediction**: Combines all algorithms with confidence scoring
- **Record Management**: Add, edit, remove, and share prediction records
- **Password Generator**: Strong, configurable passwords
- **Data Visualization**: Charts and graphs for analysis

### 💾 Data Handling
- **Import/Export**: CSV, JSON, Excel formats
- **Sample Data**: Built-in sample data generator
- **Flexible Configuration**: JSON-based settings

### 🎨 User Interface
- **Web UI**: Modern, responsive design for all devices
- **Desktop GUI**: PySide6 tabbed interface
  - Analysis tab for statistical analysis
  - Prediction tab for generating predictions
  - Data Management tab for importing/exporting data
  - Utilities tab for tools and records
- **Menu System**: File, Tools, and Help menus

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)

**Perfect for mobile access!**

```bash
# Install dependencies
pip install -r requirements.txt

# Start web server
python web_app.py
```

**Access the system:**
- **From Computer**: Open browser to `http://localhost:5000`
- **From Mobile**: Open browser to `http://[your-computer-ip]:5000`

Or use convenient startup scripts:
```bash
./start_web.sh        # Linux/Mac
start_web.bat         # Windows
```

See [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md) for detailed deployment guide.

### Option 2: Desktop GUI

```bash
# Install dependencies
pip install -r requirements.txt

# Run desktop application
python main.py
```

### Option 3: CLI Demo

```bash
# Run command-line demo
python demo_cli.py
```

## 📥 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Quick Start Guide

1. **Load Data**:
   - Go to the "Data Management" tab
   - Click "Load Data" to import CSV, JSON, or Excel files
   - Or click "Generate Sample Data" to create test data

2. **Analyze Data**:
   - Switch to the "Analysis" tab
   - Click "Run Analysis" to see statistical insights
   - View hot/cold numbers and pattern analysis

3. **Generate Predictions**:
   - Go to the "Prediction" tab
   - Set your preferences (number count, range)
   - Click "Generate Prediction"
   - Save predictions using "Save Prediction"

4. **Create Visualizations**:
   - Go to Tools > Create Visualization
   - View and save analysis dashboards

5. **Export Data**:
   - Use File > Export Data to save your data
   - Use the Utilities tab to export records

## Data Format

The system expects lottery data in the following format:

### CSV Format
```csv
date,draw_number,numbers
2024-01-01,1,"1,5,12,23,34,45"
2024-01-02,2,"3,8,15,27,38,42"
```

### JSON Format
```json
[
  {
    "date": "2024-01-01",
    "draw_number": 1,
    "numbers": [1, 5, 12, 23, 34, 45]
  },
  {
    "date": "2024-01-02",
    "draw_number": 2,
    "numbers": [3, 8, 15, 27, 38, 42]
  }
]
```

## Configuration

The system uses a `config.json` file for configuration:

```json
{
  "system": {
    "app_name": "Lottery Analysis System",
    "version": "1.0.0"
  },
  "prediction": {
    "analysis_window": 30,
    "min_data_points": 10,
    "prediction_algorithms": ["frequency", "hot_cold", "pattern"]
  },
  "ui": {
    "window_width": 1200,
    "window_height": 800
  }
}
```

## Architecture

### Module Structure
```
lottery-system/
├── main.py                 # Application entry point
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
└── src/
    ├── config/           # Configuration management
    ├── core/             # Core business logic
    │   ├── data_analyzer.py
    │   ├── prediction_engine.py
    │   └── record_manager.py
    ├── data/             # Data handling
    │   ├── data_handler.py
    │   └── visualizer.py
    ├── ui/               # User interface
    │   ├── number_button.py
    │   └── lottery_app.py
    └── utils/            # Utilities
        ├── password_generator.py
        └── logger.py
```

## Key Features Detail

### Data Analysis
- Frequency analysis of lottery numbers
- Hot and cold number identification
- Pattern detection (consecutive numbers, odd/even ratios, high/low distribution)
- Historical trend analysis

### Prediction Algorithms
1. **Frequency-based**: Predicts based on historical frequency
2. **Hot/Cold**: Uses hot numbers that appear frequently
3. **Pattern-based**: Balances odd/even and high/low numbers
4. **Ensemble**: Combines all algorithms for best results

### Visualization Tools
- Frequency distribution charts
- Hot vs cold number comparisons
- Number distribution over time
- Odd/even distribution pie charts
- Comprehensive analysis dashboards

## Android Support

For Android deployment, the application can be packaged using:
- **Buildozer**: For creating Android APK files
- **Kivy**: Alternative UI framework for mobile support
- **BeeWare**: Cross-platform Python tools

## Testing

The system includes comprehensive functionality:
- Statistical analysis algorithms
- Data import/export operations
- Prediction generation
- Record management
- Password generation

## Help and Support

### FAQ
Access the in-app FAQ through Help > FAQ menu.

### Common Issues
1. **Import fails**: Ensure data format matches expected structure
2. **No predictions**: Load historical data for better predictions
3. **Visualization errors**: Check that matplotlib is properly installed

## License

This project is developed as an open-source lottery analysis tool.

## Contributing

Contributions are welcome! Please ensure:
- Code is well-documented
- Functions include type hints
- New features include appropriate error handling

## Version History

### Version 1.0.0
- Initial release
- Core analysis and prediction features
- Data import/export functionality
- GUI interface with multiple tabs
- Password generation utility
- Record management system
