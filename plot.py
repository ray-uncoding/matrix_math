import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 創建畫布
fig = plt.figure(figsize=(10, 5))  # 設定畫布大小

# 第一個子圖：2D 折線圖
ax1 = fig.add_subplot(121)  # 1 行 2 列，第一個子圖
x = np.linspace(0, 10, 100)
y = np.sin(x)
ax1.plot(x, y, label='y = sin(x)')
ax1.set_title('2D Line Plot')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.legend()

# 第二個子圖：3D 散點圖
ax2 = fig.add_subplot(122, projection='3d')  # 1 行 2 列，第二個子圖
x = np.random.rand(100)
y = np.random.rand(100)
z = np.random.rand(100)
ax2.scatter(x, y, z, c=z, cmap='viridis', label='Random Points')
ax2.set_title('3D Scatter Plot')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.legend()

# 顯示圖表
plt.tight_layout()  # 自動調整佈局避免重疊
plt.show()
