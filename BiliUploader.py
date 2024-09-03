import json
import os
import time

import yaml

# from script.biliup_tool import BiliBili, Data
from biliup.plugins.bili_webup import BiliBili, Data

from process_cover import enhance_cover

from dTime import get_random_time_diff


def getFileNames(file_path):
    videoFile = []
    files = os.listdir(file_path)
    files = sorted(files,  key=lambda x: os.path.getctime(os.path.join(file_path, x)))
    for i in range(len(files)):
        if (files[i][-4:] == "webm" or files[i][-4:] == ".mkv" or files[i][-4:] == ".mp4"):
            videoFile.append(files[i])
    return videoFile

if __name__ == '__main__':
    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    fullpath = config['path']+config['dir']
    print(fullpath)
    videoFile = getFileNames(fullpath)
    # biliname = config['biliname']
    tid = config['tid']

    # listpath = fullpath+r'\\'+videoFile[0][:-4]+'.info.json'
    # with open(listpath, 'r', encoding='utf-8') as flistinfo:
    #     listdictinfo = json.load(flistinfo)
    #     listtitle = listdictinfo['title']
    #     listdesp = listdictinfo['description']
    #     listurl = listdictinfo['webpage_url']
    #     # uploader = listdictinfo['uploader_id']
    #     # uploaderdate = listdictinfo['modified_date']
    #     tegs = listdictinfo['tags']
    #     print(listtitle,listdesp,listurl,tegs)
    # flistinfo.close()
    # print('开始上传：'+config['dir'],fullpath,videoFile,tid,biliname,listpath)

    for file in videoFile:
        filename = file.split('.',1)[0]
        filepath = os.path.join(fullpath, file)
        srtpath = os.path.join(fullpath, filename + '.srt')
        srtpathzh = os.path.join(fullpath, filename + '-zh.srt')
        infopath = os.path.join(fullpath, filename + '.info.json')
        # print(filename,filepath,srtpath,srtpathzh,infopath)
        
        with open(infopath, 'r', encoding='utf-8') as f1:
            info_data = json.load(f1)
            f1.close()
            title = info_data['title']
            # title = config['prefix'] + title
            if len(title)>80:
                title = title[:80]
            # thumbnail = info_data['thumbnail']
            # print(thumbnail) 封面链接url
            # desp = info_data["description"]
            # uploader = info_data["uploader"]
            # uploaderdate = info_data["upload_date"]
            # desp0 = '作者：'+uploader+'\n发布时间：'+uploaderdate+'\n搬运：'+biliname+'\n原简介：'+desp
            # tags = info_data["tags"]
            
                
            desp0=title
            tags=[]
            MC_tags=["我的世界","我的世界MC","MC不灭","生存100天","沙盒游戏","像素风","游戏解说","实况解说","沙雕","搞笑"]
            # MC_tags=["我的世界","我的世界MC","生物的秘密传说系列","沙盒游戏","像素风","游戏解说","实况解说","沙雕","搞笑"]
            # MC_tags=["#推荐宝藏游戏","我的世界","我的世界MC","MC的发展历史系列","沙盒游戏","像素风","游戏解说","实况解说","沙雕","搞笑"]
            # MC_tags=["我的世界","我的世界MC","大佬挑战记录系列","沙盒游戏","像素风","游戏解说","实况解说","沙雕","搞笑"]

            tags=MC_tags
            
            # webpage_url = info_data['webpage_url']
        video = Data()
        video.title = title # title
        video.desc = title  # 简介
        
        
        # cover = os.path.join(fullpath, filename + '.webp')    # cover
        cover_path=os.path.join(fullpath, filename + '.webp')
        if os.path.exists(cover_path):
            cover=enhance_cover(cover_path,(1146, 717))
            cover_path=os.path.join(fullpath, filename + '.png')
            cover.save(cover_path)
            cover=cover_path
        else:
            cover_path=os.path.join(fullpath, filename + '.jpg')
            if os.path.exists(cover_path):
                cover=enhance_cover(cover_path,(1146, 717))
                cover_path=os.path.join(fullpath, filename + '.png')
                cover.save(cover_path)
                cover=cover_path
            else:
                print(f"{cover_path}路径错误")
        



        # video.source = webpage_url     #'添加转载地址说明'
        # video.tid = tid # 设置视频分区,默认为122 野生技能协会
        video.tid = 17 # 单机游戏分区 17    

        video.set_tag(tags) # 设置标签
        # video.dynamic = '动态内容'
        lines = 'cs-bda2' #auto
        tasks = 3
        
        # 延后时间，单位秒
        dtime = get_random_time_diff(15, 16, 19)

        # dtime=0

        print(f"延迟发布时间：{dtime}")
        video.delay_time(dtime) # 设置延后发布（2小时~15天）
        video.no_reprint = 1 # 禁止转载
        video.open_elec = 1 # 开启充电
        
        
        
        sessdata = ''
        bili_jct = ''
        dedeuserid_ckmd5 = ''
        dedeuserid = ''
        access_token = ''

        with open('bilibili.json', 'r') as f:
            cookie_contents = json.loads(f.read())
        f.close()
        

        with BiliBili(video) as bili:
            print(cover)
            # bili.login("bili.cookie", login_access)
            bili.login_by_cookies({
            "buvid3": "69832727-7D37-3079-491C-D7A199E5F82195977infoc",
            "b_nut": "1714643595",
            "_uuid": "11017534E-8BF7-6B7E-2499-8D1D4910F6721095318infoc",
            # "rpdid": "0z9Zw2XGud|vDuqhiq2|28h|3w1PzVaG",
            "buvid4": "63445531-C357-1477-133E-AF50253C4A7D97327-024050209-xt0mcWQ1yT4XHldUO637EpS4EGFhS0H3xGd859ek6J5Yd3rEhabtWYy%2BE3%2Bh1eOi",
            "i-wanna-go-back": "-1",
            "header_theme_version": "CLOSE",
            "DedeUserID": "1533519019",
            "DedeUserID__ckMd5": "e3788eddcf6dcaf6",
            "b_ut": "5",
            "nostalgia_conf": "-1",
            "CURRENT_PID": "b46592e0-cd65-11ed-b997-652e8d723e28",
            "hit-new-style-dyn": "0",
            "hit-dyn-v2": "1",
            "FEED_LIVE_VERSION": "V8",
            "buvid_fp_plain": "undefined",
            "CURRENT_BLACKGAP": "0",
            "CURRENT_FNVAL": "4048",
            "LIVE_BUVID": "AUTO7316894305456997",
            "enable_web_push": "DISABLE",
            "CURRENT_QUALITY": "0",
            "fingerprint": "ca8b927273abfbf032b850b0587cc748",
            "bili_ticket": "eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTgyMTYzNjYsImlhdCI6MTY5Nzk1NzEwNiwicGx0IjotMX0.tRqoeTyw0IH_3Nm5QJoyPWfWOlvSB6wJaex5OAVl_0Y",
            "bili_ticket_expires": "1698216306",
            "buvid_fp": "436aa2d056ff6b87ec93131660e46a76",
            "PVID": "1",
            "innersign": "0",
            "b_lsid": "89D7E1037_18F38B8F01A",
            "bsource": "search_bing",
            "bp_video_offset_1533519019": "855905502285004834",
            "SESSDATA": "bec78a2b%2C1730195622%2C91145%2A52CjDWv5U9Mq84-R46vXF2NCWhAk7Cl1sUcnYOSX1GJ6y4zlgRwbgU2JheekPPGJCODy8SVm9naGVqS2RDb3hLazBKN0Q1S3pXcEhhajZKRFZyUE9DYXM5cGxIcm1lZEdtM0tyZFgxczZzLTkwR2JlTnoxUlhiZ0FRM0lJUFZibWI2OTBYam5QZXpBIIEC",
            "bili_jct": "166253fd50cf9c115bec605615a1ecf4",
            "sid": "7ti7ta60",
            "home_feed_column": "4",
            "browser_resolution": "802-707"
        })
            # bili.login_by_password("username", "password")
            # video_part = bili.upload_file(filepath, lines=lines, tasks=tasks)  # 上传视频，默认线路AUTO自动选择，线程数量3。

            video_part = bili.upload_file(filepath=filepath)
            video.append(video_part)  # 添加已经上传的视频
            video.videos[0]['title'] = video.title
            video.copyright=1 # 表示视频的版权类型。默认为 2，可能是某种特定的版权类型标识。



            video.delay_time(dtime) # 设置延后发布（2小时~15天）








            video.cover = bili.cover_up(cover).replace('http:', '')
            # ret = bili.submit()  # 提交视频
            # ret = bili.submit_client()  # 提交视频
            ret = bili.submit(submit_api='web')  # 提交视频
        time.sleep(10)
        print('上传成功：'+title)

    

        