# Lottery Analysis and Prediction System

A cross-platform lottery analysis and prediction system built with Python that runs on both PC and Android platforms.

## Features

### Core Functionalities
- **Data Analysis and Statistics**: Comprehensive statistical analysis of lottery data including frequency analysis, hot/cold numbers, and pattern detection
- **Prediction Tools**: Multi-algorithm prediction engine using frequency analysis, hot/cold number analysis, and pattern-based predictions
- **Record Management**: Add, edit, remove, and share prediction records
- **Automatic Password Generator**: Generate strong, secure passwords automatically
- **Data Visualization**: Create charts and graphs to visualize lottery statistics

### System Components
- **Configuration Management**: Flexible configuration system with JSON-based settings
- **Data Handling**: Import/export data in CSV, JSON, and Excel formats
- **Custom UI Components**: 
  - NumberButton for interactive number selection
  - Main LotteryApp window with tabbed interface
  - Integrated visualization tools

### User Interface
- Intuitive GUI built with PySide6
- Tabbed interface for different functionalities:
  - Analysis tab for statistical analysis
  - Prediction tab for generating predictions
  - Data Management tab for importing/exporting data
  - Utilities tab for password generation and record management
- Menu system with File, Tools, and Help menus

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application
```bash
python main.py
```

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
