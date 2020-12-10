from fuzzy_controller import fuzzy_set as fs
from fuzzy_controller import fuzzy_value as fv
from fuzzy_controller import fuzzy_controller as fc


obstacle_controller = None


def setup():
    global obstacle_controller
    left_value = fv.FuzzyValue()
    left_value.add_set(fs.FuzzySet("Close", 0, 0, 0.75, 0.85))
    left_value.add_set(fs.FuzzySet("Medium", 0.75, 0.85, 1.3, 1.4))
    left_value.add_set(fs.FuzzySet("Far", 1.3, 1.4, 100, 101))

    right_value = fv.FuzzyValue()
    right_value.add_set(fs.FuzzySet("Close", 0, 0, 0.75, 0.85))
    right_value.add_set(fs.FuzzySet("Medium", 0.75, 0.85, 1.3, 1.4))
    right_value.add_set(fs.FuzzySet("Far", 1.3, 1.4, 100, 101))

    front_value = fv.FuzzyValue()
    front_value.add_set(fs.FuzzySet("Close", 0, 0, 1.6, 1.8))
    front_value.add_set(fs.FuzzySet("Medium", 1.6, 1.8, 2, 2.2))
    front_value.add_set(fs.FuzzySet("Far", 2, 2.2, 100, 101))

    speed_value = fv.FuzzyValue(output=True)
    speed_value.add_set(fs.FuzzySet("Low", 0, 0.2, 0.2, 0.3))
    speed_value.add_set(fs.FuzzySet("Medium", 0.2, 0.3, 0.4, 0.5))
    speed_value.add_set(fs.FuzzySet("High", 0.4, 0.5, 0.9, 1))

    turn_value = fv.FuzzyValue(output=True)
    turn_value.add_set(fs.FuzzySet("Left", 0.8, 0.8, 0.02, 0.01))
    turn_value.add_set(fs.FuzzySet("Centered", 0.02, 0.01, -0.01, -0.02))
    turn_value.add_set(fs.FuzzySet("Right", -0.01, -0.02, -0.8, -0.8))

    obstacle_controller = fc.FuzzyController([left_value, front_value, right_value], [
                                             speed_value, turn_value], fc.FuzzyController.FuzzyOperator.AND)
    obstacle_controller.add_rule(["Close", "Close", "Close"], ["Low", "Left"])
    obstacle_controller.add_rule(
        ["Close", "Close", "Medium"], ["Low", "Left"])
    obstacle_controller.add_rule(["Close", "Close", "Far"], ["Low", "Right"])
    obstacle_controller.add_rule(["Close", "Medium", "Close"], ["Low", "Centered"])
    obstacle_controller.add_rule(
        ["Close", "Medium", "Medium"], ["Low", "Right"])
    obstacle_controller.add_rule(["Close", "Medium", "Far"], ["Low", "Left"])
    obstacle_controller.add_rule(["Close", "Far", "Close"], ["Low", "Centered"])
    obstacle_controller.add_rule(["Close", "Far", "Medium"], ["Low", "Centered"])
    obstacle_controller.add_rule(["Close", "Far", "Far"], ["Low", "Right"])

    obstacle_controller.add_rule(["Medium", "Close", "Close"], ["Low", "Left"])
    obstacle_controller.add_rule(
        ["Medium", "Close", "Medium"], ["Low", "Left"])
    obstacle_controller.add_rule(["Medium", "Close", "Far"], ["Low", "Right"])
    obstacle_controller.add_rule(
        ["Medium", "Medium", "Close"], ["Low", "Right"])
    obstacle_controller.add_rule(
        ["Medium", "Medium", "Medium"], ["Low", "Left"])
    obstacle_controller.add_rule(["Medium", "Medium", "Far"], ["Low", "Right"])
    obstacle_controller.add_rule(["Medium", "Far", "Close"], ["Low", "Centered"])
    obstacle_controller.add_rule(
        ["Medium", "Far", "Medium"], ["Low", "Centered"])
    obstacle_controller.add_rule(["Medium", "Far", "Far"], ["Low", "Right"])

    obstacle_controller.add_rule(["Far", "Close", "Close"], ["Low", "Left"])
    obstacle_controller.add_rule(["Far", "Close", "Medium"], ["Low", "Left"])
    obstacle_controller.add_rule(["Far", "Close", "Far"], ["Low", "Right"])
    obstacle_controller.add_rule(["Far", "Medium", "Close"], ["Low", "Left"])
    obstacle_controller.add_rule(["Far", "Medium", "Medium"], ["Low", "Left"])
    obstacle_controller.add_rule(["Far", "Medium", "Far"], ["Low", "Right"])
    obstacle_controller.add_rule(["Far", "Far", "Close"], ["Low", "Centered"])
    obstacle_controller.add_rule(["Far", "Far", "Medium"], ["Low", "Centered"])
    obstacle_controller.add_rule(["Far", "Far", "Far"], ["Low", "Centered"])


def calculate_turn(left_distance, front_distance, right_distance):
    global obstacle_controller
    result = obstacle_controller.fire(
        [left_distance, front_distance, right_distance])

    return result[1]


def calculate_speed(left_distance, front_distance, right_distance):
    global obstacle_controller
    result = obstacle_controller.fire(
        [left_distance, front_distance, right_distance])

    return result[0]


