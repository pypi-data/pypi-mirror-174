from save_excel.utils import set_value

from openpyxl.styles import PatternFill, Font, Alignment, Side, Border
from openpyxl.styles.differential import DifferentialStyle

class CellStyle:
    
    def __init__(self, height=None):
        self.__height = height
        self.__font = Font()
        self.__fill = PatternFill()
        self.__alignment = Alignment()
        self.__border = Border()
        
    @property
    def height(self):
        return self.__height
    
    @height.setter
    @set_value([int])
    def height(self, new_height):
        self.__height = new_height
        
    @property
    def font(self):
        return self.__font
    
    @property
    def fill(self):
        return self.__fill
    
    @property
    def alignment(self):
        return self.__alignment
    
    @property
    def border(self):
        return self.__border
    
    @border.setter
    @set_value([None])
    def border(self, value):
        self.__border = value


class TitleStyle(CellStyle):
    
    def __init__(self):
        
        super().__init__(height=20)
        
        self.font.color = 'FFFFFF'
        self.font.name = 'Segoe UI Semibold'
        self.font.size = 14
        self.font.bold = True
        
        self.fill.start_color = '244062'
        self.fill.end_color = '244062'
        self.fill.fill_type = 'solid'
        
        self.alignment.horizontal = 'center'
        self.alignment.vertical = 'center'
        self.alignment.wrap_text = True
        
        self.border.left = Side(style='thin')
        self.border.right = Side(style='thin')
        self.border.bottom = Side(style='thin')
        self.border.top = Side(style='thin')


class HeaderStyle(CellStyle):
    
    def __init__(self):
        
        super().__init__()
        
        self.font.color = '000000'
        self.font.name = 'Calibri'
        self.font.size = 12
        self.font.bold = False
        
        self.fill.start_color = 'BFBFBF'
        self.fill.end_color = 'BFBFBF'
        self.fill.fill_type = 'solid'
        
        self.alignment.horizontal = 'center'
        self.alignment.vertical = 'center'
        self.alignment.wrap_text = True
        
        self.border.left = Side(style='thin')
        self.border.right = Side(style='thin')
        self.border.bottom = Side(style='thin')
        self.border.top = Side(style='thin')


class DataStyle(CellStyle):
    
    def __init__(self):
        
        super().__init__()
        
        self.font.color = '000000'
        self.font.name = 'Calibri'
        self.font.size = 11
        self.font.bold = False
        
        self.alignment.horizontal = 'center'
        self.alignment.vertical = 'center'
        self.alignment.wrap_text = True
        
        self.border.left = Side(style='thin')
        self.border.right = Side(style='thin')
        self.border.bottom = Side(style='thin')
        self.border.top = Side(style='thin')


class TableStyles:
    
    def __init__(self):
        self.__title = TitleStyle()
        self.__header = HeaderStyle()
        self.__data = DataStyle()
        
    @property
    def title(self):
        return self.__title
    
    @title.setter
    @set_value([None])
    def title(self, value):
        self.__title = value
    
    @property
    def header(self):
        return self.__header
    
    @header.setter
    @set_value([None])
    def header(self, value):
        self.__header = value
    
    @property
    def data(self):
        return self.__data
    
    @data.setter
    @set_value([None])
    def data(self, value):
        self.__data = value