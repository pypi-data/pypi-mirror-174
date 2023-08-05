import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics

'''
利用dbscan做聚类

样例数据：
X是矢量集合
X = [
[-1.6822287,0.619684],
[-1.6691374,0.68791944],
[-1.5431411,0.64482975],
[-1.710473,0.69649506]
...
]

Y是对应的标签
Y = [['0'], ['0'], ['1'], ['1']...]
'''
def train_cluster(X):
    db = DBSCAN(min_samples=2).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    # 此label是分类后的类别标签，不是手动打的那个
    print(labels)
    print("Estimated number of clusters: %d" % n_clusters_)
    print("Estimated number of noise points: %d" % n_noise_)
    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))

    return labels



# 聚类功能
'''
输入一个目标向量的序号，返回同一类向量的序号列表
'''
def find_cluster(index, labels):
    find_dic = {}
    for i, label in enumerate(labels):
        if not label in find_dic:
            find_dic[label] = []
        find_dic[label].append(i)

    i_label = labels[index]

    result = find_dic[i_label]

    return result
