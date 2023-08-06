from typing import List, Callable, Dict
from datetime import datetime
from pathlib import Path, PosixPath
import importlib.util
from . import ActionStore
from .http import serve
from sys import argv, exit
from os import environ

def get_funcs_from_file(file: PosixPath) -> List[Callable]:
    if not file.is_file():
        raise AssertionError(f"File {file} does not exist")
    try:
        parents = str(file.parent)
        filename = file.name
        # print(f"Loading action store {filename} from {parents}")
        spec = importlib.util.spec_from_file_location(parents, file.absolute())
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        ret = list()
        for o in dir(module):
            if o.startswith("_"):
                continue
            try:
                func = getattr(module, o)
                if not callable(func):
                    continue
                ActionStore.validate_action(func)
                ret.append(func)
            except Exception as ex:
                print("Error loading action: "+module.__name__ + "."+ o, ex)
                pass
        return ret

    except Exception as e:
        print(f"Error loading actions store file: {e}")
        pass

def get_all_dir_funcs(dirpath: PosixPath) -> Dict[str, List[Callable]]:
    dirpath = Path(dirpath)
    if not dirpath.exists():
        raise AssertionError(f"Directory {dirpath} does not exist")
    ret = dict()
    for path in dirpath.glob("**/*.py"):
        funcs = get_funcs_from_file(path)
        if funcs:
            ret[path.stem] = funcs
    return ret

def create_actionstore_from_dir(dirpath: PosixPath, actionstore_name, actionstore_version: str) -> ActionStore:
    if not dirpath.exists() or not dirpath.is_dir():
        raise AssertionError(f"Directory {dirpath} does not exist")
    
    actionstore = ActionStore(actionstore_name, actionstore_version)
    dirfuncs = get_all_dir_funcs(dirpath)
    if not dirfuncs:
        raise AssertionError(f"No actions found in {dirpath}")
    for file, funcs in dirfuncs.items():
        for func in funcs:
            try:
                actionname = func.__name__ if len(dirfuncs) == 1 else f"{file}.{func.__name__}"
                actionstore.register_action(actionname, func)
            except Exception as e:
                print(f"Error registering action {file}.{func.__name__}: {e}")
                pass


    return actionstore

def load_dir_as_actionstore(dirname):
    dirpath = Path(dirname)
    actionstore_name = environ.get("ACTIONSTORE_NAME", dirpath.stem)
    actionstore_version = environ.get("ACTIONSTORE_VERSION", "bundled at: " + str(datetime.now()))
    actionstore = create_actionstore_from_dir(dirpath, actionstore_name, actionstore_version)
    if environ.get("ACTIONSTORE_SECRETS",""):
        actionstore.uses_secrets(environ.get("ACTIONSTORE_SECRETS").split(","))            
    return actionstore

if __name__ == "__main__":    
    if len(argv) != 2:
        print("Usage: python3 -m kubiya.bundle <dirname>")
        exit(1)
    
    actionstore = load_dir_as_actionstore(argv[1])
    serve(actionstore)