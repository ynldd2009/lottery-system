#!/usr/bin/env python3
"""
彩票分析系统的命令行演示。
展示核心功能，无需 GUI。
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import ConfigManager
from src.core import DataAnalyzer, PredictionEngine, RecordManager
from src.data import DataHandler, DataVisualizer
from src.utils import PasswordGenerator


def print_section(title):
    """打印章节标题。"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_data_handling():
    """演示数据处理功能。"""
    print_section("数据处理演示")
    
    handler = DataHandler()
    
    # Generate sample data
    print("\n1. 生成示例彩票数据...")
    data = handler.create_sample_data(num_draws=100, num_count=6, num_range=(1, 49))
    print(f"   ✓ 已生成 {len(data)} 期彩票数据")
    print(f"   ✓ 日期范围: {data['date'].min()} 到 {data['date'].max()}")
    
    # Show first few records
    print("\n   示例记录:")
    for i, row in data.head(5).iterrows():
        print(f"   第 {row['draw_number']:3d} 期: {row['numbers']}")
    
    return data


def demo_data_analysis(data):
    """演示数据分析功能。"""
    print_section("数据分析演示")
    
    analyzer = DataAnalyzer()
    analyzer.load_data(data)
    
    print("\n1. 运行频率分析...")
    frequency = analyzer.get_frequency_analysis()
    
    # Show top 10 most frequent numbers
    sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n   前 10 个最常出现的号码:")
    for num, freq in sorted_freq:
        print(f"   号码 {num:2d}: 出现 {freq:3d} 次")
    
    print("\n2. 识别热门和冷门号码...")
    hot_numbers, cold_numbers = analyzer.get_hot_cold_numbers()
    print(f"\n   热门号码 (常出现): {hot_numbers}")
    print(f"   冷门号码 (少出现): {cold_numbers}")
    
    print("\n3. 分析模式...")
    patterns = analyzer.get_pattern_analysis()
    print(f"\n   发现的连续号码: {patterns.get('consecutive_numbers', 0)}")
    print(f"   奇偶比: {patterns.get('odd_even_ratio', 0):.2%}")
    print(f"   大小比: {patterns.get('high_low_ratio', 0):.2%}")
    sum_range = patterns.get('sum_range', (0, 0))
    print(f"   和值范围: {sum_range[0]} 到 {sum_range[1]}")
    
    return analyzer


def demo_prediction(data):
    """演示预测功能。"""
    print_section("预测演示")
    
    # Load config to get all algorithms
    config = ConfigManager()
    engine = PredictionEngine(config.config.get('prediction', {}))
    engine.load_historical_data(data)
    
    print("\n1. 使用不同算法生成预测...")
    
    # Original algorithms
    print("\n   原始算法:")
    print("   -------------------")
    
    # Frequency-based prediction
    print("\n   a) 基于频率的预测:")
    freq_pred = engine.predict_by_frequency(count=6, number_range=(1, 49))
    print(f"      {freq_pred}")
    
    # Hot numbers prediction
    print("\n   b) 热门号码预测:")
    hot_pred = engine.predict_by_hot_numbers(count=6, number_range=(1, 49))
    print(f"      {hot_pred}")
    
    # Pattern-based prediction
    print("\n   c) 基于模式的预测:")
    pattern_pred = engine.predict_by_pattern(count=6, number_range=(1, 49))
    print(f"      {pattern_pred}")
    
    # New statistical models
    print("\n   新统计模型:")
    print("   ----------------------")
    
    # Weighted frequency
    print("\n   d) 加权频率 (近期更重要):")
    weighted_pred = engine.predict_by_weighted_frequency(count=6, number_range=(1, 49))
    print(f"      {weighted_pred}")
    
    # Gap analysis
    print("\n   e) 间隔分析 (应出现号码):")
    gap_pred = engine.predict_by_gap_analysis(count=6, number_range=(1, 49))
    print(f"      {gap_pred}")
    
    # Moving average
    print("\n   f) 移动平均 (趋势分析):")
    ma_pred = engine.predict_by_moving_average(count=6, number_range=(1, 49))
    print(f"      {ma_pred}")
    
    # Cyclic pattern
    print("\n   g) 周期模式 (周期检测):")
    cyclic_pred = engine.predict_by_cyclic_pattern(count=6, number_range=(1, 49))
    print(f"      {cyclic_pred}")
    
    # Combined prediction with confidence
    print("\n2. 生成集成预测及置信度...")
    result = engine.generate_prediction_with_confidence(count=6, number_range=(1, 49))
    
    print(f"\n   推荐号码: {result['recommended']}")
    print(f"   置信度: {result['confidence']:.1%}")
    print(f"   基于 {result['data_points_used']} 期历史数据")
    print(f"   使用算法: {len(result['algorithms_used'])} 个模型")
    print(f"   模型: {', '.join(result['algorithms_used'])}")


