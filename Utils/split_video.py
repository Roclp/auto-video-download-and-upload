# 使用ffmpeg库分割视频
import subprocess
import os
import math

from moviepy.video.io.VideoFileClip import VideoFileClip

def get_video_duration(input_file):
    clip = VideoFileClip(input_file)
    duration = clip.duration
    return duration



def split_video_ffmpeg(input_video, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        print(f"输出文件夹不存在，已为您创建：{output_folder}")

    # 获取视频总时长
    total_duration = get_video_duration(input_video)
    print(f"视频总时长：{total_duration}秒")

    # 确定分段时长和数量
    # 上取整ceil
    # num_segments = math.ceil(total_duration / (5 * 60))
    # num_segments = math.ceil(total_duration / (4 * 60))
    num_segments = math.ceil(total_duration / (3 * 60))
    segment_duration = total_duration / num_segments
    print(f"视频将分为{num_segments}段，平均每段时长为{segment_duration}秒")

    # 获取原视频文件名
    filename_with_extension = os.path.basename(input_video)
    # 分割文件名和扩展名
    filename, _ = os.path.splitext(filename_with_extension)

    # 使用ffmpeg分割视频
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min(start_time + segment_duration, total_duration)

        # 生成输出文件名
        output_file = os.path.join(output_folder, f"{filename}【第{i+1}集】.mp4")

        # 构建ffmpeg命令
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', input_video,
            '-ss', str(start_time),
            '-to', str(end_time),
            '-c', 'copy',
            output_file
        ]

        # 执行ffmpeg命令
        subprocess.run(ffmpeg_cmd, check=True)

if __name__ == "__main__":
    input_video = r"D:\desktop\myself\videos\我的世界：变成各种角色生存100天系列\我的世界：变成钻石骷髅在MC中生存100天！.mp4"
    output_folder = "video"

    split_video_ffmpeg(input_video, output_folder)













# 使用moviepy库分割视频
# from moviepy.video.io.VideoFileClip import VideoFileClip
# import math

# def split_video(input_file, output_folder):
#     clip = VideoFileClip(input_file)
#     total_duration = clip.duration
#     print(f"视频总时长：{total_duration}秒")

#     # 确定分段时长和数量
    
#     num_segments = math.floor(total_duration //(5 * 60))
#     print(f"视频分为{num_segments}段")

#     segment_duration = total_duration / num_segments

#     start_time = 0
#     for i in range(1, num_segments + 1):
#         end_time = min(start_time + segment_duration, total_duration)

#         # 从原视频中截取片段
#         segment = clip.subclip(start_time, end_time)

#         # 生成输出文件名
#         # output_file = f"{output_folder}/segment_{i}_{input_file}"
#         output_file = f"{output_folder}/segment_{i}_output_video.mp4"

#         # 保存视频片段
#         segment.write_videofile(output_file, codec="libx264", audio_codec="aac")

#         # 更新起始时间
#         start_time = end_time

# if __name__ == "__main__":
#     input_video = r"D:\desktop\myself\videos\我的世界：变成各种角色生存100天系列\我的世界：变成钻石骷髅在MC中生存100天！.mp4"
#     output_folder = "video"

#     split_video(input_video, output_folder)

