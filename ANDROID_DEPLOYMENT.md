# Android Deployment Guide

This guide explains how to deploy the Lottery Analysis System to Android platforms.

## Option 1: Using Buildozer with Kivy

### Prerequisites
- Linux or macOS (recommended)
- Python 3.8+
- Android SDK and NDK

### Steps

1. Install Buildozer:
```bash
pip install buildozer
```

2. Create a `buildozer.spec` file in the project root:
```bash
buildozer init
```

3. Modify the `buildozer.spec` file:
```ini
[app]
title = Lottery Analysis
package.name = lotteryanalysis
package.domain = org.lottery

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0.0

requirements = python3,kivy,numpy,pandas,matplotlib,requests

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
```

4. Build the APK:
```bash
buildozer android debug
```

5. Install on device:
```bash
buildozer android deploy run
```

## Option 2: Using BeeWare

### Prerequisites
- Python 3.8+
- BeeWare Briefcase

### Steps

1. Install BeeWare:
```bash
pip install briefcase
```

2. Create a `pyproject.toml` file:
```toml
[tool.briefcase]
project_name = "Lottery Analysis System"
bundle = "org.lottery"

[tool.briefcase.app.lotteryanalysis]
formal_name = "Lottery Analysis"
description = "Lottery analysis and prediction system"
sources = ["src"]
requires = [
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "matplotlib>=3.7.0",
    "requests>=2.31.0",
]

[tool.briefcase.app.lotteryanalysis.android]
build_gradle_dependencies = []
```

3. Create Android app:
```bash
briefcase create android
```

4. Build the Android app:
```bash
briefcase build android
```

5. Run on device/emulator:
```bash
briefcase run android
```

## Option 3: Using Chaquopy (Python in Android Studio)

### Prerequisites
- Android Studio
- Chaquopy plugin

### Steps

1. Create a new Android project in Android Studio

2. Add Chaquopy to `build.gradle`:
```gradle
plugins {
    id 'com.chaquo.python' version '14.0.2'
}

android {
    defaultConfig {
        python {
            pip {
                install "numpy"
                install "pandas"
                install "matplotlib"
            }
        }
    }
}
```

3. Copy Python source files to `app/src/main/python/`

4. Create Android UI in Java/Kotlin that calls Python code

5. Build and run the app

## Adapting the UI for Mobile

The current PySide6 GUI is designed for desktop. For Android, you'll need to:

### Using Kivy (Recommended for Mobile)

Create a mobile-friendly UI using Kivy:

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class LotteryMobileApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Add title
        title = Label(text='Lottery Analysis', font_size='20sp')
        layout.add_widget(title)
        
        # Add buttons
        analyze_btn = Button(text='Analyze Data')
        analyze_btn.bind(on_press=self.analyze_data)
        layout.add_widget(analyze_btn)
        
        predict_btn = Button(text='Generate Prediction')
        predict_btn.bind(on_press=self.generate_prediction)
        layout.add_widget(predict_btn)
        
        return layout
    
    def analyze_data(self, instance):
        # Use existing DataAnalyzer
        pass
    
    def generate_prediction(self, instance):
        # Use existing PredictionEngine
        pass

if __name__ == '__main__':
    LotteryMobileApp().run()
```

## Core Modules Compatibility

The following modules are fully compatible with Android without modification:

- ✅ `src/config/config_manager.py` - Configuration management
- ✅ `src/core/data_analyzer.py` - Data analysis
- ✅ `src/core/prediction_engine.py` - Prediction engine
- ✅ `src/core/record_manager.py` - Record management
- ✅ `src/data/data_handler.py` - Data import/export
- ✅ `src/utils/password_generator.py` - Password generation
- ✅ `src/utils/logger.py` - Logging

Modules requiring adaptation for Android:

- ⚠️ `src/ui/lottery_app.py` - Desktop GUI (needs mobile UI replacement)
- ⚠️ `src/ui/number_button.py` - Desktop widget (needs mobile widget replacement)
- ⚠️ `src/data/visualizer.py` - May need Android-specific backend for matplotlib

## Testing on Android

1. Use Android emulator for initial testing
2. Test on physical devices with different screen sizes
3. Verify file permissions for data import/export
4. Test network permissions if adding live data features
5. Verify storage permissions for saving records

## Performance Considerations

- Pre-compile Python code to reduce startup time
- Optimize data loading for mobile devices
- Consider using SQLite for large datasets
- Implement lazy loading for visualizations
- Cache frequently accessed data

## Distribution

### Google Play Store
1. Sign the APK with a release keystore
2. Create app listing with screenshots
3. Set up pricing and distribution
4. Submit for review

### Alternative Distribution
1. Direct APK download from website
2. F-Droid for open-source distribution
3. Amazon Appstore

## Permissions Required

Add to `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are included in requirements
2. **File not found**: Use proper Android storage paths
3. **Permission denied**: Request runtime permissions in Android 6+
4. **Out of memory**: Reduce data size or implement pagination
5. **Slow startup**: Pre-compile Python code and optimize imports

## Resources

- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [BeeWare Tutorial](https://docs.beeware.org/en/latest/tutorial/)
- [Chaquopy Documentation](https://chaquo.com/chaquopy/doc/current/)
- [Kivy Documentation](https://kivy.org/doc/stable/)
- [Android Python Guide](https://developer.android.com/guide/practices)
