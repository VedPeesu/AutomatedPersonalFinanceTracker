class Expense:
    def __init__(self, name, type, cost, date):
        self.name = name
        self.type = type
        self.cost = cost
        self.date = date
    
    def __str__(self):
        return f"({self.name}, {self.type}, ${self.cost:.2f}, {self.date})"
