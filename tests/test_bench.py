import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from uniq_ch import BJKST


@pytest.fixture(scope="session")
def full_bjkst() -> BJKST:
    return BJKST(range(100_000))


@pytest.mark.benchmark(group="serialize")
def test_serialize(benchmark: BenchmarkFixture, full_bjkst: BJKST) -> None:
    assert len(full_bjkst.serialize()) == 532_899
    benchmark(full_bjkst.serialize)


@pytest.mark.benchmark(group="deserialize")
def test_deserialize(benchmark: BenchmarkFixture, full_bjkst: BJKST) -> None:
    benchmark(BJKST.deserialize, full_bjkst.serialize())
