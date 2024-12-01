import requests
from PIL import Image, ImageEnhance
import os

def enhance_cover(cover_path,size):
    print(cover_path)
    cover = Image.open(cover_path)
    # 增强画质
    enhancer = ImageEnhance.Sharpness(cover)
    enhanced_cover = enhancer.enhance(2.0)  # 调整参数来增强画质
    # new_size = (1146, 717)  # 设置新的尺寸  哔哩哔哩封面尺寸1146*717
    # new_size = (1080, 1464) # 设置新的尺寸  抖音封面尺寸1080*1464
    # new_size = (864, 516) # 设置新的尺寸  快手封面尺寸864*516
    # new_size = (1920, 1080) # 设置新的尺寸  西瓜视频封面尺寸1080*1920
    new_size = size
    resized_image = enhanced_cover.resize(new_size)
    print('enhance_cover成功')
    return resized_image

def remove_watermark(cover_path):
    cover = Image.open(cover_path)

    # 在这里添加去除水印的代码

    return cover


if __name__ == '__main__':
    img_path = r"D:\desktop\myself\videos\我的世界：变成各种角色生存100天系列"
    img_path=r"D:\desktop\myself\我的世界：变成各种角色生存100天系列"
    # 把img_path下的所有图片调用enhance_cover函数进行处理
    img_path = [os.path.join(img_path, i) for i in os.listdir(img_path) if i.endswith('.webp')]
    index=0
    for i in img_path:
        
        enhanced_img=enhance_cover(i,(1146, 717))
        png_path = f"{i}bili{index}.png"
        enhanced_img.save(png_path, format='PNG')

        enhanced_img=enhance_cover(i,(1080, 1464))
        png_path = f"{i}douyin{index}.png"
        enhanced_img.save(png_path, format='PNG')

        enhanced_img=enhance_cover(i,(1920, 1080))
        png_path = f"{i}xigua{index}.png"
        enhanced_img.save(png_path, format='PNG')
        index+=1

    

