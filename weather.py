from singleton import Singleton


class Weather(metaclass=Singleton):

    def __init__(self):
        self.wind = False
        self.ticks = 0
        self.wind_speed = 0
        self.rain = False