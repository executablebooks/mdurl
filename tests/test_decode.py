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
