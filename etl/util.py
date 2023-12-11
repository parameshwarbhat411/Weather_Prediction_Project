import configparser

config = configparser.ConfigParser()
config.read("config.ini")

class Util:

    API_KEY = config['DEFAULT']['API_KEY']