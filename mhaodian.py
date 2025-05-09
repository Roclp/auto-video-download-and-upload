import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 时间轴：24小时，每小时12个点，即每5分钟一个点，共288个点
hours = np.linspace(0, 24, 24 * 12 + 1)
initial_battery = 100
np.random.seed(42)

# 生成持续下降的电量曲线
def generate_battery_curve(base_rate, noise_level):
    # 平均每5分钟的耗电率 = 每小时耗电 / 12
    base_drain = (base_rate / 12) + np.random.normal(0, noise_level, len(hours))
    base_drain = np.maximum(base_drain, 0.01)  # 避免负值
    cumulative_drain = np.cumsum(base_drain)
    cumulative_drain = np.minimum(cumulative_drain, initial_battery)
    battery = initial_battery - cumulative_drain
    for i in range(1, len(battery)):
        battery[i] = min(battery[i], battery[i - 1])
    return battery

# 原始电量数据（每小时平均耗电：Pixel 1.1，Medium 1.4，Small 2.0）
battery_pixel = generate_battery_curve(base_rate=1.1, noise_level=0.1)
battery_medium = generate_battery_curve(base_rate=1.4, noise_level=0.1)
battery_small = generate_battery_curve(base_rate=2.0, noise_level=0.1)

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(hours, battery_small, label='小屏手机（Small Phone）')
plt.plot(hours, battery_medium, label='中屏手机（Medium Phone）')
plt.plot(hours, battery_pixel, label='Pixel 9 Pro XL')

plt.xlabel('时间（小时）')
plt.ylabel('电量（%）')
plt.title('三款机型在24小时内的电量变化曲线')
plt.xticks(np.arange(0, 25, 1))
plt.ylim(0, 100)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("mhaodian_12pts_per_hour.pdf", format='pdf')
plt.show()
