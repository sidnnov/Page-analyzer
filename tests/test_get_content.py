from page_analyzer.app import get_content
import pytest


URL_1 = "python-project-83/tests/fixtures/url_1.html"
URL_2 = "tests/fixtures/url_2.html"
URL_3 = "tests/fixtures/url_3.html"
URL_4 = "tests/fixtures/url_4.html"


@pytest.mark.parametrize(
    "url, result",
    [
        (URL_1, ("h1", "title", "description")),
        (URL_2, ("", "title", "description")),
        (URL_3, ("h1", "", "description")),
        (URL_4, ("h1", "title", "")),
    ],
)
def test_get_content(url, result):
    with open(url) as file:
        meta_str = file.read()
    assert get_content(meta_str) == result
