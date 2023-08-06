# Installation

pip install astana-hub

# Features

- Get company list from https://astanahub.com/account/company/
    - Optional filter by tags: ('tag_startup', 'tag_it_company', 'tag_corp_partner', 'tag_techpark', 'tag_ts_member')
- Get user list from https://astanahub.com/account/company/
    - Optional filter by tags: ('tag_intern', 'tag_it_specialist', 'tag_investor', 'tag_international_agent')
- Async by aiohttp
- HTML parsing with bs4+lxml

# Usage

```
import asyncio
import astana_hub

async def main():
    async with astana_hub.Parser.create() as p:
        company_list_page1 = await p.get_company_page()
        print(company_list_page1)
        
        user_list_page1 = await p.get_user_page()
        print(user_list_page1)

        all_users = await p.parse_all(page_type='user')
        print(all_users)

        all_startups = await p.parse_all(page_type='company', tag='tag_startup')
        print(all_startups)

asyncio.run(main())
```
