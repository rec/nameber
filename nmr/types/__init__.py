from __future__ import annotations

from typing import Any, cast

from ..categories import Category, make_category
from ..nameable_type import NameableType
from .fraction import Fraction
from .integer import Integer
from .ip_address import IPv4Address, IPv6Address
from .lat_long import LatLong
from .sem_ver import Semver
from .uuid import Uuid


def str_to_index(s: str) -> int:
    for cls in NameableType.SUBCLASSES.values():
        try:
            t = cls.str_to_type(s)
        except Exception:
            continue
        n = cls.type_to_index(t)
        r = cls.category.number_to_index(n)
        assert isinstance(r, int)
        return r

    raise ValueError(f"Cannot understand string '{s}'")


def index_to_str(index: int) -> str:
    category, n = make_category(index)
    cls = NameableType.SUBCLASSES[category.name.lower()]
    t = cls.index_to_type(n)
    print('XXXXX', t, type(t))
    return cls.type_to_str(t)


def names() -> list[str]:
    return list(NameableType.SUBCLASSES)
