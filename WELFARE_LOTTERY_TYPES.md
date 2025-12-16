# Chinese Welfare Lottery Types (福利彩票)

This document describes the Chinese Welfare Lottery games supported by the lottery analysis system.

## Overview

The system now supports **4 Chinese Welfare Lottery games** (福利彩票):
1. **双色球** (Double Color Ball)
2. **快乐8** (Happy 8)
3. **七乐彩** (7 Happy Lottery)
4. **福彩3D** (Welfare 3D)

These complement the existing Sports Lottery games (体育彩票) to provide comprehensive coverage of Chinese lottery games.

---

## 1. 双色球 (Double Color Ball)

### Game Description
双色球 is one of the most popular lottery games in China. Players select 6 red balls from 1-33 and 1 blue ball from 1-16.

### Configuration
```python
{
    "name": "Double Color Ball (双色球)",
    "category": "welfare",
    "description": "6 red balls (1-33) + 1 blue ball (1-16)",
    "main_numbers": {
        "count": 6,
        "range": (1, 33),
        "name": "Red Balls"
    },
    "bonus_numbers": {
        "count": 1,
        "range": (1, 16),
        "name": "Blue Ball"
    }
}
```

### Prize Structure
| Prize Level | Match Requirement | Base Prize (¥) |
|------------|-------------------|----------------|
| 一等奖 | 6 red + 1 blue | 5,000,000 |
| 二等奖 | 6 red + 0 blue | 200,000 |
| 三等奖 | 5 red + 1 blue | 3,000 |
| 四等奖 | 5 red or 4 red + 1 blue | 200 |
| 五等奖 | 4 red or 3 red + 1 blue | 10 |
| 六等奖 | 2 red + 1 blue or 1 red + 1 blue or 0 red + 1 blue | 5 |

### Usage Example
```python
from src.core import PredictionEngine

# Create prediction engine for 双色球
engine = PredictionEngine(lottery_type="双色球")

# Generate prediction
result = engine.predict_for_lottery_type()

print(result['formatted'])
# Output: Red: [3, 12, 18, 25, 28, 31] + Blue: [8]

# Validate numbers
from src.config.lottery_types import get_lottery_type
lottery = get_lottery_type("双色球")
is_valid = lottery.validate_numbers(result['numbers'])
```

---

## 2. 快乐8 (Happy 8)

### Game Description
快乐8 is a high-frequency lottery game where players select 1-10 numbers from 1-80. The system draws 20 numbers each game.

### Configuration
```python
{
    "name": "Happy 8 (快乐8)",
    "category": "welfare",
    "description": "Select 1-10 numbers from 1-80, draw 20 numbers",
    "main_numbers": {
        "count": 10,
        "range": (1, 80),
        "name": "Numbers"
    },
    "draw_count": 20
}
```

### Prize Structure (Select 10)
| Prize Level | Match Requirement | Base Prize (¥) |
|------------|-------------------|----------------|
| 选十中十 | 10 of 10 | 5,000,000 |
| 选十中九 | 9 of 10 | 50,000 |
| 选十中八 | 8 of 10 | 9,000 |
| 选十中七 | 7 of 10 | 300 |
| 选十中六 | 6 of 10 | 50 |
| 选十中五 | 5 of 10 | 20 |
| 选十中零 | 0 of 10 | 5 |

### Usage Example
```python
from src.core import PredictionEngine

# Create prediction engine for 快乐8
engine = PredictionEngine(lottery_type="快乐8")

# Generate prediction (10 numbers)
result = engine.predict_for_lottery_type()

print(result['formatted'])
# Output: Selected: [3, 12, 18, 25, 33, 42, 51, 60, 68, 77]
```

---

## 3. 七乐彩 (7 Happy Lottery)

### Game Description
七乐彩 requires players to select 7 main numbers from 1-30, plus the system draws 1 special number from the same pool.

### Configuration
```python
{
    "name": "7 Happy Lottery (七乐彩)",
    "category": "welfare",
    "description": "7 main numbers (1-30) + 1 special number (1-30)",
    "main_numbers": {
        "count": 7,
        "range": (1, 30),
        "name": "Main Numbers"
    },
    "bonus_numbers": {
        "count": 1,
        "range": (1, 30),
        "name": "Special Number"
    }
}
```

### Prize Structure
| Prize Level | Match Requirement | Base Prize (¥) |
|------------|-------------------|----------------|
| 一等奖 | 7 main numbers | 5,000,000 |
| 二等奖 | 6 main + special | 50,000 |
| 三等奖 | 6 main numbers | 3,000 |
| 四等奖 | 5 main + special | 500 |
| 五等奖 | 5 main numbers | 50 |
| 六等奖 | 4 main + special | 10 |
| 七等奖 | 4 main numbers | 5 |

### Usage Example
```python
from src.core import PredictionEngine

# Create prediction engine for 七乐彩
engine = PredictionEngine(lottery_type="七乐彩")

# Generate prediction
result = engine.predict_for_lottery_type()

print(result['formatted'])
# Output: Main: [3, 8, 12, 18, 22, 25, 29] + Special: [15]
```

---

## 4. 福彩3D (Welfare 3D)

### Game Description
福彩3D is a 3-digit lottery game where each digit ranges from 0-9. Players can choose different play types: straight (exact order) or group (any order).

