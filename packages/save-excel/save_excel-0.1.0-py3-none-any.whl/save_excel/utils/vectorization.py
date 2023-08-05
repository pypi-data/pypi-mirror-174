from save_excel.utils.alphabet import get_column_letter
from numpy import vectorize


get_column_letter_vectorized = vectorize(get_column_letter)
len_vectorized = vectorize(len)