from page_analyzer.utils import get_data_from_url
import responses


@responses.activate
def test_get_data_from_url():
    url = "https://example.com/"
    expected_status_code = 200
    expected_text = "Some text"
    responses.add(
        responses.GET,
        url,
        status=expected_status_code,
        body=expected_text
    )
    assert expected_status_code, expected_text == get_data_from_url(url)

    responses.reset()
    responses.add(responses.GET, url, status=404)
    assert get_data_from_url(url) is None
