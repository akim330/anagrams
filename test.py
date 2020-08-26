class GameState:
    def __init__(self):
        # -------- #
        #  BANANA  #
        # -------- #
        self.tiles = []


class Banana:
    def __init__(self, game_state=None):
        if game_state:
            self.game_state = game_state
        else:
            self.game_state = GameState()

class Test:
    def __init__(self):
        self.x = 2

class Foo():
    def __init__(self, t=None):
        if t:
            self.test = t
        else:
            self.test = Test()