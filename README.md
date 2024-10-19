# auto-video-download-and-upload

下载Youtube（油管）视频，上传Bilibili（B站）国内可使用，免翻墙 视频搬运


个人搬运工具，用于自动下载Youtube的播放列表中的视频、封面、字幕，并上传至bilibili。

## USAGE

yt-dlp: a youtube downloader to download videos from youtube.com or other video platforms

install/update with pip:

```
pip install yt-dlp
```

**download & upload:**

​	 set your config.yaml, cookies.json(upload to bilibili)(generate by [biliup-rs](https://github.com/biliup/biliup-rs)'s release). 

​	 **run:** Downloader.py ---> BiliUploader.py


项目依赖：

* [yt_dlp](https://github.com/yt-dlp/yt-dlp)

* [biliup](https://github.com/biliup/biliup)

* [whisper](https://github.com/openai/whisper)

* [social-auto-upload](https://github.com/dreammis/social-auto-upload)

第三方工具

* [ffmpeg](https://ffmpeg.org/)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [biliup-rs](https://github.com/biliup/biliup-rs)

