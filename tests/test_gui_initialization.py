"""
Test GUI initialization without displaying the window.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set QT_QPA_PLATFORM to offscreen to avoid display issues
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PySide6.QtWidgets import QApplication
from src.ui.lottery_app import LotteryApp


def test_gui_initialization():
    """Test that the GUI can be initialized."""
    print("Testing GUI initialization...")
    
    # Create QApplication instance
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create main window (without showing)
    window = LotteryApp()
    
    # Verify window properties
    assert window is not None
    assert window.windowTitle() == 'Lottery Analysis System'
    assert window.config_manager is not None
    assert window.data_handler is not None
    assert window.data_analyzer is not None
    assert window.prediction_engine is not None
    assert window.record_manager is not None
    assert window.password_generator is not None
    
    # Verify tabs
    assert window.tabs.count() == 4  # Analysis, Prediction, Data Management, Utilities
    
    print("✓ GUI initialization test passed")
    
    return True


if __name__ == '__main__':
    try:
        success = test_gui_initialization()
        print("\nGUI test completed successfully!")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ GUI test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
