from save_excel.utils import EXCEL_ALPHABET, cell_from_coordinates
from itertools import product


class Shape:
    
    def __init__(self, width, length):
        if length==0 or width==0:
            self.__shape = None
        else:
            self.__shape = (length, width)
        
    @property
    def shape(self):
        return self.__shape
    
    def __repr__(self):
        return f'Shape({self.__shape})'


class Coordinates:
    
    def __init__(self, startcol, startrow):
        if startcol<0 or startrow<0:
            raise ValueError('startcol and startrow must be greater or equal to 0')
        else:
            self.__coord = (startcol, startrow)
            
    @property
    def coord(self):
        return self.__coord
    
    @coord.setter
    def coord(self, new_coord):
        self.__coord = new_coord
    
    def increase(self, values):
        self.__coord = tuple((x+y) for x, y in zip(self.__coord, values))
        
    def __eq__(self, other):
        return self.__coord==other.__coord

    def __repr__(self):
        return f'Coordinates({self.__coord})'


class CellRange(Shape, Coordinates):
    
    def __init__(self, startcol=0, startrow=0, width=1, length=1):
        
        Shape.__init__(self, width=width, length=length)
        Coordinates.__init__(self, startcol=startcol, startrow=startrow)
        
        if self.shape is None:
            self.coord = None
        
    @property
    def origin(self):
        if self.shape is None:
            return None
        else:
            col, row = self.coord
            return cell_from_coordinates(col=col, row=row)
    
    @property
    def fin(self):
        if self.shape is None:
            return None
        else:
            col, row = self.coord
            length, width = self.shape
            return cell_from_coordinates(col=col+width-1, row=row+length-1)
        
    @property
    def range(self):
        if self.shape is None:
            return None
        else:
            return f'{self.origin}:{self.fin}'
    
    @property
    def rows(self):
        """
        Returns rows as coordinates
        """
        
        if self.shape is None:
            return []
        else:
            for row in range(self.coord[1], self.coord[1] + self.shape[0]):
                yield row
        
    @property
    def cols(self):
        """
        Returns columns as coordinates
        """
        
        if self.shape is None:
            return []
        else:
            for col in range(self.coord[0], self.coord[0] + self.shape[1]):
                yield col
            
    @property
    def cells(self):
        """
        Returns individual cells from the range
        """

        col_list = [EXCEL_ALPHABET[r] for r in self.cols]
        row_list = [str(r+1) for r in self.rows]

        for cell in product(col_list, row_list):
            yield ''.join(cell)
            
    def __repr__(self):
        if self.shape is None:
            return f'CellRange(None)'
        else:
            return f'CellRange({self.range})'