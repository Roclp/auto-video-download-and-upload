import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 时间设置
total_time = 8 * 60  # 8小时，单位：分钟
time_periods = total_time // 5  # 每5分钟1个点

# 构造更真实的睡眠阶段（睡眠监测系统）
# 模拟阶段：清醒(前期)、浅睡->深睡交替、偶尔快速眼动
sleep_monitor = (
    [0] * 6 +                 # 清醒（30分钟）
    [1, 2, 1, 2, 1, 2] * 3 +  # 浅睡深睡交替
    [1] * 6 +                 # 稳定浅睡
    [2] * 6 +                 # 深睡
    [3] +                     # 快速眼动（1次）
    [1, 2, 1, 2] * 3 +        # 再次交替
    [1] * (time_periods - 45)  # 后段浅睡填充
)
sleep_monitor = sleep_monitor[:time_periods]

# 手环识别效果更好，跟实际监测略有偏差，但整体趋势更合理
band_watch = []
for i, state in enumerate(sleep_monitor):
    if i < 6:
        band_watch.append(0)  # 清醒
    elif state == 3:
        band_watch.append(2)  # 快速眼动识别为深睡
    elif state == 2:
        band_watch.append(2)
    elif state == 1:
        band_watch.append(1)
    else:
        band_watch.append(1)

# 睡眠状态标签
sleep_state_map = {0: '清醒', 1: '浅睡', 2: '深睡', 3: '快速眼动'}
stage_order = {'清醒': 0, '浅睡': 1, '深睡': 2, '快速眼动': 3}

# 转换为阶段名称与深度值
sleep_monitor_stages = [sleep_state_map[s] for s in sleep_monitor]
band_watch_stages = [sleep_state_map[s] for s in band_watch]
sleep_monitor_depth = [stage_order[s] for s in sleep_monitor_stages]
band_watch_depth = [stage_order[s] for s in band_watch_stages]

# 画图
fig, axs = plt.subplots(1, 2, figsize=(15, 6))
time = np.arange(time_periods) * 5 / 60  # 小时

# 折线图
axs[0].plot(time, sleep_monitor_depth, label='睡眠监测系统', marker='o', linestyle='-', color='b')
axs[0].plot(time, band_watch_depth, label='智能手环', marker='x', linestyle='--', color='r')
axs[0].set_yticks([0, 1, 2, 3])
axs[0].set_yticklabels(['清醒', '浅睡', '深睡', '快速眼动'])
axs[0].set_xlabel('时间 (小时)')
axs[0].set_ylabel('睡眠状态')
axs[0].legend()

# 柱形图
labels = ['清醒', '浅睡', '深睡', '快速眼动']
sleep_monitor_counts = [sleep_monitor.count(i) for i in range(4)]
band_watch_counts = [band_watch.count(i) for i in range(4)]
x = np.arange(len(labels))
bar_width = 0.35

axs[1].bar(x - bar_width / 2, sleep_monitor_counts, bar_width, label='睡眠监测系统', color='b')
axs[1].bar(x + bar_width / 2, band_watch_counts, bar_width, label='智能手环', color='r')
axs[1].set_xlabel('睡眠阶段')
axs[1].set_ylabel('数量')
axs[1].set_xticks(x)
axs[1].set_xticklabels(labels)
axs[1].legend()

plt.tight_layout()
plt.show()
