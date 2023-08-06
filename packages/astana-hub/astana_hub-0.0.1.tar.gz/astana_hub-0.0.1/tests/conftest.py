# this hack allows pytest to find astana_hub package without installing package inside pipenv.
import sys
sys.path.append('../astana_hub')

import os
import pytest
import astana_hub


# не разобрался я как правильно ее отдавать так чтобы она и работала т отдалась объектои Parser именно и тирдаун у нее был правильный
# @pytest.fixture
# async def astana_hub_parser():
#     """Instance of astana_hub Parser object with some random useragent"""
#     async with astana_hub.Parser.create(useragent="very unsuspicious useragent!") as ah:
#         return ah

@pytest.fixture
def useragent():
    """sample useragent"""
    return "Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2909.25 Safari/537.36"

@pytest.fixture
def Parser():
    """astana_hub Parser class object"""
    return astana_hub.Parser


@pytest.fixture
def company_list_html():
    """Copy of https://astanahub.com/account/company/  html page as of 30/10/2022."""
    with open(os.path.join(os.path.dirname(__file__), "company_list.html"), "r") as f:
        return f.read()

@pytest.fixture
def company_list_page_52_html():
    """Copy of https://astanahub.com/account/company/?page=52  html page as of 30/10/2022."""
    with open(os.path.join(os.path.dirname(__file__), "company_list_52.html"), "r") as f:
        return f.read()
