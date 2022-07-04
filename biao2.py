
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
 
name_list = ['Radar','Radar+DP','LiDAR','Radar+LiDAR','Radar+LiDAR+DP','IMMF','CMSF','M${^2}$-Fusion']
# 'Camera+LiDAR','Camera+Radar','R+L'
# num_list = [1.5,0.6,7.8,6]
plt.rc('font',family='Times New Roman')
plt.ylim(15,70)


plt.title("Accuracy",fontsize=20)
plt.tick_params(axis='y', labelsize=15)

Radar = [20.49,38.21]
Radar_DP = [  21.99,  41.83]
LiDAR = [44.21,47.67]
Radar_LiDAR = [ 44.33,  55.75]
Radar_LiDAR_DP = [ 45.16,  57.18]
Immf = [ 48.24,  58.12]
Cmsf = [47.67,  57.35]
M2_Fusion = [ 49.85, 61.24]

threed = [20.49,21.99,44.21,44.33,45.16,48.24,47.67,49.85]
bev = [38.21,41.83,47.67, 55.75,57.18,58.12,57.35,61.24]
# num_list1 = [1,2,3,1]
x =list(range(len(threed)))
total_width, n = 2.8, 8
width = total_width / n
 
plt.bar(x, threed, width=width, label='3D',fc = 'lightblue',edgecolor='black',lw=0.5)
for i, j in zip(x, threed):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=10)

for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, bev, width=width, label='BEV',fc = 'deepskyblue',edgecolor='black',lw=0.5)
for i, j in zip(x, bev):
    plt.text(i, j + 0.01, "%.2f" % j, ha="center", va="bottom", fontsize=10)
for i in range(len(x)):
    x[i] = x[i] - 0.5 * width
# plt.bar(x,height=0,tick_label=name_list,fontsize=15)
plt.xticks(x,name_list,fontsize=11,rotation=20)
plt.ylabel('Performance(mAP)',fontsize=18)

plt.legend(loc='upper left',fontsize=14)
plt.show()