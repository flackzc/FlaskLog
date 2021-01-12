#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# 
import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("display_path.py pos_file_name")
    exit

file_name = sys.argv[1]
x, y = np.loadtxt(file_name, delimiter=',', unpack=True)
y = -y
# 轨迹
plt.plot(x, y, linewidth=0.5) #设置线条宽度
plt.plot(x, y, ',', label='path', color='blue')
plt.xlabel('x')
plt.ylabel('y')
plt.title('path')
plt.legend()
plt.gcf().set_size_inches(20, 20)
ax = plt.gca()
ax.set_aspect(1)
plt.show()
