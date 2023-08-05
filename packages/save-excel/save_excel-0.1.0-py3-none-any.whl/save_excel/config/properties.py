from save_excel.utils import set_value


class Distribution:

    def __init__(self):
        self.index = False
        self.startcol = 0
        self.startrow = 0
        self.cols_between_tables = 1
        self.rows_between_tables = 1

class View:

    def __init__(self):
        self.view = 'normal'
        self.grid_lines = False
        self.freeze_panes = None


class Printer:

    def __init__(self):
        self.margins = self.__Margins()
        self.orientation = 'portrait'
        self.fit_to_page = False
        self.fit_to_height = False
        self.fit_to_width = False
        self.horizontal_centered = True
        self.vertical_centered = False
        
    class __Margins:
        
        def __init__(self):
            self.left = .3
            self.right = .3
            self.top = .3
            self.bottom = .3


class Properties:

    def __init__(self):
        self.distribution = Distribution()
        self.view = View()
        self.printer = Printer()
