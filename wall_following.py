from fuzzy_controller import fuzzy_set as fs
from fuzzy_controller import fuzzy_value as fv
from fuzzy_controller import fuzzy_controller as fc


# Controller to know how much right to turn
right_controller = None

# Controller to know how much left to turn
left_controller = None


def setup():
    global right_controller, left_controller
    wall_value = fv.FuzzyValue()
    wall_value.add_set(fs.FuzzySet("Close", 0, 0, 0.2, 0.5))
    wall_value.add_set(fs.FuzzySet("Medium", 0.2, 0.5, 0.5, 0.8))
    wall_value.add_set(fs.FuzzySet("Far", 0.5, 0.8, 1.2, 11))

    front_value = fv.FuzzyValue()
    front_value.add_set(fs.FuzzySet("Close", 0, 0.2, 0.3, 0.5))
    front_value.add_set(fs.FuzzySet("Medium", 0.3, 0.5, 1, 1.2))
    front_value.add_set(fs.FuzzySet("Far", 1, 1.2, 2, 2.2))

    speed_value = fv.FuzzyValue(output=True)
    speed_value.add_set(fs.FuzzySet("Low", 0, 0.1, 0.2, 0.3))
    speed_value.add_set(fs.FuzzySet("Medium", 0.2, 0.3, 0.4, 0.5))
    speed_value.add_set(fs.FuzzySet("High", 0.4, 0.5, 0.6, 1))

    turn_value = fv.FuzzyValue(output=True)
    turn_value.add_set(fs.FuzzySet("Centered", 0, 0, 0.01, 0.05))
    turn_value.add_set(fs.FuzzySet("Low Turn", 0.01, 0.05, 0.05, 0.1))
    turn_value.add_set(fs.FuzzySet("High Turn", 0.1, 0.5, 1, 1.4))

    right_controller = fc.FuzzyController(
        [wall_value, front_value], [speed_value, turn_value], fc.FuzzyController.FuzzyOperator.AND)
    right_controller.add_rule(["Close", "Close"], ["Low", "Centered"])
    right_controller.add_rule(["Close", "Medium"], ["Low", "Centered"])
    right_controller.add_rule(["Close", "Far"], ["Medium", "Centered"])
    right_controller.add_rule(["Medium", "Close"], ["Medium", "Low Turn"])
    right_controller.add_rule(["Medium", "Medium"], ["Medium", "Low Turn"])
    right_controller.add_rule(["Medium", "Far"], ["Medium", "Low Turn"])
    right_controller.add_rule(["Far", "Close"], ["High", "High Turn"])
    right_controller.add_rule(["Far", "Medium"], ["High", "High Turn"])
    right_controller.add_rule(["Far", "Far"], ["High", "High Turn"])

    left_controller = fc.FuzzyController([wall_value, front_value], [
                                         speed_value, turn_value], fc.FuzzyController.FuzzyOperator.AND)
    left_controller.add_rule(["Close", "Close"], ["Low", "High Turn"])
    left_controller.add_rule(["Close", "Medium"], ["Low", "High Turn"])
    left_controller.add_rule(["Close", "Far"], ["Medium", "High Turn"])
    left_controller.add_rule(["Medium", "Close"], ["Medium", "Low Turn"])
    left_controller.add_rule(["Medium", "Medium"], ["Medium", "Low Turn"])
    left_controller.add_rule(["Medium", "Far"], ["Medium", "Low Turn"])
    left_controller.add_rule(["Far", "Close"], ["High", "Centered"])
    left_controller.add_rule(["Far", "Medium"], ["High", "Centered"])
    left_controller.add_rule(["Far", "Far"], ["High", "Centered"])


def calculate_turn(right_distance, front_distance):
    global right_controller, left_controller
    right_turn = right_controller.fire([right_distance, front_distance])[1]
    left_turn = left_controller.fire([right_distance, front_distance])[1]
    
    return left_turn - right_turn


