import pytest

from swapigronka.task_one import find_film_idx


dummy_film_list_01 = [
    {
        "film": "title01",
        "character": ["shouldn't", "matter"],
    },
    {
        "film": "title02",
        "character": ["shouldn't", "matter"],
    },
]

empty_film_list = []


@pytest.mark.parametrize(
    "film_list,title,expected",
    [
        (dummy_film_list_01, "title01", 0),
        (dummy_film_list_01, "title02", 1),
        (dummy_film_list_01, "missing", -1),
        (empty_film_list, "missing", -1),
    ])
def test_find_film_idx(film_list, title, expected):
    res = find_film_idx(film_list, title)
    assert res == expected
