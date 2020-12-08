import fuzzy_set as fs
import fuzzy_value as fv
import fuzzy_controller as fc


temp_value = fv.FuzzyValue()
temp_value.add_set(fs.FuzzySet("Low", 0, 5, 5, 10))
temp_value.add_set(fs.FuzzySet("Medium", 5, 10, 10, 15))
temp_value.add_set(fs.FuzzySet("High", 10, 15, 15, 20))

cloud_value = fv.FuzzyValue()
cloud_value.add_set(fs.FuzzySet("Low", 0, 5, 5, 10))
cloud_value.add_set(fs.FuzzySet("Medium", 5, 10, 10, 15))
cloud_value.add_set(fs.FuzzySet("High", 10, 15, 15, 20))

speed_value = fv.FuzzyValue(output=True)
speed_value.add_set(fs.FuzzySet("Low", 0, 10, 10, 20))
speed_value.add_set(fs.FuzzySet("Medium", 10, 20, 20, 30))
speed_value.add_set(fs.FuzzySet("High", 20, 30, 30, 40))

turn_value = fv.FuzzyValue(output=True)
turn_value.add_set(fs.FuzzySet("Centered", 0, 0, 0.5, 0.8))
turn_value.add_set(fs.FuzzySet("Low Turn", 0.5, 1, 1.5, 2))
turn_value.add_set(fs.FuzzySet("High Turn", 1.5, 2, 4, 4))

controller = fc.FuzzyController(
    [temp_value, cloud_value], [speed_value, turn_value], fc.FuzzyController.FuzzyOperator.AND)
controller.add_rule(["Low", "Low"], ["Low", "Centered"])
controller.add_rule(["Low", "Medium"], ["Low", "Centered"])
controller.add_rule(["Low", "High"], ["Medium", "Centered"])
controller.add_rule(["Medium", "Low"], ["Medium", "Low Turn"])
controller.add_rule(["Medium", "Medium"], ["Medium", "Low Turn"])
controller.add_rule(["Medium", "High"], ["Medium", "High Turn"])
controller.add_rule(["High", "Low"], ["High", "High Turn"])
controller.add_rule(["High", "Medium"], ["High", "Low Turn"])
controller.add_rule(["High", "High"], ["High", "Low Turn"])

print(controller.fire([3, 14]))
