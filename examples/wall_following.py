import fuzzy_set as fs
from . import fuzzy_value as fv
from . import fuzzy_controller as fc


# Controller to know how much right to turn
right_controller = None

# Controller to know how much left to turn
left_controller = None


def setup():
    wall_value = fv.FuzzyValue()
    wall_value.add_set(fs.FuzzySet("Close", 0, 0.1, 0.2, 0.3))
    wall_value.add_set(fs.FuzzySet("Medium", 0.2, 0.3, 0.6, 0.7))
    wall_value.add_set(fs.FuzzySet("Far", 0.6, 0.7, 1.5, 2))

    front_value = fv.FuzzyValue()
    front_value.add_set(fs.FuzzySet("Close", 0, 0.2, 0.3, 0.5))
    front_value.add_set(fs.FuzzySet("Medium", 0.3, 0.5, 1, 1.2))
    front_value.add_set(fs.FuzzySet("Far", 1, 1.2, 2, 2.2))

    speed_value = fv.FuzzyValue(output=True)
    speed_value.add_set(fs.FuzzySet("Low", 0, 0.1, 0.2, 0.3))
    speed_value.add_set(fs.FuzzySet("Medium", 0.2, 0.3, 0.4, 0.5))
    speed_value.add_set(fs.FuzzySet("High", 0.4, 0.5, 0.6, 1))

    turn_value = fv.FuzzyValue(output=True)
    turn_value.add_set(fs.FuzzySet("Centered", 0, 0, 0.05, 0.1))
    turn_value.add_set(fs.FuzzySet("Low Turn", 0.5, 1, 1.5, 2))
    turn_value.add_set(fs.FuzzySet("High Turn", 1.5, 2, 4, 4))

    right_controller = fc.FuzzyController(
        [wall_value, front_value], [speed_value, turn_value], fc.FuzzyController.FuzzyOperator.AND)
    right_controller.add_rule(["Low", "Low"], ["Low", "Centered"])
    right_controller.add_rule(["Low", "Medium"], ["Low", "Centered"])
    right_controller.add_rule(["Low", "High"], ["Medium", "Centered"])
    right_controller.add_rule(["Medium", "Low"], ["Medium", "Low Turn"])
    right_controller.add_rule(["Medium", "Medium"], ["Medium", "Low Turn"])
    right_controller.add_rule(["Medium", "High"], ["Medium", "Low Turn"])
    right_controller.add_rule(["High", "Low"], ["High", "High Turn"])
    right_controller.add_rule(["High", "Medium"], ["High", "High Turn"])
    right_controller.add_rule(["High", "High"], ["High", "High Turn"])

    left_controller = fc.FuzzyController([wall_value, front_value], [
                                         speed_value, turn_value], fc.FuzzyController.FuzzyOperator.AND)
    left_controller.add_rule(["Low", "Low"], ["Low", "High Turn"])
    left_controller.add_rule(["Low", "Medium"], ["Low", "High Turn"])
    left_controller.add_rule(["Low", "High"], ["Medium", "High Turn"])
    left_controller.add_rule(["Medium", "Low"], ["Medium", "Low Turn"])
    left_controller.add_rule(["Medium", "Medium"], ["Medium", "Low Turn"])
    left_controller.add_rule(["Medium", "High"], ["Medium", "Low Turn"])
    left_controller.add_rule(["High", "Low"], ["High", "Centered"])
    left_controller.add_rule(["High", "Medium"], ["High", "Centered"])
    left_controller.add_rule(["High", "High"], ["High", "Centered"])


def calculate_turn(right_distance, front_distance):
    right_turn = right_controller.fire(right_distance, front_distance)[1]
    left_turn = left_controller.fire(right_distance, front_distance)[1]

    return right_turn - left_turn


print(calculate_turn(0.3, 2))
