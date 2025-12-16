"""
Lottery Types Configuration
Defines rules and configurations for different lottery games.
"""

from typing import Dict, List, Tuple


# Chinese Sports Lottery Game Configurations
# Chinese Welfare Lottery Game Configurations
LOTTERY_GAMES = {
    # Sports Lottery Games (体育彩票)
    "大乐透": {
        "name": "Super Lotto (大乐透)",
        "name_en": "Super Lotto",
        "category": "sports",
        "description": "5 main numbers (1-35) + 2 bonus numbers (1-12)",
        "main_numbers": {
            "count": 5,
            "range": (1, 35),
            "name": "Main Numbers"
        },
        "bonus_numbers": {
            "count": 2,
            "range": (1, 12),
            "name": "Bonus Numbers"
        },
        "prize_levels": [
            {"level": "一等奖", "description": "5+2", "base_prize": 10000000},
            {"level": "二等奖", "description": "5+1", "base_prize": 500000},
            {"level": "三等奖", "description": "5+0", "base_prize": 10000},
            {"level": "四等奖", "description": "4+2", "base_prize": 3000},
            {"level": "五等奖", "description": "4+1", "base_prize": 300},
            {"level": "六等奖", "description": "3+2", "base_prize": 200},
            {"level": "七等奖", "description": "4+0 or 3+1 or 2+2", "base_prize": 100},
            {"level": "八等奖", "description": "3+0 or 2+1 or 1+2 or 0+2", "base_prize": 15},
            {"level": "九等奖", "description": "2+0 or 1+1 or 0+1", "base_prize": 5}
        ]
    },
    
    "七星彩": {
        "name": "7-Star Lottery (七星彩)",
        "name_en": "7-Star Lottery",
        "category": "sports",
        "description": "7 digits, each from 0-9",
        "digits": {
            "count": 7,
            "range": (0, 9),
            "name": "Digits"
        },
        "prize_levels": [
            {"level": "一等奖", "description": "7 digits match", "base_prize": 5000000},
            {"level": "二等奖", "description": "6 consecutive digits match", "base_prize": 100000},
            {"level": "三等奖", "description": "5 consecutive digits match", "base_prize": 1800},
            {"level": "四等奖", "description": "4 consecutive digits match", "base_prize": 300},
            {"level": "五等奖", "description": "3 consecutive digits match", "base_prize": 20},
            {"level": "六等奖", "description": "2 consecutive digits match", "base_prize": 5}
        ]
    },
    
    "排列三": {
        "name": "Pick 3 (排列三)",
        "name_en": "Pick 3",
        "category": "sports",
        "description": "3 digits, each from 0-9",
        "digits": {
            "count": 3,
            "range": (0, 9),
            "name": "Digits"
        },
        "play_types": {
            "直选": "Exact order match",
            "组选3": "2 same + 1 different",
            "组选6": "All different"
        },
        "prize_levels": [
            {"level": "直选", "description": "Exact order", "base_prize": 1040},
            {"level": "组选3", "description": "2 same", "base_prize": 346},
            {"level": "组选6", "description": "All different", "base_prize": 173}
        ]
    },
    
    "排列五": {
        "name": "Pick 5 (排列五)",
        "name_en": "Pick 5",
        "category": "sports",
        "description": "5 digits, each from 0-9",
        "digits": {
            "count": 5,
            "range": (0, 9),
            "name": "Digits"
        },
        "prize_levels": [
            {"level": "一等奖", "description": "5 digits exact match", "base_prize": 100000}
        ]
    },
    
    # Welfare Lottery Games (福利彩票)
    "双色球": {
        "name": "Double Color Ball (双色球)",
        "name_en": "Double Color Ball",
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
        },
        "prize_levels": [
            {"level": "一等奖", "description": "6+1", "base_prize": 5000000},
            {"level": "二等奖", "description": "6+0", "base_prize": 200000},
            {"level": "三等奖", "description": "5+1", "base_prize": 3000},
            {"level": "四等奖", "description": "5+0 or 4+1", "base_prize": 200},
            {"level": "五等奖", "description": "4+0 or 3+1", "base_prize": 10},
            {"level": "六等奖", "description": "2+1 or 1+1 or 0+1", "base_prize": 5}
        ]
    },
    
    "快乐8": {
        "name": "Happy 8 (快乐8)",
        "name_en": "Happy 8",
        "category": "welfare",
        "description": "Select 1-10 numbers from 1-80, draw 20 numbers",
        "main_numbers": {
            "count": 10,  # Player can choose 1-10, we default to 10
            "range": (1, 80),
            "name": "Numbers"
        },
        "draw_count": 20,  # 20 numbers are drawn each game
        "prize_levels": [
            {"level": "选十中十", "description": "10 of 10", "base_prize": 5000000},
            {"level": "选十中九", "description": "9 of 10", "base_prize": 50000},
            {"level": "选十中八", "description": "8 of 10", "base_prize": 9000},
            {"level": "选十中七", "description": "7 of 10", "base_prize": 300},
            {"level": "选十中六", "description": "6 of 10", "base_prize": 50},
            {"level": "选十中五", "description": "5 of 10", "base_prize": 20},
            {"level": "选十中零", "description": "0 of 10", "base_prize": 5}
        ]
    },
    
    "七乐彩": {
        "name": "7 Happy Lottery (七乐彩)",
        "name_en": "7 Happy Lottery",
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
        },
        "prize_levels": [
            {"level": "一等奖", "description": "7 main numbers", "base_prize": 5000000},
            {"level": "二等奖", "description": "6 main + special", "base_prize": 50000},
            {"level": "三等奖", "description": "6 main numbers", "base_prize": 3000},
            {"level": "四等奖", "description": "5 main + special", "base_prize": 500},
            {"level": "五等奖", "description": "5 main numbers", "base_prize": 50},
            {"level": "六等奖", "description": "4 main + special", "base_prize": 10},
            {"level": "七等奖", "description": "4 main numbers", "base_prize": 5}
        ]
    },
    
    "福彩3D": {
        "name": "Welfare 3D (福彩3D)",
        "name_en": "Welfare 3D",
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
        },
        "prize_levels": [
            {"level": "直选", "description": "Exact order", "base_prize": 1040},
            {"level": "组选3", "description": "2 same", "base_prize": 346},
            {"level": "组选6", "description": "All different", "base_prize": 173}
        ]
    },
    
    # Generic lottery for backward compatibility
    "通用": {
        "name": "General Lottery (通用)",
        "name_en": "General Lottery",
        "category": "general",
        "description": "Configurable lottery game",
        "main_numbers": {
            "count": 6,
            "range": (1, 49),
            "name": "Numbers"
        }
    }
}


