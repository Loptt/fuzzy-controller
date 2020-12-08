
class Rule():

    def __init__(self, ant1, ant2, consequent, operator):
        self.ant1 = ant1
        self.ant2 = ant2
        self.consequent = consequent
        self.operator = operator

    def calculate_fire(self, ant1_membership, ant2_membership):
        ant1_val = ant1_membership[self.ant1]
        ant2_val = ant2_membership[self.ant2]

        if self.operator == FuzzyOperator.AND:
            return min(ant1_val, ant2_val)
        elif self.operator == FuzzyOperator.OR:
            return max(ant1_val, ant2_val)
        else:
            raise Exception("Invalid Fuzzy Operator")


class FuzzyOperator():
    AND = 0
    OR = 1
