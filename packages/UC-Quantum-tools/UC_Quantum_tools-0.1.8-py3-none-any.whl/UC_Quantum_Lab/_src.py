from . import _config_dir, _trigger_file
import os

"""
Creates a file that triggers the vscode extension

"""
def _trigger():
    global _config_dir, _trigger_file
    
    if _config_dir in os.listdir():
        with open(os.path.join(_config_dir, _trigger_file), 'w'): pass


"""
prepends inputted path with the config directory if it exists

"""
def _get_path(path:str):
    global _config_dir
    if _config_dir in os.listdir(): 
        if os.path.isdir(_config_dir): return os.path.join(_config_dir, path)
    else: return path


