import sys
import importlib.util



def find_module_main_function(script_path):
    spec = importlib.util.spec_from_file_location("module.name", script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = module
    spec.loader.exec_module(module)
    for name, func in module.__dict__.items():
        if callable(func) and getattr(func, "__module_main__", False):
            return func
    return None


if __name__ == "__main__":
    script_path = sys.argv[1]
    func = find_module_main_function(script_path)
    if func is None:
        print("No module main function found")
        sys.exit(1)
    func()