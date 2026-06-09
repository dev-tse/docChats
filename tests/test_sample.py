from src.main import greet


def test_greet():
    assert greet("Alice") == "Hello, Alice!"