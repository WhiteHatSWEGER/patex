from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from datetime import datetime
from flask_cors import CORS  # Import CORS

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS on the app, default to allow all origins
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Configure SocketIO with CORS


class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)


# Serve the index.html page
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


# Serve the log.html page
@app.route('/log')
def log():
    return send_from_directory('static', 'log.html')


# Serve the toolsData.html page
@app.route('/toolsData')
def tools_data():
    return send_from_directory('static', 'toolsData.html')


# API endpoint to store sensor data
@app.route('/api/sensor-data', methods=['POST'])
def store_sensor_data():
    try:
        data = request.json
        timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')  # Ensure your timestamp format matches
        for sensor in data['sensors']:
            new_sensor_data = SensorData(timestamp=timestamp,
                                         temperature=sensor['value'] if sensor['id'] == 'temperature' else None,
                                         humidity=sensor['value'] if sensor['id'] == 'humidity' else None)
            db.session.add(new_sensor_data)
        db.session.commit()
        # Broadcast the data to all connected WebSocket clients
        socketio.emit('update_data', data, broadcast=True)
        return jsonify({'message': 'Data received and stored successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@socketio.on('connect')
def test_connect():
    emit('my_response', {'data': 'Connected'})


if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
