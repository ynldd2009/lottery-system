# Quick Start Guide

Get started with the Lottery Analysis System in 5 minutes!

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/ynldd2009/lottery-system.git
cd lottery-system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

That's it! You're ready to use the system.

## First Steps

### Option 1: Run the GUI Application

```bash
python main.py
```

This launches the full graphical interface with:
- Data Analysis tab
- Prediction Generator tab
- Data Management tab
- Utilities tab

### Option 2: Run the CLI Demo

```bash
python demo_cli.py
```

This runs a command-line demonstration of all features:
- Configuration management
- Data handling
- Statistical analysis
- Prediction generation
- Password generation
- Record management
- Visualization creation

### Option 3: Run Tests

```bash
python tests/test_core_modules.py
```

Validates that all core modules are working correctly.

## Basic Usage

### 1. Load or Generate Data

**In GUI:**
1. Go to "Data Management" tab
2. Click "Generate Sample Data" for test data
3. Or click "Load Data" to import your own CSV/JSON/Excel file

**In Python:**
```python
from src.data import DataHandler

handler = DataHandler()
data = handler.create_sample_data(num_draws=100)
```

### 2. Analyze the Data

**In GUI:**
1. Go to "Analysis" tab
2. Click "Run Analysis"
3. View statistics, hot/cold numbers, and patterns

**In Python:**
```python
from src.core import DataAnalyzer

analyzer = DataAnalyzer()
analyzer.load_data(data)
stats = analyzer.get_statistics_summary()
print(stats)
```

### 3. Generate Predictions

**In GUI:**
1. Go to "Prediction" tab
2. Set your preferences (number count, range)
3. Click "Generate Prediction"
4. Save predictions using "Save Prediction"

**In Python:**
```python
from src.core import PredictionEngine

engine = PredictionEngine()
engine.load_historical_data(data)
predictions = engine.generate_prediction_with_confidence(count=6)
print(predictions['recommended'])
```

### 4. Create Visualizations

**In GUI:**
1. Go to Tools > Create Visualization
2. Dashboard is saved to your home directory

**In Python:**
```python
from src.data import DataVisualizer

visualizer = DataVisualizer()
# Create various charts
visualizer.create_analysis_dashboard(
    frequency, hot_nums, cold_nums, data, 
    'dashboard.png'
)
```

## Example Workflows

### Workflow 1: Quick Prediction

```bash
# 1. Run the demo to see it in action
python demo_cli.py

# Output will show sample predictions like:
# Recommended numbers: [1, 4, 15, 22, 23, 44]
# Confidence level: 100.0%
```

### Workflow 2: Analyze Your Data

```python
# your_script.py
from src.data import DataHandler
from src.core import DataAnalyzer

# Import your lottery data
handler = DataHandler()
data = handler.import_csv('my_lottery_data.csv')

# Analyze it
analyzer = DataAnalyzer()
analyzer.load_data(data)
stats = analyzer.get_statistics_summary()

print(f"Total draws: {stats['total_draws']}")
print(f"Hot numbers: {stats['hot_numbers']}")
print(f"Cold numbers: {stats['cold_numbers']}")
```

### Workflow 3: Generate Multiple Predictions

```python
from src.core import PredictionEngine
from src.data import DataHandler

# Load data
handler = DataHandler()
data = handler.create_sample_data(100)

# Generate predictions
engine = PredictionEngine()
engine.load_historical_data(data)

# Get predictions from all algorithms
predictions = engine.predict_combined(count=6, number_range=(1, 49))

print("Frequency-based:", predictions['frequency'])
print("Hot numbers:", predictions['hot_cold'])
print("Pattern-based:", predictions['pattern'])
print("Ensemble (recommended):", predictions['ensemble'])
```

### Workflow 4: Export Analysis Results

```python
from src.data import DataHandler
from src.core import DataAnalyzer, RecordManager

# Analyze data
handler = DataHandler()
data = handler.create_sample_data(100)

analyzer = DataAnalyzer()
analyzer.load_data(data)
stats = analyzer.get_statistics_summary()

# Save as record
manager = RecordManager()
record = {
    'type': 'analysis',
    'title': 'Monthly Analysis',
    'data': stats
}
record_id = manager.add_record(record)

# Export records
manager.export_to_json('analysis_results.json')
```

## Data Format

Your CSV should look like:
```csv
date,draw_number,numbers
2024-01-01,1,"1,5,12,23,34,45"
2024-01-02,2,"3,8,15,27,38,42"
```

Your JSON should look like:
```json
[
  {
    "date": "2024-01-01",
    "draw_number": 1,
    "numbers": [1, 5, 12, 23, 34, 45]
  }
]
```

## Configuration

Edit `config.json` to customize:

```json
{
  "prediction": {
    "analysis_window": 30,
    "prediction_algorithms": ["frequency", "hot_cold", "pattern"]
  },
  "ui": {
    "window_width": 1200,
    "window_height": 800
  }
}
```

## Troubleshooting

### Issue: "Module not found"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "No display"
**Solution:** Use CLI demo or set headless mode
```bash
export QT_QPA_PLATFORM=offscreen
python demo_cli.py
```

### Issue: "Import fails"
**Solution:** Check your data format matches the examples above

### Issue: "Permission denied"
**Solution:** Make scripts executable
```bash
chmod +x main.py demo_cli.py
```

## Next Steps

1. **Read the full README**: `README.md`
2. **Explore features**: `FEATURES.md`
3. **Learn about Android**: `ANDROID_DEPLOYMENT.md`
4. **Contribute**: `CONTRIBUTING.md`

## Quick Command Reference

```bash
# Run GUI app
python main.py

# Run demo
python demo_cli.py

# Run tests
python tests/test_core_modules.py

# Install in development mode
pip install -e .

# Generate documentation
python -m pydoc -w src.core.prediction_engine
```

## Getting Help

- **Documentation**: Read `README.md` and `FEATURES.md`
- **Issues**: Open an issue on GitHub
- **Examples**: Check `demo_cli.py` for code examples

Happy analyzing! 🎲
