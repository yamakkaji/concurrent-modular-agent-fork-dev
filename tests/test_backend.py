from concurrent_modular_agent import backend


def test_server():
    backend.start(test_env=True)
    assert backend.is_alive(test_env=True)
    backend.stop(test_env=True)
    assert not backend.is_alive(test_env=True)

