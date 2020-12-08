import rule as r


class FuzzyController():
    FuzzyOperator = r.FuzzyOperator()

    def __init__(self, antecedent_fvs, consequent_fvs, operator):
        # Ensure al antecedent and consequent fuzzy values have at least one set
        if len([x for x in antecedent_fvs if x.set_amount() < 1]) > 0:
            raise Exception("Cannot add Fuzzy Value with empty sets")
        if len([x for x in consequent_fvs if x.set_amount() < 1]) > 0:
            raise Exception("Cannot add Fuzzy Value with empty sets")

        self.rules = []
        self.antecedent_fvs = antecedent_fvs
        self.consequent_fvs = consequent_fvs
        self.operator = operator

    def add_rule(self, ant_labels, consequent_labels):
        if len(ant_labels) != len(self.antecedent_fvs):
            raise Exception("Number of labels for antecedents do not match")
        if len(consequent_labels) != len(self.consequent_fvs):
            raise Exception("Number of labels for consequents do not match")

        antecedent_sets = [fv.get_set(label) for fv, label in zip(
            self.antecedent_fvs, ant_labels)]
        consequent_sets = [fv.get_set(label) for fv, label in zip(
            self.consequent_fvs, consequent_labels)]

        self.rules.append(
            r.Rule(antecedent_sets, consequent_sets, self.operator))

    def fire(self, antecedent_values):
        if len(antecedent_values) != len(self.antecedent_fvs):
            raise Exception(
                "Number of values does not match number of Fuzzy Values")

        ant_memberships = [fv.calculate_memberships(value) for fv, value in zip(
            self.antecedent_fvs, antecedent_values)]

        firing_strengths = {}
        for rule in self.rules:
            firing_strengths[rule] = rule.calculate_fire(ant_memberships)

        # Ensure we have non-zero firing strength
        if sum([firing_strengths[rule] for rule in firing_strengths]) == 0:
            return [0 for x in self.consequent_fvs]

        return [sum([firing_strengths[rule] * rule.consequents[i].get_centroid() for rule in firing_strengths]) /
                sum([firing_strengths[rule] for rule in firing_strengths]) for i, consequent_fv in enumerate(self.consequent_fvs)]
