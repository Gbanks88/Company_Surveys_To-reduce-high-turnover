"""
Local configuration settings for the Eco-Vehicle Production System
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

# Database
DATABASE = {
    'requirements': os.path.join(BASE_DIR, 'requirements.db'),
    'metrics': os.path.join(BASE_DIR, 'metrics.db')
}

# Server settings
SERVER = {
    'host': '127.0.0.1',
    'port': 8004,
    'debug': True,
    'reload': True
}

# Static files
STATIC = {
    'directory': os.path.join(BASE_DIR, 'static'),
    'assets': os.path.join(BASE_DIR, 'static', 'assets')
}

# Machine simulation settings
SIMULATION = {
    'update_interval': 1.0,  # seconds
    'motion_limits': {
        'max_velocity': 1000,  # mm/s
        'max_acceleration': 2000,  # mm/s²
        'max_jerk': 5000  # mm/s³
    },
    'safety_thresholds': {
        'temperature_max': 45,  # °C
        'collision_distance': 100,  # mm
        'emergency_stop_time': 0.1  # seconds
    }
}

# Vehicle production settings
VEHICLE = {
    'requirements': {
        'range': 250,  # miles
        'top_speed': 130,  # mph
        'acceleration': 7.0,  # seconds (0-60 mph)
        'battery_capacity': 75,  # kWh
        'charging_rate': 150,  # kW
        'cycle_life': 2000  # cycles
    },
    'production': {
        'daily_target': 100,  # units
        'quality_threshold': 95,  # percent
        'cycle_time_target': 45  # minutes
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'app.log'),
            'mode': 'a',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
