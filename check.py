# check_api.py
import importlib, traceback
try:
    m = importlib.import_module("src.api")
    print("Imported src.api OK")
    print("Exports:", [n for n in dir(m) if not n.startswith('_')])
except Exception as e:
    print("IMPORT ERROR:", repr(e))
    traceback.print_exc()
