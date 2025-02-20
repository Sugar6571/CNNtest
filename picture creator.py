import os
import numpy as np
import matplotlib.pyplot as plt
import json
from PIL import Image

# 创建文件夹以保存图像和标签
image_folder = "generated_images"
label_folder = "labels"
os.makedirs(image_folder, exist_ok=True)
os.makedirs(label_folder, exist_ok=True)


# 定义生成图像和标签的函数
def generate_image_and_label(value, image_id):
    # 创建一个新的图形
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    # 设置表盘的范围（角度：0到2π）
    ax.set_theta_zero_location('S')  # 0 度位于下方
    ax.set_theta_direction(-1)  # 顺时针方向

    # 绘制表盘背景
    ax.set_facecolor('white')  # 白色背景

    # 定义大刻度和小刻度
    start_angle = np.pi / 4  # 从左下 45° 开始
    end_angle = 7 * np.pi / 4  # 结束于右下 45°（315°）

    num_big_ticks = 6  # 从0到100有6个大刻度
    big_ticks = np.linspace(start_angle, end_angle, num_big_ticks)  # 均匀分布在45°至315°之间
    big_values = np.linspace(0, 100, num_big_ticks)  # 对应的数值是0到100

    # 每个大刻度的夹角
    big_tick_angle = (end_angle - start_angle) / (num_big_ticks - 1)

    # 绘制大刻度及数字
    for i, angle in enumerate(big_ticks):
        ax.plot([angle, angle], [0.8, 1], color='black', lw=3)  # 大刻度线

        # 在刻度内侧标注数字
        ax.text(angle, 0.75, f'{int(big_values[i])}', horizontalalignment='center', verticalalignment='center',
                fontsize=12, color='black')

        # 小刻度分隔，每大刻度之间分为10个小刻度，确保均匀分布
        for j in range(1, 10):
            if i < num_big_ticks - 1:  # 不绘制超出100之后的小刻度
                small_angle = angle + j * big_tick_angle / 10  # 小刻度线的夹角是大刻度夹角的1/10
                ax.plot([small_angle, small_angle], [0.9, 1], color='black', lw=1)  # 小刻度线

    # 计算指针的角度
    pointer_angle = np.interp(value, big_values, big_ticks)  # 根据数值计算指针角度

    # 绘制指针，指向给定值
    ax.plot([0, pointer_angle], [0, 0.9], color='red', lw=2)  # 红色指针，指向给定位置（value）

    # 隐藏极坐标轴的网格线和角度标注
    ax.grid(False)
    ax.set_yticklabels([])  # 隐藏Y轴标签
    ax.set_xticklabels([])  # 删除角度标注
    ax.set_ylim(0, 1)  # 设置半径范围

    # 设置图形比例
    ax.set_aspect('equal')

    # 保存图像
    image_filename = os.path.join(image_folder, f"image_{image_id}.png")
    plt.savefig(image_filename, bbox_inches="tight", pad_inches=0.1)

    # 关闭绘图，避免内存占用
    plt.close()

    # 将图像标签保存为json文件
    label_data = {
        "image_id": image_id,
        "value": value,
        "angle": pointer_angle
    }
    label_filename = os.path.join(label_folder, f"image_{image_id}.json")
    with open(label_filename, 'w') as f:
        json.dump(label_data, f)

    # 缩放图像为较小尺寸（例如：128x128）
    img = Image.open(image_filename)
    img = img.resize((128, 128))
    img.save(image_filename)


# 生成3000张图像和标签
for i in range(3000):
    random_value = np.random.uniform(0, 100)  # 生成随机值
    generate_image_and_label(random_value, i)

print("生成完成！")
