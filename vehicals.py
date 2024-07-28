class Vehicle:
    def __init__(self, start, goal, max_fuel):
        self.start = start
        self.goal = goal
        self.max_fuel = max_fuel
        self.current_position = start
        self.current_goal = goal
        self.path = []
    def path(self, path):
        self.path = path