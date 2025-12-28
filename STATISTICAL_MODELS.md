# Statistical Models Documentation

This document describes all prediction models available in the Lottery Analysis System.

## Overview

The system now includes **7 statistical models** for lottery number prediction:
- 3 Original models
- 4 New statistical models (Phase 1 implementation)

All models can be used individually or combined in an ensemble prediction for best results.

---

## Original Models

### 1. Frequency-Based Prediction
**Algorithm:** `frequency`

**Description:** Predicts numbers based on their historical appearance frequency.

**Logic:**
- Counts how often each number has appeared in all historical draws
- Selects the most frequently drawn numbers
- Assumption: Numbers that appeared frequently in the past are likely to appear again

**Best For:**
- Large datasets (100+ draws)
- General-purpose predictions
- Baseline comparisons

**Example:**
```python
engine.predict_by_frequency(count=6, number_range=(1, 49))
# Returns: [5, 10, 32, 37, 40, 49]
```

---

### 2. Hot/Cold Numbers
**Algorithm:** `hot_cold`

**Description:** Uses "hot" numbers that are currently frequently drawn.

**Logic:**
- Identifies numbers in the top 30th percentile of frequency (hot numbers)
- Identifies numbers in the bottom 30th percentile (cold numbers - not used in prediction)
- Randomly selects from hot numbers for prediction
- Assumption: Hot streaks continue for a period

**Best For:**
- Trend-following strategies
- Short to medium-term predictions
- Capturing momentum

**Example:**
```python
engine.predict_by_hot_numbers(count=6, number_range=(1, 49))
# Returns: [7, 22, 37, 41, 44, 47]
```

---

### 3. Pattern-Based Prediction
**Algorithm:** `pattern`

**Description:** Creates balanced predictions based on odd/even and high/low ratios.

**Logic:**
- Analyzes historical patterns (odd/even ratio, high/low distribution)
- Generates predictions maintaining statistical balance
- Uses weighted random selection based on frequency
- Assumption: Lottery draws tend to be balanced

**Best For:**
- Creating realistic number combinations
- Avoiding extreme selections
- Balanced portfolio approach

**Example:**
```python
engine.predict_by_pattern(count=6, number_range=(1, 49))
# Returns: [6, 21, 36, 40, 41, 43]
```

---

## New Statistical Models (Phase 1)

### 4. Weighted Frequency
**Algorithm:** `weighted_frequency`

**Description:** Enhanced frequency analysis giving more weight to recent draws.

**Logic:**
- Applies exponential decay to historical frequencies
- Recent draws weighted more heavily than older draws
- Weight formula: `weight = exp(-(total_draws - draw_index) / (total_draws * 0.3))`
- Assumption: Recent patterns are more relevant than distant history

**Mathematical Model:**
```
weighted_freq[number] = Σ (appearance * exp(-age_factor))
```

**Best For:**
- Adapting to recent trends
- Dynamic datasets
- Short-term predictions

**Example:**
```python
engine.predict_by_weighted_frequency(count=6, number_range=(1, 49))
# Returns: [5, 10, 14, 32, 48, 49]
```

---

### 5. Gap Analysis
**Algorithm:** `gap_analysis`

**Description:** Predicts numbers that are "due" based on how long since last appearance.

**Logic:**
- Calculates gap (number of draws) since each number last appeared
- Numbers with larger gaps are considered more "due"
- Adds randomness to avoid deterministic patterns
- Assumption: Numbers that haven't appeared recently are due to appear

**Mathematical Model:**
```
gap[number] = current_draw - last_appearance_draw
score = gap_size (with random selection from top candidates)
```

**Best For:**
- Regression to mean strategies
- Long-term patterns
- Complementing hot number strategies

**Example:**
```python
engine.predict_by_gap_analysis(count=6, number_range=(1, 49))
# Returns: [9, 16, 28, 31, 42, 47]
```

---

### 6. Moving Average
**Algorithm:** `moving_average`

**Description:** Uses frequency within a recent window of draws.

**Logic:**
- Analyzes only the most recent N draws (default: 10)
- Calculates frequency within this window
- Adapts quickly to recent changes
- Assumption: Recent local trends are predictive

**Parameters:**
- `window`: Number of recent draws to consider (default: 10)

**Mathematical Model:**
```
frequency[number] = count in last N draws
N = window size (configurable)
```

**Best For:**
- Capturing short-term trends
- Volatile patterns
- Quick adaptation to changes

**Example:**
```python
engine.predict_by_moving_average(count=6, number_range=(1, 49), window=10)
# Returns: [5, 7, 14, 20, 32, 43]
```

---

### 7. Cyclic Pattern
**Algorithm:** `cyclic_pattern`

**Description:** Detects cyclical patterns in number appearances.

