#coding:utf-8
import os
import rosbag
import cv2
from cv_bridge import CvBridge
from tqdm import tqdm
import time
import numpy as np
import open3d as o3d
import shutil

def read_pcd(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    colors = np.asarray(pcd.colors) * 255
    points = np.asarray(pcd.points)
    res=[]
    for i in points:
        res.append(np.array(list(i)+[0.]))
    return np.array(res)

class ExtractBagData(object):

    def __init__(self, bagfile_path, camera_topic, pointcloud_topic, root):
        self.bagfile_path = bagfile_path
        self.camera_topic = camera_topic
        self.pointcloud_topic = pointcloud_topic
        self.root = root
        self.image_dir = os.path.join(root, "image_2")
        self.pointcloud_dir = os.path.join(root, "pcds")
	self.pointcloud_dir_bins = os.path.join(root, "velodyne")
	self.calib_dir = os.path.join(root,"calib")
	self.ImageSets_dir = os.path.join(root,"ImageSets")

        #创建提取图片和点云的目录 ./root/images  root/pointcloud
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        if not os.path.exists(self.pointcloud_dir):
            os.makedirs(self.pointcloud_dir)
	if not os.path.exists(self.pointcloud_dir_bins):
            os.makedirs(self.pointcloud_dir_bins)
	if not os.path.exists(self.calib_dir):
            os.makedirs(self.calib_dir)
        if not os.path.exists(self.ImageSets_dir):
            os.makedirs(self.ImageSets_dir)

    
    def extract_camera_topic(self):
        bag = rosbag.Bag(self.bagfile_path, "r")
        bridge = CvBridge()
        bag_data_imgs = bag.read_messages(self.camera_topic)

        index = 0

        # for topic, msg, t in bag_data_imgs:
        # for topic, msg, t in tqdm(bag_data_imgs):
        pbar = tqdm(bag_data_imgs)
        for topic, msg, t in pbar:
            pbar.set_description("Processing extract image id: %s" % (index+1))
            cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
            # print('\033[31m=\033[0m'*120)
            # print(topic)  # /usb_cam/image_raw
            # print(msg)
            # print(t)  # 1616554905461126311
            #print(type(cv_image))  # <type 'numpy.ndarray'>
            # cv2.imshow("Image window", cv_image)
            # cv2.waitKey(3)
            # 如果你需要使用时间戳对提取的图片命名，可以使用msg.header.stamp.to_sec()获取时间戳
            # timestr = "%.6f" %  msg.header.stamp.to_sec()
            cv2.imwrite(os.path.join(self.image_dir, str(format(index,"06d")) + ".png"), cv_image)
            index += 1
	# 生成ImageSets,包括train.txt,val.txt,test.txt,trainval.txt
	path=self.ImageSets_dir

	f= open(path+'test.txt','w')
	for num in range(0,index):
	    f.write(format(num,'06d'))
	    f.write('\n')
	f.close()

	f= open(path+'trainval.txt','w')
	for num in range(1,index):
	    f.write(format(num,'06d'))
	    f.write('\n')
	f.close()

	f= open(path+'train.txt','w')
	for num in range(0,index):
	    f.write(format(num,'06d'))
	    f.write('\n')
	f.close()

	f= open(path+'val.txt','w')
	for num in range(0,index):
	    f.write(format(num,'06d'))
	    f.write('\n')
	f.close()
	# 生成calib
	src_path = "./calib.txt"
	des_path = self.calib_dir
	for i in range(0,index):
	    shutil.copyfile(src_path,des_path+str(format(i,"06d"))+".txt")
	    if os.path.exists(des_path+str(format(i,"06d"))+".txt"):
	       print("succeed",i)



    def extract_pointcloud_topic(self):
        '''
        # 提取点云数据为pcd后缀文件，默认提取以为时间戳命名
        # 提取命令：rosrun pcl_ros bag_to_pcd result.bag /velodyne_points ./pointcloud
        # 提取点云以时间戳命令：1616554905.476288682.pcd
        :return:
        '''
	
        cmd = "rosrun pcl_ros bag_to_pcd %s /rslidar_car_points %s" % (self.bagfile_path, self.pointcloud_dir)
        os.system(cmd)
	
        # 再读取提取的pcd点云数据，把文件名修改为按照顺序索引名
        pcd_files_list = os.listdir(self.pointcloud_dir)
        # 因为提取的pcd是以时间戳命令的，但是存放到列表中并不是按照时间戳从小到大排列，这里对时间戳进行重新排序
        pcd_files_list_sorted = sorted(pcd_files_list)
	print(pcd_files_list_sorted)
        # print(zip(pcd_files_list, pcd_files_list_sorted))

        index = 0
        pbar = tqdm(pcd_files_list_sorted)
        for pcd_file in pbar:
            pbar.set_description("Processing extract poindcloud id: %s" % (index + 1))
	    velodyne_file = os.path.join(self.pointcloud_dir, pcd_file)
	    pl = read_pcd(velodyne_file)
            pl = pl.reshape(-1, 4).astype(np.float32)
            velodyne_file_new = os.path.join(self.pointcloud_dir_bins, str(format(index,"06d")) + '.bin')
	    print(velodyne_file_new)
            pl.tofile(velodyne_file_new)
            #os.rename(os.path.join(self.pointcloud_dir, pcd_file),
                      #os.path.join(self.pointcloud_dir, str(format(index,"06d")) + ".pcd"))
	    
            print("pcd_file name: ", pcd_file)
            index += 1



if __name__ == '__main__':
    # bagfile_path = "/home/shl/extract_rosbag_data/0324_bags/plycal_calib/2021-03-24-11-01-45.bag"
    # camera_topic = "/usb_cam/image_raw"
    # pointcloud_topic = "/velodyne_points"
    # extract_bag = ExtractBagData(bagfile_path, camera_topic, pointcloud_topic,  "root")
    # extract_bag.extract_camera_topic()
    # extract_bag.extract_pointcloud_topic()



    bagfile_path = "./傍晚/城市支路/2022-02-21-18-51-58.bag"
    camera_topic = "/ca_front_right/image_raw"
    pointcloud_topic = "/rslidar_car_points"
    extract_bag = ExtractBagData(bagfile_path, camera_topic, pointcloud_topic,"output/extract_data/傍晚/城市支路/")
    extract_bag.extract_camera_topic()
    extract_bag.extract_pointcloud_topic()
