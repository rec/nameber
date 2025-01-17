from __future__ import annotations

from typing import Any, Generic, Type, TypeVar, cast, get_args

from .categories import Subcategory

DataType = TypeVar("DataType")


class NameableType(Generic[DataType]):
    category: Subcategory

    @classmethod
    def index_to_type(cls, i: int) -> DataType:
        return cls._make(i)

    @classmethod
    def str_to_type(cls, s: str) -> DataType:
        return cls._make(s)

    @staticmethod
    def type_to_index(t: DataType) -> int:
        return int(t)  # type: ignore[no-any-return, call-overload]

    @staticmethod
    def type_to_str(t: DataType) -> str:
        return str(t)

    SUBCLASSES: dict[str, Type[NameableType[Any]]] = {}

    def __init_subclass__(cls) -> None:
        name = cls.category.name.lower()
        assert name not in NameableType.SUBCLASSES
        NameableType.SUBCLASSES[name] = cls

    @classmethod
    def _make(cls, s: int | str) -> DataType:
        data_type = get_args(cls.__orig_bases__[0])[0]  # type: ignore[attr-defined]
        return cast(DataType, data_type(s))


def get_class(prefix: str) -> type[NameableType[Any]]:
    cl = [
        c
        for c in NameableType.SUBCLASSES.values()
        if c.__class__.__name__.lower().startswith(prefix.lower())
    ]
    if not cl:
        raise ValueError(f"Unknown {prefix=}")
    if len(cl) > 1:
        raise ValueError(f"Ambiguous {prefix=}, could be {cl}")
    return cl[0]
