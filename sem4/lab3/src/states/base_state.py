class BaseState:
    def __init__(self, game, state_manager):
        self.game = game
        self.state_manager = state_manager

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass