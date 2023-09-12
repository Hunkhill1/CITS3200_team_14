from script.study_planner_interface import update_semester_column, add_unit_to_matrix
from script.available_units import CanDo

update_semester_column()

completed_units = ['a','b','c']
incomplete_units = [['d',['a']],['e',['a','b']],['f',['l','m','n']]]

post_req = CanDo(completed_units, incomplete_units)
for units in  post_req:
    add_unit_to_matrix(units, 1)

