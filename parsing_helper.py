from enum import Enum

class Exp(Enum):
    MODIFIER = 0
    LITERAL = 1
    VARIABLE = 2
    COMPARISON = 3
    IF_KEY_WORD = 4


MODIFIERS = ['+', '-', 'NOR', 'AND', '&&', 'XOR', '^', "RSH"]
COMPARISONS = ['==', '!=', '>=', '<']
IF_KEY_WORDS = ["if", "endif"]

def is_literal(string: str):
    if string[0].isalpha():
        return False
    return True

def get_exp_type(exp_part: str):
    if exp_part in MODIFIERS:
        return Exp.MODIFIER
    if exp_part in COMPARISONS:
        return Exp.COMPARISON
    if exp_part in IF_KEY_WORDS:
        return Exp.IF_KEY_WORD
    elif is_literal(exp_part):
        return Exp.LITERAL
    else:
        return Exp.VARIABLE
