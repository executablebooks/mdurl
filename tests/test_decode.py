import re
import urllib.parse

import pytest

from mdurl import decode


def test_decode_multi_byte():
    assert decode("https://host.invalid/%F0%9F%91%A9") == "https://host.invalid/👩"


def test_decode_invalid_utf8():
    assert decode("https://host.invalid/%CF") == "https://host.invalid/\ufffd"
    assert decode("https://host.invalid/%C0%bf") == "https://host.invalid/\ufffd\ufffd"
    # This is different from `urllib.parse.unquote`. We add 3 * \ufffd as does
    # Javascript upstream, urllib only adds 2 * \ufffd.
    assert (
        decode("https://host.invalid/%F1%81%d1%45")
        == "https://host.invalid/\ufffd\ufffd\ufffdE"
    )


def _percent_encode(binary):
    # Mirror the ``encodeBinary`` helper in ``tests/decode.js``: strip all
    # whitespace, then convert each trailing 8-bit chunk to a two-digit
    # lowercase hex escape, prepending to the result.
    binary = re.sub(r"\s+", "", binary)
    result = ""
    while binary:
        chunk = binary[-8:]
        result = "%" + format(int(chunk, 2), "02x") + result
        binary = binary[:-8]
    return result


def _decode_uri_component(percent):
    # Mimic JavaScript ``decodeURIComponent``: strict UTF-8 decoding, which
    # raises ``UnicodeDecodeError`` on malformed sequences just like
    # ``decodeURIComponent`` throws URIError on them.
    return urllib.parse.unquote_to_bytes(percent).decode("utf-8", "strict")


# Binary UTF-8 sample matrix ported verbatim from tests/decode.js. As in the
# JS test, the True/False marks are documentation only: each sample's
# validity is decided by the strict UTF-8 oracle above (the JS test likewise
# probes decodeURIComponent directly and never reads the marks).
SAMPLES = {
    "00000000": True,
    "01010101": True,
    "01111111": True,
    # invalid as 1st byte
    "10000000": True,
    "10111111": True,
    # invalid sequences, 2nd byte should be >= 0x80
    "11000111 01010101": False,
    "11100011 01010101": False,
    "11110001 01010101": False,
    # invalid sequences, 2nd byte should be < 0xc0
    "11000111 11000000": False,
    "11100011 11000000": False,
    "11110001 11000000": False,
    # invalid 3rd byte
    "11100011 10010101 01010101": False,
    "11110001 10010101 01010101": False,
    # invalid 4th byte
    "11110001 10010101 10010101 01010101": False,
    # valid sequences
    "11000111 10101010": True,
    "11100011 10101010 10101010": True,
    "11110001 10101010 10101010 10101010": True,
    # minimal chars with given length
    "11000010 10000000": True,
    "11100000 10100000 10000000": True,
    # impossible sequences
    "11000001 10111111": False,
    "11100000 10011111 10111111": False,
    "11000001 10000000": False,
    "11100000 10010000 10000000": False,
    # maximum chars with given length
    "11011111 10111111": True,
    "11101111 10111111 10111111": True,
    "11110000 10010000 10000000 10000000": True,
    "11110000 10010000 10001111 10001111": True,
    "11110100 10001111 10110000 10000000": True,
    "11110100 10001111 10111111 10111111": True,
    # too low
    "11110000 10001111 10111111 10111111": False,
    # too high
    "11110100 10010000 10000000 10000000": False,
    "11110100 10011111 10111111 10111111": False,
    # surrogate range
    "11101101 10011111 10111111": True,
    "11101101 10100000 10000000": False,
    "11101101 10111111 10111111": False,
    "11101110 10000000 10000000": True,
}


def test_decode_percent():
    assert decode("x%20xx%20%2520") == "x xx %20"


def test_decode_invalid_sequences():
    assert decode("%2g%z1%%") == "%2g%z1%%"


def test_decode_reserved_set_percent():
    assert decode("%20%25%20", "%") == " %25 "


def test_decode_reserved_set_space():
    assert decode("%20%25%20", " ") == "%20%%20"


def test_decode_reserved_set_both():
    assert decode("%20%25%20", " %") == "%20%25%20"


@pytest.mark.parametrize("binary", SAMPLES.keys())
def test_decode_utf8_sample_matrix(binary):
    percent = _percent_encode(binary)
    try:
        expected = _decode_uri_component(percent)
        error = None
    except UnicodeDecodeError:
        error = True

    result = decode(percent)

    if error:
        assert "\ufffd" in result
    else:
        assert result == expected
        assert "\ufffd" not in result
