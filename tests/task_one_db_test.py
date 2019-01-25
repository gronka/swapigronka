import pytest

from swapigronka.task_one import reset_tables
from swapigronka.task_one import get_db


@pytest.fixture(autouse=True)
def mock_mysql_connector(monkeypatch):
    def mock_get_db(*args, **kargs):
        return MockDb()
    monkeypatch.setattr("swapigronka.task_one.get_db", mock_get_db)


class MockDb:
    def cursor():
        return MockCursor()


class MockCursor:
    def execute(*args, **kargs):
        pass


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

def test_reset_tables():
    """This test passing indicates that mocking is working well."""
    reset_tables(ctx)
