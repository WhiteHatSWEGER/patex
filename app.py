from flasgger import Swagger
from flask import Flask, jsonify, request
from Api import Api
app = Flask(__name__)
app.config["Swagger"] = { "Title" : "WingSS"}
Swagger = Swagger(app)


path_to_data = "/Tmp/SensorData"
api = Api(path_to_data)

@app.route("/api/sensors")
def index():
    return api.get_sensors()