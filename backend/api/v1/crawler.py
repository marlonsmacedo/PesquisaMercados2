import re
import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import List
from pprint import pprint as print


class Guanabara:

    def __init__(self):
        self.url = "https://www.supermercadosguanabara.com.br/produtos/"
        self.headers = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
        }

    async def fetch_sections_url(self) -> List:
        async with httpx.AsyncClient() as session:
            response = await session.get(self.url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            section_name = [
                name.text
                for name in soup.find(
                    "div", {"class": "item item-menu item-sections"}
                ).find_all("a")
            ]
            section_url = [
                url.get("href")
                for url in soup.find(
                    "div", {"class": "item item-menu item-sections"}
                ).find_all("a")
            ]
            sections = [
                {"section": section, "url": url}
                for section, url in zip(section_name, section_url)
            ]

        return sections

    async def fetch_products_for_sections(self):
        """
            Asynchronously fetches products for sections and returns a list of dictionaries containing section information and product details.
        """
        sections = await self.fetch_sections_url()
        tasks = []
        async with httpx.AsyncClient() as client:
            for section in sections:
                tasks.append(
                    client.get(f'{self.url}{section["url"][10:]}', headers=self.headers)
                )
            responses = await asyncio.gather(*tasks)
            htmls = [
                BeautifulSoup(response.text, "html.parser") for response in responses
            ]
            list_items = []
            for html in htmls:
                list_items.append(
                    {
                        "section": html.find("div", {"class": "products-list"})
                        .find_previous("div", {"class": "title"})
                        .find("h3")
                        .text,
                        "items": [
                            {"product": item.text, "price": price.text, "validUntil":  re.sub('\n|Validade: ', '', html.find('div', {'class': 'products-list'}).find_previous('div', {'class': 'validate'}).find('p').text)}
                            for item, price in zip(
                                html.find("div", {"class": "products-list"}).find_all('div', {'class': 'name'}),
                                html.find("div", {"class": "products-list"}).find_all("span", {"class": "number"}), 
                            )
                        ],
                    })
            print(list_items)
            return list_items


if __name__ == "__main__":
    g = Guanabara()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(g.fetch_products_for_sections())
    #    for section in sections:
    #        tasks.append(await client.get(f'{self.url}{section["url"][10:]}', headers=self.headers))
    #    print(tasks)
    # return await asyncio.gather(*tasks)
    # tasks = []
    # for section in sections:
    #     tasks.append(self.fetch_products(section["Url"]))
    # return await asyncio.gather(*tasks)
