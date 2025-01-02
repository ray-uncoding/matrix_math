import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def rotation_matrix(axis, angle):
    """
    生成旋轉矩陣。
    :param axis: 旋轉軸（'x', 'y', 或 'z'）
    :param angle: 旋轉角度（以度為單位）
    :return: 3x3 旋轉矩陣
    """
    angle = np.radians(angle)
    if axis == 'x':
        R = np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ])
    elif axis == 'y':
        R = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])
    elif axis == 'z':
        R = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError("無效的旋轉軸！")
    return R

def update(num, lines, axis, total_angle, translation, steps):
    """
    更新動畫的每一幀。
    """
    angle = (num / steps) * total_angle
    partial_translation = (num / steps) * np.array(translation)
    R = rotation_matrix(axis, angle)
    
    # 更新基向量的位置和方向
    new_vectors = np.dot(R, base_vectors.T).T + partial_translation
    for line, vec in zip(lines, new_vectors):
        line.set_data([partial_translation[0], vec[0]], 
                      [partial_translation[1], vec[1]])
        line.set_3d_properties([partial_translation[2], vec[2]])

# 主程序
if __name__ == "__main__":
    axis = input("請輸入旋轉軸（x, y, z）：").lower()
    total_angle = float(input("請輸入總旋轉角度（度）："))
    translation = list(map(float, input("請輸入平移向量（格式: tx ty tz）：").split()))
    steps = int(input("請輸入動畫步數："))

    # 基向量
    base_vectors = np.eye(3) * 5  # 基向量放大

    # 創建畫布
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-50, 50])
    ax.set_ylim([-50, 50])
    ax.set_zlim([-50, 50])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 初始化基向量
    lines = []
    colors = ['r', 'g', 'b']
    for vec, color in zip(base_vectors, colors):
        line, = ax.plot([0, vec[0]], [0, vec[1]], [0, vec[2]], color=color, lw=2)
        lines.append(line)

    # 動畫設置
    ani = FuncAnimation(fig, update, frames=steps, 
                        fargs=(lines, axis, total_angle, translation, steps), 
                        interval=100)

    plt.show()
