from urllib.parse import urlparse
from bs4 import BeautifulSoup


def normalize_url(url: str) -> str:
    url_parse = urlparse(url)
    correct_url = url_parse._replace(
        path="", params="", query="", fragment="").geturl()
    return correct_url


def get_content(data: str) -> tuple:
    content = BeautifulSoup(data, "lxml")
    h1 = content.find("h1")
    title = content.find("title")
    meta_data = content.find("meta", attrs={"name": "description"})
    h1 = h1.text if h1 else ""
    title = title.text if title else ""
    description = meta_data.get("content") if meta_data else ""
    return h1, title, description
