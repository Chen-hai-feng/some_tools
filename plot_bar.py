# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
 
name_list = ['Radar','LiDAR','C+R','C+L','M${^2}$-Fusion']
# 'Camera+LiDAR','Camera+Radar','R+L'
# num_list = [1.5,0.6,7.8,6]
plt.rc('font',family='Times New Roman')
plt.subplot(1,2,1)

plt.tick_params(axis='y', labelsize=30)
plt.ylim(10,70)
plt.title("3D",fontsize=35)
###3d的数据
## 单模态的
pointrcnn = [11.40,29.97]
second = [ 18.02, 43.54]
pvrcnn = [ 22.08,44.71]
pointpillars = [ 20.49,44.21]
parta2 = [13.76, 38.45]
voxelrcnn = [18.71, 44.08]

## 融合多模态的
mvxnet_cr  =   11.69
mvxnet_cl = 31.43

R_L = 49.85

# num_list1 = [1,2,3,1]
x =list(range(len(pointrcnn)))
total_width, n = 0.8, 6
width = total_width / n
 
plt.bar(x, pointrcnn, width=width, label='PointRCNN',fc = 'slategray',edgecolor='black',lw=0.5)
for i, j in zip(x, pointrcnn):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)

for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, second, width=width, label='SECOND',fc = 'skyblue',edgecolor='black',lw=0.5)
for i, j in zip(x, second):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)

for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, pvrcnn, width=width, label='PV-RCNN',fc = 'moccasin',edgecolor='black',lw=0.5)
for i, j in zip(x, pvrcnn):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)

for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, pointpillars, width=width, label='PointPillars',fc = 'darkseagreen',edgecolor='black',lw=0.5)
for i, j in zip(x, pointpillars):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)

for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, parta2, width=width, label='Part-A${^2}$',fc = 'dodgerblue',edgecolor='black',lw=0.5)
for i, j in zip(x, parta2):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, voxelrcnn, width=width, label='Voxel R-CNN',fc = 'royalblue',edgecolor='black',lw=0.5)
for i, j in zip(x, voxelrcnn):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)
# print(x)
plt.bar(2, mvxnet_cr, width=width, label='MVX-Net(Camera+Radar)',fc = 'mediumpurple',edgecolor='black',lw=0.5)

plt.text(2, mvxnet_cr+0.01 , "%.2f" % mvxnet_cr, ha="center", va="bottom", fontsize=14)

plt.bar(2+2*width, mvxnet_cl, width=width, label='MVX-Net(Camera+LiDAR)',fc ='mediumslateblue',edgecolor='black',lw=0.5)
plt.text(2+2*width, mvxnet_cl+0.01 , "%.2f" % mvxnet_cl, ha="center", va="bottom", fontsize=14)

plt.bar(2+4*width, R_L, width=width, label='M${^2}$-Fusion',fc = 'plum',edgecolor='black',lw=0.5)
plt.text(2+4*width, R_L+0.01 , "%.2f" % R_L, ha="center", va="bottom", fontsize=14)
for i in range(len(x)):
    x[i] = x[i] - 2.5 * width


print(x+[2,2+width,2+2*width])
plt.xticks(x+[2,2+2*width,2+4*width],name_list,rotation=20,fontsize=28)
# plt.bar(x+[2,2+2*width,2+4*width],height=0,tick_label=name_list)

plt.ylabel('Performance(mAP)',fontsize=33)

plt.legend(loc='upper left',fontsize=18)


plt.subplot(1,2,2)
plt.tick_params(axis='y', labelsize=30)
plt.ylim(10,70)
plt.title("BEV",fontsize=35)
###3d的数据
## 单模态的
pointrcnn = [18.74,34.22]
second = [ 31.01,  45.63]
pvrcnn = [ 39.88, 46.68]
pointpillars = [ 38.21, 47.67]
parta2 = [ 21.47, 41.85]
voxelrcnn = [31.26, 44.54]

## 融合多模态的
mvxnet_cr  =   20.36
mvxnet_cl = 38.15

R_L = 61.24

# num_list1 = [1,2,3,1]
x =list(range(len(pointrcnn)))
total_width, n = 0.8, 6
width = total_width / n
 
plt.bar(x, pointrcnn, width=width, label='PointRCNN',fc = 'slategray',edgecolor='black',lw=0.5)
for i, j in zip(x, pointrcnn):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)

for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, second, width=width, label='SECOND',fc = 'skyblue',edgecolor='black',lw=0.5)
for i, j in zip(x, second):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)

for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, pvrcnn, width=width, label='PV-RCNN',fc = 'moccasin',edgecolor='black',lw=0.5)
for i, j in zip(x, pvrcnn):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)

for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, pointpillars, width=width, label='PointPillars',fc = 'darkseagreen',edgecolor='black',lw=0.5)
for i, j in zip(x, pointpillars):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)

for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, parta2, width=width, label='Part-A${^2}$',fc = 'dodgerblue',edgecolor='black',lw=0.5)
for i, j in zip(x, parta2):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, voxelrcnn, width=width, label='Voxel R-CNN',fc = 'royalblue',edgecolor='black',lw=0.5)
for i, j in zip(x, voxelrcnn):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=14)
# print(x)
plt.bar(2, mvxnet_cr, width=width, label='MVX-Net(Camera+Radar)',fc = 'mediumpurple',edgecolor='black',lw=0.5)

plt.text(2, mvxnet_cr+0.01 , "%.2f" % mvxnet_cr, ha="center", va="bottom", fontsize=14)

plt.bar(2+2*width, mvxnet_cl, width=width, label='MVX-Net(Camera+LiDAR)',fc ='mediumslateblue',edgecolor='black',lw=0.5)
plt.text(2+2*width, mvxnet_cl+0.01 , "%.2f" % mvxnet_cl, ha="center", va="bottom", fontsize=14)

plt.bar(2+4*width, R_L, width=width, label='M${^2}$-Fusion',fc = 'plum',edgecolor='black',lw=0.5)
plt.text(2+4*width, R_L+0.01 , "%.2f" % R_L, ha="center", va="bottom", fontsize=14)
for i in range(len(x)):
    x[i] = x[i] - 2.5 * width


print(x+[2,2+width,2+2*width])
plt.xticks(x+[2,2+2*width,2+4*width],name_list,rotation=20,fontsize=28)
# plt.bar(x+[2,2+2*width,2+4*width],height=0,tick_label=name_list)

plt.ylabel('Performance(mAP)',fontsize=33)

plt.legend(loc='upper left',fontsize=18)
plt.show()