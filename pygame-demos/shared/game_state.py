# game_state.py
class GameState:
    def __init__(self):
        self.selected_spaceship = None

    def set_selected_spaceship(self, spaceship):
        self.selected_spaceship = spaceship

    def get_selected_spaceship(self):
        return self.selected_spaceship

game_state = GameState()