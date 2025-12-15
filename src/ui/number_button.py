"""
Number Button Component
Custom button widget for selecting lottery numbers.
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont


class NumberButton(QPushButton):
    """Custom button for lottery number selection."""
    
    number_selected = Signal(int, bool)  # number, is_selected
    
    def __init__(self, number: int, parent=None):
        """
        Initialize number button.
        
        Args:
            number: The lottery number this button represents.
            parent: Parent widget.
        """
        super().__init__(str(number), parent)
        self.number = number
        self.is_selected = False
        
        # Set button styling
        self.setCheckable(True)
        self.setMinimumSize(50, 50)
        self.setMaximumSize(80, 80)
        
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.setFont(font)
        
        # Connect signal
        self.clicked.connect(self._on_clicked)
        
        # Initial style
        self._update_style()
    
    def _on_clicked(self):
        """Handle button click."""
        self.is_selected = self.isChecked()
        self._update_style()
        self.number_selected.emit(self.number, self.is_selected)
    
    def _update_style(self):
        """Update button appearance based on selection state."""
        if self.is_selected:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: 2px solid #45a049;
                    border-radius: 25px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    color: #333;
                    border: 2px solid #ccc;
                    border-radius: 25px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border-color: #999;
                }
            """)
    
    def set_selected(self, selected: bool):
        """
        Set selection state programmatically.
        
        Args:
            selected: Whether the button should be selected.
        """
        self.is_selected = selected
        self.setChecked(selected)
        self._update_style()
    
    def get_number(self) -> int:
        """Get the number represented by this button."""
        return self.number
