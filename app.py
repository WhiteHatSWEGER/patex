from flask import Flask, jsonify, request, send_from_directory
import sqlite3
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__, static_folder='static')

# CORS = Cross Origin Ressource Sharing, wurde hier aktiviert
# für erhöhte skalierbarkeit und Fehlervermeidung

CORS(app, origins='*')
DATABASE = 'sensor_data.db'


# Die SQL-Suche innerhalb der Datenbank wurde generiert mit Hilfe von Blackbox: blackbox.ai, unterstützt mit
# docs.python.org/3/library/sqlite3.html

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/log')
def log():
    return send_from_directory('static', 'log.html')


@app.route('/toolsData')
def tools_data():
    return send_from_directory('static', 'toolsData.html')


@app.route('/api/logs', methods=['GET'])
def get_logs():
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT timestamp, Alcohol, Methane, NaturalGas, CO, H2, CO2 
            FROM sensor_data 
            WHERE Alcohol > 100 OR Methane > 100 OR NaturalGas > 100 OR CO > 100 OR H2 > 100 OR CO2 > 100
        """)
        rows = cur.fetchall()
        logs = [{'timestamp': row['timestamp'],
                 'Alcohol': row['Alcohol'],
                 'Methane': row['Methane'],
                 'NaturalGas': row['NaturalGas'],
                 'CO': row['CO'],
                 'H2': row['H2'],
                 'CO2': row['CO2']} for row in rows]
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
    return jsonify(logs)


@app.route('/api/add-system', methods=['POST'])
def add_system():
    system_name = request.json.get('name')
    gases = request.json.get('gases')
    api_url = request.json.get('api_url')
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO systems (name, gases, api_url) VALUES (?, ?, ?)",
                    (system_name, ','.join(gases), api_url))
        conn.commit()
        system_id = cur.lastrowid
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
    return jsonify({'message': 'System added successfully', 'system_id': system_id}), 201


@app.route('/api/systems', methods=['GET'])
def get_systems():
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name FROM systems")
        systems = [{'id': row['id'], 'name': row['name']} for row in cur.fetchall()]
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
    return jsonify(systems)


### Swagger UI setup ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sensor Data API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
