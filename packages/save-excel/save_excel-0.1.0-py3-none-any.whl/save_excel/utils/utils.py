from save_excel.utils.vectorization import len_vectorized
from numpy import array


def check_empty_frame(df):
    """Checks if a dataframe is completely empty (no columns, no rows)"""
    if df.shape==(0,0):
        return True
    else:
        return False


def set_value(datatypes):
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            
            for n, (arg, datatype) in enumerate(zip(args[1:], datatypes)):
                
                if datatype is None:
                    if arg is not None:
                        raise ValueError(f'{func.__name__}: attribute can only be setted to {datatype}')
                else:
                    if not isinstance(arg, datatype):
                        raise ValueError(f'{func.__name__}: attribute can only be setted to {datatype}')

            return func(*args, **kwargs)
    
        return wrapper
    return decorator


def max_column_lengths(df, include_header=True, include_index=False):
    """
    Returns an array containing the maximun lenght of each column.
    Args:
        include_header (bool): If include_header is True, the length of column names will be considered. 
                               In case of having multiindex in the columns only the last row will be considered.
        include_index (bool): If include_index is True, index will be considered.
    """

    if include_index==True:
        # Add index to the frame
        df_copy = df.reset_index().copy()
    else:
        # Ignore index
        df_copy = df.copy()
    
    # Calculate max length of values for each column
    max_values_lengths = len_vectorized(df_copy.values.astype(str)).max(axis=0)
    
    if include_header==True:
        
        if len(df_copy.columns.names)>1:
            # Calculate lengths of column names (having multiindex)
            max_header_lengths = len_vectorized(array(list(zip(*df_copy.columns))[-1]).astype(str))
        else:
            # Calculate lengths of column names
            max_header_lengths = len_vectorized(df_copy.columns.astype(str))
        
        # Returns max lengths of the comparison between values and column names
        return array([max_values_lengths, max_header_lengths]).max(axis=0)
    
    else:
        return max_values_lengths


def validate_path(path):
    """Validates and returns path"""
    if path is None:
        return ''
    elif path.endswith('/'):
        return path
    else:
        return path + '/'