### Configuration
```python
{
    "name": "Welfare 3D (福彩3D)",
    "category": "welfare",
    "description": "3 digits, each from 0-9",
    "digits": {
        "count": 3,
        "range": (0, 9),
        "name": "Digits"
    },
    "play_types": {
        "直选": "Exact order match",
        "组选3": "2 same + 1 different (any order)",
        "组选6": "All different (any order)"
    }
}
```

### Prize Structure
| Play Type | Description | Base Prize (¥) |
|-----------|-------------|----------------|
| 直选 | Exact order match | 1,040 |
| 组选3 | 2 same + 1 different | 346 |
| 组选6 | All different digits | 173 |

### Usage Example
```python
from src.core import PredictionEngine

# Create prediction engine for 福彩3D
engine = PredictionEngine(lottery_type="福彩3D")

# Generate prediction
result = engine.predict_for_lottery_type()

print(result['formatted'])
# Output: 379
```

---

## Complete Lottery Game List

The system now supports **9 lottery types** in total:

### Sports Lottery (体育彩票) - 4 games
1. **大乐透** (Super Lotto) - 5+2 numbers
2. **七星彩** (7-Star Lottery) - 7 digits
3. **排列三** (Pick 3) - 3 digits
4. **排列五** (Pick 5) - 5 digits

### Welfare Lottery (福利彩票) - 4 games
5. **双色球** (Double Color Ball) - 6+1 numbers
6. **快乐8** (Happy 8) - 10 from 80
7. **七乐彩** (7 Happy Lottery) - 7+1 numbers
8. **福彩3D** (Welfare 3D) - 3 digits

### General
9. **通用** (General) - Configurable

---

## Using Predictions with All 7 Algorithms

All welfare lottery types work with all 7 prediction algorithms:

```python
from src.core import PredictionEngine

# Create engine for any welfare lottery type
engine = PredictionEngine(lottery_type="双色球")

# Test individual algorithms
algorithms = [
    "frequency", 
    "hot_cold", 
    "pattern",
    "weighted_frequency",
    "gap_analysis",
    "moving_average",
    "cyclic_pattern"
]

for algo in algorithms:
    result = engine.predict(algorithm=algo, count=7)
    print(f"{algo}: {result}")

# Or use ensemble prediction (combines all algorithms)
ensemble_result = engine.predict_ensemble()
print(f"Ensemble: {ensemble_result['numbers']}")
print(f"Confidence: {ensemble_result['confidence']:.2f}")
```

---

## Validation and Formatting

Each lottery type includes validation and formatting:

```python
from src.config.lottery_types import get_lottery_type

# Get lottery type
lottery = get_lottery_type("双色球")

# Validate numbers
numbers = [3, 12, 18, 25, 28, 31, 8]
is_valid = lottery.validate_numbers(numbers)
print(f"Valid: {is_valid}")  # True

# Format for display
formatted = lottery.format_prediction(numbers)
print(formatted)  # Red: [3, 12, 18, 25, 28, 31] + Blue: [8]

# Get prize structure
prizes = lottery.get_prize_structure()
for prize in prizes:
    print(f"{prize['level']}: {prize['description']} - ¥{prize['base_prize']:,}")
```

---

## Web Interface Support

All welfare lottery types are fully supported in the web interface:

### Access via Web
```bash
# Start web server
python web_app.py

# Access from browser
# Computer: http://localhost:5000
# Mobile: http://[your-ip]:5000
```

### Features in Web Interface
1. **Lottery Type Selector**: Choose from all 9 lottery types
2. **Algorithm Selection**: Test individual algorithms or ensemble
3. **Prediction History**: Save and review predictions
4. **Data Analysis**: Statistical analysis for each lottery type
5. **Mobile Optimized**: Perfect display on phones and tablets

---

## API Endpoints

Use the REST API to generate predictions programmatically:

```bash
# Generate prediction for 双色球
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "lottery_type": "双色球",
    "algorithm": "ensemble"
  }'

# Response
{
  "success": true,
  "lottery_type": "双色球",
  "algorithm": "ensemble",
  "numbers": [3, 12, 18, 25, 28, 31, 8],
  "formatted": "Red: [3, 12, 18, 25, 28, 31] + Blue: [8]",
  "confidence": 0.85
}
```

---

## Testing

Comprehensive test suite validates all welfare lottery types:

```bash
# Run welfare lottery tests
python tests/test_welfare_lottery_types.py

# Run all lottery type tests
python -m pytest tests/test_lottery_types.py tests/test_welfare_lottery_types.py -v
```

---

## Additional Resources

- **LOTTERY_TYPES.md** - Sports lottery documentation
- **STATISTICAL_MODELS.md** - Prediction algorithm details
- **WEB_INTERFACE_GUIDE.md** - Web interface user guide
- **WEB_DEPLOYMENT.md** - Deployment instructions

---

## Summary

The lottery analysis system now provides complete coverage of Chinese lottery games:

✅ **4 Sports Lottery games** (体育彩票)  
✅ **4 Welfare Lottery games** (福利彩票)  
✅ **7 Prediction algorithms**  
✅ **Desktop GUI** + **Web Interface** + **CLI**  
✅ **Multi-device access** (PC, phone, tablet)  
✅ **Comprehensive testing** and documentation

Perfect for analyzing and predicting both sports and welfare lottery games in China!
