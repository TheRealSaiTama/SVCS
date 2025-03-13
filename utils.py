import os
import time
import json
from datetime import datetime

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def format_timestamp(ts):
    if isinstance(ts, str):
        try:
            dt = datetime.fromisoformat(ts)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return ts
    elif isinstance(ts, (int, float)):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
    return str(ts)

def load_json_file(path, default=None):
    if default is None:
        default = {}
    
    if not os.path.exists(path):
        return default
        
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Could not parse JSON in {path}")
        return default
    except Exception as e:
        print(f"Warning: Error reading {path}: {str(e)}")
        return default

def save_json_file(path, data):
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving to {path}: {str(e)}")
        return False

def get_file_extension(path):
    _, ext = os.path.splitext(path)
    return ext.lower()[1:] if ext else ""

def is_text_file(path):
    text_exts = {
        'txt', 'py', 'md', 'js', 'html', 'css', 'json', 'xml', 
        'csv', 'c', 'cpp', 'h', 'java', 'sh', 'bat', 'ps1',
        'yaml', 'yml', 'toml', 'ini', 'cfg'
    }
    return get_file_extension(path) in text_exts

def get_relative_path(path, base):
    return os.path.relpath(path, base)
    
def human_readable_size(bytes):
    if bytes < 1024:
        return f"{bytes} B"
    
    for unit in ['KB', 'MB', 'GB', 'TB']:
        bytes /= 1024.0
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
            
    return f"{bytes:.2f} PB"