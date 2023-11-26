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

    def test_deserialize(self) -> None:
        bjkst = BJKST.deserialize(
            b"\x02\x00\x00\x00\x00\x00\x00\x00\x04\x10\x00\x00\x10\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01"
            b"\xb21J\xc2H\xeb\x95~\x00\x00\x018\xcb\xac\x11\x98P\x7f\xcf\x00"
        )
        assert len(bjkst) == 2

        # Values 1 and 2 are in the BJKST already. Adding them again should not
        # change the size of the BJKST.
        bjkst.update([1, 2])
        assert len(bjkst) == 2

        # On the other hand, adding 3 should increase the size of the BJKST.
        bjkst.add(3)
        assert len(bjkst) == 3

        with pytest.raises(ValueError):
            bjkst.deserialize(b"invalid")

        with pytest.raises(TypeError):
            bjkst.deserialize(1)  # type: ignore

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

    def test_serialize(self) -> None:
        bjkst = BJKST()

        bjkst.add(1)
        assert bjkst.serialize() == (
            b"\x01\x00\x00\x00\x00\x00\x00\x00\x04\x10\x00\x00\x10\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x018\xcb\xac\x11\x98P\x7f\xcf\x00"
        )

        bjkst.add(2)
        assert bjkst.serialize() == (
            b"\x02\x00\x00\x00\x00\x00\x00\x00\x04\x10\x00\x00\x10\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01"
            b"\xb21J\xc2H\xeb\x95~\x00\x00\x018\xcb\xac\x11\x98P\x7f\xcf\x00"
        )

    def test_update(self) -> None:
        bjkst = BJKST()

        with pytest.raises(TypeError):
            bjkst.update([1, b"two", "three", (4, 5)])  # type: ignore

        # Update has failed, the BJKST should still be empty.
        assert len(bjkst) == 0

        bjkst.update([1, b"two", "three"])
        assert len(bjkst) == 3
