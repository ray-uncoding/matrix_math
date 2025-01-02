import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def rotation_matrix_xyz_fixed(angles):
    """
    根據固定角（XYZ）生成旋轉矩陣。
    :param angles: 旋轉角度 [gamma, beta, alpha] (以度為單位)
    :return: 3x3 旋轉矩陣
    """
    gamma, beta, alpha = np.radians(angles)

    # 繞 X 軸旋轉
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(gamma), -np.sin(gamma)],
        [0, np.sin(gamma), np.cos(gamma)]
    ])

    # 繞 Y 軸旋轉
    R_y = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])

    # 繞 Z 軸旋轉
    R_z = np.array([
        [np.cos(alpha), -np.sin(alpha), 0],
        [np.sin(alpha), np.cos(alpha), 0],
        [0, 0, 1]
    ])

    # 固定角順序：R_Z * R_Y * R_X
    return R_z @ R_y @ R_x


def update(num, lines, base_vectors, angles, steps):
    """
    更新動畫中的每一幀。
    """
    current_angles = [angle * num / steps for angle in angles]
    R = rotation_matrix_xyz_fixed(current_angles)

    # 計算新的向量位置
    transformed_vectors = np.dot(R, base_vectors.T).T
    for line, vec in zip(lines, transformed_vectors):
        line.set_data([0, vec[0]], [0, vec[1]])
        line.set_3d_properties([0, vec[2]])


# 主程序
if __name__ == "__main__":
    # 初始旋轉角度
    gamma = float(input("輸入繞 X 軸旋轉的角度（gamma）："))
    beta = float(input("輸入繞 Y 軸旋轉的角度（beta）："))
    alpha = float(input("輸入繞 Z 軸旋轉的角度（alpha）："))

    angles = [gamma, beta, alpha]
    steps = 100  # 動畫幀數

    # 基向量（紅、綠、藍對應 X、Y、Z 軸）
    base_vectors = np.eye(3) * 5  # 放大比例

    # 創建畫布
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 初始化坐標軸
    colors = ['r', 'g', 'b']
    lines = []
    for vec, color in zip(base_vectors, colors):
        line, = ax.plot([0, vec[0]], [0, vec[1]], [0, vec[2]], color=color, lw=2)
        lines.append(line)

    # 動畫設置
    ani = FuncAnimation(
        fig, update, frames=steps, fargs=(lines, base_vectors, angles, steps), interval=100
    )

    plt.show()
