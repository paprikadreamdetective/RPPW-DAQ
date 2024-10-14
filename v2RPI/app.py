from master import MasterDAQ
from config import ApplicationConfig
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_session import Session
import json

def create_flask_app():
    app = Flask(__name__) 
    CORS(app, supports_credentials=True)
    return app
  
def create_master_daq(adc, outputs, i2c_inputs):
    master = MasterDAQ(adc, outputs, i2c_inputs)
    return master

with open('daq_info.json', 'r') as archivo:
    daq_data = json.load(archivo)