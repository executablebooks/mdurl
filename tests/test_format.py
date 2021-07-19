import pytest

from mdurl import format, parse
from tests.fixtures.url import PARSED as FIXTURES


@pytest.mark.parametrize(
    "url,expected_dict",
    FIXTURES.items(),
)
def test_format(url, expected_dict):
    parsed = parse(url)
    assert format(parsed) == url
