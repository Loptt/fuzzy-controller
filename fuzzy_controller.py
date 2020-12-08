import rule as r


class FuzzyController():
    FuzzyOperator = r.FuzzyOperator()

    def __init__(self, ant1_fv, ant2_fv, consequent_fv, operator):
        if ant1_fv.set_amount() < 1 or ant2_fv.set_amount() < 1 or consequent_fv.set_amount() < 1:
            raise Exception("Cannot add Fuzzy Value with empty sets")
        self.rules = []
        self.ant1_fv = ant1_fv
        self.ant2_fv = ant2_fv
        self.consequent_fv = consequent_fv
        self.operator = operator

    def add_rule(self, label_ant1, label_ant2, label_consequent):
        self.rules.append(r.Rule(self.ant1_fv.get_set(label_ant1), self.ant2_fv.get_set(
            label_ant2), self.consequent_fv.get_set(label_consequent), self.operator))

    def fire(self, ant1_value, ant2_value):
        ant1_membership = self.ant1_fv.calculate_memberships(ant1_value)
        ant2_membership = self.ant2_fv.calculate_memberships(ant2_value)

        firing_strengths = {}
        for rule in self.rules:
            firing_strengths[rule] = rule.calculate_fire(
                ant1_membership, ant2_membership)

        numerator = sum([firing_strengths[rule] * rule.consequent.get_centroid()
                         for rule in firing_strengths])
        denominator = sum([firing_strengths[rule]
                           for rule in firing_strengths])

        if denominator == 0:
            return 0

        return numerator / denominator
