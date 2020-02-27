# 线性回归计算：

1. 确定一个假设的函数关系
2. 确定一个损失函数（cost）  最小二乘法
3. 求最优解（cost求导数 == 0 w最优解）
4. 计算出w系数，相当于求出了假设的函数关系

[Ridge、Lasso]添加了惩罚系数，估计函数是一样的，他们都属于狭义线型回归模型

# LinearRegression(fit_interception=True)

优点：计算效率高，大部分时间花费在训练上，预测过程快

缺点：如果数据存在多重共线性，算法表现极其不稳定

普通线型回归模型，无法消除多重共线性、样本个数少于样本特征的情况，所以引入其他模型：岭回归、劳斯回归

# Ridge回归

引入了二阶正则项的线型回归模型，引入了这个偏差，可以让样本集变成一个奇异矩阵，进而使得样本集可以求逆，进而可以求解。达到缩减系数的目的，可以更好的理解数据。

岭回归只能处理**回归**问题，不能处理线型问题

关系ridge系数，不应该取太大或太小的值。太大所有的系数会无线趋向于0，太小会导致系数波动很大，导致算法很不稳定

为了确认这个系数，可以绘制岭迹线（应该取所有系数都围绕在0上下的区间）


# Lasso回归

引入了惩罚项来压缩系数，$$|W|.sum < λ$$，达到索引效果

Ridge、Lasso算法都属于缩减算法

**缩减**不是**降维**

缩减：将对数据没有影响的维度筛除

降维：降维就是指采用某种映射方法，将原高维空间中的数据点映射到低维度的空间中。降维的本质是学习一个映射函数$$ f :x \rightarrow y$$，其中x是原始数据点的表达，目前最多使用向量表达形式。


# 线型回归模型有截距

如何求最优解？

梯度下降法（当无法求导 == 0时，可以采用多次迭代来计算最优解）

**梯度**：在微积分里面，对多元函数的参数求∂偏导数，把求得的各个参数的偏导数以向量的形式写出来，就是梯度。比如函数$$f(x,y)$$, 分别对x,y求偏导数，求得的梯度向量就是$$({{∂f}\over{∂x}}, {{∂f}\over {∂y}})T$$,简称$$grad\quad f(x,y)$$或者$$▽f(x,y)$$。对于在点$$(x_0,y_0)$$的具体梯度向量就是$$({{∂f}\over{∂x}}, {{∂f}\over {∂y}})T$$.或者$$▽f(x_0,y_0)$$，如果是3个参数的向量梯度，就是$$({{∂f}\over{∂x}}, {{∂f}\over {∂y}})T$$,以此类推。



# logistic逻辑斯蒂回归

广义线性回归模型。利用Logistics回归进行分类的主要思想是：根据现有数据对分类边界线建立回归公式，以此进行分类。这里的“回归” 一词源于最佳拟合，表示要找到最佳拟合参数集。

$\ln{{y}\over{(1-y)}}=w\times x + b$  对数几率回归，源自于sigmoid函数$f(x) = {{1}\over {(1 + e^{-x})}}$

$\ln y = w \times x + b$


$y = \begin{cases}1, x\gt 0\\0.5, x = 0\\0, x \lt 0 \end{cases}阶跃函数$

处理分类问题，二分类问题。

## 极大似然估计

极大似然估计：只是一种概率论在统计学的应用，它是参数估计的方法之一。说的是已知某个随机样本满足某种概率分布，但是其中具体的参数不清楚，参数估计就是通过若干次试验，观察其结果，利用结果推出参数的大概值。极大似然估计是建立在这样的思想上：已知某个参数能使这个样本出现的概率最大，我们当然不会再去选择其他小概率的样本，所以干脆就把这个参数作为估计的真实值。

## 优缺点

优点：运算效率高，易于理解

缺点：容易欠拟合

**过拟合**产生原因：对无用的特征国度学习。

避免：降维（特征选择、PCA、缩减算法）

## logistic实现过程

Logistic Regression和Linear Regression的原理是相似的，可以简单的描述为这样的过程：

1. 找一个合适的预测函数，一般表示为h函数，该函数就是我们需要找的分类函数，它用来预测输入数据的判断结果。这个过程是非常关键的，需要对数据有一定的了解或分析，知道或者猜测预测函数的“大概”形式，比如是线性函数还是非线性函数
2. 构造一个Cost函数（损失函数），该函数表示预测的输出（h）与训练数据类别（y）之间的偏差，可以是二者之间的差（h-y）或者是其他的形式。综合考虑所有训练数据的“损失”，将Cost求和或者求平均，记为$$J(θ)$$函数，表示所有训练数据预测值与实际类别的偏差
3. 显然，$$J(θ)$$函数的值越小表示预测函数越准确（即h函数越准确），所以这一步需要做的是找到$$J(θ)$$函数的最小值。找函数的最小值有不同的方法，Logistic Regression实现时有梯度下降法（Gradient Descent）


