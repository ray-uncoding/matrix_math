import numpy as np

def transformation_matrix(axis, angle, translation):
    """
    生成移動矩陣。
    :param axis: 旋轉軸（'x', 'y', 'z'）
    :param angle: 旋轉角度（度數）
    :param translation: 平移向量 [tx, ty, tz]
    :return: 4x4 移動矩陣
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
        raise ValueError("無效的旋轉軸！請使用 'x', 'y', 或 'z'。")

    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = translation
    return T

def apply_transformation(T, point):
    """
    使用移動矩陣轉換一個點。
    :param T: 4x4 移動矩陣
    :param point: 3D 點 [x, y, z]
    :return: 轉換後的 3D 點 [x', y', z']
    """
    point_homogeneous = np.append(point, 1)  # 擴展為齊次坐標
    transformed_point = T @ point_homogeneous
    return transformed_point[:3]  # 返回前三個分量

# 測試代碼
if __name__ == "__main__":
    # 初始點
    point = [1.0, 2.0, 3.0]  # 初始位置

    # 依次對 x, y, z 軸旋轉 30°, 60°, 90°
    rotations = [('x', 30), ('y', 60), ('z', 90)]
    translation = [10, 5, 6]  # 平移向量

    # 構造初始的單位矩陣
    T_combined = np.eye(4)

    for axis, angle in rotations:
        T = transformation_matrix(axis, angle, [0, 0, 0])  # 只旋轉，不平移
        T_combined = T_combined @ T  # 將每次旋轉的矩陣相乘

    # 加入平移
    T_translation = transformation_matrix('z', 0, translation)  # 僅平移
    T_combined = T_combined @ T_translation

    # 計算結果
    transformed_point = apply_transformation(T_combined, point)

    print("最終的移動矩陣 T：")
    print(T_combined)

    print("\n初始點：", point)
    print("最終轉換後的點：", transformed_point)
