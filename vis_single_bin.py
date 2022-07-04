import open3d as o3d
import numpy as np 


def get_pointcloud(pc_type):
    # rotate = T_from_radar_to_lidar[0:3, 0:3]
    # translation = T_from_radar_to_lidar[0:3, 3]
    if pc_type == 'lidar':
        lidar_file = "C:\\Users\\12975\Desktop\\000032_lidar.txt"
        # assert lidar_file.exists()
        return np.loadtxt(str(lidar_file), dtype=np.float32, skiprows=1, usecols=(0, 1, 2))
    elif pc_type == 'radar':
        radar_file = "C:\\Users\\12975\Desktop\\000032_radar.txt"
        # assert radar_file.exists()
        return np.loadtxt(str(radar_file), dtype=np.float32, skiprows=2, usecols=(0, 1, 2))
    elif pc_type == 'fusion':
        lidar_file = "D:\\astyx\\astyx\\training\\lidar_vlp16\\000036.txt"
        # assert lidar_file.exists()
        lidar = np.loadtxt(str(lidar_file), dtype=np.float32, skiprows=1, usecols=(0, 1, 2))
        radar_file = "D:\\astyx\\astyx\\training\\radar_6455\\000036.txt"
        # assert radar_file.exists()
        radar = np.loadtxt(str(radar_file), dtype=np.float32, skiprows=2, usecols=(0, 1, 2))
        # lidar[:, :3] = np.dot(lidar[:, :3], rotate)
        # lidar[:, :3] += translation
        # x = radar[:, 0]
        # z = radar[:, 2]
        # x = np.sqrt(x*x + z*z)*np.cos(20/96*np.arctan2(z, x))
        # z = np.sqrt(x*x + z*z)*np.sin(20/96*np.arctan2(z, x))
        # radar[:, 0] = x
        # radar[:, 2] = z

        # x = radar[:, 0]
        # z = radar[:, 2]
        # x = np.sqrt(x*x + z*z)*np.cos(20/96*np.arctan2(z, x))
        # z = np.sqrt(x*x + z*z)*np.sin(20/96*np.arctan2(z, x))

        # angle = np.pi/180 * (4)
        # x = x*np.cos(angle) - z*np.sin(angle)
        # z = x*np.sin(angle) + z*np.cos(angle)
        # radar[:, 0] = x
        # radar[:, 2] = z
        return lidar, radar
    else:
        pass



def main():
    lidar,radar = get_pointcloud('fusion')
    raw_point = np.array(radar) #读取1.npy数据  N*[x,y,z]
    # raw_point[:,1]= 0 
    # lidar[:,1]=0
    
    #创建窗口对象
    vis = o3d.visualization.Visualizer()
    #设置窗口标题
    vis.create_window(window_name="kitti")
    #设置点云大小
    vis.get_render_option().point_size = 5
    #设置颜色背景为bai色
    opt = vis.get_render_option()
    opt.background_color = np.asarray([1, 1, 1])
    # opt.line_width = 3
    # opt.show_coordinate_frame = True
    #创建点云对象
    pcd1=o3d.open3d.geometry.PointCloud()
    pcd2=o3d.open3d.geometry.PointCloud()
    #将点云数据转换为Open3d可以直接使用的数据类型
    pcd1.points= o3d.open3d.utility.Vector3dVector(raw_point)
    pcd2.points= o3d.open3d.utility.Vector3dVector(lidar)




    origin = [0,0,0]
    # 坐标系
    coordinate = o3d.geometry.TriangleMesh.create_coordinate_frame(size=50,origin=origin)
    
    # 可视化
    # o3d.visualization.draw_geometries([lidar])
    # o3d.visualization.draw_geometries([pcd2, coordinate])



    #设置点的颜色为白色
    pcd1.paint_uniform_color([1,0,1])
    pcd2.paint_uniform_color([0,1,1])
    #将点云加入到窗口中
    vis.add_geometry(pcd1)
    vis.get_render_option().point_size = 2
    vis.add_geometry(pcd2)
    vis.add_geometry(coordinate)
    vis.run()
    vis.capture_screen_image("1111.png")
    vis.destroy_window()

    
if __name__=="__main__":
    # radar = get_pointcloud('radar')
    # print(radar)
    main()