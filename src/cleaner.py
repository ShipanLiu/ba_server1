import glob
import os

class Cleaner:
    
    def __init__(self, config):
        self.config = config
        self.paths = self.extract_paths(self.config["paths"], parent_path='')
        for path in self.paths:
            print(path)
        pass

    def extract_paths(self, dictionary, parent_path=''):
        paths = []
        for value in dictionary.values():
            if isinstance(value, dict):
                paths.extend(self.extract_paths(value, parent_path))
            elif isinstance(value, str):
                paths.append(value)
        return paths
    
    def setup_dirs(self):
        for dir_path in self.paths:
            os.makedirs(dir_path, exist_ok=True)
                                                    
    def clean_dirs(self):
        for dir_path in self.paths:
            files = glob.glob(dir_path)
            for f in files:
                if os.path.isfile(f):
                    os.remove(f)
