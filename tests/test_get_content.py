from page_analyzer.app import get_content
import pytest

URL_1 = "tests/fixtures/url_1.html"
URL_2 = "tests/fixtures/url_2.html"
URL_3 = "tests/fixtures/url_3.html"
URL_4 = "tests/fixtures/url_4.html"


def read_html(url):
    with open(url) as file:
        meta = file.read()
    return meta


@pytest.mark.parametrize(
    "url, result",
    [
        (read_html(URL_1), ("h1", "title", "description")),
        (read_html(URL_2), ("", "title", "description")),
        (read_html(URL_3), ("h1", "", "description")),
        (read_html(URL_4), ("h1", "title", "")),
    ],
)
def test_get_content(url, result):
    assert get_content(url) == result
