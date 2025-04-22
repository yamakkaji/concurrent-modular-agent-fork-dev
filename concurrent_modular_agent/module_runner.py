import sys
import importlib.util

from .cli import find_module_main_function

if __name__ == "__main__":
    script_path = sys.argv[1]
    func = find_module_main_function(script_path)
    if func is None:
        print("No module main function found")
        sys.exit(1)
    func()