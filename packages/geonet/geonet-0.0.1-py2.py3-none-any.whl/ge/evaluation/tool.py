import time
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
import networkx as nx

from sklearn.linear_model import LogisticRegression
from sklearn.manifold import TSNE
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix

from ge.classify import Classifier, read_node_label_from_csv


# ground_truth：标签的真值
def evaluate_embeddings(embeddings, ground_truth):

    # 这个为什么可以读标签？
    # 下面读的都是偶数行
    # X是node id：['0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', ...]
    # Y是lable：  [['0'], ['0'], ['0'], ['0'], ['1'], ['0'], ['3'], ['3'], ['3'], ['1'], ['3'], ['1'], ['0'], ['1'],...]
    X, Y = read_node_label_from_csv(ground_truth)

    tr_frac = 0.8

    print("Training classifier using {:.2f}% nodes...".format(

        tr_frac * 100))

    clf = Classifier(embeddings=embeddings, clf=LogisticRegression())

    clf.split_train_evaluate(X, Y, tr_frac)


# 经常出现的问题是，混淆矩阵已经非常好了，但是图像还是很差
# tsne标签评估，输出地址：./result/grid-result-时间
def plot_embeddings(embeddings, ground_truth):

    '''
    embeddings格式：
    {
        '节点编号'：array([嵌入维度数],dtype = floa32),
        ...(遍历所有节点)
    }

    比如：
    {
        '10': array([3.26998353e-01, -1.39750559e-02, 1.82545796e-01, ...共128列 ], dtype = float32),
        '11': array([-0.17985347, 0.08804768, -0.21643116, ... 共128列 ], dtype = float32),
        ...
    }
    '''

    # X是节点列表： ['10', '12', '14', ... ]
    # Y是标签列表：[['0'], ['10'], ['0'], ...]
    X, Y = read_node_label_from_csv(ground_truth)
    emb_list = []
    for k in X:
        emb_list.append(embeddings[k])
    # emb_list是个二维数组，每一行是一个节点嵌入后的向量：
    # [[-0.2907387  -0.23431493  0.20258395 ... -0.23829292]
    #  [-0.30266264  0.04610238  0.20382825 ... 0.09379437]]
    emb_list = np.array(emb_list)

    # sklearn.manifold.TSNE 函数
    # n_components : int, default=2 Dimension of the embedded space.
    # 使用方法，是mode.fit_transform(self, X, y=None)，Fit X into an embedded space and return that transformed output.
    model = TSNE(n_components=2, method='exact')  # 图像是二维的，嵌入2维空间


    # 参考这个文章，TSNE主要是计算多维数组的聚类：https://blog.csdn.net/Avery123123/article/details/104907491
    # 而下面评估的是emb_list，也就是embedding后（skip-gram后），也就是对于多维的隐藏层的聚类效果的可视化
    node_pos = model.fit_transform(emb_list)

    # color来源于，Y，来源于labels文件，是真值
    color_idx = {}

    for i in range(len(X)):
        color_idx.setdefault(Y[i][0], [])
        color_idx[Y[i][0]].append(i)
    for c, idx in color_idx.items():
        # c是颜色，是真值
        # node_pos来源于emb_list的TSNE，是embedding后的结果。位置代表embedding结果
        plt.scatter(node_pos[idx, 0], node_pos[idx, 1], label=c)  # c=node_colors)

    plt.legend()
    plt.savefig( './result/grid-result-'+time.strftime("%m%d %H:%M:%S", time.localtime()) + '.png')

    plt.show()


