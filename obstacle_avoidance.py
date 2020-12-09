import fuzzy_set as fs
import fuzzy_value as fv
import fuzzy_controller as fc


obstacle_controller = None


def setup():
    global obstacle_controller
    left_value = fv.FuzzyValue()
    left_value.add_set(fs.FuzzySet("Close", 0, 0, 0.75, 0.85))
    left_value.add_set(fs.FuzzySet("Medium", 0.2, 0.75, 0.85, 1.4))
    left_value.add_set(fs.FuzzySet("Far", 0.85, 1.4, 10, 11))

    right_value = fv.FuzzyValue()
    right_value.add_set(fs.FuzzySet("Close", 0, 0, 0.75, 0.85))
    right_value.add_set(fs.FuzzySet("Medium", 0.2, 0.75, 0.85, 1.4))
    right_value.add_set(fs.FuzzySet("Far", 0.85, 1.4, 10, 11))

    front_value = fv.FuzzyValue()
    front_value.add_set(fs.FuzzySet("Close", 0.05, 0.05, 1.2, 1.4))
    front_value.add_set(fs.FuzzySet("Medium", 1.2, 1.4, 1.8, 2))
    front_value.add_set(fs.FuzzySet("Far", 1.8, 2, 100, 101))

    speed_value = fv.FuzzyValue(output=True)
    speed_value.add_set(fs.FuzzySet("Low", 0, 0.2, 0.2, 0.3))
    speed_value.add_set(fs.FuzzySet("Medium", 0.2, 0.3, 0.4, 0.5))
    speed_value.add_set(fs.FuzzySet("High", 0.4, 0.5, 0.9, 1))

    turn_value = fv.FuzzyValue(output=True)
    turn_value.add_set(fs.FuzzySet("Left", -0.4, -0.4, -0.02, -0.01))
    turn_value.add_set(fs.FuzzySet("Centered", -0.02, -0.01, 0.01, 0.02))
    turn_value.add_set(fs.FuzzySet("Right", 0.01, 0.02, 0.4, 0.4))

    obstacle_controller = fc.FuzzyController([left_value, front_value, right_value], [
                                             speed_value, turn_value], fc.FuzzyController.FuzzyOperator.AND)
    obstacle_controller.add_rule(["Close", "Close", "Close"], ["Low", "Left"])
    obstacle_controller.add_rule(
        ["Close", "Close", "Medium"], ["Low", "Right"])
    obstacle_controller.add_rule(["Close", "Close", "Far"], ["Low", "Right"])
    obstacle_controller.add_rule(["Close", "Medium", "Close"], ["Low", "Left"])
    obstacle_controller.add_rule(
        ["Close", "Medium", "Medium"], ["Low", "Right"])
    obstacle_controller.add_rule(["Close", "Medium", "Far"], ["Low", "Left"])
    obstacle_controller.add_rule(["Close", "Far", "Close"], ["Low", "Left"])
    obstacle_controller.add_rule(["Close", "Far", "Medium"], ["Low", "Right"])
    obstacle_controller.add_rule(["Close", "Far", "Far"], ["Low", "Right"])

    obstacle_controller.add_rule(["Medium", "Close", "Close"], ["Low", "Left"])
    obstacle_controller.add_rule(
        ["Medium", "Close", "Medium"], ["Low", "Left"])
    obstacle_controller.add_rule(["Medium", "Close", "Far"], ["Low", "Right"])
    obstacle_controller.add_rule(
        ["Medium", "Medium", "Close"], ["Low", "Right"])
    obstacle_controller.add_rule(
        ["Medium", "Medium", "Medium"], ["Low", "Right"])
    obstacle_controller.add_rule(["Medium", "Medium", "Far"], ["Low", "Right"])
    obstacle_controller.add_rule(["Medium", "Far", "Close"], ["Low", "Right"])
    obstacle_controller.add_rule(
        ["Medium", "Far", "Medium"], ["Low", "Centered"])
    obstacle_controller.add_rule(["Medium", "Far", "Far"], ["Low", "Right"])

    obstacle_controller.add_rule(["Far", "Close", "Close"], ["Low", "Left"])
    obstacle_controller.add_rule(["Far", "Close", "Medium"], ["Low", "Left"])
    obstacle_controller.add_rule(["Far", "Close", "Far"], ["Low", "Right"])
    obstacle_controller.add_rule(["Far", "Medium", "Close"], ["Low", "Left"])
    obstacle_controller.add_rule(["Far", "Medium", "Medium"], ["Low", "Left"])
    obstacle_controller.add_rule(["Far", "Medium", "Far"], ["Low", "Right"])
    obstacle_controller.add_rule(["Far", "Far", "Close"], ["Low", "Right"])
    obstacle_controller.add_rule(["Far", "Far", "Medium"], ["Low", "Centered"])
    obstacle_controller.add_rule(["Far", "Far", "Far"], ["Low", "Centered"])


def get_obstacle_turn(left_distance, front_distance, right_distance):
    global obstacle_controller
    result = obstacle_controller.fire(
        [left_distance, front_distance, right_distance])

    return result[1]


def get_obstacle_speed(left_distance, front_distance, right_distance):
    global obstacle_controller
    result = obstacle_controller.fire(
        [left_distance, front_distance, right_distance])

    return result[0]


setup()
print(get_obstacle_turn(0.6, 0.3, 0.4))
