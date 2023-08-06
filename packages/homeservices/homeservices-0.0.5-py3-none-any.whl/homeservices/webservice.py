from flask import Flask, request, jsonify, make_response
from flask_compress import Compress
from influxdb import InfluxDBClient, client

class HomeServices:

    def __init__(self,  template_folder, static_folder):
        self.app = Flask(__name__,  template_folder=template_folder, static_folder=static_folder)
        self.app.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.app.add_url_rule('/alexaintent', 'alexaintent', self.alexa_intent, methods=['GET'])
        Compress(self.app)

        host = 'pi02'
        user = 'writer'
        password = '24$Qw7LVRjOI'
        bucket = 'hometelemetry'

        self.influx_conn = InfluxDBClient(host=host, username=user, password=password, database=bucket)

    def getApp(self):
        return self.app

    def run(self):
        self.app.run()

    def index(self):
        return 'This is the Pi server.'

    def alexa_intent(self):
        if request.method == 'GET':
            query = "SELECT * from DHT22 WHERE sensorid='1' ORDER BY time DESC LIMIT 1"
            result_set = self.influx_conn.query(query)
            points = list(result_set.get_points())

            response_dict = "La temperatura es de {} grados, y la humedad es del {} por ciento."\
                            .format(points[0]['temp'], points[0]['humidity'])

            response = make_response(response_dict.encode('UTF-8'))
            response.mimetype = "text/plain"
            response.headers['Pragma'] = 'no-cache'
            response.headers["Expires"] = 0
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return response


