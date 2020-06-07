from singleton import Singleton


class GlobalState(metaclass=Singleton):
    def __init__(self, bracing):
        self.y0 = bracing.rect.bottom
        self.acceleration = 500
        self.bracing_speed = 5
        self.spawn_latency = 3
        self.game_over = False
        self.blocked = False
        self.falling = False
        self.score = 0
        self.limit = 5
        self.played = True
        self.over = True
        self.ticks = 0
        self.ctrl_is_down = False
