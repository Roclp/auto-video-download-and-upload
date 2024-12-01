from datetime import datetime, timedelta


def generate_schedule_within_7_days(*hour_time_list):
    now = datetime.now()
    schedule = []
    day_cnt=13
    # day_cnt=6
    # 循环7天，包括今天
    for day_offset in range(14):
        # 计算目标日期
        day = now.date() + timedelta(days=day_offset)
        # 为每个目标日期计算三个时间点
        for hour in hour_time_list:
            # 计算时间点
            time_point = datetime.combine(day, datetime.min.time()) + timedelta(hours=hour)
            # 确保时间点在当前时间之后，并且在24小时*6天的时间范围内
            if time_point > now and time_point < now+timedelta(hours=2):
                schedule.append(0)
            elif time_point > now and time_point < now + timedelta(hours=24*day_cnt):
                schedule.append(time_point)

    return schedule

if __name__ == '__main__':
    # 调用函数并打印结果
    print([time_point for time_point in generate_schedule_within_7_days(10,12,13, 15, 23)])
    schedule_list = generate_schedule_within_7_days(10,11, 15, 23)
    for i in schedule_list:
        print(i)