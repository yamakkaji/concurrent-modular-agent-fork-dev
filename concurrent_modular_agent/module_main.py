import functools
from .agent import AgentInterface


def module_main(module_name):
    def _module_main(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            agent = AgentInterface('myagent', module_name)
            return f(agent)
        wrapper.__module_main__ = True
        return wrapper
    return _module_main
