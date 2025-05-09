from PIL import Image

# 打开图片并统一为 RGB 模式
img1 = Image.open('b.png').convert('RGB')
img2 = Image.open('c.png').convert('RGB')

# 获取原始尺寸
w1, h1 = img1.size
w2, h2 = img2.size

# 目标尺寸为宽度和高度中的最大值
target_width = max(w1, w2)
target_height = max(h1, h2)

# 按目标尺寸分别缩放两张图片（放大较小图像）
img1_resized = img1.resize((target_width, target_height), Image.LANCZOS)
img2_resized = img2.resize((target_width, target_height), Image.LANCZOS)

# 创建拼接后的画布
combined_img = Image.new('RGB', (target_width * 2, target_height), (255, 255, 255))
combined_img.paste(img1_resized, (0, 0))
combined_img.paste(img2_resized, (target_width, 0))

# 保存为 PDF
combined_img.save('stage.pdf', format='PDF')
