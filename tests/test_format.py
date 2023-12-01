import pytest

from mdurl import format, parse  # noqa: A004
from tests.fixtures.url import PARSED as FIXTURES


@pytest.mark.parametrize("url", FIXTURES.keys())
def test_format(url):
    parsed = parse(url)
    assert format(parsed) == url
