import pytest

from mdurl import parse
from tests.fixtures.url import PARSED as FIXTURES


def is_url_and_dict_equal(url, url_dict):
    return (
        url.protocol == url_dict.get("protocol")
        and url.slashes == url_dict.get("slashes", False)
        and url.auth == url_dict.get("auth")
        and url.port == url_dict.get("port")
        and url.hostname == url_dict.get("hostname")
        and url.hash == url_dict.get("hash")
        and url.search == url_dict.get("search")
        and url.pathname == url_dict.get("pathname")
    )


@pytest.mark.parametrize(
    "url,expected_dict",
    FIXTURES.items(),
)
def test_parse(url, expected_dict):
    parsed = parse(url)
    assert is_url_and_dict_equal(parsed, expected_dict)
