from collections.abc import Callable, Iterable
from typing import Any, TypeAlias, TypeVar

import numpy as np
from pendulum import DateTime, from_timestamp

T = TypeVar("T")
ItemConv: TypeAlias = Callable[[Any], T]
ListConv: TypeAlias = Callable[[Iterable[Any]], list[T]]
NDArrayConv: TypeAlias = Callable[[Iterable[Any]], np.ndarray]


def to_list_of(item_type: ItemConv[T]) -> ListConv[T]:
    def converter(iterable: Iterable[Any]) -> list[T]:
        return [item_type(item) for item in iterable]

    return converter


def to_ndarray_of(item_type: ItemConv[T]) -> NDArrayConv:
    def converter(iterable: Iterable[Any]) -> np.ndarray:
        return np.array(iterable, dtype=item_type)

    return converter


def ms_ts_to_datetime(timestamp) -> DateTime:
    return from_timestamp(timestamp // 1000)


def ms_ts_to_datetime_ndarray(timestamps) -> np.ndarray:
    if isinstance(timestamps, np.ndarray):
        return timestamps
    return np.array([from_timestamp(ts // 1000) for ts in timestamps], dtype=DateTime)
