import re

from parseUrl.definition import OPERATOR_EQUAL, OPERATOR_LESS_THAN_OR_EQUAL, OPERATOR_LESS_THAN, \
    OPERATOR_GREATER_THAN_OR_EQUAL, OPERATOR_GREATER_THAN, OPERATOR_NOT_EQUAL, LOGICAL_OPERATOR_AND, \
    LOGICAL_OPERATOR_NOT, LOGICAL_OPERATOR_OR


def replace_comparison_operators(s):
    s = s.replace('eq', OPERATOR_EQUAL)
    s = s.replace('ne', OPERATOR_NOT_EQUAL)
    s = s.replace('gt', OPERATOR_GREATER_THAN)
    s = s.replace('ge', OPERATOR_GREATER_THAN_OR_EQUAL)
    s = s.replace('lt', OPERATOR_LESS_THAN)
    s = s.replace('le', OPERATOR_LESS_THAN_OR_EQUAL)
    s = s.replace('`', '"')
    return s


def is_valid_string(str):
    parts = str.split()
    return len(parts) == 3


def add_and_to_result(condition1, condition2):
    return f'{LOGICAL_OPERATOR_AND}({condition1}, {condition2})'


def add_not_to_result(condition):
    return f'{LOGICAL_OPERATOR_NOT}({condition})'


def add_or_to_result(condition1, condition2):
    return f'{LOGICAL_OPERATOR_OR}({condition1}, {condition2})'


def split_conditions_or(condition_string):
    conditions = re.split(r'\b(and|or)\b', condition_string)
    return [condition.strip() for condition in conditions if condition.strip()]


def convert_to_sqlalchemy(conditions):
    result = ''
    i = 0
    while i < len(conditions):
        if conditions[i] == 'and':
            left, right = conditions[i - 1], conditions[i + 1]
            if is_valid_string(left) and is_valid_string(right):
                result += add_and_to_result(left, right)
                i += 2
            else:
                left = split_conditions_or(left)
                right = split_conditions_or(right)

                result += add_and_to_result(add_or_to_result(left[0], left[2]), add_or_to_result(right[0], right[2]))
                i += 2
        elif conditions[i] == 'not':
            result += add_not_to_result(condition=conditions[i + 1])
            i += 2
        elif conditions[i] == 'or':
            result += add_or_to_result(condition1=conditions[i - 1], condition2=conditions[i + 1])
            i += 2
        else:
            i += 1
    if len(result) == 0:
        result = conditions[0]
    return result.strip()