## LogisticRegression

导入sklearn库

```python
from sklearn.linear_model import LogisticRegression
```

使用这个类，实例化一个训练器对象，参数主要为：

```python
LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, 
                   fit_intercept=True, intercept_scaling=1, class_weight=None, 
                   random_state=None, solver='liblinear', max_iter=100,
                   multi_class='ovr', verbose=0, warm_start=False, n_jobs=1)
```

- penalty：指定正则化策略，即惩罚项，str类型，可选L1,L2，默认L2
- dual：是否求解对偶形式。对偶方法只用在求解线性多核(liblinear)的L2惩罚项上。当样本数量>样本特征的时候，dual通常设置为False。
- tol：停止求解的标准，float类型，默认为1e-4。就是求解到多少的时候，停止，认为已经求出最优解。
- C：惩罚项系数的倒数，越大，正则化项越小，越容易欠拟合，越小越容易过拟合。必须是正浮点型数。像SVM一样，越小的数值表示越强的正则化。
- fit_intercept：是否拟合截距
- intercept_scaling：当solver='liblinear'、fit_intercept=True时，会制造出一个恒为1的特征，权重为b，为了降低这个人造特征对正则化的影响，可以将其设为1
- class_weight：可以是一个字典或'balanced'。字典：可以指定每一个分类的权重；'balanced'：可以指定每个分类的权重与该分类在训练集中的频率成反比
- max_iter：最大迭代数，int类型，默认为10。仅在正则化优化算法为newton-cg, sag和lbfgs才有用，算法收敛的最大迭代次数。
- random_state：int或RandomState对象，随机数种子，控制随机方式，可以控制每次随机的结果是一样的，便于调参。仅在正则化优化算法为sag,liblinear时有用。
- solver：指定求解最优化问题的算法：
    - 'newton-cg':牛顿法，利用损失函数二阶导数矩阵即海森矩阵来迭代优化损失函数。
    - 'lbfgs':拟牛顿法，利用损失函数二阶导数矩阵即海森矩阵来迭代优化损失函数。
    - 'liblinear':使用liblinear，适用于小数据集
    - 'sag':使用Stochastic Average Gradient Descent算法(适用于大数据集)
- multi_class：
    - 'ovr':采用one-vs-class策略
    - 'multi_class':采用多类分类Logistic回归
- verbose：日志冗长度，int类型。默认为0。就是不输出训练过程，1的时候偶尔输出结果，大于1，对于每个子模型都输出。
- warm_start：是否使用前一次训练结果继续训练
- n_jobs：任务并行时指定使用的CPU数，-1表示使用所有可用的CPU

属性：

- coef_：权重向量，斜率
- intercept_：截距b
- n_iter_：实际迭代次数

方法：

- `fit(X, y[, sample_weight])`：训练模型
- `predict_log_proba(x)`：返回x预测为各类别概率的对数
- `predict_proba(x)`：返回x预测为各类别的概率
- `score(X, y[, sample_weight])`：计算在(X, y)上的预测的准确率

## 逻辑斯蒂回归代码步骤

1. 创建一个逻辑斯蒂回归对象

```python
lr = LogisticRegression()
```
2. 喂数据，训练模型

```python
train, target = make_blobs(n_samples=150, n_features=2, centers=3,
                           random_state=4, cluster_std=[1.5, 1.1, 1.3])
lr.fit(train, target)
```

分析`make_blobs()`的参数：

```python
make_blobs(n_samples=100, n_features=2, centers=3, cluster_std=1.0, 
           center_box=(-10.0, 10.0), shuffle=True, random_state=None)
		
```

- n_samples：产生的样本数据个数
- n_features：数据的特征数
- centers：随机数据的中心点个数，数据将会围绕中心点分布
- cluster_std：集群的标准差
- shuffle：布尔值，是否进行数据洗牌
- random_state：int或RandomState对象，随机数种子，控制随机方式，可以控制每次随机的结果是一样的，便于调参

3. 绘制分类边界，查看分类情况

```python
# 分类边界
x = np.linspace(train[:, 0].min()-0.5, train[:, 0].max()+0.5, 200)
y = np.linspace(train[:, 1].min()-0.5, train[:, 1].max()+0.5, 200)

xx, yy = np.meshgrid(x, y)
# 生成测试数据
test = np.c_[xx.ravel(), yy.ravel()]

# 获取测试结果
y = lr.predict(test)
```


