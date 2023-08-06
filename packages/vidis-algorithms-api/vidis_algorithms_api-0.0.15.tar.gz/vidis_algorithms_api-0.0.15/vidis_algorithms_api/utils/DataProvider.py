from typing import Optional, List, Iterable
import os
import re

import numpy as np


FNAME_CONTAIN_NUMBER_PATTERN = r'(\d+).npy'


def glob_re(pattern: str, filenames: Iterable[str]) -> Iterable[str]:
    return filter(re.compile(pattern).match, filenames)


class DataProvider:
    def __init__(self, mmap_mode: Optional[str] = 'c'):
        self.mmap_mode = mmap_mode

    def get_specter(self, path: str) -> np.ndarray:
        layers = []
        for file_path in glob_re(FNAME_CONTAIN_NUMBER_PATTERN, os.listdir(path)):
            layers.append(
                np.load(file_path, mmap_mode=self.mmap_mode)
            )
        return np.array(layers)
