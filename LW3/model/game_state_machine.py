# State machine constants for the class below
STATE_MENU = 1
STATE_HELP = 2
STATE_PLAY = 3
STATE_SAVE_RECORD = 4
STATE_RECORDS = 5
STATE_GAME_OVER = 6


# Stack-based navigation system
class StateMachine:
    def __init__(self):
        self.state_stack = []

    def peek(self):
        try:
            return self.state_stack[-1]
        except IndexError:
            # empty stack
            return None

    def pop(self):
        try:
            self.state_stack.pop()
            return len(self.state_stack) > 0
        except IndexError:
            # empty stack
            return None

    def push(self, state):
        self.state_stack.append(state)
        return state
