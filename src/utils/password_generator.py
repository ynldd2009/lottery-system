"""
Password Generator Module
Generates strong, secure passwords automatically using cryptographically strong random sources.
"""

import secrets
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
        Generate a strong password using cryptographically strong random source.
        
        Args:
            length: Password length. If None, uses configured default.
            
        Returns:
            Generated password string.
            
        Raises:
            ValueError: If length is less than minimum required.
        """
        if length is None:
            length = self.length
        
        # Ensure minimum length for character requirements
        min_length = sum([
            1,  # Always at least one lowercase
            1 if self.include_uppercase else 0,
            1 if self.include_numbers else 0,
            1 if self.include_special else 0
        ])
        
        if length < min_length:
            raise ValueError(f"Password length must be at least {min_length} to meet all requirements")
        
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
            password.append(secrets.choice(string.ascii_uppercase))
        
        if self.include_numbers:
            password.append(secrets.choice(string.digits))
        
        if self.include_special:
            password.append(secrets.choice(string.punctuation))
        
        # Always include at least one lowercase letter
        password.append(secrets.choice(string.ascii_lowercase))
        
        # Fill the rest with random characters from the full set
        remaining_length = length - len(password)
        if remaining_length > 0:
            password.extend([secrets.choice(chars) for _ in range(remaining_length)])
        
        # Shuffle to avoid predictable patterns using Fisher-Yates with secrets
        for i in range(len(password) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password[i], password[j] = password[j], password[i]
        
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
