from typing import Any, Iterable, NoReturn, Union

from ._core import BJKST as _BJKST

ValueT = Union[int, bytes, str]


def _unsupported_operand_types(op: str, left: Any, right: Any) -> NoReturn:
    raise TypeError(
        f"unsupported operand type(s) for {op}: {type(left)!r} and {type(right)}",
    )


class BJKST:
    """Estimate the number of distinct elements in a data stream.

    Examples:
        >>> # Create an empty BJKST.
        >>> bjkst = BJKST()
        >>> # Add some elements, with duplicates.
        >>> bjkst.update(range(75_000))
        >>> bjkst.update(range(25_000, 100_000))
        >>> # Count the distinct elements.
        >>> assert 99_000 <= len(bjkst) <= 101_000
    """

    __slots__ = ["_inner"]

    _inner: _BJKST

    def __init__(
        self,
        values: Union[Iterable[ValueT], "BJKST", None] = None,
        *,
        precision: int = 16,
    ) -> None:
        if isinstance(values, BJKST):
            self._inner = values._inner.copy()
            return
        self._inner = _BJKST(precision)
        if values is not None:
            self.update(values)

    def __bool__(self) -> bool:
        """Return ``True`` if the BJKST is nonempty.

        Examples:
            >>> bjkst = BJKST()
            >>> bool(bjkst)
            False
            >>> bjkst.add(1)
            >>> bool(bjkst)
            True
        """
        return bool(self._inner)

    def __ior__(self, other: "BJKST") -> "BJKST":
        """Update this BJKST with the elements of another one.

        Examples:
            >>> bjkst_1 = BJKST(range(75_000))
            >>> bjkst_2 = BJKST(range(25_000, 100_000))
            >>> bjkst_1 |= bjkst_2
            >>> assert 99_000 <= len(bjkst_1) <= 101_000
        """
        if not isinstance(other, BJKST):
            _unsupported_operand_types("|=", self, other)
        self._inner.update_bjkst(other._inner)
        return self

    def __len__(self) -> int:
        """Estimate the number of distinct elements in the BJKST.

        Examples:
            >>> bjkst = BJKST(range(75_000))
            >>> bjkst.update(range(25_000, 100_000))
            >>> assert 99_000 <= len(bjkst) <= 101_000
        """
        return len(self._inner)

    def __or__(self, other: "BJKST") -> "BJKST":
        """Return a new BJKST with the elements of this BJKST and another one.

        Examples:
            >>> bjkst_1 = BJKST(range(75_000))
            >>> bjkst_2 = BJKST(range(25_000, 100_000))
            >>> bjkst = bjkst_1 | bjkst_2
            >>> assert 99_000 <= len(bjkst) <= 101_000
        """
        if not isinstance(other, BJKST):
            _unsupported_operand_types("|", self, other)
        result = self.copy()
        result._inner.update_bjkst(other._inner)
        return result

    def add(self, value: ValueT) -> None:
        """Add an element to the BJKST.

        Examples:
            >>> bjkst = BJKST()
            >>> bjkst.add(1)
            >>> len(bjkst)
            1
            >>> bjkst.add(2)
            >>> len(bjkst)
            2
            >>> bjkst.add(2)
            >>> len(bjkst)
            2
        """
        self._inner.add(value)

    def clear(self) -> None:
        """Clear the BJKST, removing all values.

        Examples:
            >>> bjkst = BJKST()
            >>> bjkst.add(1)
            >>> bjkst.clear()
            >>> len(bjkst)
            0
        """
        self._inner.clear()

    def copy(self) -> "BJKST":
        """Return a copy of this BJKST."""
        return BJKST(self)

    @staticmethod
    def deserialize(data: bytes) -> "BJKST":
        """Deserialize a BJKST."""
        bjkst = BJKST.__new__(BJKST)
        bjkst._inner = _BJKST.deserialize(data)
        return bjkst

    def _hash(self, value: ValueT) -> int:
        return self._inner.hash(value)  # type: ignore

    def serialize(self) -> bytes:
        """Serialize this BJKST."""
        return self._inner.serialize()  # type: ignore

    def union(self, *others: Union[Iterable[ValueT], "BJKST"]) -> "BJKST":
        """Return a new BJKST with elements from this one and all others.

        Examples:
            >>> bjkst_1 = BJKST(range(75_000))
            >>> bjkst_2 = BJKST(range(25_000, 100_000))
            >>> bjkst = bjkst_1.union(bjkst_2)
            >>> assert 99_000 <= len(bjkst) <= 101_000
        """
        result = self.copy()
        result.update(*others)
        return result

    def update(self, *others: Union[Iterable[ValueT], "BJKST"]) -> None:
        """Update this BJKST, adding elements from all others.

        Examples:
            >>> bjkst = BJKST(range(75_000))
            >>> bjkst.update(range(25_000, 100_000))
            >>> assert 99_000 <= len(bjkst) <= 101_000
        """
        for values in others:
            if isinstance(values, BJKST):
                self._inner.update_bjkst(values._inner)
                continue
            hashes = [self._hash(value) for value in values]
            self._inner.update_hashes(hashes)
