import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms

# 创建一个子图
fig, ax = plt.subplots()

# 绘制实线矩形
rect1 = patches.Rectangle((100, 100), 100, 50, linewidth=3, edgecolor='r', facecolor='none')
ax.add_patch(rect1)

# 计算矩形中心位置
center_x = 100 + 100 / 2
center_y = 100 + 50 / 2

# 绘制虚线矩形
rect2 = patches.Rectangle((0, 0), 100, 50, linewidth=3, edgecolor='r', facecolor='none', linestyle='--')
t = transforms.Affine2D().rotate_deg_around(center_x, center_y, 30) + ax.transData
rect2.set_transform(t)
ax.add_patch(rect2)

# 设置坐标轴范围
ax.set_xlim([0, 300])
ax.set_ylim([0, 300])

# 显示图形
plt.show()