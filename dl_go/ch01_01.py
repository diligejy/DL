class GenericLinearFunction:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def evaluate(self, x):
        return self.a * x + self.b

height_to_weight = GenericLinearFunction(a = 4.2, b = -137)
height_of_new_person = 73
estimated_weight = height_to_weight.evaluate(height_of_new_person)

