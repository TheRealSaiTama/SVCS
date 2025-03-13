import os
import shutil
import json
from datetime import datetime
from utils import ensure_dir, save_json_file, load_json_file

class VersionManager:
    def __init__(self, path):
        self.path = path
        self.vcs = os.path.join(path, '.svcs')
        self.versions = os.path.join(self.vcs, 'versions')
        ensure_dir(self.versions)
        
    def create_version(self, msg):
        vid = datetime.now().strftime('%Y%m%d%H%M%S')
        vdir = os.path.join(self.versions, vid)
        ensure_dir(vdir)
        
        manifest = {
            'id': vid,
            'timestamp': datetime.now().isoformat(),
            'message': msg,
            'files': {}
        }
        
        for root, _, files in os.walk(self.path):
            if '.svcs' in root.split(os.path.sep):
                continue
                
            for f in files:
                try:
                    src = os.path.join(root, f)
                    rel = os.path.relpath(src, self.path)
                    dst = os.path.join(vdir, rel)
                    
                    ensure_dir(os.path.dirname(dst))
                    shutil.copy2(src, dst)
                    
                    manifest['files'][rel] = {
                        'size': os.path.getsize(src),
                        'mtime': os.path.getmtime(src),
                        'mode': os.stat(src).st_mode
                    }
                except Exception as e:
                    print(f"Warning: Could not copy file {rel}: {str(e)}")
        
        mpath = os.path.join(vdir, 'manifest.json')
        save_json_file(mpath, manifest)
            
        return vid
    
    def get_versions(self):
        vers = []
        
        if not os.path.exists(self.versions):
            return vers
        
        for vid in os.listdir(self.versions):
            vdir = os.path.join(self.versions, vid)
            if os.path.isdir(vdir):
                mpath = os.path.join(vdir, 'manifest.json')
                manifest = load_json_file(mpath)
                if manifest:
                    vers.append(manifest)
        
        return sorted(vers, key=lambda v: v['timestamp'])
    
    def get_version(self, vid):
        mpath = os.path.join(self.versions, vid, 'manifest.json')
        return load_json_file(mpath)
    
    def checkout_version(self, vid):
        vdir = os.path.join(self.versions, vid)
        if not os.path.exists(vdir):
            raise ValueError(f"Version {vid} does not exist")
        
        manifest = load_json_file(os.path.join(vdir, 'manifest.json'))
        if not manifest:
            raise ValueError(f"Invalid manifest for version {vid}")
        
        for rel, info in manifest['files'].items():
            try:
                src = os.path.join(vdir, rel)
                dst = os.path.join(self.path, rel)
                
                if not os.path.exists(src):
                    print(f"Warning: File {rel} not found in version {vid}")
                    continue
                
                ensure_dir(os.path.dirname(dst))
                shutil.copy2(src, dst)
                
                try:
                    os.chmod(dst, info['mode'])
                except:
                    pass
            except Exception as e:
                print(f"Error restoring {rel}: {str(e)}")
        
        return manifest
    
    def compare_versions(self, v1id, v2id):
        v1 = self.get_version(v1id)
        v2 = self.get_version(v2id)
        
        if not v1 or not v2:
            raise ValueError("One or both versions do not exist")
        
        changes = {
            'added': [],
            'removed': [],
            'modified': []
        }
        
        for f in v2['files']:
            if f not in v1['files']:
                changes['added'].append(f)
            elif v1['files'][f]['size'] != v2['files'][f]['size'] or \
                 v1['files'][f]['mtime'] != v2['files'][f]['mtime']:
                changes['modified'].append(f)
        
        for f in v1['files']:
            if f not in v2['files']:
                changes['removed'].append(f)
        
        return changes