from tests.fixtures.url import PARSED as FIXTURES

from mdurl import parse


def test_parse():
    for url, expected in FIXTURES.items():
        parsed = parse(url)
        parsed = {k: v for k, v in parsed.items() if v is not None}
        assert parsed == expected
