"""
Password Generator Module
Generates strong, secure passwords automatically.
"""

import random
import string
from typing import Optional


class PasswordGenerator:
    """Generates strong passwords based on specified criteria."""
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize password generator with configuration.
        
        Args:
            config: Configuration dictionary with password settings.
        """
        if config is None:
            config = {}
        
        self.length = config.get('password_length', 16)
        self.include_special = config.get('password_include_special', True)
        self.include_numbers = config.get('password_include_numbers', True)
        self.include_uppercase = config.get('password_include_uppercase', True)
    
    def generate(self, length: Optional[int] = None) -> str:
        """
        Generate a strong password.
        
        Args:
            length: Password length. If None, uses configured default.
            
        Returns:
            Generated password string.
        """
        if length is None:
            length = self.length
        
        # Build character set based on configuration
        chars = string.ascii_lowercase
        
        if self.include_uppercase:
            chars += string.ascii_uppercase
        
        if self.include_numbers:
            chars += string.digits
        
        if self.include_special:
            chars += string.punctuation
        
        # Ensure password has at least one character from each enabled category
        password = []
        
        if self.include_uppercase:
            password.append(random.choice(string.ascii_uppercase))
        
        if self.include_numbers:
            password.append(random.choice(string.digits))
        
        if self.include_special:
            password.append(random.choice(string.punctuation))
        
        # Always include at least one lowercase letter
        password.append(random.choice(string.ascii_lowercase))
        
        # Fill the rest with random characters from the full set
        remaining_length = length - len(password)
        password.extend(random.choices(chars, k=remaining_length))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password)
        
        return ''.join(password)
    
    def generate_multiple(self, count: int = 5, length: Optional[int] = None) -> list:
        """
        Generate multiple passwords.
        
        Args:
            count: Number of passwords to generate.
            length: Password length for each password.
            
        Returns:
            List of generated passwords.
        """
        return [self.generate(length) for _ in range(count)]
