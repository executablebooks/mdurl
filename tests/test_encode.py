import pytest

from mdurl import encode


@pytest.mark.parametrize(
    "input_,expected",
    [
        pytest.param("%%%", "%25%25%25", id="should encode percent"),
        pytest.param("\r\n", "%0D%0A", id="should encode control chars"),
        pytest.param("?#", "?#", id="should not encode parts of an url"),
        pytest.param("[]^", "%5B%5D%5E", id="should not encode []^ - commonmark tests"),
        pytest.param("my url", "my%20url", id="should encode spaces"),
        pytest.param("φου", "%CF%86%CE%BF%CF%85", id="should encode unicode"),
        pytest.param(
            "%FG", "%25FG", id="should encode % if it doesn't start a valid escape seq"
        ),
        pytest.param(
            "%00%FF", "%00%FF", id="should preserve non-utf8 encoded characters"
        ),
        pytest.param(
            "\x00\x7F\x80",
            "%00%7F%C2%80",
            id="should encode characters on the cache borders",
        ),  # protects against off-by-one in cache implementation
    ],
)
def test_encode(input_, expected):
    assert encode(input_) == expected


def test_encode_arguments():
    assert encode("!@#$", exclude="@$") == "%21@%23$"
    assert encode("%20%2G", keep_escaped=True) == "%20%252G"
    assert encode("%20%2G", keep_escaped=False) == "%2520%252G"
    assert encode("!@%25", exclude="@", keep_escaped=False) == "%21@%2525"


def test_encode_surrogates():
    # bad surrogates (high)
    assert encode("\uD800foo") == "%EF%BF%BDfoo"
    assert encode("foo\uD800") == "foo%EF%BF%BD"

    # bad surrogates (low)
    assert encode("\uDD00foo") == "%EF%BF%BDfoo"
    assert encode("foo\uDD00") == "foo%EF%BF%BD"

    # valid one
    # (the codepoint is "D800 DD00" in UTF-16BE)
    assert encode("𐄀") == "%F0%90%84%80"
