# conditions = ['priority eq 1', 'and', 'city eq `Redmond`', 'and', 'price gt 100', 'and', 'price gt 200', 'not',
#               'price le 3.5']
import re


def is_valid_string(str):
    parts = str.split()
    return len(parts) == 3


conditions = ['(priority eq 1 or city eq `Redmond`)', 'and', '(price gt 100 or price gt 200)', 'not', '(price le 3.5)']


def add_and_to_result(condition1, condition2):
    return f'and_({condition1}, {condition2})'


def add_not_to_result(condition):
    return f'not_({condition})'


def add_or_to_reuslt(condition1, condition2):
    return f'or_({condition1}, {condition2})'


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
                left = re.split(r'\b(and|or)\b', left)
                right = re.split(r'\b(and|or)\b', right)

                result += add_and_to_result(add_or_to_reuslt(left[0], left[2]), add_or_to_reuslt(right[0], right[2]))
                i += 2
        elif conditions[i] == 'not':
            result += add_not_to_result(condition=conditions[i + 1])
            i += 2
        else:
            i += 1

    print(result)
print(convert_to_sqlalchemy(conditions=conditions))