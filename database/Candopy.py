from database_interface import get_prerequisites
'''
Cando

param;
completed_units:  list of completed unit codes
incomplete_units: list of uncompleted unit codes

return;
post_units: list of units whose pre-reqs are within completed_units

'''
def CanDo(completed_units, incomplete_units):
    post_units = []
    #transverse incomplete
    for unit in incomplete_units:
        pre_reqs = unit[1]
        #check if pre_reqs of incomplete are contained within the completed untits 
        if all(item in completed_units for item in pre_reqs):
            post_units.append(unit[0])
    return post_units
