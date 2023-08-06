import pytest

def test_company_list_parse_html_properties(Parser, company_list_html):
    page = Parser._parse_html(company_list_html)

    assert len(page.items) == 30
    assert page.total_pages == 52
    assert page.page_num == 1

def test_company_list_parse_html_page_52_properties(Parser, company_list_page_52_html):
    page = Parser._parse_html(company_list_page_52_html)

    assert len(page.items) == 1
    assert page.total_pages == 52
    assert page.page_num == 52

def test_company_list_parse_single_card(Parser, company_list_html):
    page = Parser._parse_html(company_list_html)

    item = page.items[0]

    assert item.href == '/account/company/2464/'
    assert item.title == 'Abay Academy'
    assert item.description == 'IT-компания'
