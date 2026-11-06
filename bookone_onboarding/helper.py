import configparser
from pathlib import Path


def read_config():
    config = configparser.ConfigParser()
    candidates = [
        Path(__file__).resolve().parent.parent / 'bookone_configurations.ini',
        Path(__file__).resolve().parent / 'bookone_configurations.ini',
        Path(__file__).resolve().parent / 'configurations.ini',
        Path.cwd() / 'bookone_configurations.ini'
    ]
    for candidate in candidates:
        if candidate.is_file():
            config.read(str(candidate))
            return config
    config.read('bookone_configurations.ini')
    return config
