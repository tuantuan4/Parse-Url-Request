import pytest
from parseUrl.parse import split_url, format_sort, parse_condition_to_mysql, split_conditions


@pytest.fixture()
def data_url():
    return '/api/resources?page=1&page_size=10?order_by=name desc, hireDate asc?filter=(priority eq 1 or city eq `Redmond`) and (price gt 100 or price gt 200) not price le 3.5'


def test_split_url_request(data_url):
    page, page_size, order_by, filter = split_url(data=data_url)
    assert page == '1'
    assert page_size == '10'

    assert order_by == {'name': 'desc', 'hireDate': 'asc'}
    assert filter == ['(priority eq 1 or city eq `Redmond`)', 'and', '(price gt 100 or price gt 200)', 'not',
                      'price le 3.5']


def test_format_sort_is_null():
    dict_null = None
    dict_sort = format_sort(dict_null)
    assert dict_sort is None


def test_format_sort():
    dict_sort = format_sort('name desc, hireDate asc')
    assert dict_sort == {'name': 'desc', 'hireDate': 'asc'}
