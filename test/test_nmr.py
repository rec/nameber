import pytest

from nmr import Nmr, nmr
from nmr.count_words import CountWords


def test_count():
    M = 2**64 - 1

    def count(n, i):
        return CountWords(n).count(i)

    assert count(nmr.count, 6) > M > count(nmr.count - 1, 6)
    assert count(nmr.count, 6) > 1.0001 * M
    assert M / 1.003 > count(nmr.count - 1, 6)


_STABILITY_TABLE = (
    (0, ["the"]),
    (1, ["of"]),
    (999, ["hans"]),
    (134123978423341234, ["this", "valid", "menu", "gamma", "phase", "ban"]),
    (
        341279384172341314120987134123443434734134913248132481234812341823413,
        [
            "i",
            "proud",
            "door",
            "fight",
            "ink",
            "later",
            "fixed",
            "tree",
            "truck",
            "bruce",
            "taxi",
            "play",
            "log",
            "all",
            "res",
            "also",
            "cube",
            "doing",
            "reid",
            "cool",
            "iron",
            "night",
        ],
    ),
)


@pytest.mark.parametrize("number, words", _STABILITY_TABLE)
def test_stability(number, words):
    actual_words = nmr.encode_to_name(number)
    assert actual_words == words
    assert nmr.decode_from_name(words) == number
