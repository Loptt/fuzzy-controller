
class FuzzySet:
    
    def __init__(self, label, a, b, c, d):
        self.label = label
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def calculate_membership(self, value):
        if value > self.a and value <= self.b:
            return (value - self.a) / (self.b - self.a)
        if value > self.b and value < self.c:
            return 1
        if value >= self.c and value < self.d:
            return (self.d - value) / (self.d - self.c)
        return 0

    def __str__(self):
        return "{}: a:{}, b:{}, c:{}, d:{}".format(self.label, self.a, self.b, self.c, self.d)
