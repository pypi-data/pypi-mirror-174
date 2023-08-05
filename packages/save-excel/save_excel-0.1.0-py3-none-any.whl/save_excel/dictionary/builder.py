from save_excel.dictionary.structures import validate_structure, XL_DICT_STRUCTURE
from save_excel.utils import dict_depth, list_depth


class ExcelDict:
    
    def __init__(self, dict):
        validate_structure(dict, XL_DICT_STRUCTURE)
        self.dict = dict
        
    @classmethod
    def from_nested_dict(cls, obj):
        return cls(obj)
        
    @classmethod
    def from_simple_dict(cls, obj, bookname, sheetname):
        return cls({bookname:{sheetname:[obj]}})

    @classmethod
    def from_nested_list(cls, obj, bookname, sheetname):
        return cls({bookname:{sheetname:obj}})
    
    @classmethod
    def from_simple_list(cls, obj, bookname, sheetname):
        return cls({bookname:{sheetname:[obj]}})
    
    @classmethod
    def from_dataframe(cls, obj, bookname, sheetname):
        return cls({bookname:{sheetname:[[obj]]}})


def factory_dict(obj, bookname, sheetname):
        
    # Building from dict
    if isinstance(obj, dict):
        if dict_depth(obj)==1:
            return ExcelDict.from_simple_dict(obj, bookname=bookname, sheetname=sheetname)
        else:
            return ExcelDict.from_nested_dict(obj)

    # Building from list
    elif isinstance(obj, list):
        if list_depth(obj)==1:
            return ExcelDict.from_simple_list(obj, bookname=bookname, sheetname=sheetname)
        else:
            return ExcelDict.from_nested_list(obj, bookname=bookname, sheetname=sheetname)

    # Building from dataframe
    else:
        return ExcelDict.from_dataframe(obj, bookname=bookname, sheetname=sheetname)