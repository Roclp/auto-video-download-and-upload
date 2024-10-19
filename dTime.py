from datetime import datetime, timedelta
import random,os

# 生成真随机时间点
def get_random_time_diff(days, start_hour, end_hour):
    current_date = datetime.now()

    # 设置起始日期
    if current_date.hour >= end_hour:
        start_date = current_date + timedelta(days=1)
    else:
        start_date = current_date

    time_points = []

    for i in range(days):
        target_date = start_date + timedelta(days=i)
        for hour in range(start_hour, end_hour):
            for minute in range(60):
                time_point = datetime(target_date.year, target_date.month, target_date.day, hour, minute)
                time_points.append(time_point)

    # 生成真随机索引
    random_bytes = os.urandom(4)  # 4字节可以表示0到4294967295的整数
    random_index = int.from_bytes(random_bytes, 'little') % len(time_points)

    selected_time_point = time_points[random_index]
    time_diff = (selected_time_point - current_date).total_seconds()
    selected_timestamp = int(selected_time_point.timestamp())
    
    print(f"随机时间点：{selected_time_point}")
    print(f"选定时间点的时间戳：{selected_timestamp}")
    
    return selected_timestamp


# 测试
# for i in range(20):
#     time_diff = get_random_time_diff(10, 15, 20)
#     print(time_diff)
# time_diff = get_random_time_diff(1, 19, 20)
# print(time_diff)

