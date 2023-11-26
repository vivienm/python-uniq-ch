import pytest
from pytest_benchmark.fixture import BenchmarkFixture
from uniq_ch import BJKST


@pytest.fixture(scope="session")
def bjkst_12b() -> BJKST:
    return BJKST(range(100_000), precision=12)


@pytest.fixture(scope="session")
def bjkst_16b() -> BJKST:
    return BJKST(range(100_000), precision=16)


@pytest.mark.benchmark(group="serialize")
def test_serialize_12b(benchmark: BenchmarkFixture, bjkst_12b: BJKST) -> None:
    assert len(bjkst_12b.serialize()) == 33_476
    benchmark(bjkst_12b.serialize)


@pytest.mark.benchmark(group="serialize")
def test_serialize_16b(benchmark: BenchmarkFixture, bjkst_16b: BJKST) -> None:
    assert len(bjkst_16b.serialize()) == 532_900
    benchmark(bjkst_16b.serialize)


@pytest.mark.benchmark(group="deserialize")
def test_deserialize_12b(benchmark: BenchmarkFixture, bjkst_12b: BJKST) -> None:
    benchmark(BJKST.deserialize, bjkst_12b.serialize())


@pytest.mark.benchmark(group="deserialize")
def test_deserialize_16b(benchmark: BenchmarkFixture, bjkst_16b: BJKST) -> None:
    benchmark(BJKST.deserialize, bjkst_16b.serialize())
