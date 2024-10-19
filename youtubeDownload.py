import requests
import urllib.parse
from tqdm import tqdm
import time
import os
from PIL import Image, ImageEnhance
from ai import *
# import sys
#
# sys.setrecursionlimit(25)
requests.adapters.DEFAULT_RETRIES = 5


# 解析请求地址
def parse_url(url):
    encoded_url = urllib.parse.quote(url, safe=':/')
    new_url = f"https://y2b.455556.xyz/y2b/parse?{encoded_url}"
    return new_url

# 获取视频相关信息 video_id, video, audio,cover,title
def get_info(url):
    # 发送GET请求
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://y2b.455556.xyz/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
                            'Connection': 'close',
    }
    try:
        r = requests.get(url, headers=headers)
        r_dic = r.json()
    except Exception as e:
        # 处理请求异常
        print("请求异常:", e)


    try:
        if r_dic.get('success', False):
            video_id = r_dic['result']['v']
            # video×audio
            audio = r_dic['result']['best']['audio']['id']
            video = r_dic['result']['best']['video']['id']
            cover=r_dic['result']['thumbnail']
            title=r_dic['result']['title']

            return video_id, video, audio,cover,title
    except Exception as e:
        print("url请求异常，请稍后再试")
        return None

def enhance_cover(cover_path):
    cover = Image.open(cover_path)
    # 增强画质
    enhancer = ImageEnhance.Sharpness(cover)
    enhanced_cover = enhancer.enhance(2.0)  # 调整参数来增强画质
    new_size = (1146, 717)  # 设置新的尺寸  哔哩哔哩封面尺寸1146*717
    resized_image = enhanced_cover.resize(new_size)
    return resized_image

def remove_watermark(cover_path):
    cover = Image.open(cover_path)

    # 在这里添加去除水印的代码

    return cover
def download_cover(cover_url,title):
    # 下载图片
    cover_data = None
    try:
        r = requests.get(url)
        cover_data=r.content
        if cover_data:
            # 保存图片到本地
            save_dir = 'image'
            # 检查文件夹是否存在，若不存在则创建
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            save_path = f'{title}.png'
            save_path = os.path.join(save_dir, save_path)
            with open(save_path, "wb") as file:
                file.write(cover_data)
            # 增强画质
            enhanced_cover = enhance_cover(save_path)
            enhanced_cover.save(f"image/{title}.png")

            # 去除水印
            # watermark_removed_cover = remove_watermark(save_path)
            # watermark_removed_cover.save(f"{title}watermark_removed_cover.png")
    except Exception as e:
        print(f"{title}封面下载失败！抱歉，目前下载封面需要翻墙，暂未找到国内渠道,请翻墙后重试")
        return None

def download_video(video_id,video,audio,title):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://y2b.455556.xyz/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    url = "https://y2b.455556.xyz/"  # 视频文件的基础地址

    file_path1 = f"file/{video_id}/{video}x{audio}/{video_id}.mkv"  # 视频文件路径
    # 发起请求获取文件大小
    response = requests.head(url + file_path1)
    time.sleep(2)
    file_size1 = int(response.headers.get("Content-Length", 0))

    file_path2 = f"file/{video_id}/{video}x{audio}/{video_id}.mp4"  # 视频文件路径
    # 发起请求获取文件大小
    response = requests.head(url + file_path2)
    time.sleep(2)
    file_size2 = int(response.headers.get("Content-Length", 0))
    print(file_size1, file_size2, audio, video, video_id)
    print(url + file_path1)
    print(url + file_path2)
    if file_size1 == 0 and file_size2 == 0:
        print("文件大小为0，重新下载...")
        download_video(video_id, video, audio, title)  # 递归调用download函数
        return None
    if file_size1 > file_size2:
        # 指定保存的文件路径
        file_size = file_size1
        file_path = file_path1
    else:
        file_size = file_size2
        file_path = file_path2
    print(url + file_path)
    # 保存路径
    save_dir = 'video'
    # 检查文件夹是否存在，若不存在则创建
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = f'{title}.mp4'
    save_path = os.path.join(save_dir, save_path)
    with open(save_path, 'wb') as file:
        file.write(requests.get(url + file_path, headers=headers).content)
        print(f'{title}视频已成功下载到本地')


title_lst=[]
content_lst=[]
if __name__=='__main__':
    urls = [
        # "https://www.youtube.com/watch?v=9zw2cJ8juxI",
        # "https://www.youtube.com/watch?v=AqT7ZZznhkA",
        # "https://www.youtube.com/watch?v=c8fMWoofJG0",
        # "https://www.youtube.com/watch?v=jHPqghk5C-c",
        # "https://www.youtube.com/watch?v=uS2Bd_tVHeI",
        # "https://www.youtube.com/watch?v=Dc6A-SJRXjo",
        # "https://www.youtube.com/watch?v=OYAyuESW5xk"


        'https://www.youtube.com/watch?v=8EA_mhKWn7o',
        'https://www.youtube.com/watch?v=AeqEOhgrXLc',
        'https://www.youtube.com/watch?v=EwOoVcO0u7Y',
        'https://www.youtube.com/watch?v=MioVcERdRPA',
        'https://www.youtube.com/watch?v=mzPvlV3SwCo',
        'https://www.youtube.com/watch?v=gw2elb25wPA',
        'https://www.youtube.com/watch?v=eMLHpGKe5_Y',
        'https://www.youtube.com/watch?v=p_9trQkmNrI',

    ]

    for url in urls:
        video_info = get_info(parse_url(url))
        if video_info:
            # AI 润色
            title=aiBytitle(video_info[4])[0]
            content=aiBytitle(video_info[4])[1]
            title_lst.append(title)
            content_lst.append(content)
            download_video(video_info[0],video_info[1],video_info[2],title)
            download_cover(video_info[3],title)
    for i in tuple(zip(title_lst,content_lst)):
        print(i)