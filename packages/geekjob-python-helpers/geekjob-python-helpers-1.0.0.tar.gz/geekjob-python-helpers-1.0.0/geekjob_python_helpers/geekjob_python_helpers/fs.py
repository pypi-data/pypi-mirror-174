import os
from magic_config import Config


def _import_(fn: str) -> None:
    """
    Import module from path
    """
    if fn.startswith("_") or not fn.endswith(".py"):
        return None
    fn = fn[:-3].replace("/", ".")
    if Config.DEBUG:
        print("✅  import(" + fn + ")")
    return __import__(fn)


def recursive_import(path: str) -> None:
    """
    Import all modules from path
    """
    for fs_name in os.listdir(path):
        if fs_name.startswith("_"):
            continue
        pathname = f"{path}/{fs_name}"
        if os.path.isdir(pathname):
            recursive_import(pathname)
        else:
            _import_(pathname)
