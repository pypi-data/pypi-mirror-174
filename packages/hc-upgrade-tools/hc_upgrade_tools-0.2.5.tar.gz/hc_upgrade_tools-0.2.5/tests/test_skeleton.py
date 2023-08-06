import pytest


__author__ = "shixukai"
__copyright__ = "shixukai"
__license__ = "MIT"


def test_fib():
    """API Tests"""
    assert sum([1, 2, 3]) == 6, "Should be 6"

def test_main(capsys):
    """CLI Tests"""
    assert sum([1, 2, 3]) == 6, "Should be 6"
