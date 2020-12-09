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
    wall_value.add_set(fs.FuzzySet("Close", 0, 0, 0.75, 0.85))
    wall_value.add_set(fs.FuzzySet("Medium", 0.2, 0.75, 0.85, 1.4))
    wall_value.add_set(fs.FuzzySet("Far", 0.85, 1.4, 10, 11))

    front_value = fv.FuzzyValue()
    front_value.add_set(fs.FuzzySet("Close", 0.05, 0.05, 1.2, 1.4))
    front_value.add_set(fs.FuzzySet("Medium", 1.2, 1.4, 1.8, 2))
    front_value.add_set(fs.FuzzySet("Far", 1.8, 2, 100, 101))

    speed_value = fv.FuzzyValue(output=True)
    speed_value.add_set(fs.FuzzySet("Low", 0, 0.2, 0.2, 0.3))
    speed_value.add_set(fs.FuzzySet("Medium", 0.2, 0.3, 0.4, 0.5))
    speed_value.add_set(fs.FuzzySet("High", 0.4, 0.5, 0.9, 1))

    turn_value = fv.FuzzyValue(output=True)
    turn_value.add_set(fs.FuzzySet("Centered", 0, 0, 0.01, 0.02))
    turn_value.add_set(fs.FuzzySet("Low Turn", 0, 0.02, 0.1, 0.4))
    turn_value.add_set(fs.FuzzySet("High Turn", 0.1, 0.4, 0.4, 0.4))

    right_controller = fc.FuzzyController(
        [wall_value, front_value], [speed_value, turn_value], fc.FuzzyController.FuzzyOperator.AND)
    right_controller.add_rule(["Close", "Close"], ["Low", "Centered"])
    right_controller.add_rule(["Close", "Medium"], ["Low", "Centered"])
    right_controller.add_rule(["Close", "Far"], ["Low", "Centered"])
    right_controller.add_rule(["Medium", "Close"], ["Low", "Centered"])
    right_controller.add_rule(["Medium", "Medium"], ["Low", "Low Turn"])
    right_controller.add_rule(["Medium", "Far"], ["Low", "Low Turn"])
    right_controller.add_rule(["Far", "Close"], ["Low", "Centered"])
    right_controller.add_rule(["Far", "Medium"], ["Low", "Centered"])
    right_controller.add_rule(["Far", "Far"], ["Low", "High Turn"])

    left_controller = fc.FuzzyController([wall_value, front_value], [
                                         speed_value, turn_value], fc.FuzzyController.FuzzyOperator.AND)
    left_controller.add_rule(["Close", "Close"], ["Low", "High Turn"])
    left_controller.add_rule(["Close", "Medium"], ["Low", "High Turn"])
    left_controller.add_rule(["Close", "Far"], ["Low", "High Turn"])
    left_controller.add_rule(["Medium", "Close"], ["Low", "High Turn"])
    left_controller.add_rule(["Medium", "Medium"], ["Low", "Low Turn"])
    left_controller.add_rule(["Medium", "Far"], ["Low", "Low Turn"])
    left_controller.add_rule(["Far", "Close"], ["Low", "High Turn"])
    left_controller.add_rule(["Far", "Medium"], ["Low", "Low Turn"])
    left_controller.add_rule(["Far", "Far"], ["Low", "Centered"])


def calculate_turn(right_distance, front_distance):
    global right_controller, left_controller
    right_turn = right_controller.fire([right_distance, front_distance])[1]
    left_turn = left_controller.fire([right_distance, front_distance])[1]
    
    return left_turn - right_turn


def calculate_speed(right_distance, front_distance):
    global right_controller, left_controller
    speed1 = right_controller.fire([right_distance, front_distance])[0]
    speed2 = left_controller.fire([right_distance, front_distance])[0]
    
    return min(speed1, speed2) 


