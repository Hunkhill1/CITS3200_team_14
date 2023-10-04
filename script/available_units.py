from script.database_interface import get_prerequisites
import script.constants as constants 

def CanDo(completed_units:list[str], incomplete_units:list[str])->list[str]:
    """ Checks if a unit can be done based on the pre-requisites

    Args:
        completed_units (list[str]): list of completed unit codes
        incomplete_units (list[str],): list of uncompleted unit codes

    Returns:
        post_units (list[str]): list of units whose pre-reqs are within completed_units
    """ 
    post_units: list[str] = []
    #transverse incomplete
    for unit in incomplete_units:
        pre_reqs = get_prerequisites(unit)
       
        # Check if pre_reqs is None (unit has no prerequisites)
        if pre_reqs is None:
            post_units.append(unit)
        else:
            # Check if all prerequisites are in completed_units
            temp_list = completed_units + constants.summer_units
            if all(item in temp_list for item in pre_reqs):
                post_units.append(unit)
    return post_units

