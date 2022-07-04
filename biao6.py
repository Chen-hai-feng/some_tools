import sys
import vispy
import numpy as np
import json
import math
from vispy.scene import visuals, SceneCanvas

def load(radar, lidar, calib):
    # def load(radar, lidar, calib, gtbox):
    radar = np.loadtxt(radar, dtype=np.float32, skiprows=2, usecols=(0,1,2))
    x = radar[:, 0]
    z = radar[:, 2]
    x = np.sqrt(x*x + z*z)*np.cos(20/96*np.arctan2(z, x))
    z = np.sqrt(x*x + z*z)*np.sin(20/96*np.arctan2(z, x))
   
    angle = np.pi/180 * (7)
    x = x*np.cos(angle) - z*np.sin(angle)
    z = x*np.sin(angle) + z*np.cos(angle)
    radar[:, 0] = x
    radar[:, 2] = z



    lidar = np.loadtxt(lidar, dtype=np.float32, skiprows=2, usecols=(0,1,2))
    radar[:,1]=0
    lidar[:,1]=0
    with open(calib) as f:
        calib = json.load(f)
    # with open(gtbox) as f:
    #     gtbox = json.load(f)
    return radar, lidar, calib 

def inv_trans(T):
    rotation = np.linalg.inv(T[0:3, 0:3])  # rotation matrix
    translation = T[0:3, 3]
    translation = -1 * np.dot(rotation, translation.T)
    translation = np.reshape(translation, (3, 1))
    Q = np.hstack((rotation, translation))
    return Q

def transforms(lidar, calib):
    T_from_lidar_to_radar = np.array(calib['sensors'][1]['calib_data']['T_to_ref_COS'])
    T_from_radar_to_lidar = inv_trans(T_from_lidar_to_radar)
    rotate = np.array(T_from_radar_to_lidar[:, :3])
    translation = np.array(T_from_radar_to_lidar[:, 3:])
    lidar = np.dot(lidar, rotate)
    x = lidar[:, :1] - translation[0]
    y = lidar[:, 1:2] - translation[1]
    z = lidar[:, 2:3] - translation[2]
    lidar = np.concatenate([x, y, z], axis=1)
    return lidar

def my_compute_box_3d(center, size, heading_angle):
    h = size[2]
    w = size[0]
    l = size[1]
    heading_angle = -heading_angle - np.pi / 2 
    center[2] = center[2] + h / 2
    R = rotz(1*heading_angle)
    l = l/2
    w = w/2
    h = h/2
    x_corners = [-l,l,l,-l,-l,l,l,-l]
    y_corners = [w,w,-w,-w,w,w,-w,-w]
    z_corners = [h,h,h,h,-h,-h,-h,-h]
    corners_3d = np.dot(R, np.vstack([x_corners, y_corners, z_corners]))
    corners_3d[0,:] += center[0]
    corners_3d[1,:] += center[1]
    corners_3d[2,:] += center[2]
    return np.transpose(corners_3d)

def quart_to_rpy(x, y, z, w):
    roll = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    pitch = math.asin(2 * (w * y - x * z))
    yaw = math.atan2(2 * (w * z + x * y), 1 - 2 * (z * z + y * y))
    return roll, pitch, yaw

def rotation(center, size, angle, format='HWL', high_bias=True):
    H, W, L = size[format.find('H')], size[format.find('W')], size[format.find('L')]
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    box_2d = np.array([[L/2, W/2], [-L/2, W/2], [-L/2, -W/2], [L/2, -W/2]])
    box_2d = box_2d@R.transpose()
    box_3d = np.zeros([8, 3])
    if high_bias:
        box_3d[:4, :2], box_3d[:4, 2] = box_2d, H
        box_3d[-4:, :2], box_3d[-4:, 2] = box_2d, 0
    else:
        box_3d[:4, :2], box_3d[:4, 2] = box_2d, H/2
        box_3d[-4:, :2], box_3d[-4:, 2] = box_2d, -H/2

    return box_3d + center

def rotz(t):
    """Rotation about the z-axis."""
    c = np.cos(t)
    s = np.sin(t)
    return np.array([[c, -s,  0],
                     [s,  c,  0],
                     [0,  0,  1]])

