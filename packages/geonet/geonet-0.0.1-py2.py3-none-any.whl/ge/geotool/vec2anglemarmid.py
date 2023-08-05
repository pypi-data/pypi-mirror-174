import pandas as pd
from shapely.geometry import Point, LineString
from shapely import wkt
from .geoplot import multiple_plot
from .geoangle import getAngle

WKT_COL = 'wkt_geom'  # 老版本是'WKT'


# 提取图形的线计算所需要计算的点：端点、交叉点
def get_lines(file_path):
    df = pd.read_csv(file_path, header=0)
    # print(df.head(5)) # 输出前五行数据查看
    lines_group = []  # 线段列表

    for index, row in df.iterrows():
        wkt_line = row[WKT_COL]
        s_line = wkt.loads(wkt_line)
        # print(s_line) # 打印wkt格式的line
        # print(s_line.coords[:]) # 打印坐标
        lines_group.append(s_line)
    return lines_group


# 根据图形计算所需要计算的点：端点、交叉点
def get_pointsandlabel(fromfile=True, containendpoint=False, containcrossopoint=False, pointfile_path='',
                       lines_group=[]):
    endpoints_group = []  # 端点列表

    point_dic = {}
    label_dic = {}

    if fromfile:
        df = pd.read_csv(pointfile_path, header=0)
        # print(df.head(5)) # 输出前五行数据查看
        for index, row in df.iterrows():
            wkt_point = row[WKT_COL]
            point_id = row['id']
            label = row['label']
            s_point = wkt.loads(wkt_point)
            # print(s_point) # 打印wkt格式的line
            # print(s_point.coords[:]) # 打印坐标
            endpoints_group.append(s_point)
            point_dic[point_id] = s_point
            label_dic[point_id] = label

    # 添加端点
    if containendpoint:
        for s_line in lines_group:
            first_endpoint = Point(s_line.coords[0])
            last_endpoint = Point(s_line.coords[-1])
            endpoints_group.append(first_endpoint)
            endpoints_group.append(last_endpoint)

    # 添加直线交点
    if containcrossopoint:
        for i in range(len(lines_group)):
            for j in range(i + 1, len(lines_group)):
                intersection_point = lines_group[i].intersection(lines_group[j])
                if intersection_point.is_empty != True:
                    endpoints_group.append(intersection_point)

    return endpoints_group, point_dic, label_dic


# 从一个顶点，计算环交点，返回角度列表、环交点、环本身
def cal_ring_intersection(orgin_point, reference_lines_group):
    radius_list = [0.1]  # 可以调节这个数组，来调节多少环，环的半径是多少
    angle_marmid = []
    plotpoints_total = []
    ring_total = []
    for radius in radius_list:
        # ring1 = orgin_point.buffer(0.5) # 返回的是polygon,求inteserction返回的是条线
        ring = orgin_point.buffer(radius).boundary  # 这样返回的是linestring，求inteserction返回的是multipoint

        # 求圆交点
        plotpoints = []
        for line in reference_lines_group:
            ring_intersection = ring.intersection(line)
            if ring_intersection.is_empty == False:
                if ring_intersection.geom_type == 'MultiPoint':
                    for i in range(len(ring_intersection.geoms)):
                        plotpoints.append(ring_intersection.geoms[i])
                else:
                    plotpoints.append(ring_intersection)

        #  求角度
        target_angle_list = []
        for point in plotpoints:
            target_angle = getAngle(orgin_pt=orgin_point, target_pt=point)
            target_angle_list.append(target_angle)
        target_angle_list.sort()

        angle_marmid.append(target_angle_list)
        plotpoints_total = plotpoints_total + plotpoints
        ring_total.append(ring)

    return angle_marmid, plotpoints_total, ring_total


# 全量节点的角度序列机选
def cal_group_anglelist(point_dic, lines_group):
    angle_list = {}
    ring_intersectpoint = []
    ring_list = []
    for id, orgin_point in point_dic.items():
        target_angle_list, plotpoints, ring = cal_ring_intersection(orgin_point, lines_group)
        angle_list[id] = target_angle_list
        ring_intersectpoint = ring_intersectpoint + plotpoints
        ring_list = ring_list + ring
    return angle_list, ring_intersectpoint, ring_list


# 画图
def plot_ringpoint(plotpoints, plotlines):
    multiple_plot(pointgroup=plotpoints, linegroup=plotlines)

