import pytest
import pexpect
from pytest import raises

@pytest.fixture
def true_function():
    return True

def test_fixture_returns():
    assert true_function()
