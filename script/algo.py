from script.study_planner_interface import *
from script.available_units import CanDo


def algorithm(completed_units_list: list[str], incomplete_units: list[str], start_sem:int) -> None:
    """ Algorithm to add units to the study plan matrix

    Args:
        completed_units_list (list[str]): list of completed unit codes
        incomplete_units (list[str]): list of uncompleted unit codes
    """
    # Rearrange compelteed units in joshs heuristic order
    
    # Step 1: Add completed units to the study planner
    for unit in completed_units_list:
        add_completed_unit_to_planner(unit)
    while True:
        units_to_add: list[str] = []  # Temporary list for units to add in this iteration

        # First Iteration
        post_req = CanDo(completed_units_list, incomplete_units)
        for unit in post_req:
                units_to_add.append(unit)

        # Add units from the first iteration to the study planner
        for unit in units_to_add:
            add_incompleted_unit_to_planner(unit,start_sem)

        # Update completed_units_list with units from this iteration
        completed_units_list += units_to_add
        
        # Create a new list of remaining incomplete units
        remaining_units = [unit for unit in incomplete_units if unit not in completed_units_list]

        # Check if there are no more units to add
        if not remaining_units:
            break

        # Set incomplete_units to the remaining units for the next iteration
        incomplete_units = remaining_units
        
    update_null_values(start_sem)

        
def remove_string_from_list(input_list:list[str], string_to_remove:str)->list[str]:
    """ Remove all occurrences of a specified string from the list.

    Args:
        input_list (list[str]):  The list to remove the string from.
        string_to_remove (str):  The string to remove from the list.

    Returns:
        list[str]:  The list with all occurrences of the specified string removed.
    """    
    return [item for item in input_list if item != string_to_remove]

def clean_list(input_list:list[str])->list[str]:
    """ Remove all occurrences of a specified string from the list.

    Args:
        input_list (list[str]):  The list to remove the string from.

    Returns:
        list[str]:  The list with all occurrences of the specified string removed.
    """    
    temp_list_1 = remove_string_from_list(input_list, constants.select_unit_str)
    temp_list_2 = remove_string_from_list(temp_list_1, constants.option_str)
    return temp_list_2
        

