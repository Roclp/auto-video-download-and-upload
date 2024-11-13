import yaml
import yt_dlp


# path = config['path']
# proxy = config['proxy']
path='videos/'

URLS = [
    # "https://www.youtube.com/playlist?list=PLsFouWTyKWsq6XkYDG43VvTNrFnf8dRaX",
    # "https://www.youtube.com/playlist?list=PLsFouWTyKWspy8pd4eB8jl7RgtwSNZ2dF",
    # "https://www.youtube.com/playlist?list=PLsFouWTyKWspXt22JSR4AvLedBe1mSmr7",
    # "https://www.youtube.com/playlist?list=PLsFouWTyKWsqJGbY3623pWfX-qfonOLbe",
    # "https://www.youtube.com/playlist?list=PLsFouWTyKWsoWT4kjS02joxegm1TFRhYe",
    # "https://www.youtube.com/playlist?list=PLsFouWTyKWsrDvsL6M6qHcLgLuW6H73oj",
    # "https://www.youtube.com/playlist?list=PLsFouWTyKWsoRhPJwNswXIGDkD9pDQw-w",
    # "https://www.youtube.com/watch?v=oxGBjEpkTc4",
    "https://www.youtube.com/playlist?list=PLsFouWTyKWsraAiYu4skJPRTlBq2Fz24F",
    # "https://www.youtube.com/playlist?list=PLsFouWTyKWsqaG0L9EhYmGHRE6uzoqoAL"
]
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'download_archive': 'videos.txt',
    'extract_flat': 'discard_in_playlist',
    'fragment_retries': 10,
    'ignoreerrors': 'only_download',
    'outtmpl': {'default': path + '%(playlist_title)s/%(title)s.%(ext)s'},
    # 'outtmpl': {'default': '%(playlist_title)s/%(title)s.%(ext)s'},
    'merge_output_format': 'mp4',  # 添加这一行以指定合并输出格式为MP4
    'postprocessors': [
    {
        'key': 'FFmpegConcat',
        'only_multi_video': True,
        'when': 'playlist',
    },
    ],
    'retries': 10,
    'writeautomaticsub': True,
    'writeinfojson': True,
    'writethumbnail': 'maxresdefault',


    'concurrent-fragments': 16, # 并发帧
    'http-chunk-size': '10M' , # 分片大小
}


with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)


#  yt-dlp https://www.youtube.com/watch?v=5H-APkk_fUE --external-downloader aria2c --external-downloader-args "-x 16 -k 1M"


# 大神Dream系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsq6XkYDG43VvTNrFnf8dRaX
# 有趣的生存通关系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsqaG0L9EhYmGHRE6uzoqoAL
# MC的发展系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWspy8pd4eB8jl7RgtwSNZ2dF
# 揭秘逃离监狱系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsoE1eq23Wx18olrV832hL8h
# 大佬挑战记录系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWspXt22JSR4AvLedBe1mSmr7
# 猎杀10000个村民系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsqSAJBPbVfgGbXERtjy6EaF
# 生物的秘密传说系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsqJGbY3623pWfX-qfonOLbe
# 丧尸惊变生存100天系列    没有记录？
# https://www.youtube.com/playlist?list=PLsFouWTyKWspEY4Sdk2LLOYcvLNkv806v
# 变成各种角色生存100天系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsraAiYu4skJPRTlBq2Fz24F
# 生物改造系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsoWT4kjS02joxegm1TFRhYe
# 怪物竞技场系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsrDvsL6M6qHcLgLuW6H73oj
# 猎人复仇系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsr8S5rgd164f0afOZ7CChHT
# 冷知识系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWso-zJh4zwhv6EONEPdupfNF
# 村民杀手Grox系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsoRhPJwNswXIGDkD9pDQw-w
# 大型社会模拟实验系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsr2p9T741L05LcNzXV3SHI9
# 肝帝系列
# https://www.youtube.com/playlist?list=PLsFouWTyKWsopxd843IvzhKocA2KKCdkB


# # yt-dlp --external-downloader "aria2c" --external-downloader-args "aria2c:-x 16 -k 1M" -f "bestvideo+bestaudio/best" --download-archive "videos.txt" --fragment-retries 10 --output "videos/%(playlist_title)s/%(title)s.%(ext)s" --merge-output-format "mp4" --retries 10 --write-info-json --write-thumbnail --http-chunk-size 10485760 --cookies "cookies.txt" https://www.youtube.com/playlist?list=PLsFouWTyKWsraAiYu4skJPRTlBq2Fz24F
# --downloader aria2c --downloader-args 'aria2c:--continue --max-concurrent-downloads=30 --max-connection-per-server=16 --split=30 --min-split-size=1M'
# --async-dns=false

# yt-dlp -f "bestvideo+bestaudio/best" --download-archive "videos.txt" --fragment-retries 10 --output "videos/%(playlist_title)s/%(title)s.%(ext)s" --merge-output-format "mp4" --retries 10 --write-info-json --write-thumbnail --http-chunk-size 10485760 --cookies "cookies.txt" 

# https://www.youtube.com/playlist?list=PLsFouWTyKWsraAiYu4skJPRTlBq2Fz24F


# yt-dlp -f "bestvideo+bestaudio/best" --download-archive "videos.txt" --fragment-retries 10 --output "videos/%(playlist_title)s/%(title)s.%(ext)s" --merge-output-format "mp4" --retries 10 --write-info-json --write-thumbnail --http-chunk-size 10485760 --cookies "cookies.txt" https://www.youtube.com/playlist?list=PLsFouWTyKWsq6XkYDG43VvTNrFnf8dRaX https://www.youtube.com/playlist?list=PLsFouWTyKWspy8pd4eB8jl7RgtwSNZ2dF https://www.youtube.com/playlist?list=PLsFouWTyKWspXt22JSR4AvLedBe1mSmr7 https://www.youtube.com/playlist?list=PLsFouWTyKWsqJGbY3623pWfX-qfonOLbe https://www.youtube.com/playlist?list=PLsFouWTyKWsoWT4kjS02joxegm1TFRhYe https://www.youtube.com/playlist?list=PLsFouWTyKWsrDvsL6M6qHcLgLuW6H73oj https://www.youtube.com/playlist?list=PLsFouWTyKWsoRhPJwNswXIGDkD9pDQw-w
# https://www.youtube.com/playlist?list=PLsFouWTyKWsraAiYu4skJPRTlBq2Fz24F
# https://www.youtube.com/playlist?list=PLsFouWTyKWsqaG0L9EhYmGHRE6uzoqoAL

# https://www.youtube.com/@SaoHutiger/playlists
# https://www.youtube.com/@imYangZai/playlists
# https://www.youtube.com/@XiangKai-Official/videos
# https://www.youtube.com/@loveminecraft99/videos
# https://www.youtube.com/@user-tv7kp8nb2k/playlists
# https://www.youtube.com/@user-mt1tv4qj4e/search?query=%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C
# https://www.youtube.com/@chaohaokan/search?query=%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C
# https://www.youtube.com/@YiHanYouXiJieShuo/playlists
# https://www.youtube.com/@Minecraft-rj1cs/videos
# https://www.youtube.com/@YangzaiF-Game/playlists
# https://www.youtube.com/@yefengmc/videos