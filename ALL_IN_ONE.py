import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk, messagebox


# === 旋轉矩陣生成函數 ===

def rotation_matrix_xyz(angles):
    gamma, beta, alpha = np.radians(angles)
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(gamma), -np.sin(gamma)],
        [0, np.sin(gamma), np.cos(gamma)]
    ])
    R_y = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])
    R_z = np.array([
        [np.cos(alpha), -np.sin(alpha), 0],
        [np.sin(alpha), np.cos(alpha), 0],
        [0, 0, 1]
    ])
    return R_z @ R_y @ R_x


def rotation_matrix_zyx(angles):
    alpha, beta, gamma = np.radians(angles)
    R_z = np.array([
        [np.cos(alpha), -np.sin(alpha), 0],
        [np.sin(alpha), np.cos(alpha), 0],
        [0, 0, 1]
    ])
    R_y = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(gamma), -np.sin(gamma)],
        [0, np.sin(gamma), np.cos(gamma)]
    ])
    return R_z @ R_y @ R_x


def rotation_matrix_zyz(angles):
    alpha, beta, gamma = np.radians(angles)
    R_z1 = np.array([
        [np.cos(alpha), -np.sin(alpha), 0],
        [np.sin(alpha), np.cos(alpha), 0],
        [0, 0, 1]
    ])
    R_y = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])
    R_z2 = np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
    ])
    return R_z1 @ R_y @ R_z2


# === 動畫函數 ===

def update_animation(num, lines, base_vectors, angles, steps, rotation_fn):
    current_angles = [angle * num / steps for angle in angles]
    R = rotation_fn(current_angles)

    # 計算新的基向量
    transformed_vectors = np.dot(R, base_vectors.T).T
    for line, vec in zip(lines, transformed_vectors):
        line.set_data([0, vec[0]], [0, vec[1]])
        line.set_3d_properties([0, vec[2]])


def animate_rotation(angles, steps, interval, rotation_fn):
    base_vectors = np.eye(3) * 5  # 基向量，紅綠藍對應 X、Y、Z

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 初始化基向量（紅、綠、藍）
    lines = []
    colors = ['r', 'g', 'b']
    for vec, color in zip(base_vectors, colors):
        line, = ax.plot([0, vec[0]], [0, vec[1]], [0, vec[2]], color=color, lw=2)
        lines.append(line)

    # 動畫
    ani = FuncAnimation(
        fig, update_animation, frames=steps,
        fargs=(lines, base_vectors, angles, steps, rotation_fn),
        interval=interval
    )
    plt.show()


# === GUI 部分 ===

def start_animation():
    try:
        rotation_type = rotation_var.get()
        angles = list(map(float, angle_entry.get().split()))
        if len(angles) != 3:
            raise ValueError("請輸入三個角度（用空格分隔）！")

        interval = int(speed_var.get())  # 獲取動畫速度
        if rotation_type == "XYZ 固定角":
            animate_rotation(angles, 100, interval, rotation_matrix_xyz)
        elif rotation_type == "ZYX 歐拉角":
            animate_rotation(angles, 100, interval, rotation_matrix_zyx)
        elif rotation_type == "ZYZ 歐拉角":
            animate_rotation(angles, 100, interval, rotation_matrix_zyz)
        else:
            messagebox.showerror("錯誤", "無效的旋轉類型！")
    except ValueError as e:
        messagebox.showerror("錯誤", f"輸入錯誤：{e}")


# 創建主視窗
root = tk.Tk()
root.title("旋轉動畫")

# 旋轉類型選擇
rotation_var = tk.StringVar(value="XYZ 固定角")
ttk.Label(root, text="選擇旋轉方式：").grid(row=0, column=0, padx=10, pady=10, sticky="w")
ttk.Radiobutton(root, text="XYZ 固定角", variable=rotation_var, value="XYZ 固定角").grid(row=1, column=0, padx=20, sticky="w")
ttk.Radiobutton(root, text="ZYX 歐拉角", variable=rotation_var, value="ZYX 歐拉角").grid(row=2, column=0, padx=20, sticky="w")
ttk.Radiobutton(root, text="ZYZ 歐拉角", variable=rotation_var, value="ZYZ 歐拉角").grid(row=3, column=0, padx=20, sticky="w")

# 輸入角度
ttk.Label(root, text="輸入旋轉角度（用空格分隔，例如 30 45 60）：").grid(row=4, column=0, padx=10, pady=10, sticky="w")
angle_entry = ttk.Entry(root, width=30)
angle_entry.grid(row=5, column=0, padx=10, pady=5)

# 動畫速度
speed_var = tk.StringVar(value="100")
ttk.Label(root, text="動畫速度（毫秒/幀）：").grid(row=6, column=0, padx=10, pady=10, sticky="w")
speed_entry = ttk.Entry(root, width=10, textvariable=speed_var)
speed_entry.grid(row=7, column=0, padx=10, pady=5)

# 開始動畫按鈕
start_button = ttk.Button(root, text="開始動畫", command=start_animation)
start_button.grid(row=8, column=0, padx=10, pady=20)

# 啟動主循環
root.mainloop()
