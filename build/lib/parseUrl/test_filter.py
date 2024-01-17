# import re
#
#
# def parse_condition_to_mysql(query_string):
#     query_string = query_string.replace('eq', '=').replace('gt', '>').replace('le', '<=').replace('not', 'NOT')
#
#     pattern = re.compile(r'\((.*?)\)')
#     matches = pattern.findall(query_string)
#
#     for match in matches:
#         subquery = parse_condition_to_mysql(match)
#         query_string = query_string.replace(f'({match})', f'({subquery})')
#
#     return query_string
#
#
# def split_conditions(condition_string):
#     # Tách các điều kiện bằng 'and'
#     conditions = re.split(r'\b(and|not)\b', condition_string)
#
#     # Loại bỏ các phần tử rỗng và trả về danh sách các điều kiện
#     return [condition.strip() for condition in conditions if condition.strip()]
#
#
# def generate_sql_queries(conditions):
#     # Tạo danh sách các câu lệnh SQL
#     sql_queries = []
#     for condition in conditions:
#         mysql_query = parse_condition_to_mysql(condition)
#         sql_queries.append(mysql_query)
#
#     return sql_queries
#
#
# # Chuỗi điều kiện mới
# condition_string = "(priority eq 1 or city eq `Redmond`) and price gt 100 and price gt 200 not price le 3.5"
#
# # Tách các điều kiện
# conditions = split_conditions(condition_string)
#
# # Tạo danh sách các câu lệnh SQL
# sql_queries = generate_sql_queries(conditions)
#
# # In ra danh sách các câu lệnh SQL
# print(sql_queries)
