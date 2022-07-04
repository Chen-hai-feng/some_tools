
# 计算每个3d框的8个顶点
def compute_3d_box(bbox):
    """
    :param bbox:
    bbox include (x,y,z,l,w,h,yaw)
    :return:
    3xn in velo coordinate
    """
    yaw = bbox[6]
    w = bbox[4]
    l = bbox[3]
    h = bbox[5]
    x = bbox[0]
    y = bbox[1]
    z = bbox[2]
    R = np.array([[np.cos(yaw), np.sin(yaw), 0], [-np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])
    x_corners = [l/2,l/2,-l/2,-l/2,l/2,l/2,-l/2,-l/2]
    y_corners = [w/2,-w/2,-w/2,w/2,w/2,-w/2,-w/2,w/2]
    z_corners = [-h/2,-h/2,-h/2,-h/2,h/2,h/2,h/2,h/2]

    corners_3d_velo = np.dot(R, np.vstack([x_corners,y_corners,z_corners]))
    corners_3d_velo += np.vstack([x, y, z+1])
    return corners_3d_velo
   


# 发布3d框
def publish_3dbbox(box3d_pub,corners_3d):
    marker_array = MarkerArray()
    for i , corners_3d_velo in enumerate(corners_3d):
        marker = Marker()
        marker.header.frame_id = Fram_id
        marker.header.stamp = rospy.Time.now()

        marker.id = i
        marker.action = Marker.ADD
        marker.lifetime = rospy.Duration(0.2)
        marker.type = Marker.LINE_LIST

        b, g, r = (255,255,0)
        marker.color.r = r/255.0
        marker.color.g = g/255.0
        marker.color.b = b/255.0

        marker.color.a = 1.0

        marker.scale.x = 0.1
        marker.points = []
        for l in LINES:
            p1 = corners_3d_velo[l[0]]
            marker.points.append(Point(p1[0], p1[1], p1[2]))
            p2 = corners_3d_velo[l[1]]
            marker.points.append(Point(p2[0], p2[1], p2[2]))
        marker_array.markers.append(marker)
    box3d_pub.publish(marker_array)

