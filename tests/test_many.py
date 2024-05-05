from types import GeneratorType
from typing import Any, Callable, Generator, cast

import pytest

from pypeline.many import Many


@pytest.fixture
def finite_generator(start: int = -100, size: int = 200):
    def _finite_generator():
        for i in range(size):
            yield start + i

    return _finite_generator


@pytest.fixture
def int_list():
    return list(range(-100, 100))


def test_unwrap(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    assert isinstance(Many(finite_generator()).unwrap(), GeneratorType)
    assert isinstance(Many(int_list).unwrap(), list)


def test_map(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).map(lambda i: i + 1).unwrap()
    assert min(r) == -99
    assert max(r) == 100

    r = Many(int_list).map(lambda i: i + 1).unwrap()
    assert min(r) == -99
    assert max(r) == 100


def test_map_lazy(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).map_lazy(lambda i: i + 1).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert min(r) == -99
    assert max(r) == 100

    r = Many(int_list).map_lazy(lambda i: i + 1).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert min(r) == -99
    assert max(r) == 100


def test_skip(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).skip(100).unwrap()
    assert len(cast(list[int], r)) == 100

    r = Many(int_list).skip(100).unwrap()
    assert len(cast(list[int], r)) == 100


def test_skip_lazy(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).skip_lazy(100).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert len(r) == 100

    r = Many(int_list).skip_lazy(100).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert len(r) == 100


def test_skip_raises_error():
    with pytest.raises(ValueError):
        Many([1, 2, 3]).skip(-1)


def test_skip_lazy_raises_error():
    with pytest.raises(ValueError):
        Many([1, 2, 3]).skip_lazy(-1)


def test_take(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).take(100).unwrap()
    assert len(cast(list[int], r)) == 100

    r = Many(int_list).take(100).unwrap()
    assert len(cast(list[int], r)) == 100


def test_take_lazy(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).take_lazy(100).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert len(r) == 100

    r = Many(int_list).take_lazy(100).unwrap()
    assert isinstance(r, GeneratorType)
    r = [_r for _r in r]
    assert len(r) == 100


def test_take_raises_error():
    with pytest.raises(ValueError):
        Many([1, 2, 3]).take(-1)


def test_take_lazy_raises_error():
    with pytest.raises(ValueError):
        Many([1, 2, 3]).take_lazy(-1)


def test_filter(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).filter(lambda x: x < 0).unwrap()
    assert isinstance(r, list)
    assert all([x < 0 for x in r])

    r = Many(int_list).filter(lambda x: x < 0).unwrap()
    assert isinstance(r, list)
    assert all([x < 0 for x in r])


def test_filter_lazy(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).filter_lazy(lambda x: x < 0).unwrap()
    assert isinstance(r, GeneratorType)
    assert all([x < 0 for x in r])

    r = Many(int_list).filter_lazy(lambda x: x < 0).unwrap()
    assert isinstance(r, GeneratorType)
    assert all([x < 0 for x in r])


def test_reduce(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).reduce(lambda acc, nxt: acc + nxt)
    assert isinstance(r, int)
    assert r == sum(finite_generator())

    r = Many(int_list).reduce(lambda acc, nxt: acc + nxt)
    assert isinstance(r, int)
    assert r == sum(int_list)


def test_reduce_to(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    r = Many(finite_generator()).reduce_to(
        lambda acc, nxt: acc + nxt, -sum(finite_generator())
    )
    assert isinstance(r, int)
    assert r == 0

    r = Many(int_list).reduce_to(lambda acc, nxt: acc + nxt, -sum(int_list))
    assert isinstance(r, int)
    assert r == 0


def test_compute(
    finite_generator: Callable[[], Generator[int, Any, None]],
    int_list: list[int],
):
    assert isinstance(Many(finite_generator()).compute().unwrap(), list)
    assert isinstance(Many(int_list).compute().unwrap(), list)