
class Rule():

    def __init__(self, antecedents, consequents, operator):
        self.antecedents = antecedents
        self.consequents = consequents
        self.operator = operator

    def calculate_fire(self, ant_memberships):
        ant_values = [membership[ant] for membership,
                      ant in zip(ant_memberships, self.antecedents)]

        consequent_fires = {}

        if self.operator == FuzzyOperator.AND:
            return min(ant_values)
        elif self.operator == FuzzyOperator.OR:
            return max(ant_values)
        else:
            raise Exception("Invalid Fuzzy Operator")


class FuzzyOperator():
    AND = 0
    OR = 1
