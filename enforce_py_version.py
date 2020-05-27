import sys

def enforce_py_version():
    if not sys.version_info >= (3,8,0):
        raise EnvironmentError("Use Python 3.8.0 or higher")
