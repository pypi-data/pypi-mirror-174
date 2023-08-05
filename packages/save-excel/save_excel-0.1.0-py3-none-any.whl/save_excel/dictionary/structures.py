from schema import Schema, Or
from pandas import DataFrame
from openpyxl.formatting.rule import Rule


def validate_structure(dict, structure):
    if structure.is_valid(dict)==False:
        raise ValueError(f'Object provided does not match expected structure: {structure.schema}')


XL_DICT_STRUCTURE = Schema(
    {
        str: {
            str: [
                Or(
                    [DataFrame],
                    {str: DataFrame}
                )
            ]
        }
    }
)

CONDITIONAL_FORMAT_STRUCTURE = Schema(
    {
        str: [Rule]
    }
)

COMMENTS_STRUCTURE = Schema(
    {
        str: str
    }
)

DATA_VALIDATION_STRUCTURE = Schema(
    {
        str: [str]
    }
)
