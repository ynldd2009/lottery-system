#!/usr/bin/env python3
"""
Web-based interface for the Lottery Analysis and Prediction System.
Can be accessed from computers and mobile devices via browser.
"""

from flask import Flask, render_template, request, jsonify, send_file
import sys
from pathlib import Path
import json
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.config_manager import ConfigManager
from src.config.lottery_types import LOTTERY_GAMES
from src.core.data_analyzer import DataAnalyzer
from src.core.prediction_engine import PredictionEngine
from src.core.record_manager import RecordManager
from src.data.data_handler import DataHandler
from src.data.visualizer import Visualizer
from src.utils.password_generator import PasswordGenerator
from src.utils.logger import setup_logger
from src.utils.api_client import get_api_client, configure_api

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'lottery-system-secret-key-change-in-production'

# Initialize components
logger = setup_logger('web_app')
config_manager = ConfigManager()
data_handler = DataHandler()
record_manager = RecordManager()
password_generator = PasswordGenerator()

# Initialize API client
api_client = get_api_client()
try:
    # Try to load API credentials from api_config.json
    api_config_path = Path(__file__).parent / 'api_config.json'
    if api_config_path.exists():
        with open(api_config_path, 'r', encoding='utf-8') as f:
            api_config = json.load(f)
            configure_api(api_config.get('app_id', ''), api_config.get('app_secret', ''))
            logger.info("API client configured successfully")
    else:
        logger.warning("API config file not found. Using sample data. Create api_config.json from api_config.json.example")
except Exception as e:
    logger.warning(f"Failed to configure API client: {e}. Using sample data.")

# Global data storage (in production, use a database)
current_data = []


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', lottery_types=list(LOTTERY_GAMES.keys()))


