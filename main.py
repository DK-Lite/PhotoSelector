import os, sys, json
import pandas as pd
import cv2
from skimage.measure import compare_ssim
import numpy as np
import contextlib
import shutil

## load photo -> get path -> 분류 -> dir 별 사진 셀렉터 -> best사진 선정 -> 
class PhotoLoader:
    def __init__(self, dirpath):
        self.dirpath = dirpath
        
    def get_realpath_list(self):
        return self._make_realpath()
    
    def _make_realpath(self):
        paths = os.listdir(self.dirpath)
        return [ f'{self.dirpath}/{path}' for path in paths ]



class PhotoWriter:
    def __init__(self):
        pass

class PhotoSpliter:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


PHOTO_DIR_PATH = 'C:/Users/kdk5g/Desktop/git/PhotoSelector/photo'

def run_cluster(paths: list):
    PhotoCluster(paths)

class FileHandler(contextlib.ContextDecorator):
    def __enter__(sef):
        pass

    def __exit__(self):
        pass


def includes(src: list, target: list) -> bool:
    for value in src:
        if value in target:
            return True
    return False


# 1. load all Photo path 
# 2. load end info path
# 3. split paths
# 4. create dir
# 5. .info setting

class PhotoBoxInfo:
    __data = {}
    def __init__(self):
        self.__data['remote'] = None
        self.__data['path_list'] = None

    @property
    def remote(self) -> str:
        return self.__data['remote']

    @remote.setter
    def remote(self, remote: str):
        self.__data['remote'] = remote

    @property
    def path_list(self) -> list:
        return self.__data['path_list']

    @path_list.setter
    def path_list(self, path_list: list):
        self.__data['path_list'] = path_list

    def load(self, path: str):
        with open(f'{path}/pd.json', 'r') as f:
            self.__data = json.load(f)
    
    def save(self, path: str):
        with open(f'{path}/pd.json', 'w', encoding='utf-8') as mk:
            json.dump(self.__data, mk, indent="\t")

class PhotoBox:
    def __init__(self):
        self._info = PhotoBoxInfo()
    
    def _mkdir(self, path: str):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print ('Error: Creating directory. ' +  path)

    def _mkinfo(self):
        try:
            if not os.path.exists(self.dirpath+'/pb.json'):
               self.save([])
        except OSError:
            print ('Error: Creating file. ' + self.dirpath+'/pb.json')

    def init(self, dirpath: str):
        self.dirpath = dirpath
        self._mkdir(dirpath)
        self._mkinfo()
        self._info.load(dirpath)
            
    def remote(self, store: str):
        self._info.remote = store
    
    def save(self, path_list: list):
        self._info.path_list = path_list
        self._info.save(self.dirpath)

    def pull(self):
        self._mkdir(f'{self.dirpath}/photo')
        for path in self._info.path_list:
            shutil.copy(path, f'{self.dirpath}/photo')
        
        


def main():

    loader = PhotoLoader(dirpath=PHOTO_DIR_PATH)
    photo_path_list = loader.get_realpath_list()

    f = open("./photo_path.txt", 'r')
    endPos = f.read().splitlines()
    f.close()

    endPoint = []
    paths = []
    for path in photo_path_list:
        paths.append(path)
        if(includes(endPos, path)):
            endPoint.append(paths)
            paths = []

    for i, path_list in enumerate(endPoint):
        pb = PhotoBox()
        pb.init(dirpath=f'./collect/photo_{i}')
        pb.remote(store=PHOTO_DIR_PATH)
        pb.save(path_list)
        pb.pull()

if __name__ == "__main__":
    main()