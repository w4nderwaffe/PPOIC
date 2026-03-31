class StateManager:
    def __init__(self):
        self.current_state = None

    def set_state(self, state):
        self.current_state = state

    def handle_event(self, event):
        if self.current_state is not None:
            self.current_state.handle_event(event)

    def update(self, dt):
        if self.current_state is not None:
            self.current_state.update(dt)

    def render(self, screen):
        if self.current_state is not None:
            self.current_state.render(screen)