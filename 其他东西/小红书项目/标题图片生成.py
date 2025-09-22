from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import os


def draw_title_on_image(config, title_text, figure_num=1):
    """绘制标题图片"""
    image_path = config['image_path']
    font_size = config['font_size']
    text_color = config['text_color']
    left_margin = config['left_margin']
    right_margin = config['right_margin']
    top_margin = config['top_margin']
    line_spacing = config['line_spacing']

    # 打开图片
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # 加载字体 - 使用更适合标题的字体
    try:
        # 优先使用粗体字体
        font_paths = [
            "C:/Windows/Fonts/msyhbd.ttc",  # 微软雅黑粗体
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
            "/System/Library/Fonts/PingFang-Bold.ttc",  # macOS 粗体
            "/System/Library/Fonts/Helvetica.ttc"  # macOS Helvetica
        ]

        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue

        if font is None:
            font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", font_size)
        except:
            font = ImageFont.load_default()

    # 计算可用宽度
    available_width = width - left_margin - right_margin

    # 过滤掉特殊图标字符
    filtered_text = ""
    for char in title_text:
        if ord(char) < 0x10000 and char not in ['\u200b', '\u200c', '\u200d']:
            filtered_text += char

    # 手动换行处理（更安全的方式）
    lines = []
    paragraphs = filtered_text.split('\n')

    for paragraph in paragraphs:
        if not paragraph.strip():
            lines.append("")
            continue

        words = list(paragraph)
        current_line = ""

        for word in words:
            test_line = current_line + word
            try:
                bbox = draw.textbbox((0, 0), test_line, font=font)
                line_width = bbox[2] - bbox[0]

                if line_width > available_width:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
                else:
                    current_line = test_line
            except:
                current_line += word

        if current_line:
            lines.append(current_line)

    # 绘制文字
    y = top_margin
    for line in lines:
        try:
            draw.text((left_margin, y), line, font=font, fill=text_color)
        except:
            pass
        y += font_size + line_spacing

    return image


def draw_multiple_titles(config, output_folder=None):
    """处理多个标题，生成多张标题图片"""
    text = config['text']

    # 如果指定了输出文件夹，确保文件夹存在
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        print(f"标题图片将保存到文件夹: {output_folder}")

    # 按双换行符分割标题
    titles = [t.strip() for t in text.split('\n\n') if t.strip()]

    if not titles:
        titles = [t.strip() for t in text.split('\n') if t.strip()]

    print(f"检测到 {len(titles)} 个标题，将生成 {len(titles)} 张标题图片")

    # 为每个标题生成一张图片
    images = []
    for i, title in enumerate(titles, 1):
        print(f"生成第 {i} 张标题图片...")
        image = draw_title_on_image(config, title, i)
        images.append(image)

        # 显示图片
        plt.figure(figsize=(12, 8))
        plt.imshow(image)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

        # 保存图片
        if output_folder:
            # 生成文件名
            filename = f"标题_{i:02d}.png"
            filepath = os.path.join(output_folder, filename)
            try:
                image.save(filepath)
                print(f"已保存标题图片: {filename}")
            except Exception as e:
                print(f"保存标题图片失败 {filename}: {e}")

    return images


# 标题配置参数（更深的颜色，适合标题）
TITLE_CONFIG = {
    'image_path': "备忘录.png",  # 背景图片路径
    'text': """
    美团试点「现制现炒」信息栏！
一键看后厨，干饭更安心。""",
    'font_size': 75,  # 更大的字体适合标题
    'text_color': "#222222",  # 更深的颜色（比之前的 #333333 更黑）
    'left_margin': 80,  # 稍大的边距
    'right_margin': 80,
    'top_margin': 150,  # 更大的上边距
    'line_spacing': 12  # 更大的行间距
}

if __name__ == "__main__":
    # 调试阶段可以设为 None，最后保存时再指定文件夹
    output_folder = "C:\\Users\\11440\\Pictures\\小红书\\temp\\其他\\9.20.1"
    draw_multiple_titles(TITLE_CONFIG, output_folder)