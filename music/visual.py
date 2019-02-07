# -*- coding:utf-8
import matplotlib.pyplot as plt
import numpy as np
emo_count={'encourage': 17173, 'happy': 9763, 'angry': 11471, 'romantic': 25454, 'healing': 17863, 'sad': 13467}


# 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
plt.figure(figsize=(8, 6), dpi=80)

# 再创建一个规格为 1 x 1 的子图
plt.subplot(1, 1, 1)

# 柱子总数
N = 6
# 包含每个柱子对应值的序列
values = list(emo_count.values())

# 包含每个柱子下标的序列
index = np.arange(N)

# 柱子的宽度
width = 0.35

# 绘制柱状图, 每根柱子的颜色为紫罗兰色
p2 = plt.bar(index, values, width,  color="#87CEFA")

# 设置横轴标签
plt.xlabel('Emotion Class')
# 设置纵轴标签
plt.ylabel('Count')


plt.text(fontsize=7)


# 添加纵横轴的刻度
plt.xticks(index, emo_count.keys())
plt.yticks(np.arange(0, 28000, 5000))

# 添加图例
plt.legend(loc="upper right")

plt.show()

#柱状图
from random import seed
from random import randint
import pyecharts

emo_count=emo_count={'励志': 17173, '快乐': 9763, '宣泄': 11471, '甜蜜': 25454, '治愈': 17863, '伤感': 13467}
x=[]
y=[]
for k,v in emo_count.items():
    x.append(k)
    y.append(v)
bar=pyecharts.Bar('情感类别')
bar.add('个数',x,y,is_label_show=True)
bar.render('D:/qq.html')