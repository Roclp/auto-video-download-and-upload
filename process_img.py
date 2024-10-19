import requests
import urllib.parse
from tqdm import tqdm
import time
import os
from PIL import Image, ImageEnhance


def enhance_cover(cover_path):
    cover = Image.open(cover_path)
    # 增强画质
    enhancer = ImageEnhance.Sharpness(cover)
    enhanced_cover = enhancer.enhance(2.0)  # 调整参数来增强画质
    new_size = (1146, 717)  # 设置新的尺寸  哔哩哔哩封面尺寸1146*717
    resized_image = enhanced_cover.resize(new_size)
    return resized_image

enhanced_cover = enhance_cover('eMLHpGKe5_Y-SD.jpg')
enhanced_cover.save("image/f.png")
