import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read('bookone_configurations.ini')
    return config