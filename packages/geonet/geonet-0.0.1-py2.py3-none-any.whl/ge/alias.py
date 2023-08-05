import numpy as np


def create_alias_table(area_ratio):
    """

    :param area_ratio: sum(area_ratio)=1
    :return: accept,alias
    """
    l = len(area_ratio)
    accept, alias = [0] * l, [0] * l
    small, large = [], []
    # 注意，星号乘法是对应元素相乘.flight的案例里，一般是有大有小比如1。089，0.73
    # 因为area_ratio求和是1，所以area_ratio_乘完自己的长度，都是一个跟1差不多的值
    area_ratio_ = np.array(area_ratio) * l
    # 这里面small和large存的是area_ratio_大于和小于1元素的编号
    for i, prob in enumerate(area_ratio_):
        if prob < 1.0:
            small.append(i)
        else:
            large.append(i)

    while small and large:
        small_idx, large_idx = small.pop(), large.pop()
        # 小于1的被接受，值放进accept里。非接受的还是0
        accept[small_idx] = area_ratio_[small_idx]
        # 大于1的，编号依次放到alias的接受位置里。
        alias[small_idx] = large_idx
        # 大的值，减去小的值与1的差
        area_ratio_[large_idx] = area_ratio_[large_idx] - \
            (1 - area_ratio_[small_idx])
        # 继续，小于1的放到小的里面，大于1的往大的里面放
        if area_ratio_[large_idx] < 1.0:
            small.append(large_idx)
        else:
            large.append(large_idx)

    while large:
        # accept大的位置变为1
        large_idx = large.pop()
        accept[large_idx] = 1
    while small:
        # accept小的位置变为1
        small_idx = small.pop()
        accept[small_idx] = 1

    return accept, alias


def alias_sample(accept, alias):
    """

    :param accept: 给每个节点一个0～1的数。现在看起来都太小了（e-10，基本上全命中）
    :param alias: 每个元素都一样，比较奇怪。这两个入参有问题，需要查一下
    :return: sample index
    """
    N = len(accept)
    # 先随机选个节点
    i = int(np.random.random()*N)
    r = np.random.random()
    # 如果节点的数大于某个随机数r，则返回节点i的id。否则，返回
    if r < accept[i]:
        return i
    else:
        return alias[i]
