from save_excel.utils import EXCEL_ALPHABET, check_empty_frame, max_column_lengths, get_column_letter_vectorized, last
from save_excel.layout.cell_range import CellRange


class FrameLayout:
    
    def __init__(self, df, index=False, title=None, startcol=0, startrow=0):
        
        totally_empty = check_empty_frame(df)
        
        # Ancho del index
        if index==False or totally_empty:
            index_width = 0
        else:
            index_width = len(df.index.names)
            
        # Ancho total
        total_width = df.shape[1] + index_width
        
        # Largo del título
        if title is None:
            title_length = 0
        else:
            title_length = 1
        
        # Largo del header
        if totally_empty:
            header_length = 0
        else:
            header_length = len(df.columns.names)
            if header_length>1:
                header_length += 1 # Si el dataframe tiene multicolumns, se añade 1
        
        # Largo total
        total_length = df.shape[0] + header_length + title_length
        
        # Largo de los datos
        data_length = total_length - title_length - header_length
        
        self.total = CellRange(startcol=startcol, startrow=startrow, width=total_width, length=total_length)
        self.title = CellRange(startcol=startcol, startrow=startrow, width=total_width, length=title_length)
        self.header = CellRange(startcol=startcol, startrow=startrow+title_length, width=total_width, length=header_length)
        self.data = CellRange(startcol=startcol, startrow=startrow+title_length+header_length, width=total_width, length=data_length)
        self.df = df
        self.title_name = title
        self.column_widths = max_column_lengths(df, include_header=True, include_index=index)
        
    def find_column(self, col_name):
        column_list = self.df.columns.to_list()
        index = -len(column_list)+column_list.index(col_name)
        
        col = EXCEL_ALPHABET[self.total.coord[0]+self.total.shape[1]+index]
        
        header_row = str(self.header.coord[1]+1)
        header_cell = ''.join([col, header_row])
        
        data_start_row = str(self.data.coord[1]+1)
        data_end_row = str(self.data.coord[1]+self.data.shape[0])
        data_cell_range = ''.join([col, data_start_row]) + ':' + ''.join([col, data_end_row])
        
        return header_cell, data_cell_range
        
    def next_coord(self, direction, spaces):
        if direction=='vertical':
            last_value = last(self.total.rows)
        elif direction=='horizontal':
            last_value = last(self.total.cols)
        else:
            raise ValueError("Direction options are: 'vertical', 'horizontal'")
        
        if last_value is None:
            return None
        else:
            return last_value + spaces + 1
    
    def __repr__(self):
        return f'FrameLayout(\n\tTotal: {self.total}\n\tTitle: {self.title}\n\tHeader: {self.header}\n\tData: {self.data}\n)'


class ExcelLayout:
    
    def __init__(self, data, index=True, startcol=0, startrow=0, 
                 cols_between_tables=1, rows_between_tables=1):
        
        self.data = []
        self.column_dimensions = {}
        
        next_row = startrow
        tmp_row = startrow
        
        for data_iter in data:
            if isinstance(data_iter, dict):
                iter_obj = list(data_iter.items())
            elif isinstance(data_iter, list):
                iter_obj = [(None, df) for df in data_iter]
            
            next_col = startcol
            
            for title, df in iter_obj:
                
                frame_layout = FrameLayout(df, index=index, title=title, startcol=next_col, startrow=next_row)
                self.data.append(frame_layout)
                
                columns = get_column_letter_vectorized([*frame_layout.total.cols])
                new_column_dimensions = dict(zip(columns, frame_layout.column_widths))

                for col in new_column_dimensions:
                    if col in self.column_dimensions:
                        self.column_dimensions[col] = max(new_column_dimensions[col], self.column_dimensions[col])
                    else:
                        self.column_dimensions[col] = new_column_dimensions[col]
                
                next_col = frame_layout.next_coord('horizontal', spaces=cols_between_tables)
                tmp_row = max(tmp_row, frame_layout.next_coord('vertical', spaces=rows_between_tables))
                
            next_row = tmp_row
            tmp_row = 0