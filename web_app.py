#!/usr/bin/env python3
"""
Web-based interface for the Lottery Analysis and Prediction System.
Can be accessed from computers and mobile devices via browser.
"""

from flask import Flask, render_template, request, jsonify, send_file
import sys
from pathlib import Path
import json

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

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'lottery-system-secret-key-change-in-production'

# Initialize components
logger = setup_logger('web_app')
config_manager = ConfigManager()
data_handler = DataHandler()
record_manager = RecordManager()
password_generator = PasswordGenerator()

# Global data storage (in production, use a database)
current_data = []


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', lottery_types=list(LOTTERY_GAMES.keys()))


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
        lottery_type = request.json.get('lottery_type', '通用')
        algorithm = request.json.get('algorithm', 'ensemble')
        
        if not current_data:
            return jsonify({'success': False, 'error': 'No data available. Generate or import data first.'}), 400
        
        engine = PredictionEngine(current_data, lottery_type=lottery_type)
        
        if lottery_type != '通用':
            result = engine.predict_for_lottery_type()
        else:
            if algorithm == 'ensemble':
                result = engine.predict_ensemble()
            else:
                result = engine.predict(algorithm=algorithm)
        
        return jsonify({'success': True, 'prediction': result})
    except Exception as e:
        logger.error(f"Error generating prediction: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


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
