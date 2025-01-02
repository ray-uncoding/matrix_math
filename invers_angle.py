import numpy as np

def extract_zyx_angles_from_matrix(R):
    """
    從旋轉矩陣中提取 ZYX 歐拉角（alpha, beta, gamma）。
    :param R: 3x3 旋轉矩陣
    :return: ZYX 歐拉角 [alpha, beta, gamma] (以度為單位)
    """
    steps = []
    
    # 提取 beta
    r31, r32, r33 = R[2, 0], R[2, 1], R[2, 2]
    beta = np.arctan2(-r31, np.sqrt(r32**2 + r33**2))
    steps.append(f"beta = atan2(-r31, sqrt(r32^2 + r33^2)) = atan2({-r31:.4f}, {np.sqrt(r32**2 + r33**2):.4f}) = {np.degrees(beta):.4f}°")
    
    # 提取 alpha 和 gamma
    cos_beta = np.cos(beta)
    if np.abs(cos_beta) > 1e-6:  # 避免 cos(beta) = 0
        alpha = np.arctan2(r32 / cos_beta, r33 / cos_beta)
        gamma = np.arctan2(R[1, 0] / cos_beta, R[0, 0] / cos_beta)
        steps.append(f"alpha = atan2(r32/cos(beta), r33/cos(beta)) = atan2({r32:.4f}/{cos_beta:.4f}, {r33:.4f}/{cos_beta:.4f}) = {np.degrees(alpha):.4f}°")
        steps.append(f"gamma = atan2(r21/cos(beta), r11/cos(beta)) = atan2({R[1, 0]:.4f}/{cos_beta:.4f}, {R[0, 0]:.4f}/{cos_beta:.4f}) = {np.degrees(gamma):.4f}°")
    else:
        # 特殊情況
        alpha = 0
        gamma = np.arctan2(-R[0, 1], R[1, 1])
        steps.append(f"cos(beta) ≈ 0, 特殊情況：")
        steps.append(f"alpha = 0")
        steps.append(f"gamma = atan2(-r12, r11) = atan2({-R[0, 1]:.4f}, {R[1, 1]:.4f}) = {np.degrees(gamma):.4f}°")

    return np.degrees([gamma, beta, alpha]), steps

def extract_zyz_angles_from_matrix(R):
    """
    從旋轉矩陣中提取 ZYZ 歐拉角（alpha, beta, gamma）。
    :param R: 3x3 旋轉矩陣
    :return: ZYZ 歐拉角 [alpha, beta, gamma] (以度為單位)
    """
    steps = []
    
    # 提取 beta
    r31, r32, r33 = R[2, 0], R[2, 1], R[2, 2]
    beta = np.arccos(r33)
    steps.append(f"beta = acos(r33) = acos({r33:.4f}) = {np.degrees(beta):.4f}°")
    
    # 提取 alpha 和 gamma
    sin_beta = np.sin(beta)
    if np.abs(sin_beta) > 1e-6:  # 避免 sin(beta) = 0
        alpha = np.arctan2(r31 / sin_beta, r32 / sin_beta)
        gamma = np.arctan2(R[0, 2] / sin_beta, R[1, 2] / sin_beta)
        steps.append(f"alpha = atan2(r31/sin(beta), r32/sin(beta)) = atan2({r31:.4f}/{sin_beta:.4f}, {r32:.4f}/{sin_beta:.4f}) = {np.degrees(alpha):.4f}°")
        steps.append(f"gamma = atan2(r13/sin(beta), r23/sin(beta)) = atan2({R[0, 2]:.4f}/{sin_beta:.4f}, {R[1, 2]:.4f}/{sin_beta:.4f}) = {np.degrees(gamma):.4f}°")
    else:
        # 特殊情況
        alpha = 0
        gamma = np.arctan2(R[1, 0], R[0, 0])
        steps.append(f"sin(beta) ≈ 0, 特殊情況：")
        steps.append(f"alpha = 0")
        steps.append(f"gamma = atan2(r21, r11) = atan2({R[1, 0]:.4f}, {R[0, 0]:.4f}) = {np.degrees(gamma):.4f}°")

    return np.degrees([gamma, beta, alpha]), steps


# 測試代碼
if __name__ == "__main__":
    # 測試旋轉矩陣
    R = np.array([
        [0.5, -0.866, 0],
        [0.866, 0.5, 0],
        [0, 0, 1]
    ])  # 替換為其他旋轉矩陣

    print("輸入的旋轉矩陣 R：")
    print(R)

    # ZYX 歐拉角
    angles_zyx, process_zyx = extract_zyx_angles_from_matrix(R)
    print("\nZYX 反推計算過程：")
    for step in process_zyx:
        print(step)
    print(f"\nZYX 歐拉角：{angles_zyx}")

    # ZYZ 歐拉角
    angles_zyz, process_zyz = extract_zyz_angles_from_matrix(R)
    print("\nZYZ 反推計算過程：")
    for step in process_zyz:
        print(step)
    print(f"\nZYZ 歐拉角：{angles_zyz}")
