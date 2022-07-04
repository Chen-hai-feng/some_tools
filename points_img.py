#-*- coding:utf-8 -*-
import pcl
import numpy as np
import cv2 as cv
from PIL import Image
from pylab import imshow
from pylab import array
from pylab import plot
from pylab import title
from pylab import *
import matplotlib.pyplot as plt
#import open3d as o3d

x=[]
y=[]
distance=[]    #存放需要投影点转换成二维前的雷达坐标的x坐标（距离信息），以此为依据对投影点进行染色。
distance_3d=[]    #存放转换前雷达坐标的x坐标（距离信息）。



cloud = pcl.load('/home/kuangda/workspace/datasets/Day/Campus/6.pcd')
im = Image.open('/home/kuangda/workspace/datasets/Day/Campus/6.png')

pix = im.load()
points_3d = []
# print('Loaded ' + str(cloud.width * cloud.height) +
#       ' data points from test_pcd.pcd with the following fields: ')
for i in range(0, cloud.size):
    x_raw = float(cloud[i][0])
    y_raw = float(cloud[i][1])
    z_raw = float(cloud[i][2])
    point_3d = []

    point_3d.append(x_raw)
    point_3d.append(y_raw)
    point_3d.append(z_raw)
    if x_raw>0:
        points_3d.append(point_3d)
        distance_3d.append(x_raw)

cube = np.float64(points_3d)


RT = np.float64([[1.335141827810683579e-01, -9.891042291622222926e-01, -6.202247052245707382e-02],
    [-1.423795211386183479e-01, 4.278974444751798556e-02, -9.888868032947215614e-01],
    [9.807660449651796064e-01, 1.408611430576996448e-01, -1.351151487429785303e-01]])
#RT = np.transpose(RT)
rvec = cv.Rodrigues(RT)[0]
print(rvec)
tvec = np.float64([-2.741854637247170823e-01, -4.599472972705090368e-02, 7.809504787062500342e-02]) 


# 相机内部参数
camera_matrix = np.float64([[1.0884950350184852e+03, 0,  9.4695426618613169e+02],
                            [0, 1.0938193104627710e+03,  6.1030563788249447e+02],
                            [0, 0, 1]])  # 相机内部参数

# 相机形变矩阵
distCoeffs = np.float64([-1.2513805215520665e-01, 9.1613181903773405e-02,
                         -5.2811413733704149e-03, -2.1819806858093831e-04, -3.0002234321010124e-02]) 
point_2d, _ = cv.projectPoints(cube, rvec, tvec, camera_matrix, distCoeffs)

m=-1
for point in point_2d:
    m=m+1
    x_2d = point[0][0]
    y_2d = point[0][1]

    if 0<=x_2d<=1920 and 0<=y_2d<=1200:
        x.append(x_2d)
        y.append(y_2d)
        distance.append(-distance_3d[m]*100)#数值取反是为了让colormap颜色由红到蓝显示而非由蓝到红
        RGB=pix[x_2d,y_2d]
        print('x,y,z,(r,g,b):',([x_2d,y_2d,distance_3d[m]],RGB))


x=np.array(x)
y=np.array(y)
plt.scatter(x, y, c=distance, cmap='jet',s=4,marker='.')
plt.imshow(im)
#plt.show()
plt.savefig("pointsimg.png",dpi=500,bbox_inches = 'tight')


