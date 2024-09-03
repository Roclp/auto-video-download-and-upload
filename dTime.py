from datetime import datetime, timedelta
import random

def get_random_time_diff(days, start_hour, end_hour):
    current_date = datetime.now()

    if current_date.hour >= end_hour:
        start_date = current_date + timedelta(days=1)
    else:
        start_date = current_date

    time_points = []

    for i in range(days):
        target_date = start_date + timedelta(days=i)
        for hour in range(24):
            for minute in range(60):
                time_point = datetime(target_date.year, target_date.month, target_date.day, hour, minute)
                if time_point.time() >= datetime.strptime(f"{start_hour:02d}:00", "%H:%M").time() and time_point.time() < datetime.strptime(f"{end_hour:02d}:00", "%H:%M").time():
                    time_points.append(time_point)

    selected_time_point = random.choice(time_points)
    time_diff = (selected_time_point - current_date).total_seconds()
    selected_timestamp = int(selected_time_point.timestamp())
    
    print(f"随机时间点：{selected_time_point}")
    # print(f"当前时间和随机时间点的差值为：{time_diff}秒")
    print(f"选定时间点的时间戳：{selected_timestamp}")
    
    return selected_timestamp


# 测试
# for i in range(20):
#     time_diff = get_random_time_diff(1, 10, 20)
#     print(time_diff)
# time_diff = get_random_time_diff(1, 19, 20)
# print(time_diff)

