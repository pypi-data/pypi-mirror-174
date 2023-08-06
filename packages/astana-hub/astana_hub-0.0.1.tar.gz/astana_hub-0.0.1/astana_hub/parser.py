import asyncio
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
import logging

import aiohttp
from bs4 import BeautifulSoup


@dataclass
class Page:
    items: list
    page_num: int
    total_pages: int


@dataclass
class Item:
    title: str
    href: str
    description: str
    img_src: str = field(default=None, repr=False)
    full_description: str = field(default=None, repr=False)


class Parser:
    BASE_URL = 'https://astanahub.com'
    DEFAULT_USERAGENT = "Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2909.25 Safari/537.36"

    TAGS = {
        "company": ('', 'tag_startup', 'tag_it_company', 'tag_corp_partner', 'tag_techpark', 'tag_ts_member'),
        "user": ('', 'tag_intern', 'tag_it_specialist', 'tag_investor', 'tag_international_agent'),
    }

    def __init__(self, useragent=None, proxy=None):
        self.useragent = useragent if useragent else Parser.DEFAULT_USERAGENT
        self.proxy = proxy if proxy else {}

        self.session = aiohttp.ClientSession()
        self.logger = logging.getLogger('astana_hub.parser')

        assert type(self.useragent) is str, f"invalid {useragent=}"
        assert type(self.proxy) is dict, f"unsupported {proxy=}"

    @asynccontextmanager
    async def create(*args, **kwargs):
        parser = Parser(*args, **kwargs)
        try:
            yield parser
        finally:
            await parser.close()

    async def close(self):
        if self.session is not None and not self.session.closed:
            await self.session.close()

    def _soup_factory(html):
        return BeautifulSoup(html, "lxml")

    def _parse_html(html):
        soup = Parser._soup_factory(html)
        company_list = soup.find("div", class_="company-list")

        assert company_list

        items = []
        for card in company_list.find_all("a", class_="card"):
            item = Item(
                title = card.find('h4').text,
                href = card.attrs['href'],
                description = card.find('span').text,
                img_src = card.find('img') and card.find('img').attrs['src'],                      # optional
                full_description = card.find('p') and card.find('p').text.strip()                 # optional
            )
            items.append(item)

        # if there is only one page, ther is no pagination block and 1, 1 is valid
        page_num, total_pages = 1, 1

        pagination = soup.find("ul", class_="pagination-list")
        if pagination:
            li_list = pagination.find_all("li")
            if li_list:
                el = li_list[-1].find("a", class_="paginator")
                if el:
                    total_pages = int(el.text)

            current_a = pagination.find("a", class_="active")
            if current_a:
                page_num = int(current_a.text)

        return Page(items=items, page_num=page_num, total_pages=total_pages)

    async def get_page(self, page_type, page=1, tag=''):
        assert page_type in ('company', 'user'), f"unsupported {page_type=} for get_page request!"
        assert tag in Parser.TAGS[page_type], f"unsupported {tag=} for get_page request with {page_type=}!"

        url = f"{Parser.BASE_URL}/account/{page_type}/"
        params = {"page": page, "tag": tag}
        headers = {'User-Agent': self.useragent, 'Referer': url}

        async with self.session.get(url, params=params, **self.proxy) as response:
            self.logger.info(f"get_page request ({page_type=}, {params=}, {headers=})")
            assert response.status == 200, f"{response.status=}"

            html = await response.text()
            page_obj = Parser._parse_html(html)

            assert page_obj.page_num == page
            return page_obj

    async def get_company_page(self, page=1, tag=''):
        return await self.get_page(page_type='company', page=page, tag=tag)

    async def get_user_page(self, page=1, tag=''):
        return await self.get_page(page_type='user', page=page, tag=tag)

    async def parse_all(self, page_type, tag='', sleep=1):
        items = []
        page_num = 1
        while True:
            page = await self.get_page(page_type=page_type, page=page_num,  tag=tag)
            items.extend( page.items )

            if page.page_num == page.total_pages:
                return items

            assert page_num < page.total_pages, f"we somehow got here: {page_num=} {page.total_pages=}"

            await asyncio.sleep(sleep)
            page_num += 1
