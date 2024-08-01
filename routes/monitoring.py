from flask import Blueprint, render_template
from flask_socketio import SocketIO, emit
import psutil
import time
import os

socketio = SocketIO()
monitoring_bp = Blueprint('monitoring', __name__, template_folder='templates')

@monitoring_bp.route('/monitoring')
def monitoring():
    return render_template('monitoring.html')

@socketio.on('connect')
def handle_connect():
    emit('connected', {'data': 'Connected'})

@socketio.on('request_data')
def handle_request_data():
    process = psutil.Process(os.getpid())  
    while True:
        cpu_usage = process.cpu_percent(interval=1)  
        memory_info = process.memory_info()
        memory_usage = memory_info.rss / (1024 * 1024) 
        data = {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage
        }
        emit('update_data', data)
        time.sleep(1)