def compute_gtbox(gtbox):
    # gtbox
    cube = np.zeros([len(gtbox['objects']), 7])
    corners_3d = np.zeros([len(gtbox['objects']), 8, 3])
    for i in range(len(gtbox['objects'])):
        x = gtbox['objects'][i]['orientation_quat'][0]
        y = gtbox['objects'][i]['orientation_quat'][1]
        z = gtbox['objects'][i]['orientation_quat'][2]
        w = gtbox['objects'][i]['orientation_quat'][3]
        roll, pitch, yaw = quart_to_rpy(x, y, z, w)

        cub = gtbox['objects'][i]['center3d'] + gtbox['objects'][i]['dimension3d']
        cub.append(roll)
        corners = my_compute_box_3d(cub[0:3], cub[3:6], cub[6])
        cube[i] = cub
        corners_3d[i] = corners

    return corners_3d

def compute_valbox(valbox):
    # valbox
    corners_3d = np.zeros([len(valbox), 8, 3])
    for i in range(len(valbox)):
        vbbox = valbox[i].split(' ')[11:14] + valbox[0].split(' ')[8:11]
        vbbox.append(valbox[0].split(' ')[14])
        vbbox[0] = float(vbbox[0])
        vbbox[1] = float(vbbox[1])
        vbbox[2] = float(vbbox[2])
        vbbox[3] = float(vbbox[3])
        vbbox[4] = float(vbbox[4])
        vbbox[5] = float(vbbox[5])
        vbbox[6] = float(vbbox[6])

        T_from_camera_to_radar = np.array(calib['sensors'][2]['calib_data']['T_to_ref_COS'])
        T_from_radar_to_camera = inv_trans(T_from_camera_to_radar)

        rotate = np.array(T_from_radar_to_camera[:, :3])
        translation = np.array(T_from_radar_to_camera[:, 3:])
        vbbox[0:3] = np.dot(vbbox[0:3], rotate)
        vbbox[0:3][0] = vbbox[0:3][0] - translation[0]
        vbbox[0:3][1] = vbbox[0:3][1] - translation[1]
        vbbox[0:3][2] = vbbox[0:3][2] - translation[2]

        corners_3d[i] = my_compute_box_3d(vbbox[0:3], vbbox[3:6], vbbox[6])
    
    return corners_3d

def compute_box_parameter(gtbox, corners_3d):
    num = len(gtbox['objects'])
    boxes = np.empty([0, 3])
    for box in corners_3d:
        boxes = np.concatenate((boxes, box), axis=0)
    box_c = np.array([[0, 1], [1, 2], [2, 3], [3, 0],
                        [4, 5], [5, 6], [6, 7], [7, 4],
                        [0, 4], [1, 5], [2, 6], [3, 7]])
    connect = np.empty([0, 2], dtype=np.int)

    for i in range(num):
        connect = np.concatenate((connect, box_c + 8*i), axis=0)
        # color_array = (1,0,1)

    # return boxes, color_array, connect
    return boxes, connect

if __name__ == '__main__':

    root_path = 'D:\\astyx\\astyx\\training\\'
    #### 初始化 ####
    canvas = SceneCanvas(keys='interactive', show=True, bgcolor='white')     # 创建画布

    grid = canvas.central_widget.add_view()


    key_input = '036'
    scan_vis_lidar0 = visuals.Markers()
    scan_vis_radar0 = visuals.Markers()

    #### 数据获取 ####
    # key_input = '031'

    radar = root_path+'radar_6455/000' + key_input + '.txt'
    lidar = root_path+'lidar_vlp16/000' + key_input + '.txt'
    calib = root_path+'calibration/000' + key_input + '.json'
    gtbox = root_path+'groundtruth_obj3d/000' + key_input + '.json'
    radar, lidar, calib= load(radar, lidar, calib)
    lidar = transforms(lidar, calib)

 
    # point_color
    radar_edge_color = [0,0,1]
    radar_face_color = radar_edge_color

    du = 0.5
    lidar_edge_color = [1,0,0]
    lidar_face_color = lidar_edge_color

    scan_vis_radar0.set_data(radar, edge_color=radar_edge_color, face_color=radar_face_color, size=5)
    scan_vis_lidar0.set_data(lidar, edge_color=lidar_edge_color, face_color=lidar_face_color, size=2)
    grid.add(scan_vis_radar0)
    grid.add(scan_vis_lidar0)

    grid.camera = 'turntable'  # or try 'arcball'
    axis = visuals.XYZAxis(parent=grid.scene)



    if sys.flags.interactive != 1:
        vispy.app.run() #开始运行

    
