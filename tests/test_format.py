from tests.fixtures.url import PARSED as FIXTURES

from mdurl import parse, format


def test_format():
    for url, expected in FIXTURES.items():
        parsed = parse(url)
        assert format(parsed) == url
