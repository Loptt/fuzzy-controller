
class FuzzyValue():

    def __init__(self):
        self.sets = []

    def add_set(self, set):
        if set.label in [s.label for s in self.sets]:
            raise Exception("Duplicate label in sets")
        self.sets.append(set)

    def calculate_memberships(self, value):
        memberships_dict = {}
        for set in self.sets:
            memberships_dict[set] = set.calculate_membership(value)
        return memberships_dict
