from script.study_planner_interface import update_semester_column, add_unit_to_matrix
from script.available_units import CanDo

completed_units = ['a','b','c']
incomplete_units = [['d',['a']],['e',['a','b']],['f',['l','m','n']]]

def algorithm(completed_units:list[str], incomplete_units:list[list[str]])->None:
    """ Algorithm to add units to the study plan matrix

    Args:
        completed_units (list[str]): list of completed unit codes
        incomplete_units (list[list[str]]): list of uncompleted unit codes
    """
    post_req = CanDo(completed_units, incomplete_units)
    for units in  post_req:
        add_unit_to_matrix(units)
        
algorithm(completed_units, incomplete_units)
