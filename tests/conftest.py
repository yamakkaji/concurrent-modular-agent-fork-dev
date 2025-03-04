from concurrent_modular_agent import backend
import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_before_all_tests():
    assert backend.is_alive(), "Backend is necessary to run tests."
