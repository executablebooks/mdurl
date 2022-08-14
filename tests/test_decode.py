from mdurl import decode


def test_decode_multi_byte():
    assert decode("https://host.invalid/%F0%9F%91%A9") == "https://host.invalid/👩"
