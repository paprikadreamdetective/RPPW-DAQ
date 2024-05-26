""" config.py

configuration variables for wlan credentials

    "ssid" : [84, 111, 116, 97, 108, 112, 108, 97, 121, 45, 54, 53, 65, 53],
        "pswd" : [54, 53, 65, 53, 50, 56, 56, 52, 77, 89, 72, 66, 84, 121, 87, 120]

        "ssid" : [108, 97, 98, 114, 101, 100],
        "pswd" : [108, 97, 98, 114, 101, 100, 50, 48, 49, 55]
"""
cfg = {
    "wlan": {
        "ssid" : [84, 111, 116, 97, 108, 112, 108, 97, 121, 45, 54, 53, 65, 53],
        "pswd" : [54, 53, 65, 53, 50, 56, 56, 52, 77, 89, 72, 66, 84, 121, 87, 120]
    }
}

'''
configuration variables for sensors data

'''
data = {
    'time' : '',
    'area' : 1, 
    'IS': 4,
    'sensor' : {'AHT10' : {'ID' : 10, 'measurement' : 'Humidity', 'data_representation' : 'float', 'magnitude' : 0}, 
                'MQ-135': {'ID' : 20, 'measurement' : 'CO2', 'data_representation' : 'integer', 'magnitude' : 0}, 
                'THERMISTOR': {'ID' : 30, 'measurement' : 'Temperature', 'data_representation' : 'float', 'magnitude' : 0}}}