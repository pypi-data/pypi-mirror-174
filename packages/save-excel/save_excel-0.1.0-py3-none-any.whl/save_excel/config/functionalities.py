from save_excel.utils import set_value
from save_excel.dictionary.structures import (
    validate_structure,
    CONDITIONAL_FORMAT_STRUCTURE, 
    COMMENTS_STRUCTURE, 
    DATA_VALIDATION_STRUCTURE
)

class Functionalities:
    
    def __init__(self):
        self.__conditional_format = {}
        self.__comments = {}
        self.__data_validation = {}
        self.__autofilter = False
        self.__columns_width = self.__ColumnsWidth()
        
    class __ColumnsWidth:

        def __init__(self):
            self.autofit = True
            self.increase = 0
            self.min_limit = None
            self.max_limit = None
        
    @property
    def conditional_format(self):
        return self.__conditional_format
    
    @conditional_format.setter
    def conditional_format(self, new_dict):
        validate_structure(new_dict, CONDITIONAL_FORMAT_STRUCTURE)
        self.__conditional_format = new_dict
    
    @property
    def comments(self):
        return self.__comments
    
    @comments.setter
    @set_value([dict])
    def comments(self, new_dict):
        validate_structure(new_dict, COMMENTS_STRUCTURE)
        self.__comments = new_dict
        
    @property
    def data_validation(self):
        return self.__data_validation
    
    @data_validation.setter
    @set_value([dict])
    def data_validation(self, new_dict):
        validate_structure(new_dict, DATA_VALIDATION_STRUCTURE)
        self.__data_validation = new_dict
        
    @property
    def autofilter(self):
        return self.__autofilter
    
    @autofilter.setter
    @set_value([bool])
    def autofilter(self, new_dict):
        self.__autofilter = new_dict
        
    @property
    def columns_width(self):
        return self.__columns_width