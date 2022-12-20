from . import count_words, types
from pathlib import Path
from typing import Sequence, Union
import bisect

# The minimum total number of words needed to be able to represent all 64-bit
# integers with six words or less is 1628
COUNT = 1628
FILE = Path(__file__).parent.parent / 'words.txt'


def read_words(file=None):
    lines = (i.strip() for i in Path(file or FILE).read_text().splitlines())
    return tuple(i for i in lines if i and not i.startswith('#'))


class Nmr:
    COUNT = 1628
    WORDS = read_words()

    def __init__(self, count=None, words=None):
        if not isinstance(words, (list, tuple)):
            if words is None and count is None:
                count = self.COUNT
                words = self.WORDS
            else:
                words = read_words(words)

        if count is not None:
            words = words[:count]
        assert len(set(words)) == len(words), 'Duplicate words'
        self.words = words

        self.count = count_words.CountWords(self.n).count
        self.inverse = {w: i for i, w in enumerate(self.words)}

    def __call__(self, s: Union[int, Sequence[str], str]):
        if isinstance(s, list):
            return self.name_to_int(s)

        if isinstance(s, int):
            return self.int_to_name(s)

        st = types.try_to_int(s)
        if st is not None:
            return st

        return self.name_to_int(s.split())

    def int_to_name(self, num: int) -> Sequence[str]:
        if num < 0:
            raise ValueError('Only accepts non-negative numbers')
        return [self.words[i] for i in self._to_digits(num)]

    def name_to_int(self, words: Sequence[str]) -> int:
        words = list(words)
        if len(set(words)) != len(words):
            raise ValueError('Repeated words not allowed')

        try:
            indexes = [self.inverse[w] for w in reversed(words)]
        except KeyError:
            raise KeyError(*sorted(set(words) - set(self.inverse))) from None

        return self._from_digits(list(self._redupe(indexes))[::-1])

    @property
    def n(self):
        return len(self.words)

    def _to_digits(self, num):
        it = (i + 1 for i in range(self.n) if self.count(i + 1) > num)
        if (word_count := next(it, None)) is None:
            raise ValueError(f'Cannot represent {num} in base {self.n}')

        total = num - self.count(word_count - 1)
        digits = []

        for i in range(word_count):
            total, index = divmod(total, self.n - i)
            digits.append(index)
        assert not total

        return list(self._undupe(digits))[::-1]

    def _from_digits(self, digits):
        total = 0
        for i, d in enumerate(digits):
            total *= self.n - (len(digits) - i - 1)
            total += d

        return self.count(len(digits) - 1) + total

    @staticmethod
    def _undupe(indexes):
        sorted_result = []

        for i in indexes:
            for s in sorted_result:
                i += (s <= i)
            bisect.insort(sorted_result, i)
            yield i

    @staticmethod
    def _redupe(indexes):
        for i, num in enumerate(indexes):
            yield num - sum(k < num for k in indexes[:i])
