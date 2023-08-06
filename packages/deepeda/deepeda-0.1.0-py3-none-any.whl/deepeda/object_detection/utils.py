from typing import List
from PIL import Image
import numpy as np
import collections


def aspect_ratio_distribution(images: List[str]):
    ratios = []
    for img in images:
        img = np.array(Image.open(img))
        h, w = img.shape[:2]
        ratios.append(h / w)
    counts, bins = np.histogram(ratios)
    return {b: c for b, c in zip(bins, counts)}