def demo_password_generator():
    """演示密码生成功能。"""
    print_section("密码生成器演示")
    
    generator = PasswordGenerator()
    
    print("\n1. 生成强密码...")
    passwords = generator.generate_multiple(count=5)
    
    for i, pwd in enumerate(passwords, 1):
        print(f"   密码 {i}: {pwd}")
    
    print("\n   ✓ 所有密码均包含:")
    print("     - 大写字母")
    print("     - 小写字母")
    print("     - 数字")
    print("     - 特殊字符")


def demo_record_management():
    """演示记录管理功能。"""
    print_section("记录管理演示")
    
    # Use temporary storage
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        storage_path = f.name
    
    manager = RecordManager(storage_path)
    
    print("\n1. 添加预测记录...")
    
    # Add sample records
    for i in range(3):
        record = {
            'type': 'prediction',
            'title': f'预测 #{i+1}',
            'description': f'示例预测记录 {i+1}',
            'data': {
                'numbers': [1, 5, 12, 23, 34, 45],
                'confidence': 0.75,
                'algorithm': 'ensemble'
            }
        }
        record_id = manager.add_record(record)
        print(f"   ✓ 已添加记录: {record_id}")
    
    print("\n2. 检索所有记录...")
    all_records = manager.get_all_records()
    print(f"   总记录数: {len(all_records)}")
    
    for record in all_records:
        print(f"   - {record['title']}: {record.get('created_at', 'N/A')}")
    
    print("\n3. 搜索记录...")
    results = manager.search_records('预测')
    print(f"   找到 {len(results)} 条匹配记录")
    
    print("\n4. 可用的记录操作:")
    print("   ✓ 添加新记录")
    print("   ✓ 更新现有记录")
    print("   ✓ 删除记录")
    print("   ✓ 搜索记录")
    print("   ✓ 导出为 JSON")
    print("   ✓ 共享记录")


def demo_configuration():
    """演示配置管理功能。"""
    print_section("配置管理演示")
    
    config = ConfigManager()
    
    print("\n1. 系统配置:")
    print(f"   应用名称: {config.get('system.app_name')}")
    print(f"   版本: {config.get('system.version')}")
    
    print("\n2. 预测设置:")
    print(f"   分析窗口: {config.get('prediction.analysis_window')} 期")
    print(f"   最小数据点: {config.get('prediction.min_data_points')}")
    print(f"   算法: {', '.join(config.get('prediction.prediction_algorithms', []))}")
    
    print("\n3. 安全设置:")
    print(f"   密码长度: {config.get('security.password_length')}")
    print(f"   包含特殊字符: {config.get('security.password_include_special')}")
    
    print("\n4. 数据管理:")
    print(f"   有效期: {config.get('data.validity_period_days')} 天")
    print(f"   最大记录数: {config.get('data.max_records')}")
    print(f"   缓存启用: {config.get('data.cache_enabled')}")


def demo_visualization(data):
    """演示可视化功能。"""
    print_section("可视化演示")
    
    analyzer = DataAnalyzer()
    analyzer.load_data(data)
    visualizer = DataVisualizer()
    
    print("\n1. 可用的可视化类型:")
    print("   ✓ 频率分布图表")
    print("   ✓ 热门与冷门号码对比")
    print("   ✓ 号码随时间分布")
    print("   ✓ 奇偶分布饼图")
    print("   ✓ 综合分析仪表板")
    
    print("\n2. 创建示例可视化...")
    
    # Get data for visualization
    frequency = analyzer.get_frequency_analysis()
    hot_nums, cold_nums = analyzer.get_hot_cold_numbers()
    
    # Create dashboard
    output_dir = Path.home()
    dashboard_path = output_dir / "lottery_demo_dashboard.png"
    
    try:
        visualizer.create_analysis_dashboard(
            frequency, hot_nums, cold_nums, data, str(dashboard_path)
        )
        print(f"   ✓ 仪表板已保存到: {dashboard_path}")
    except Exception as e:
        print(f"   ⚠ 可视化已跳过 (显示不可用): {e}")


def main():
    """运行完整演示。"""
    print("\n" + "=" * 60)
    print("  彩票分析和预测系统 - 命令行演示")
    print("=" * 60)
    
    try:
        # 1. Configuration
        demo_configuration()
        
        # 2. Data Handling
        data = demo_data_handling()
        
        # 3. Data Analysis
        demo_data_analysis(data)
        
        # 4. Predictions
        demo_prediction(data)
        
        # 5. Password Generator
        demo_password_generator()
        
        # 6. Record Management
        demo_record_management()
        
        # 7. Visualization
        demo_visualization(data)
        
        # Summary
        print_section("演示完成")
        print("\n✓ 所有核心功能演示成功!")
        print("\n要运行完整的 GUI 应用程序，使用:")
        print("  python main.py")
        print("\n要运行 Web 界面，使用:")
        print("  python web_app.py")
        print("\n有关 Android 部署说明，请参阅:")
        print("  ANDROID_DEPLOYMENT.md")
        print()
        
    except Exception as e:
        print(f"\n✗ 演示过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
