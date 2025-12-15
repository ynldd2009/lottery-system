# Chinese Sports Lottery Games Support

This document describes the Chinese sports lottery games supported by the Lottery Analysis System.

## Supported Lottery Games

The system now supports **5 lottery types**:
1. **大乐透** (Super Lotto / Da Le Tou)
2. **七星彩** (7-Star Lottery / Qi Xing Cai)
3. **排列三** (Pick 3 / Pai Lie San)
4. **排列五** (Pick 5 / Pai Lie Wu)
5. **通用** (General Lottery)

---

## 1. 大乐透 (Super Lotto)

### Game Rules
- **Main Numbers**: Select 5 numbers from 1-35
- **Bonus Numbers**: Select 2 numbers from 1-12
- **Total**: 7 numbers (5 + 2)

### Prize Structure
| Level | Match | Base Prize (¥) |
|-------|-------|----------------|
| 一等奖 | 5+2 | 10,000,000 |
| 二等奖 | 5+1 | 500,000 |
| 三等奖 | 5+0 | 10,000 |
| 四等奖 | 4+2 | 3,000 |
| 五等奖 | 4+1 | 300 |
| 六等奖 | 3+2 | 200 |
| 七等奖 | 4+0 / 3+1 / 2+2 | 100 |
| 八等奖 | 3+0 / 2+1 / 1+2 / 0+2 | 15 |
| 九等奖 | 2+0 / 1+1 / 0+1 | 5 |

### Usage Example
```python
from src.core import PredictionEngine
from src.data import DataHandler

# Load data
handler = DataHandler()
data = handler.create_sample_data(100)

# Create prediction engine for 大乐透
engine = PredictionEngine(lottery_type="大乐透")
engine.load_historical_data(data)

# Generate prediction
result = engine.predict_for_lottery_type()
print(result['formatted'])
# Output: Main: [3, 12, 18, 25, 33] + Bonus: [5, 11]
```

---

## 2. 七星彩 (7-Star Lottery)

### Game Rules
- **Format**: 7 digits, each from 0-9
- **Example**: 1234567

### Prize Structure
| Level | Match | Base Prize (¥) |
|-------|-------|----------------|
| 一等奖 | 7 digits | 5,000,000 |
| 二等奖 | 6 consecutive | 100,000 |
| 三等奖 | 5 consecutive | 1,800 |
| 四等奖 | 4 consecutive | 300 |
| 五等奖 | 3 consecutive | 20 |
| 六等奖 | 2 consecutive | 5 |

### Usage Example
```python
engine = PredictionEngine(lottery_type="七星彩")
engine.load_historical_data(data)
result = engine.predict_for_lottery_type()
print(result['formatted'])
# Output: 1234567
```

---

## 3. 排列三 (Pick 3)

### Game Rules
- **Format**: 3 digits, each from 0-9
- **Example**: 123

### Play Types
- **直选** (Straight): Exact order match
- **组选3**: 2 same digits + 1 different
- **组选6**: All 3 digits different

### Prize Structure
| Type | Prize (¥) |
|------|-----------|
| 直选 | 1,040 |
| 组选3 | 346 |
| 组选6 | 173 |

### Usage Example
```python
engine = PredictionEngine(lottery_type="排列三")
engine.load_historical_data(data)
result = engine.predict_for_lottery_type()
print(result['formatted'])
# Output: 123
```

---

## 4. 排列五 (Pick 5)

### Game Rules
- **Format**: 5 digits, each from 0-9
- **Example**: 12345

### Prize Structure
| Level | Match | Prize (¥) |
|-------|-------|-----------|
| 一等奖 | 5 digits exact | 100,000 |

### Usage Example
```python
engine = PredictionEngine(lottery_type="排列五")
engine.load_historical_data(data)
result = engine.predict_for_lottery_type()
print(result['formatted'])
# Output: 12345
```

---

## 5. 通用 (General Lottery)

### Game Rules
- **Default**: 6 numbers from 1-49
- **Configurable**: Can be adapted to any lottery format

### Usage Example
```python
engine = PredictionEngine(lottery_type="通用")
engine.load_historical_data(data)
result = engine.predict_for_lottery_type()
print(result['formatted'])
# Output: [5, 12, 23, 34, 39, 45]
```

---

## API Reference

### LotteryType Class

