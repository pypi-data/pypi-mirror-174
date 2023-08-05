import math


## 参考：https://glenbambrick.com/tag/shapely/
## 返回的是-90~90锐角，需要再加工
def getAcuteAngle(pt1, pt2):
    x_diff = pt2.x - pt1.x
    y_diff = pt2.y - pt1.y
    return math.degrees(math.atan2(y_diff, x_diff))  # atan2返回的是一个绝对值小于180的值，逆时针为整数，顺时针为负数


## 以orgin_pt为圆心，获得target_pt相对的0~360的角度
def getAngle(orgin_pt, target_pt):
    angle = getAcuteAngle(orgin_pt, target_pt)
    # 把-180~180改到0~360
    if angle < 0:
        angle = angle + 360

    # 坐标轴旋转
    angle = angle + 90
    if angle > 360:
        angle = angle - 360

    return angle
