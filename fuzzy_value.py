
class FuzzyValue():

    def __init__(self, output=False):
        self.sets = []
        self.output = output

    def add_set(self, set):
        if set.label in [s.label for s in self.sets]:
            raise Exception("Duplicate label in sets")
        self.sets.append(set)

    def calculate_memberships(self, value):
        memberships_dict = {}
        for set in self.sets:
            memberships_dict[set] = set.calculate_membership(value)
        return memberships_dict

    def get_set(self, label):
        result = [s for s in self.sets if s.label == label]
        if len(result) != 1:
            raise Exception("Requested label set does not exist")
        return result[0]

    def set_amount(self):
        return len(self.sets)
