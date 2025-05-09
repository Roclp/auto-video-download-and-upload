# import cv2
# import numpy as np

# # 读取彩色图像
# image = cv2.imread('and.png')

# # 转换为灰度图像
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # 应用自适应二值化阈值处理
# binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

# # 使用形态学操作来连接断开的线条和填充孔洞
# kernel = np.ones((1, 1), np.uint8)
# opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
# closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

# # 中值滤波去除噪点
# median = cv2.medianBlur(closing, 3)

# # 显示原始图像和处理后的黑白图像
# cv2.imshow('Original Image', image)
# cv2.imshow('Processed Black and White Image', median)

# # 等待按键并关闭窗口
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # 保存处理后的黑白图像
# cv2.imwrite('output_.jpg', median)






# import cv2
# import numpy as np

# # 读取彩色图像
# image = cv2.imread('input.png')

# # 转换为灰度图像
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # 应用固定阈值处理
# _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# # 显示原始图像和黑白图像
# cv2.imshow('Original Image', image)
# cv2.imshow('Black and White Image', binary)

# # 等待按键并关闭窗口
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # 保存黑白图像
# cv2.imwrite('output_black_and_white.jpg', binary)



import cv2
import numpy as np

# 读取彩色图像
image = cv2.imread('input.png')

# 转换为灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 对灰度图像进行插值以增加细节
# 这里使用双线性插值，可以尝试不同的插值方法如cv2.INTER_CUBIC或cv2.INTER_NEAREST
height, width = gray.shape
resized = cv2.resize(gray, (width*2, height*2), interpolation=cv2.INTER_LINEAR)

# 对插值后的图像应用固定阈值处理
_, binary = cv2.threshold(resized, 200, 255, cv2.THRESH_BINARY)

# 显示原始图像、插值后的灰度图像和黑白图像
cv2.imshow('Original Image', image)
cv2.imshow('Resized Grayscale Image', resized)
cv2.imshow('Black and White Image', binary)

# 等待按键并关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存插值后的黑白图像
cv2.imwrite('output_bl.jpg', binary)