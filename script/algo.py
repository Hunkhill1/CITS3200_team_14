from script.study_planner_interface import  add_unit_to_planner
from script.available_units import CanDo

def algorithm(completed_units:list[str], incomplete_units:list[str])->None:
    """ Algorithm to add units to the study plan matrix

    Args:
        completed_units (list[str]): list of completed unit codes
        incomplete_units (list[str]): list of uncompleted unit codes
    """
    
    for unit in completed_units:
        add_unit_to_planner(unit)
        
    post_req = CanDo(completed_units, incomplete_units)
    print("Post reqs:", post_req)
    for units in post_req:
        add_unit_to_planner(units)
        
def remove_string_from_list(input_list:list[str], string_to_remove:str)->list[str]:
    """ Remove all occurrences of a specified string from the list.

    Args:
        input_list (list[str]):  The list to remove the string from.
        string_to_remove (str):  The string to remove from the list.

    Returns:
        list[str]:  The list with all occurrences of the specified string removed.
    """    
    return [item for item in input_list if item != string_to_remove]
        

