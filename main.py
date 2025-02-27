from Uploaders.DouyinUpload import DouYinVideo
from Uploaders.KuaishouUpload import KuaiShouVideo
from Uploaders.XiguaUpload import XiGuaVideo
from Utils.split_video import split_video_ffmpeg
from Utils.get_schedule_time import generate_schedule_within_7_days

from Utils.process_cover import enhance_cover
from multiprocessing import Process, cpu_count, Pool

import asyncio
import yaml
import os
import time
from datetime import datetime

def getFileNames(file_path):
    videoFile = []
    files = os.listdir(file_path)
    files = sorted(files,  key=lambda x: os.path.getctime(os.path.join(file_path, x)))
    for i in range(len(files)):
        if (files[i][-4:] == "webm" or files[i][-4:] == ".mkv" or files[i][-4:] == ".mp4"):
            videoFile.append(files[i])
    return videoFile

'''
    定时发布：
        抖音：2小时后及14天内
        快手：1h～7天 内
        西瓜：2h～7天 内
'''

if __name__ == '__main__':
    

    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    fullpath = config['path']+config['dir']
    douyin_cookie = config['douyin_cookie']
    kuaishou_cookie = config['kuaishou_cookie']
    xigua_cookie = config['xigua_cookie']
    
    time_list_str = config['time_list']
    time_list = [int(t.strip()) for t in time_list_str.split(',')]
    print(time_list)
    time_list=generate_schedule_within_7_days(*time_list)
    
    index=0
    print(fullpath)
    
    # p=Pool(3)

    videoFile = getFileNames(fullpath)
    for video in videoFile:

        # 视频文件完整路径
        file_path = os.path.join(fullpath, video)
        file_name = video.split('.',1)[0]


        # 创建临时文件夹
        temp_dir=os.path.join(fullpath, file_name)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
            split_video_ffmpeg(file_path, temp_dir)
        
        fenduan_video_list=getFileNames(temp_dir)
        print(fenduan_video_list)


        old_cover_path=os.path.join(fullpath, f'{file_name}.webp')

        douyin_cover_size=(1080, 1464)
        douyin_cover_path=os.path.join(temp_dir, f'{file_name}douyin.png')
        enhance_cover(old_cover_path, douyin_cover_size).save(douyin_cover_path, format='PNG')

        # 快手使用抖音封面
        kuaishou_cover_size=(864, 516)
        kuaishou_cover_path=os.path.join(temp_dir, f'{file_name}kuaishou.png')
        enhance_cover(old_cover_path, kuaishou_cover_size).save(kuaishou_cover_path, format='PNG')

        xigua_cover_size=(1920, 1080) 
        xigua_cover_path=os.path.join(temp_dir, f'{file_name}xigua.png')
        enhance_cover(old_cover_path, xigua_cover_size).save(xigua_cover_path, format='PNG')


        for i in fenduan_video_list:

            time=time_list[index]
            
            # print(i)
            temp_path = os.path.join(temp_dir, i)
            
            title=i[0:-4] # 去掉后缀.mp4
            file=temp_path
            kuaishou_tags=["我的世界","MC不灭","100天"]
            douyin_tags=["我的世界","MC不灭","游戏内容风向标"]
            xigua_tags=["我的世界","MC不灭","100天"]
            print(file, title)

            
            
            # 修改为使用多进程上传
            #   1. 上传到抖音   2. 上传到快手   3. 上传到西瓜视频
            # # p.apply_async(DouYinVideo, args=(title, file, douyin_cover_path,tags, 0, douyin_cookie))
            # # p.apply_async(KuaiShouVideo, args=(title, file, kuaishou_cover_path,tags, 0, kuaishou_cookie))
            # # p.apply_async(XiGuaVideo, args=(title, file, xigua_cover_path,tags, 0, xigua_cookie))
            

            app = DouYinVideo(title, file, douyin_cover_path,douyin_tags, time, douyin_cookie)
            asyncio.run(app.main(), debug=False)

            # 快手使用抖音封面
            app = KuaiShouVideo(title, file, douyin_cover_path,kuaishou_tags, time, kuaishou_cookie)
            asyncio.run(app.main(), debug=False)

            
            # app = XiGuaVideo(title, file, xigua_cover_path,xigua_tags, 0, xigua_cookie)
            # asyncio.run(app.main(), debug=False)
            
            index+=1

            # # app = DouYinVideo(title, file, tags, 0, douyin_cookie)
            # # app = KuaiShouVideo(title, file, tags, 0, kuaishou_cookie)
            # # app = XiGuaVideo(title, file, tags, 0, xigua_cookie)
            # # asyncio.run(app.main(), debug=False)
            # asyncio.run(upload_videos(title, file, tags, 0, cookies), debug=False)


