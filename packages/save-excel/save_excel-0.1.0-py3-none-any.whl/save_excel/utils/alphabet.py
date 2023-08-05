from string import ascii_uppercase


def excel_alphabet(cycles=1):
    """
    Returns an ordered list of letters from A to ZZ
    Args:
        cycles (int): Number of cycles in which alphabet will start again. cycles = 0 will return all possible permutations.
    """
    
    ascii_uppercase_to_cycle = ascii_uppercase[:cycles-1] if cycles>0 else ascii_uppercase
    letters = list(ascii_uppercase) + [x+y for x in ascii_uppercase_to_cycle for y in ascii_uppercase]
    
    return letters


EXCEL_ALPHABET = excel_alphabet(0)

def get_column_letter(idx):
    return EXCEL_ALPHABET[idx]