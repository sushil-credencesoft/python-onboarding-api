import configparser
from pathlib import Path


def read_config():
    config = configparser.ConfigParser()
    candidates = [
        Path(__file__).resolve().parent.parent / 'hotelmate_configurations.ini',
        Path(__file__).resolve().parent / 'hotelmate_configurations.ini',
        Path(__file__).resolve().parent / 'configurations.ini',
        Path.cwd() / 'hotelmate_configurations.ini'
    ]
    for candidate in candidates:
        if candidate.is_file():
            config.read(str(candidate))
            return config
    config.read('hotelmate_configurations.ini')
    return config
