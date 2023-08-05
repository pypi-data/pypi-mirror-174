from save_excel.utils import EXCEL_ALPHABET

def cell_from_coordinates(col, row):
    """Generates cell based on coordinates"""

    return f'{EXCEL_ALPHABET[col]}{row+1}'