import fuzzy_set as fs
import fuzzy_value as fv
import rule_set as rs


temp_value = fv.FuzzyValue()
temp_value.add_set(fs.FuzzySet("Low", 0, 3, 6, 9))
temp_value.add_set(fs.FuzzySet("Medium", 6, 9, 12, 15))
temp_value.add_set(fs.FuzzySet("High", 13, 15, 18, 21))

dist_value = fv.FuzzyValue()
dist_value.add_set(fs.FuzzySet("Low", 0, 3, 6, 9))
dist_value.add_set(fs.FuzzySet("Medium", 6, 9, 12, 15))
dist_value.add_set(fs.FuzzySet("High", 13, 15, 18, 21))

speed_value = fv.FuzzyValue(output=True)
speed_value.add_set(fs.FuzzySet("Low", 0, 3, 6, 9))
speed_value.add_set(fs.FuzzySet("Medium", 6, 9, 12, 15))
speed_value.add_set(fs.FuzzySet("High", 13, 15, 18, 21))

rules = rs.RuleSet()
rules.add_rule(temp_value.get_set("Low"), dist_value.get_set(
    "Medium"), speed_value.get_set("Medium"))
rules.add_rule(temp_value.get_set("Low"), dist_value.get_set(
    "High"), speed_value.get_set("High"))
