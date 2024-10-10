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

#with open('config.json', 'r') as archivo:
#    config_data = json.load(archivo)

#print("Configuracion actual")
#print(config_data)
'''
class User:
    def __init__(self):
        self._email = None
        self._password = None
        self._rol = None

    def set_email(self, email: str):
        self._email = email

    def set_password(self, password: str):
        self._password = password

    def set_rol(self, rol: str):
        self._rol = rol

    def get_email(self):
        return self._email

    def get_password(self):
        return self._password

    def get_rol(self):
        return self._rol
'''
