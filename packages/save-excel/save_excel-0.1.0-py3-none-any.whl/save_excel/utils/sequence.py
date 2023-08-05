def to_list(obj):
    """Converts an iterable into list"""
    return list(iter(obj))


def first(obj):
    """Returns first value of an iterable"""
    
    list_obj = to_list(obj)
    
    if len(list_obj)>0:
        return list_obj[0]
    else:
        return None
    

def last(obj):
    """Returns last value of an iterable"""
    
    list_obj = to_list(obj)
    
    if len(list_obj)>0:
        return list_obj[-1]
    else:
        return None


def dict_depth(dict_obj):
    """Returns depth of a dictionary"""
    if isinstance(dict_obj, dict):
        return 1 + (max(map(dict_depth, dict_obj.values())) if dict_obj else 0)
    else:
        return 0
    

def list_depth(list_obj):
    """Returns depth of a list"""
    if isinstance(list_obj, list):
        return 1 + (max(map(list_depth, list_obj)) if list_obj else 0)
    else:
        return 0