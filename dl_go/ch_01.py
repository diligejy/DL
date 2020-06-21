class GenericLinearFunction:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def evaluate(self, x):
        return self.a * x + self.b