# 样例代码：https://github.com/dmlc/xgboost/blob/master/demo/guide-python/sklearn_examples.py
# 样例数据1：https://wenku.baidu.com/view/2af2b0f13286bceb19e8b8f67c1cfad6195fe90f.html
# 样例数据2：https://blog.51cto.com/u_15429890/4644135
def classify_embeddings(embeddings, ground_truth):
    '''
    下面是样例数据：
    iris = load_iris()
    y = iris['target']
    x = iris['data']
    print("x")
    print(x)
    print("y")
    print(y)
    '''

    # X是节点列表： ['10', '12', '14', ... ]
    # Y是标签列表：[['0'], ['10'], ['0'], ...]
    X, Y = read_node_label_from_csv(ground_truth)

    '''
    class_emb_list = []
    for k in X:
        class_emb_list.append(embeddings[k])
    emb_list = np.array(class_emb_list)

    # emb_list是个二维数组，每一行是一个节点嵌入后的向量：
    # [[-0.2907387  -0.23431493  0.20258395 ... -0.23829292]
    #  [-0.30266264  0.04610238  0.20382825 ... 0.09379437]]
    '''

    # 教程：XGBoost多分类预测 - Yolanda的文章 - 知乎 https://zhuanlan.zhihu.com/p/107682092
    # 用xgboost做分类，预测结果输出的为什么不是类别概率？ - 火眼狻猊的回答 - 知乎https://www.zhihu.com/question/337432675/answer/766393835
    # https://github.com/dmlc/xgboost/blob/master/demo/guide-python/sklearn_examples.py

    # sklearn函数：KFold（分割训练集和测试集）
    # n_splits：表示要分割为多少个K子集
    # shuffle：是否要洗牌（打乱数据）
    # random_state：随机数种子，shuffle时防止每次执行的训练集都不同，随意给个整数即可
    kf = KFold(n_splits=2, shuffle=True, random_state=100)

    '''
    n_splits等于几，就返回个结果
    比如n_splits=3，则a, b, c = kf.split(X)，打印出来
    a=(array([ 0,  1,  4,  8,  9, 10, ...]), array([ 2,  3,  5,  6,  7, ...]))
    b=(array([ 0,  2,  3,  5,  6,  7,  8,  9, ...]), array([ 1,  4, 10, ...]))
    c=(array([ 1,  2,  3,  4,  5,  6,  7, 10, ...]), array([ 0,  8,  9, ...]))
    这两个数组合起来是全集, 注意只是序号，不是本身的内容
    '''

    # 上面n_splits是几，就循环几次，train_index和test_index分别是每个结果的第一组和第二组数
    for train_index, test_index in kf.split(X):
        # 用train_index抽出来的序号，进行训练
        class_emb_list = []
        class_label_list = []
        for k in train_index:
            class_emb_list.append(embeddings[X[k]])
            class_label_list.append(int(Y[k][0]))  # 不转换成数字，用字符串的形式，后面执行会报错
        emb_list = np.array(class_emb_list)
        label_list = np.array(class_label_list)

        '''
        emb_list (长度20）
        [[-0.38700065 -0.04681021  0.01026177 ...  0.54785144  0.07182406 0.11215009]
         ...
         [-0.22765955  0.05759353 -0.11421331 ... -0.14032339 -0.01040465 -0.31992567]]
        label_list （长度20）
        ['0' '10' '6' '5' '0' '2' '0' '2' '0' '11' '2' '2' '2' '2' '2' '0' '11' '10' '10' '5']
        '''

        '''
        xgboost.train()和xgboost.XGBClassifier().fit()的区别：
        xgboost.train是底层API，而xgboost.XGBRegressor和xgboost.XGBClassifier是上层包装器

        # 1 xgboost.XGBClassifier().fit()      
        xgm = xgb.XGBClassifier()
        xgm.fit(X_train, y_train)   
        y_pred = xgm.predict(X_train)  

        2# xgboost.train()
        param = {'max_depth':2, 'eta':1, 'silent':1, 'objective':'binary:logistic' }
        num_round = 2
        bst = xgb.train(param, dtrain, num_round)
        preds = bst.predict(dtest)
        '''
        xgb_model = xgb.XGBClassifier(n_jobs=1).fit(emb_list, label_list)

        # 用test_index抽出来的序号，进行预测
        class_emb_list_test = []
        class_label_list_test = []
        for k_t in test_index:
            class_emb_list_test.append(embeddings[X[k_t]])
            class_label_list_test.append(int(Y[k_t][0]))
        emb_list_test = np.array(class_emb_list_test)
        predictions = xgb_model.predict(emb_list_test)
        actuals = class_label_list_test

        '''
        混淆矩阵：
        纵坐标：真实分类
        横坐标：预测分类
        对角上的元素越多越好
        '''
        print("confusion_matrix")
        print(confusion_matrix(actuals, predictions))

        '''
        https://zhuanlan.zhihu.com/p/83620830?utm_source=wechat_session
        【不需要调优的参数】
        * booster ： [default=gbtree] 决定类型 ，gbtree : 树模型 gblinear :线性模型。
        * objective :
            - binary:logistic 用来二分类
            - multi:softmax 用来多分类
            - reg:linear 用来回归任务
        * silent [default=0]:
            - 设为1 则不打印执行信息
            - 设为0打印信息
        * nthread ：控制线程数目

        【可以优化的参数】
        * max_depth: 决定树的最大深度，比较重要 常用值4-6 ，深度越深越容易过拟合。
        * n_estimators: 构建多少颗数 ，树越多越容易过拟合。
        * learning_rate/eta : 学习率 ，范围0-1 。默认值 为0.3 , 常用值0.01-0.2
        * subsample: 每次迭代用多少数据集 。
        * colsample_bytree: 每次用多少特征 。可以控制过拟合。
        * min_child_weight :树的最小权重 ，越小越容易过拟合。
        * gamma：如果分裂能够使loss函数减小的值大于gamma，则这个节点才分裂。gamma设置了这个减小的最低阈值。如果gamma设置为0，表示只要使得loss函数减少，就分裂。
        * alpha：l1正则，默认为0
        * lambda ：l2正则，默认为1
        '''
        # dtrain = xgb.DMatrix(emb_list, label=label_list)
        # param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'multi:softmax'}
        # modelXG = xgb.train(param, dtrain, xgb_model='xgbmodel')
        # modelXG.save_model("xgbmodel")



def plot_data(G):
    # 用networkx做网络关系可视化
    # https://www.jianshu.com/p/6292e45da3d0
    # 结果存在./result目录里，文件名用日期来区分
    nx.draw(G,
        pos = nx.random_layout(G), # pos 指的是布局,主要有spring_layout,random_layout,circle_layout,shell_layout
        node_color = 'b',   # node_color指节点颜色,有rbykw,同理edge_color
        edge_color = 'r',
        with_labels = True,  # with_labels指节点是否显示名字
        font_size =18,  # font_size表示字体大小,font_color表示字的颜色
        node_size =20)  # font_size表示字体大小,font_color表示字的颜色
    plt.savefig( './result/grid-data-'+time.strftime("%m%d %H:%M:%S", time.localtime()) + '.png')