**Logic:**
- Tracks appearance intervals for each number
- Calculates average cycle length between appearances
- Predicts numbers whose cycle suggests they're due
- Scores based on proximity to expected cycle
- Assumption: Numbers have somewhat regular appearance cycles

**Mathematical Model:**
```
avg_cycle[number] = mean(gaps between appearances)
current_gap = draws since last appearance
cycle_score = 1 - |current_gap - avg_cycle| / avg_cycle
```

**Best For:**
- Long-term datasets with sufficient history
- Identifying periodic patterns
- Advanced statistical analysis

**Example:**
```python
engine.predict_by_cyclic_pattern(count=6, number_range=(1, 49))
# Returns: [4, 11, 12, 28, 37, 45]
```

---

## Ensemble Prediction

**Algorithm:** `ensemble`

**Description:** Combines all active algorithms through a voting mechanism.

**Logic:**
- Runs all configured algorithms
- Each algorithm "votes" for its predicted numbers
- Numbers with most votes are selected
- Provides most robust predictions by leveraging multiple strategies

**Configuration:**
```json
{
  "prediction": {
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

**Best For:**
- Most reliable predictions
- Reducing algorithm-specific biases
- Production use

**Example:**
```python
result = engine.generate_prediction_with_confidence(count=6, number_range=(1, 49))
# Returns: {
#   'predictions': {...},  # All algorithm predictions
#   'recommended': [5, 10, 32, 37, 40, 49],  # Ensemble result
#   'confidence': 1.0,
#   'data_points_used': 100,
#   'algorithms_used': ['frequency', 'hot_cold', 'pattern', ...]
# }
```

---

## Configuration

Enable/disable specific algorithms in `config.json`:

```json
{
  "prediction": {
    "analysis_window": 30,
    "min_data_points": 10,
    "prediction_algorithms": [
      "frequency",
      "hot_cold",
      "pattern",
      "weighted_frequency",
      "gap_analysis",
      "moving_average",
      "cyclic_pattern"
    ],
    "confidence_threshold": 0.6
  }
}
```

---

## Choosing the Right Model

### For Large Datasets (100+ draws):
- **Frequency-based**: Reliable baseline
- **Weighted Frequency**: Adapts to trends
- **Cyclic Pattern**: Detects long-term patterns
- **Ensemble**: Best overall choice

### For Small Datasets (10-50 draws):
- **Moving Average**: Works with limited data
- **Pattern-based**: Maintains balance
- **Gap Analysis**: Simple, effective

### For Recent Trend Focus:
- **Weighted Frequency**: Recent draws prioritized
- **Moving Average**: Short-term window
- **Hot/Cold**: Current momentum

### For Balanced Approach:
- **Pattern-based**: Maintains statistical balance
- **Ensemble**: Combines all strategies

---

## Performance Metrics

Model performance varies based on:
- **Dataset size**: Larger datasets improve accuracy
- **Pattern stability**: Stable patterns favor frequency models
- **Volatility**: High volatility favors moving average and gap analysis
- **Randomness**: Truly random lotteries make all models equal

**Confidence Scoring:**
```python
confidence = min(1.0, data_points / (min_data_points * 5))
```

Confidence increases with more historical data, capped at 100%.

---

## Testing

Run tests for all models:
```bash
python tests/test_new_statistical_models.py
```

Test individual models:
```python
from src.core import PredictionEngine
from src.data import DataHandler

# Load data
handler = DataHandler()
data = handler.create_sample_data(100)

# Test weighted frequency
engine = PredictionEngine({'prediction_algorithms': ['weighted_frequency']})
engine.load_historical_data(data)
prediction = engine.predict_by_weighted_frequency(count=6, number_range=(1, 49))
```

---

## Future Enhancements (Roadmap)

Planned for future phases:
- **Phase 2**: Chinese lottery-specific models (双色球)
- **Phase 3**: Machine Learning models (LSTM, Random Forest)
- **Phase 4**: AI-powered predictions (Deep Learning)

---

## References

Statistical concepts used:
- **Exponential Decay**: Weighted frequency model
- **Gap Analysis**: Regression to mean
- **Moving Average**: Time series analysis
- **Cyclical Analysis**: Periodic pattern detection
- **Ensemble Methods**: Voting mechanisms

---

## Summary

The system now provides 7 complementary prediction models:

| Model | Type | Best Use Case | Data Need |
|-------|------|--------------|-----------|
| Frequency | Statistical | General purpose | Medium |
| Hot/Cold | Momentum | Trend following | Medium |
| Pattern | Balance | Realistic picks | Any |
| Weighted Freq | Statistical | Recent trends | Medium |
| Gap Analysis | Regression | Due numbers | Large |
| Moving Average | Time series | Short-term | Small |
| Cyclic Pattern | Advanced | Long-term cycles | Large |
| **Ensemble** | **Combined** | **Best overall** | **Any** |

**Recommendation:** Use ensemble prediction for most reliable results.
