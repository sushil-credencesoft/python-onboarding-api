import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read('hotelmate_configurations.ini')
    return config