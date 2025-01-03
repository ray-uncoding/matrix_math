# 旋轉動畫工具

本項目提供了一個基於 Python 和 Tkinter 的 3D 旋轉動畫工具，支持多種旋轉方式（XYZ 固定角、ZYX 歐拉角、ZYZ 歐拉角以及軸-角表示法），並通過 Matplotlib 可視化展示旋轉過程。

## 功能特性

- **多種旋轉方式**：
  - **XYZ 固定角**：依次繞 X、Y、Z 軸旋轉指定角度。
  - **ZYX 歐拉角**：依次繞 Z、Y、X 軸旋轉指定角度。
  - **ZYZ 歐拉角**：依次繞 Z、Y、Z 軸旋轉指定角度。
  - **軸-角表示法**：指定旋轉軸和旋轉角度進行旋轉。

- **動畫速度控制**：
  - 通過滑條設置動畫速度（毫秒/幀），支持從慢速到快速的動畫展示。

- **動態輸入框**：
  - 根據選擇的旋轉方式，顯示相應的輸入框和範例提示，方便用戶操作。

- **錯誤處理**：
  - 提供用戶友好的錯誤提示，確保輸入的數據格式正確。

## 使用說明

1. **選擇旋轉方式**：
   - 在主界面中選擇一種旋轉方式（如 XYZ 固定角）。

2. **輸入參數**：
   - 根據所選旋轉方式，輸入對應的旋轉角度或軸角數據。例如：
     - **XYZ 固定角**：輸入 `30 45 60`
     - **軸-角表示法**：輸入旋轉軸 `1 0 0` 和旋轉角度 `45`

3. **設置動畫速度**：
   - 拖動滑條調整動畫速度（毫秒/幀）。

4. **開始動畫**：
   - 點擊 **開始動畫** 按鈕，Matplotlib 將彈出窗口展示旋轉動畫。