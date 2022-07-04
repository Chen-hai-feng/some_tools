import matplotlib.pyplot as plt
plt.rc('font',family='Times New Roman')

plt.subplot(1,2,1)

plt.title("3D",fontsize=20)
# 横坐标
x = ['0-30m','30-50m','50m-inf']

radar=[ 34.06, 14.76, 6.98] 
lidar=[ 71.90, 21.25, 9.09]
fusion1 = [67.67, 21.50, 12.50]
my_fusion= [77.26, 27.36, 15.56]

plt.plot(x, radar, linewidth=2, color="orange", marker="o",label="Radar")
plt.plot(x, lidar, linewidth=2, color="blue", marker="s",label="LiDAR")
plt.plot(x, fusion1, linewidth=2, color="green", marker="+",label="Radar+LiDAR")
plt.plot(x, my_fusion, linewidth=2, color="red", marker="^",label="M${^2}$-Fusion")


plt.tick_params(axis='both', labelsize=17)
plt.ylabel('Performance(mAP)',fontsize=17)
plt.legend(loc='upper right',fontsize=14)

plt.subplot(1,2,2)

plt.title("BEV",fontsize=20)
# 横坐标
x = ['0-30m','30-50m','50m-inf']

radar=[ 52.08,28.81 ,19.54] 
lidar=[ 76.07, 24.86, 9.09]
fusion1 = [77.92,35.64,24.22]
my_fusion= [83.73, 42.08, 27.68]

plt.plot(x, radar, linewidth=2, color="orange", marker="o",label="Radar")
plt.plot(x, lidar, linewidth=2, color="blue", marker="s",label="LiDAR")
plt.plot(x, fusion1, linewidth=2, color="green", marker="+",label="Radar+LiDAR")
plt.plot(x, my_fusion, linewidth=2, color="red", marker="^",label="M${^2}$-Fusion")


plt.tick_params(axis='both', labelsize=17)
plt.ylabel('Performance(mAP)',fontsize=17)
plt.legend(loc='upper right',fontsize=14)


plt.show()