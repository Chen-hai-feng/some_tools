
# 单一点云检测的回调函数
def detecCallBack(pcd2_data):
    # 从topic读数据
    pc = pypcd.PointCloud.from_msg(pcd2_data)

    x = pc.pc_data['x'].flatten()
    y = pc.pc_data['y'].flatten()
    z = pc.pc_data['z'].flatten()
    intensity = pc.pc_data['intensity'].flatten()
    # 将topic形式的数据转换成模型需要的numpy数据格式
    point_data = np.zeros(x.shape[0] + y.shape[0] + z.shape[0] + intensity.shape[0], dtype=np.float32)

    point_data[::4] = x
    point_data[1::4] = y
    point_data[2::4] = z
    point_data[3::4] = 0


    point_data = point_data.astype(float)

    result, data = inference_detector(model, point_data)
    bbox = convert_valid_bboxes(result[0])['box3d_lidar']

    corners_3d_velos = []
    de_ids = []

    print(result[0]['labels_3d'])
    # 条件过滤，car的置信度设高，其余低
    ziped = zip(result[0]['scores_3d'],result[0]['labels_3d'])
    for id,(score,label) in enumerate(ziped):
        # if score <0.7 :
        #     de_ids.append(id)
        if label != 1:
            de_ids.append(id)

    bboxes  = np.delete(bbox, de_ids,axis=0)
    # 将各个框的表达方式转换成8个顶点
    for box in bboxes:
        corners_3d_velo = compute_3d_box(box).T
        corners_3d_velos += [corners_3d_velo]
    # 发布3d框
    publish_3dbbox(bbox_publisher,corners_3d_velos)
    pub_bbox_info(bbox_info_puber, bboxes)