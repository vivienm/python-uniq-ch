import pytest

from uniq_ch import BJKST


class TestBJKST:
    def test_add(self) -> None:
        bjkst = BJKST()
        bjkst.add(1)
        assert len(bjkst) == 1

        bjkst.add(b"two")
        assert len(bjkst) == 2

        bjkst.add("three")
        assert len(bjkst) == 3

        with pytest.raises(TypeError):
            bjkst.add((4, 5))  # type: ignore

    def test_hash(self) -> None:
        bjkst = BJKST()

        # Hashing should be stable, that is, always produce the same hash for
        # the same input.
        assert bjkst._hash(1) == 14951757901955124024
        assert bjkst._hash(b"two") == 4084764272615746427
        assert bjkst._hash("three") == 11721900908943991347

        with pytest.raises(TypeError):
            bjkst._hash((4, 5))  # type: ignore

    def test_ior(self) -> None:
        bjkst = BJKST()
        with pytest.raises(TypeError):
            bjkst |= [1, 2]  # type: ignore

    def test_or(self) -> None:
        bjkst = BJKST()
        with pytest.raises(TypeError):
            bjkst | [1, 2]  # type: ignore

    def test_update(self) -> None:
        bjkst = BJKST()

        with pytest.raises(TypeError):
            bjkst.update([1, b"two", "three", (4, 5)])  # type: ignore

        # Update has failed, the BJKST should still be empty.
        assert len(bjkst) == 0

        bjkst.update([1, b"two", "three"])
        assert len(bjkst) == 3