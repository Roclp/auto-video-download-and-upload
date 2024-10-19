from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import subprocess

# 获取视频时长
def get_video_time(file):
    video = VideoFileClip(file)
    return video.duration

# 获取文件夹下的视频总数
def get_video_count(dir):
    count = 0
    for i in os.listdir(dir):
        if i.endswith(".mp4"):
            count += 1
    return count

# 创建 filelist.txt 文件并写入视频文件路径
def create_filelist(dir, filelist_path):
    with open(filelist_path, 'w') as f:
        for i in os.listdir(dir):
            if i.endswith(".mp4"):
                f.write(f"file '{os.path.join(dir, i)}'\n")

# 根据视频总数将文件夹下的视频合并成10个视频
def merge_video(dir):
    # 视频总数
    video_count = get_video_count(dir)
    # 视频总数除以10，使用整数除法
    every_video_count = video_count // 10
    # 计算余数
    remainder = video_count % 10
    # 创建 filelist.txt 文件
    filelist_path = os.path.join(dir, "filelist.txt")
    create_filelist(dir, filelist_path)
    
    try:
        # 合并前9个视频文件
        for i in range(0, video_count - remainder, every_video_count):
            with open(filelist_path, 'w') as f:
                for j in range(i, i + every_video_count):
                    f.write(f"file '{os.path.join(dir, os.listdir(dir)[j])}'\n")
            output_file = os.path.join(dir, f"merged_{i//every_video_count + 1}.mp4")
            ffmpeg_cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', filelist_path,
                '-c', 'copy',
                output_file
            ]
            subprocess.run(ffmpeg_cmd, check=True)
        
        # 处理余数视频
        if remainder != 0:
            with open(filelist_path, 'w') as f:
                for j in range(video_count - remainder, video_count):
                    f.write(f"file '{os.path.join(dir, os.listdir(dir)[j])}'\n")
            output_file = os.path.join(dir, f"merged_{video_count // 10 + 1}.mp4")
            ffmpeg_cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', filelist_path,
                '-c', 'copy',
                output_file
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    finally:
        # 清理 filelist.txt 文件
        os.remove(filelist_path)

if __name__ == "__main__":
    dir = r"C:\Users\LX\Downloads\Video"
    merge_video(dir)