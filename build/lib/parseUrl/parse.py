import re

from sly import Lexer, Parser

"""url_example
    /api/v1/people?page=1&page_size=10&order_by=name desc, hireDate asc&filter=name eq makai'
    EQUAL = r'eq', =
    NOT_EQUAL = r'ne', not
    GREATER_THAN = r'gt', >
    GREATER_THAN_OR_EQUAL = r'ge', >=
    LESS_THAN = r'lt', <
    LESS_THAN_OR_EQUAL = r'le' =<
    AND and
    OR or
    NOT not
"""


class ParseUrlRequest:
    def __init__(self, page, page_size):
        self.page = page
        self.page_size = page_size
        self.order_by = {}
        self.filter = []

    def add_order_by(self, key, value):
        self.order_by[key] = value

    def get_order_by(self):
        return self.order_by

    def add_filter(self, item):
        self.filter.append(item)

    def get_filter(self):
        return self.filter


class ParseException:
    pass


class MyLexer(Lexer):
    tokens = {'IDENTIFIER',
              'NUMBER',

              'LPAREN',
              'RPAREN',

              'AND',
              'OR',
              'NOT',

              'ASSIGN',
              'QM',
              'DIVIDE',
              'COMMA',
              'DOT',

              'EQUAL',
              'NOT_EQUAL',
              'GREATER_THAN',
              'GREATER_THAN_OR_EQUAL',
              'LESS_THAN',
              'LESS_THAN_OR_EQUAL',

              }

    ignore = ' \t'

    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_, \'`]*'
    NUMBER = r'\d+'
    DIVIDE = r'/'
    ASSIGN = r'='
    #
    LPAREN = r'\('
    RPAREN = r'\)'
    AND = r'&'
    OR = r'or'
    NOT = r'not'

    QM = r'\?'
    COMMA = r'\,'
    DOT = r'\.'

    EQUAL = r'eq',
    NOT_EQUAL = r'ne',
    GREATER_THAN = r'gt',
    GREATER_THAN_OR_EQUAL = r'ge',
    LESS_THAN = r'lt',
    LESS_THAN_OR_EQUAL = r'le'
    ignore_newline = r'`'


def format_sort(sort_list):
    if sort_list is None:
        return None
    pairs = sort_list.split(',')
    dict_sort = {}
    for pair in pairs:
        key, value = pair.strip().split(' ')
        dict_sort[key] = value
    return dict_sort


def parse_condition_to_mysql(query_string):
    pattern = re.compile(r'\((.*?)\)')
    matches = pattern.findall(query_string)
    for match in matches:
        subquery = parse_condition_to_mysql(match)
        query_string = query_string.replace(f'({match})', f'({subquery})')
    return query_string


def split_conditions(condition_string):
    conditions = re.split(r'\b(and|not)\b', condition_string)
    return [condition.strip() for condition in conditions if condition.strip()]


def generate_sql_queries(conditions):
    sql_queries = []
    for condition in conditions:
        mysql_query = parse_condition_to_mysql(condition)
        sql_queries.append(mysql_query)

    return sql_queries


def format_filter(filter_list):
    if filter_list is None:
        return None
    conditions = split_conditions(filter_list)
    sql_queries = generate_sql_queries(conditions)
    return sql_queries


def split_url(data):
    lexer = MyLexer()
    parts = re.split(r'\s+(?=(?:[^\']*\'[^\']*\')*[^\']*$)', data)

    tokens = []
    for part in parts:
        tokens.extend(lexer.tokenize(part))
    tokens = [tok for tok in lexer.tokenize(data)]

    page = page_size = sort = None
    i = 0
    filter_value = ''
    while i < len(tokens):

        if tokens[i].type == 'IDENTIFIER' and tokens[i + 1].type == 'ASSIGN':
            if tokens[i].value == 'page':
                page = tokens[i + 2].value
            elif tokens[i].value == 'page_size':
                page_size = tokens[i + 2].value
            elif tokens[i].value == 'order_by':
                sort = tokens[i + 2].value
            elif tokens[i].value == 'filter':
                i += 2
                while i < len(tokens):
                    filter_value += str(tokens[i].value)
                    i += 1
                break
            i += 3
        else:
            i += 1
    p = ParseUrlRequest(page=page, page_size=page_size)
    if sort is not None:
        p.order_by = dict(format_sort(sort))
        print(type(p.order_by))
    else:
        p.order_by = {}
    if filter_value is not None:
        p.filter = list(format_filter(filter_value))
    else:
        p.filter = []

    return p.page, p.page_size, p.order_by, p.filter


# if __name__ == '__main__':
#     data = (
#         '/api/resources?page=1&page_size=10&filter=(priority eq 1 or city eq `Redmond`) and (price gt 100 or price gt 200) not price le 3.5')
#     print(split_url(data=data))
