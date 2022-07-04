

# 融合算法的回调函数
def multicallback(sub_pcd,sub_img):
    # 从topic读数据
    pc = pypcd.PointCloud.from_msg(sub_pcd)
    x = pc.pc_data['x'].flatten()
    y = pc.pc_data['y'].flatten()
    z = pc.pc_data['z'].flatten()
    intensity = pc.pc_data['intensity'].flatten()

    point_data = np.zeros(x.shape[0] + y.shape[0] + z.shape[0] + intensity.shape[0], dtype=np.float32)
    # 将topic形式的数据转换成模型需要的numpy数据格式
    point_data[::4] = x
    point_data[1::4] = y
    point_data[2::4] = z
    point_data[3::4] = 0
    point_data = point_data.astype(float)

    input_img = sub_img
    sub_img = np.frombuffer(input_img.data,dtype= np.uint8).reshape(input_img.height,input_img.width,-1)

    result, data = inference_multi_modality_detector(model, point_data,sub_img)
    bbox = convert_valid_bboxes(result[0])['box3d_lidar']

    corners_3d_velos = []
    de_ids = []

    ziped = zip(result[0]['scores_3d'], result[0]['labels_3d'])
    # 条件过滤，car的置信度设高，其余低
    for id, (score, label) in enumerate(ziped):
        if label == 2:
            if score < 0.7:
                de_ids.append(id)
        else:
            if score < 0.3:
                de_ids.append(id)

    bboxes = np.delete(bbox,de_ids,axis=0)
    # 将各个框的表达方式转换成8个顶点
    for box in bboxes:
        corners_3d_velo = compute_3d_box(box).T
        corners_3d_velos += [corners_3d_velo]

    # 发布3d框
    publish_3dbbox(bbox_publisher,corners_3d_velos)
    # 发布3d框给tracking
    pub_bbox_info(bbox_info_puber, bboxes)





# 点云与图像融合检测
def pcd_and_img_listener():
   # 订阅点云topic,名称改为ros发布的pointcloud2名称
   sub_pcd = mf.Subscriber('/rslidar_points', PointCloud2)
   # 订阅图像topic,名称改为ros发布的image_raw名称
   sub_img = mf.Subscriber('/usb_cam/image_raw', numpy_msg(Image))
   # 同步订阅点云与图像
   sync = mf.ApproximateTimeSynchronizer([sub_pcd, sub_img],10,1)
   sync.registerCallback(multicallback)
   rospy.spin()