```python
from src.config.lottery_types import LotteryType, get_lottery_type

# Create lottery type instance
lottery = get_lottery_type("大乐透")

# Get game info
print(lottery.name)  # "Super Lotto (大乐透)"
print(lottery.description)  # "5 main numbers (1-35) + 2 bonus numbers (1-12)"

# Get number configuration
count = lottery.get_number_count()  # 7
ranges = lottery.get_number_ranges()  # [(1,35), (1,35), ..., (1,12), (1,12)]

# Format prediction
numbers = [3, 12, 18, 25, 33, 5, 11]
formatted = lottery.format_prediction(numbers)
# "Main: [3, 12, 18, 25, 33] + Bonus: [5, 11]"

# Validate numbers
valid = lottery.validate_numbers(numbers)  # True/False

# Get available games
games = LotteryType.get_available_games()
# ['大乐透', '七星彩', '排列三', '排列五', '通用']
```

### PredictionEngine with Lottery Types

```python
from src.core import PredictionEngine

# Initialize with lottery type
engine = PredictionEngine(
    lottery_type="大乐透",
    config={'prediction_algorithms': ['frequency', 'hot_cold', 'pattern']}
)

# Load data
engine.load_historical_data(data)

# Generate type-specific prediction
result = engine.predict_for_lottery_type()

# Result structure
{
    'lottery_type': 'Super Lotto (大乐透)',
    'main_numbers': [3, 12, 18, 25, 33],  # For 大乐透
    'bonus_numbers': [5, 11],             # For 大乐透
    'digits': [1, 2, 3, 4, 5],           # For digit lotteries
    'formatted': 'Main: [3, 12, 18, 25, 33] + Bonus: [5, 11]',
    'confidence': 0.85,
    'algorithms_used': ['frequency', 'hot_cold', 'pattern']
}
```

---

## Testing

Run tests for lottery types:

```bash
python tests/test_lottery_types.py
```

Expected output:
```
=== Testing Lottery Types Support ===

Testing lottery type initialization...
  ✓ 大乐透: Super Lotto (大乐透)
  ✓ 七星彩: 7-Star Lottery (七星彩)
  ✓ 排列三: Pick 3 (排列三)
  ✓ 排列五: Pick 5 (排列五)
  ✓ 通用: General Lottery (通用)
✓ Lottery type initialization test passed

...

=== All Lottery Types Tests Passed! ===
```

---

## Data Format

### For Number-Based Lotteries (大乐透, 通用)

CSV format:
```csv
date,draw_number,numbers
2024-01-01,2024001,"5,12,18,25,33,2,8"
2024-01-04,2024002,"3,15,22,28,35,1,11"
```

JSON format:
```json
[
  {
    "date": "2024-01-01",
    "draw_number": "2024001",
    "numbers": [5, 12, 18, 25, 33, 2, 8]
  }
]
```

### For Digit-Based Lotteries (七星彩, 排列三, 排列五)

CSV format:
```csv
date,draw_number,digits
2024-01-01,2024001,"1234567"
2024-01-04,2024002,"9876543"
```

JSON format:
```json
[
  {
    "date": "2024-01-01",
    "draw_number": "2024001",
    "digits": "1234567"
  }
]
```

---

## Configuration

Add lottery type to your configuration:

```json
{
  "lottery": {
    "default_type": "大乐透",
    "available_types": ["大乐透", "七星彩", "排列三", "排列五", "通用"]
  },
  "prediction": {
    "analysis_window": 30,
    "prediction_algorithms": [
      "frequency",
      "hot_cold",
      "pattern",
      "weighted_frequency",
      "gap_analysis",
      "moving_average",
      "cyclic_pattern"
    ]
  }
}
```

---

## Notes

### Prediction Methods

1. **Number-based lotteries** (大乐透, 通用):
   - Use all 7 statistical models
   - Ensemble prediction for best results
   - Separate predictions for main and bonus numbers

2. **Digit-based lotteries** (七星彩, 排列三, 排列五):
   - Each digit position predicted independently
   - Currently uses random selection
   - Future: Position-specific frequency analysis

### Limitations

- Digit-based predictions currently use random selection due to lack of position-specific historical data
- More accurate digit predictions require position-aware historical data
- Prize calculations are based on base amounts and don't include pool/jackpot variations

### Future Enhancements

- Position-specific frequency analysis for digit lotteries
- Integration with official lottery APIs for live data
- Prize pool calculation
- Winning statistics tracking
- Multi-lottery comparison

---

## Summary

The Lottery Analysis System now supports 5 lottery types:

| Lottery | Type | Numbers | Format |
|---------|------|---------|--------|
| 大乐透 | Number | 5 (1-35) + 2 (1-12) | Main + Bonus |
| 七星彩 | Digit | 7 digits (0-9) | 1234567 |
| 排列三 | Digit | 3 digits (0-9) | 123 |
| 排列五 | Digit | 5 digits (0-9) | 12345 |
| 通用 | Number | 6 (1-49) | [1,2,3,4,5,6] |

All lottery types integrate with the existing prediction engine and support all 7 statistical models where applicable.
