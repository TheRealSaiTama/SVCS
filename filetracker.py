import os
import hashlib
import json
from datetime import datetime
from utils import ensure_dir, is_text_file, save_json_file, load_json_file

class FileTracker:
    def __init__(self, path):
        self.path = path
        self.vcs = os.path.join(path, '.svcs')
        self.config = os.path.join(self.vcs, 'config.json')
        self.initialize_vcs()
        
    def initialize_vcs(self):
        if not os.path.exists(self.vcs):
            ensure_dir(self.vcs)
            ensure_dir(os.path.join(self.vcs, 'file_states'))
            ensure_dir(os.path.join(self.vcs, 'versions'))
            
            cfg = {
                'created': datetime.now().isoformat(),
                'tracked_extensions': ['txt', 'py', 'md', 'js', 'html', 'css', 'json', 'xml', 
                                      'csv', 'c', 'cpp', 'h', 'java', 'sh', 'bat', 'ps1',
                                      'yaml', 'yml', 'toml', 'ini', 'cfg']
            }
            save_json_file(self.config, cfg)

    def calculate_hash(self, fpath):
        hasher = hashlib.sha256()
        try:
            with open(fpath, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {fpath}: {str(e)}")
            return None

    def get_file_states(self):
        states = {}
        for root, _, files in os.walk(self.path):
            if '.svcs' in root.split(os.path.sep):
                continue
                
            for f in files:
                fpath = os.path.join(root, f)
                rel = os.path.relpath(fpath, self.path)
                
                if is_text_file(fpath):
                    fhash = self.calculate_hash(fpath)
                    if fhash:
                        states[rel] = {
                            'hash': fhash,
                            'mtime': os.path.getmtime(fpath),
                            'size': os.path.getsize(fpath)
                        }
        return states
    
    def save_file_states(self, states):
        spath = os.path.join(self.vcs, 'file_states', 'current.json')
        save_json_file(spath, states)
    
    def load_last_version_states(self):
        vdir = os.path.join(self.vcs, 'versions')
        if not os.path.exists(vdir):
            return {}
            
        vids = [d for d in os.listdir(vdir) 
                if os.path.isdir(os.path.join(vdir, d))]
        if not vids:
            return {}
            
        vids.sort(reverse=True)
        latest = vids[0]
        
        mpath = os.path.join(vdir, latest, 'manifest.json')
        manifest = load_json_file(mpath)
        if not manifest:
            return {}
            
        states = {}
        for f, info in manifest.get('files', {}).items():
            vpath = os.path.join(vdir, latest, f)
            if os.path.exists(vpath):
                fhash = self.calculate_hash(vpath)
                if fhash:
                    states[f] = {
                        'hash': fhash,
                        'mtime': info.get('mtime', 0),
                        'size': info.get('size', 0)
                    }
                
        return states
    
    def get_status(self):
        current = self.get_file_states()
        last = self.load_last_version_states()
        
        status = {
            'modified': [],
            'added': [],
            'deleted': [],
            'unchanged': []
        }
        
        for f, state in current.items():
            if f in last:
                if state['hash'] != last[f]['hash']:
                    status['modified'].append(f)
                else:
                    status['unchanged'].append(f)
            else:
                status['added'].append(f)
                
        for f in last:
            if f not in current:
                status['deleted'].append(f)
                
        return status