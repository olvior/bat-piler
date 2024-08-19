from enum import Enum

class Exp(Enum):
    MODIFIER = 0
    LITERAL = 1
    VARIABLE = 2
    COMPARISON = 3

class Ports():
    SHOW_NUMBER = 250

MODIFIERS = ['+', '-']
COMPARISONS = ['==', '!=', '>=', '<']

def is_literal(string: str):
    if string[0].isalpha():
        return False
    return True

def get_exp_type(exp_part: str):
    if exp_part in MODIFIERS:
        return Exp.MODIFIER
    if exp_part in COMPARISONS:
        return Exp.COMPARISON
    elif is_literal(exp_part):
        return Exp.LITERAL
    else:
        return Exp.VARIABLE
