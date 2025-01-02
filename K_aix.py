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


def axis_angle_to_rotation_matrix(K, theta):
    theta_rad = np.radians(theta)
    c = np.cos(theta_rad)
    s = np.sin(theta_rad)
    v = 1 - c

    kx, ky, kz = K
    R = np.array([
        [kx * kx * v + c, kx * ky * v - kz * s, kx * kz * v + ky * s],
        [ky * kx * v + kz * s, ky * ky * v + c, ky * kz * v - kx * s],
        [kz * kx * v - ky * s, kz * ky * v + kx * s, kz * kz * v + c]
    ])
    return R


# === 軸-角提取函數 ===

def rotation_matrix_to_axis_angle(R):
    theta = np.arccos((np.trace(R) - 1) / 2)
    theta_deg = np.degrees(theta)

    sin_theta = np.sin(theta)
    if np.abs(sin_theta) < 1e-6:
        raise ValueError("旋轉角度接近 0 或 180 度，旋轉軸未定義！")

    kx = (R[2, 1] - R[1, 2]) / (2 * sin_theta)
    ky = (R[0, 2] - R[2, 0]) / (2 * sin_theta)
    kz = (R[1, 0] - R[0, 1]) / (2 * sin_theta)
    K = np.array([kx, ky, kz])

    K_normalized = K / np.linalg.norm(K)
    return theta_deg, K_normalized


# === 動畫函數 ===

def update_animation(num, lines, base_vectors, angles, steps, rotation_fn):
    current_angles = [angle * num / steps for angle in angles]
    R = rotation_fn(current_angles)

    transformed_vectors = np.dot(R, base_vectors.T).T
    for line, vec in zip(lines, transformed_vectors):
        line.set_data([0, vec[0]], [0, vec[1]])
        line.set_3d_properties([0, vec[2]])


def animate_rotation(angles, steps, interval, rotation_fn):
    base_vectors = np.eye(3) * 5

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    lines = []
    colors = ['r', 'g', 'b']
    for vec, color in zip(base_vectors, colors):
        line, = ax.plot([0, vec[0]], [0, vec[1]], [0, vec[2]], color=color, lw=2)
        lines.append(line)

    ani = FuncAnimation(
        fig, update_animation, frames=steps,
        fargs=(lines, base_vectors, angles, steps, rotation_fn),
        interval=interval
    )
    plt.show()


# === GUI 部分 ===

def update_inputs(*args):
    rotation_type = rotation_var.get()
    if rotation_type == "軸-角表示法":
        angle_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        angle_entry.grid(row=7, column=0, padx=10, pady=5)
        angle_example["text"] = "範例：45（旋轉角度）"
        axis_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        axis_entry.grid(row=9, column=0, padx=10, pady=5)
        axis_example["text"] = "範例：1 0 0（沿 X 軸）"
    else:
        angle_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        angle_entry.grid(row=7, column=0, padx=10, pady=5)
        angle_example["text"] = "範例：30 45 60（XYZ 固定角度）"
        axis_label.grid_forget()
        axis_entry.grid_forget()
        axis_example["text"] = ""


def start_animation():
    try:
        rotation_type = rotation_var.get()
        if rotation_type == "軸-角表示法":
            K = list(map(float, axis_entry.get().split()))
            theta = float(angle_entry.get())
            if len(K) != 3:
                raise ValueError("請輸入三個旋轉軸分量！")
            K = np.array(K) / np.linalg.norm(K)  # 正規化旋轉軸
            animate_rotation([theta], 100, 100, lambda angles: axis_angle_to_rotation_matrix(K, angles[0]))
        else:
            angles = list(map(float, angle_entry.get().split()))
            if len(angles) != 3:
                raise ValueError("請輸入三個角度（用空格分隔）！")

            if rotation_type == "XYZ 固定角":
                animate_rotation(angles, 100, 100, rotation_matrix_xyz)
            elif rotation_type == "ZYX 歐拉角":
                animate_rotation(angles, 100, 100, rotation_matrix_zyx)
            elif rotation_type == "ZYZ 歐拉角":
                animate_rotation(angles, 100, 100, rotation_matrix_zyz)
            else:
                messagebox.showerror("錯誤", "無效的旋轉類型！")
    except ValueError as e:
        messagebox.showerror("錯誤", f"輸入錯誤：{e}")


# 創建主視窗
root = tk.Tk()
root.title("旋轉動畫")

rotation_var = tk.StringVar(value="XYZ 固定角")
rotation_var.trace("w", update_inputs)

ttk.Label(root, text="選擇旋轉方式：").grid(row=0, column=0, padx=10, pady=10, sticky="w")
ttk.Radiobutton(root, text="XYZ 固定角", variable=rotation_var, value="XYZ 固定角").grid(row=1, column=0, padx=20, sticky="w")
ttk.Radiobutton(root, text="ZYX 歐拉角", variable=rotation_var, value="ZYX 歐拉角").grid(row=2, column=0, padx=20, sticky="w")
ttk.Radiobutton(root, text="ZYZ 歐拉角", variable=rotation_var, value="ZYZ 歐拉角").grid(row=3, column=0, padx=20, sticky="w")
ttk.Radiobutton(root, text="軸-角表示法", variable=rotation_var, value="軸-角表示法").grid(row=4, column=0, padx=20, sticky="w")

angle_label = ttk.Label(root, text="輸入旋轉角度：")
angle_entry = ttk.Entry(root, width=30)
angle_example = ttk.Label(root, text="範例：30 45 60")

axis_label = ttk.Label(root, text="輸入旋轉軸：")
axis_entry = ttk.Entry(root, width=30)
axis_example = ttk.Label(root, text="範例：1 0 0（沿 X 軸）")

ttk.Label(root, text="動畫速度（毫秒/幀）：").grid(row=10, column=0, padx=10, pady=10, sticky="w")
speed_scale = ttk.Scale(root, from_=10, to=200, orient="horizontal")
#speed_scale.set(100)  # 預設值
speed_scale.grid(row=11, column=0, padx=10, pady=5)

start_button = ttk.Button(root, text="開始動畫", command=start_animation)
start_button.grid(row=12, column=0, padx=10, pady=20)

update_inputs()
root.mainloop()
