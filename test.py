import fuzzy_set as fs
import fuzzy_value as fv


speed_value = fv.FuzzyValue()
speed_value.add_set(fs.FuzzySet("Low", 0, 3, 6, 9))
speed_value.add_set(fs.FuzzySet("Medium", 6, 9, 12, 15))
speed_value.add_set(fs.FuzzySet("High", 12, 15, 18, 21))

memberships = speed_value.calculate_memberships(8)

for m in memberships:
    print("{}, value: {}".format(m, memberships[m]))