class LotteryType:
    """Represents a lottery game type with its rules and configuration."""
    
    def __init__(self, game_type: str = "通用"):
        """
        Initialize lottery type with configuration.
        
        Args:
            game_type: Type of lottery game (大乐透, 七星彩, 排列三, 排列五, 通用).
        """
        if game_type not in LOTTERY_GAMES:
            raise ValueError(f"Unknown lottery type: {game_type}. Available: {list(LOTTERY_GAMES.keys())}")
        
        self.game_type = game_type
        self.config = LOTTERY_GAMES[game_type]
        self.name = self.config['name']
        self.name_en = self.config['name_en']
        self.description = self.config['description']
    
    def get_number_count(self) -> int:
        """Get total count of numbers to predict."""
        if 'main_numbers' in self.config:
            count = self.config['main_numbers']['count']
            if 'bonus_numbers' in self.config:
                count += self.config['bonus_numbers']['count']
            return count
        elif 'digits' in self.config:
            return self.config['digits']['count']
        return 6
    
    def get_number_ranges(self) -> List[Tuple[int, int]]:
        """
        Get number ranges for this lottery type.
        
        Returns:
            List of tuples (min, max) for each number position.
        """
        ranges = []
        
        if 'main_numbers' in self.config:
            main = self.config['main_numbers']
            for _ in range(main['count']):
                ranges.append(main['range'])
            
            if 'bonus_numbers' in self.config:
                bonus = self.config['bonus_numbers']
                for _ in range(bonus['count']):
                    ranges.append(bonus['range'])
        
        elif 'digits' in self.config:
            digit_range = self.config['digits']['range']
            digit_count = self.config['digits']['count']
            for _ in range(digit_count):
                ranges.append(digit_range)
        
        return ranges
    
    def format_prediction(self, numbers: List[int]) -> str:
        """
        Format prediction numbers according to lottery type.
        
        Args:
            numbers: List of predicted numbers.
            
        Returns:
            Formatted string representation.
        """
        if self.game_type == "大乐透":
            if len(numbers) >= 7:
                main = numbers[:5]
                bonus = numbers[5:7]
                return f"Main: {main} + Bonus: {bonus}"
            else:
                return str(numbers)
        
        elif self.game_type == "双色球":
            if len(numbers) >= 7:
                red = numbers[:6]
                blue = numbers[6]
                return f"Red: {red} + Blue: [{blue}]"
            else:
                return str(numbers)
        
        elif self.game_type == "快乐8":
            # Player selections
            return f"Selected: {numbers}"
        
        elif self.game_type == "七乐彩":
            if len(numbers) >= 8:
                main = numbers[:7]
                special = numbers[7]
                return f"Main: {main} + Special: [{special}]"
            else:
                return str(numbers)
        
        elif self.game_type in ["七星彩", "排列三", "排列五", "福彩3D"]:
            # Digit-based lotteries
            return ''.join(str(d) for d in numbers)
        
        else:
            return str(numbers)
    
    def get_prize_structure(self) -> List[Dict]:
        """Get prize structure for this lottery type."""
        return self.config.get('prize_levels', [])
    
    def validate_numbers(self, numbers: List[int]) -> bool:
        """
        Validate if numbers are valid for this lottery type.
        
        Args:
            numbers: List of numbers to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        ranges = self.get_number_ranges()
        
        if len(numbers) != len(ranges):
            return False
        
        for num, (min_val, max_val) in zip(numbers, ranges):
            if not (min_val <= num <= max_val):
                return False
        
        return True
    
    @staticmethod
    def get_available_games() -> List[str]:
        """Get list of available lottery game types."""
        return list(LOTTERY_GAMES.keys())
    
    @staticmethod
    def get_game_info(game_type: str) -> Dict:
        """Get configuration info for a specific game type."""
        return LOTTERY_GAMES.get(game_type, {})


def get_lottery_type(game_type: str = "通用") -> LotteryType:
    """
    Factory function to create LotteryType instance.
    
    Args:
        game_type: Type of lottery game.
        
    Returns:
        LotteryType instance.
    """
    return LotteryType(game_type)
