import difflib
import os

class DiffEngine:
    @staticmethod
    def file_diff(f1, f2):
        with open(f1, 'r') as a, open(f2, 'r') as b:
            diff = difflib.unified_diff(
                a.readlines(),
                b.readlines(),
                fromfile=f1,
                tofile=f2,
                lineterm=''
            )
        return '\n'.join(diff)

    @staticmethod
    def repo_diff(v1path, v2path):
        diffs = {}
        
        files1 = DiffEngine._get_all_files(v1path)
        files2 = DiffEngine._get_all_files(v2path)
        
        allfiles = set(files1) | set(files2)
        
        for fpath in allfiles:
            f1 = os.path.join(v1path, fpath)
            f2 = os.path.join(v2path, fpath)
            
            if os.path.exists(f1) and os.path.exists(f2):
                try:
                    diff = DiffEngine.file_diff(f1, f2)
                    if diff:
                        diffs[fpath] = diff
                except Exception as e:
                    diffs[fpath] = f"Error comparing files: {str(e)}"
            
            elif os.path.exists(f1):
                diffs[fpath] = f"File {fpath} was deleted"
            
            else:
                diffs[fpath] = f"File {fpath} was added"
                
        return diffs
    
    @staticmethod
    def _get_all_files(path):
        files = []
        for root, _, fs in os.walk(path):
            for f in fs:
                fpath = os.path.join(root, f)
                rel = os.path.relpath(fpath, path)
                files.append(rel)
        return files