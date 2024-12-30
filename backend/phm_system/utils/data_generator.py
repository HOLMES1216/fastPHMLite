import random
from datetime import datetime

def generate_system_data():
    """生成随机系统数据并符合前端图表需求"""
    
    return {
        'contentType': 'HOME_DATA',
        'speed': round(random.uniform(0, 120), 2),
        'motorTemp': round(random.uniform(20, 80), 2),
        'bearingVib': round(random.uniform(0, 10), 2),
        'brakePressure': round(random.uniform(0, 5), 2),
        'batteryVoltage': round(random.uniform(20, 30), 2),
        'tractionCurrent': round(random.uniform(0, 100), 2),
        'wheelTemp': round(random.uniform(20, 60), 2),
        'airPressure': round(random.uniform(0, 10), 2),
        'noiseLevel': round(random.uniform(60, 90), 2),
        'gearboxTemp': round(random.uniform(30, 70), 2),
        'normalCount': random.randint(50, 100),
        'minorFaultCount': random.randint(10, 50),
        'severeFaultCount': random.randint(0, 10),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'chartData': {
            'vibrationData': [random.randint(100, 1000) for _ in range(6)],
            'temperatureData': [random.randint(100, 1000) for _ in range(6)]
        }
    }
