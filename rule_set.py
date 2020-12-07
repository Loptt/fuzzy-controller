import rule as r


class RuleSet():

    def __init__(self):
        self.rules = []

    def add_rule(self, ant1, ant2, consequent):
        self.rules.append(r.Rule(ant1, ant2, consequent))