@app.route('/api/homepage-info', methods=['GET'])
def get_homepage_info():
    """Get homepage information including time, deadlines, and announcements"""
    try:
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        today = now.weekday()
        
        # Current time
        current_time = now.strftime("%Y-%m-%d %H:%M:%S %A")
        
        # Deadline info
        deadlines = []
        if hour < 20 or (hour == 20 and minute == 0):
            if hour < 19:
                deadlines.append("双色球 20:00")
                deadlines.append("大乐透 20:00")
                deadlines.append("快乐8 20:00")
            if hour < 20:
                deadlines.append("福彩3D 20:30")
                deadlines.append("排列三 20:30")
                deadlines.append("排列五 20:30")
                deadlines.append("七星彩 20:30")
                deadlines.append("七乐彩 20:30")
        
        deadline_info = " | ".join(deadlines) if deadlines else "今日彩票销售已截止"
        
        # Announcement based on day of week
        if today in [0, 2, 4, 6]:  # Mon, Wed, Fri, Sun
            announcement = "🎯 今日开奖: 双色球、福彩3D、快乐8 | 祝您好运中大奖！"
        elif today in [1, 3, 5]:  # Tue, Thu, Sat
            announcement = "🎯 今日开奖: 大乐透、排列三、排列五、七星彩、七乐彩 | 祝您好运中大奖！"
        else:
            announcement = "🎯 今日开奖: 所有玩法 | 祝您好运中大奖！"
        
        # Get latest results from API
        latest_results = []
        api_client = get_api_client()
        
        if api_client.is_configured():
            # Try to get real data from API
            lottery_types_to_fetch = ["双色球", "大乐透", "福彩3D"]
            for lottery_type in lottery_types_to_fetch:
                try:
                    draw_data = api_client.get_latest_draw(lottery_type)
                    if draw_data:
                        formatted = api_client.format_draw_result(lottery_type, draw_data)
                        if formatted:
                            # Format numbers for display
                            if lottery_type == "双色球":
                                red_nums = ", ".join([f"{n:02d}" for n in formatted['numbers']])
                                blue_num = f"{formatted['extra_numbers'][0]:02d}" if formatted['extra_numbers'] else "??"
                                numbers_str = f"{red_nums} + {blue_num}"
                            elif lottery_type == "大乐透":
                                main_nums = ", ".join([f"{n:02d}" for n in formatted['numbers']])
                                bonus_nums = ", ".join([f"{n:02d}" for n in formatted['extra_numbers']])
                                numbers_str = f"{main_nums} + {bonus_nums}"
                            else:
                                numbers_str = " ".join([str(n) for n in formatted['numbers']])
                            
                            latest_results.append({
                                "lottery": lottery_type,
                                "period": formatted.get('period', ''),
                                "date": formatted.get('draw_date', '').split()[0] if formatted.get('draw_date') else '',
                                "numbers": numbers_str,
                                "status": "已开奖"
                            })
                except Exception as e:
                    logger.error(f"Error fetching {lottery_type} from API: {e}")
                    continue
        
        # Fallback to sample data if API is not configured or failed
        if not latest_results:
            latest_results = [
                {"lottery": "双色球", "period": "2024XXX", "date": "2024-12-15", "numbers": "03, 12, 18, 25, 28, 31 + 08", "status": "示例数据"},
                {"lottery": "大乐透", "period": "2024XXX", "date": "2024-12-14", "numbers": "05, 11, 19, 27, 33 + 02, 09", "status": "示例数据"},
                {"lottery": "福彩3D", "period": "2024XXX", "date": "2024-12-15", "numbers": "5 3 7", "status": "示例数据"}
            ]
        
        return jsonify({
            'success': True,
            'current_time': current_time,
            'deadline_info': deadline_info,
            'announcement': announcement,
            'latest_results': latest_results
        })
    except Exception as e:
        logger.error(f"Error getting homepage info: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/analysis')
def analysis():
    """Data analysis page"""
    return render_template('analysis.html')


@app.route('/prediction')
def prediction():
    """Prediction page"""
    return render_template('prediction.html', lottery_types=list(LOTTERY_GAMES.keys()))


@app.route('/data')
def data_management():
    """Data management page"""
    return render_template('data.html')


@app.route('/utilities')
def utilities():
    """Utilities page"""
    return render_template('utilities.html')


@app.route('/api/generate-sample-data', methods=['POST'])
def generate_sample_data():
    """Generate sample lottery data"""
    try:
        num_draws = request.json.get('num_draws', 100)
        data = data_handler.generate_sample_data(num_draws=num_draws)
        global current_data
        current_data = data
        return jsonify({'success': True, 'count': len(data), 'data': data[:10]})
    except Exception as e:
        logger.error(f"Error generating sample data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """Analyze lottery data"""
    try:
        if not current_data:
            return jsonify({'success': False, 'error': 'No data available. Generate or import data first.'}), 400
        
        analyzer = DataAnalyzer(current_data)
        analysis_results = analyzer.get_full_analysis()
        
        return jsonify({'success': True, 'results': analysis_results})
    except Exception as e:
        logger.error(f"Error analyzing data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def predict():
    """Generate lottery predictions"""
    try:
        lottery_type = request.json.get('lottery_type', '双色球')
        algorithm = request.json.get('algorithm', 'ensemble')
        
        if not current_data:
            return jsonify({'success': False, 'error': 'No data available. Generate or import data first.'}), 400
        
        engine = PredictionEngine(current_data, lottery_type=lottery_type)
        result = engine.predict_for_lottery_type()
        
        return jsonify({'success': True, 'prediction': result})
    except Exception as e:
        logger.error(f"Error generating prediction: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/predict-zone', methods=['POST'])
def predict_zone():
    """Generate zone-specific predictions (大乐透后区 or 双色球蓝球)"""
    try:
        lottery_type = request.json.get('lottery_type')
        zone_type = request.json.get('zone_type')  # 'daletou_back' or 'shuangseqiu_blue'
        
        if not current_data:
            return jsonify({'success': False, 'error': 'No data available. Generate or import data first.'}), 400
        
        engine = PredictionEngine(current_data, lottery_type=lottery_type)
        
        if zone_type == 'daletou_back':
            result = engine.predict_daletou_back_zone()
        elif zone_type == 'shuangseqiu_blue':
            result = engine.predict_shuangseqiu_blue_ball()
        else:
            return jsonify({'success': False, 'error': 'Invalid zone_type. Use "daletou_back" or "shuangseqiu_blue".'}), 400
        
        return jsonify({'success': True, 'prediction': result})
    except Exception as e:
        logger.error(f"Error generating zone prediction: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/check-prize', methods=['POST'])
def check_prize():
    """Check prize level for multiple lottery types"""
    try:
        numbers = request.json.get('numbers')  # Expected format: "3,9,12,13,26,32,9"
        lottery_type = request.json.get('lottery_type', '双色球')
        
        if not numbers:
            return jsonify({'success': False, 'error': '请输入号码'}), 400
        
        # Parse numbers
        try:
            num_list = [int(x.strip()) for x in numbers.split(',')]
        except ValueError:
            return jsonify({'success': False, 'error': '号码格式错误，请输入用逗号分隔的数字'}), 400
        
        # Route to appropriate checker
        if lottery_type == '双色球':
            return check_prize_ssq(num_list)
        elif lottery_type == '快乐8':
            return check_prize_kl8(num_list)
        elif lottery_type == '3D':
            return check_prize_3d(num_list)
        elif lottery_type == '七乐彩':
            return check_prize_qlc(num_list)
        else:
            return jsonify({'success': False, 'error': '不支持的彩票类型'}), 400
        
    except Exception as e:
        logger.error(f"Error checking prize: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


def check_prize_ssq(num_list):
    """Check Double Color Ball (双色球) prize"""
    if len(num_list) < 7:
        return jsonify({'success': False, 'error': '请输入至少7个号码 (6个红球 + 1个蓝球)'}), 400
    
    selected_red = num_list[:6]
    selected_blue = num_list[6]
    
    if any(num < 1 or num > 33 for num in selected_red):
        return jsonify({'success': False, 'error': '红球号码必须在 1-33 之间'}), 400
    
    if selected_blue < 1 or selected_blue > 16:
        return jsonify({'success': False, 'error': '蓝球号码必须在 1-16 之间'}), 400
    
    draw_red = [3, 9, 12, 13, 26, 32]
    draw_blue = 9
    
    red_match = len(set(selected_red) & set(draw_red))
    blue_match = 1 if selected_blue == draw_blue else 0
    
    prize_level, prize_amount, is_winner = "", "", True
    
    if red_match == 6 and blue_match == 1:
        prize_level, prize_amount = "一等奖", "浮动奖金 (500万元起)"
    elif red_match == 6 and blue_match == 0:
        prize_level, prize_amount = "二等奖", "浮动奖金 (约20万元)"
    elif red_match == 5 and blue_match == 1:
        prize_level, prize_amount = "三等奖", "固定奖金: 3,000元"
    elif (red_match == 5 and blue_match == 0) or (red_match == 4 and blue_match == 1):
        prize_level, prize_amount = "四等奖", "固定奖金: 200元"
    elif (red_match == 4 and blue_match == 0) or (red_match == 3 and blue_match == 1):
        prize_level, prize_amount = "五等奖", "固定奖金: 10元"
    elif blue_match == 1:
        prize_level, prize_amount = "六等奖", "固定奖金: 5元"
    else:
        prize_level, prize_amount, is_winner = "未中奖", "请继续努力！", False
    
    return jsonify({
        'success': True,
        'lottery_type': '双色球',
        'is_winner': is_winner,
        'prize_level': prize_level,
        'prize_amount': prize_amount,
        'selected_red': selected_red,
        'selected_blue': selected_blue,
        'draw_red': draw_red,
        'draw_blue': draw_blue,
        'red_match': red_match,
        'blue_match': blue_match
    })


def check_prize_kl8(num_list):
    """Check Happy 8 (快乐8) prize"""
    if len(num_list) != 10:
        return jsonify({'success': False, 'error': '快乐8需要选择10个号码'}), 400
    
    if any(num < 1 or num > 80 for num in num_list):
        return jsonify({'success': False, 'error': '号码必须在 1-80 之间'}), 400
    
    draw_numbers = [4, 7, 11, 17, 20, 22, 27, 29, 32, 34, 37, 48, 55, 64, 68, 69, 71, 73, 74, 78]
    match_count = len(set(num_list) & set(draw_numbers))
    
    prize_level, prize_amount, is_winner = "", "", True
    
    if match_count == 10:
        prize_level, prize_amount = "选十中十", "500万元"
    elif match_count == 9:
        prize_level, prize_amount = "选十中九", "10,000元"
    elif match_count == 8:
        prize_level, prize_amount = "选十中八", "3,000元"
    elif match_count == 7:
        prize_level, prize_amount = "选十中七", "300元"
    elif match_count == 6:
        prize_level, prize_amount = "选十中六", "50元"
    elif match_count == 5:
        prize_level, prize_amount = "选十中五", "5元"
    elif match_count == 0:
        prize_level, prize_amount = "选十中零", "5元"
    else:
        prize_level, prize_amount, is_winner = "未中奖", "请继续努力！", False
    
    return jsonify({
        'success': True,
        'lottery_type': '快乐8',
        'is_winner': is_winner,
        'prize_level': prize_level,
        'prize_amount': prize_amount,
        'selected_numbers': num_list,
        'draw_numbers': draw_numbers,
        'match_count': match_count
    })


def check_prize_3d(num_list):
    """Check 3D prize"""
    if len(num_list) != 3:
        return jsonify({'success': False, 'error': '3D需要选择3个数字'}), 400
    
    if any(num < 0 or num > 9 for num in num_list):
        return jsonify({'success': False, 'error': '数字必须在 0-9 之间'}), 400
    
    draw_numbers = [7, 9, 4]
    
    prize_level, prize_amount, is_winner = "", "", True
    
    if num_list == draw_numbers:
        prize_level, prize_amount = "直选中奖", "1,040元"
    elif sorted(num_list) == sorted(draw_numbers):
        if len(set(num_list)) == 2:
            prize_level, prize_amount = "组选3中奖", "346元"
        else:
            prize_level, prize_amount = "组选6中奖", "173元"
    else:
        prize_level, prize_amount, is_winner = "未中奖", "请继续努力！", False
    
    return jsonify({
        'success': True,
        'lottery_type': '3D',
        'is_winner': is_winner,
        'prize_level': prize_level,
        'prize_amount': prize_amount,
        'selected_numbers': num_list,
        'draw_numbers': draw_numbers
    })


def check_prize_qlc(num_list):
    """Check Seven Happy Lottery (七乐彩) prize"""
    if len(num_list) != 7:
        return jsonify({'success': False, 'error': '七乐彩需要选择7个号码'}), 400
    
    if any(num < 1 or num > 30 for num in num_list):
        return jsonify({'success': False, 'error': '号码必须在 1-30 之间'}), 400
    
    draw_main = [5, 10, 14, 15, 16, 18, 23]
    draw_special = 28
    
    main_match = len(set(num_list) & set(draw_main))
    special_match = 1 if draw_special in num_list else 0
    
    prize_level, prize_amount, is_winner = "", "", True
    
    if main_match == 7:
        prize_level, prize_amount = "一等奖", "浮动奖金 (约500万元)"
    elif main_match == 6 and special_match == 1:
        prize_level, prize_amount = "二等奖", "浮动奖金 (约10万元)"
    elif main_match == 6:
        prize_level, prize_amount = "三等奖", "固定奖金: 1,000元"
    elif main_match == 5 and special_match == 1:
        prize_level, prize_amount = "四等奖", "固定奖金: 200元"
    elif main_match == 5:
        prize_level, prize_amount = "五等奖", "固定奖金: 50元"
    elif main_match == 4 and special_match == 1:
        prize_level, prize_amount = "六等奖", "固定奖金: 10元"
    elif main_match == 4:
        prize_level, prize_amount = "七等奖", "固定奖金: 5元"
    else:
        prize_level, prize_amount, is_winner = "未中奖", "请继续努力！", False
    
    return jsonify({
        'success': True,
        'lottery_type': '七乐彩',
        'is_winner': is_winner,
        'prize_level': prize_level,
        'prize_amount': prize_amount,
        'selected_numbers': num_list,
        'draw_main': draw_main,
        'draw_special': draw_special,
        'main_match': main_match,
        'special_match': special_match
    })


@app.route('/api/predict-all-algorithms', methods=['POST'])
def predict_all():
    """Get predictions from all algorithms"""
    try:
        lottery_type = request.json.get('lottery_type', '通用')
        
        if not current_data:
            return jsonify({'success': False, 'error': 'No data available. Generate or import data first.'}), 400
        
        engine = PredictionEngine(current_data, lottery_type=lottery_type)
        algorithms = ['frequency', 'hot_cold', 'pattern', 'weighted_frequency', 
                     'gap_analysis', 'moving_average', 'cyclic_pattern']
        
        predictions = {}
        for algo in algorithms:
            try:
                result = engine.predict(algorithm=algo)
                predictions[algo] = result
            except Exception as e:
                predictions[algo] = {'error': str(e)}
        
        # Add ensemble
        ensemble = engine.predict_ensemble()
        predictions['ensemble'] = ensemble
        
        return jsonify({'success': True, 'predictions': predictions})
    except Exception as e:
        logger.error(f"Error generating predictions: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/records', methods=['GET'])
def get_records():
    """Get all prediction records"""
    try:
        records = record_manager.get_all_records()
        return jsonify({'success': True, 'records': records})
    except Exception as e:
        logger.error(f"Error getting records: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/records', methods=['POST'])
def add_record():
    """Add a new prediction record"""
    try:
        title = request.json.get('title')
        numbers = request.json.get('numbers')
        notes = request.json.get('notes', '')
        
        if not title or not numbers:
            return jsonify({'success': False, 'error': 'Title and numbers are required'}), 400
        
        record_id = record_manager.add_record(title, numbers, notes)
        return jsonify({'success': True, 'record_id': record_id})
    except Exception as e:
        logger.error(f"Error adding record: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/records/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete a prediction record"""
    try:
        success = record_manager.remove_record(record_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Record not found'}), 404
    except Exception as e:
        logger.error(f"Error deleting record: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/generate-password', methods=['POST'])
def generate_password():
    """Generate a secure password"""
    try:
        length = request.json.get('length', 16)
        use_uppercase = request.json.get('use_uppercase', True)
        use_lowercase = request.json.get('use_lowercase', True)
        use_digits = request.json.get('use_digits', True)
        use_special = request.json.get('use_special', True)
        
        password = password_generator.generate(
            length=length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_digits=use_digits,
            use_special=use_special
        )
        
        return jsonify({'success': True, 'password': password})
    except Exception as e:
        logger.error(f"Error generating password: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/lottery-types', methods=['GET'])
def get_lottery_types():
    """Get available lottery types and their configurations"""
    try:
        types_info = {}
        for name, config in LOTTERY_GAMES.items():
            types_info[name] = {
                'description': config['description'],
                'format': config['format']
            }
        return jsonify({'success': True, 'lottery_types': types_info})
    except Exception as e:
        logger.error(f"Error getting lottery types: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/import-data', methods=['POST'])
def import_data():
    """Import lottery data from uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Save temporarily
        temp_path = f"/tmp/{file.filename}"
        file.save(temp_path)
        
        # Import data
        data = data_handler.import_data(temp_path)
        global current_data
        current_data = data
        
        return jsonify({'success': True, 'count': len(data), 'data': data[:10]})
    except Exception as e:
        logger.error(f"Error importing data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


def run_web_app(host='0.0.0.0', port=5000, debug=False):
    """
    Run the web application.
    
    Args:
        host: Host to bind to (0.0.0.0 allows external access)
        port: Port to run on
        debug: Enable debug mode
    """
    logger.info(f"Starting Lottery System Web Application on http://{host}:{port}")
    logger.info(f"Access from computer: http://localhost:{port}")
    logger.info(f"Access from mobile: http://[your-computer-ip]:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_web_app()
