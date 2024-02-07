import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import List


class Guanabara:

    def __init__(self):
        self.url = "https://www.supermercadosguanabara.com.br/produtos"
        self.headers = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
        }

    async def fetch_sections(self) -> List:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url, headers=self.headers)
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
                {"Section": section, "Url": url}
                for section, url in zip(section_name, section_url)
            ]

        return sections

    async def fetch_products_for_sections(self, sections_list: List) -> List:
        sections_list = fetch_sections()
        return sections_list
