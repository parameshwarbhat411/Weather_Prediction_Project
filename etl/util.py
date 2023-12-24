import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class Util:
    API_KEY = config['DEFAULT']['API_KEY']
    WORK_DIR = config['DEFAULT']['WORK_DIR']
