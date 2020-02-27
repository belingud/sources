<h1>Python数据分析中的绘图函数<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#pandas" data-toc-modified-id="pandas-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>pandas</a></span><ul class="toc-item"><li><span><a href="#折线图" data-toc-modified-id="折线图-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>折线图</a></span><ul class="toc-item"><li><span><a href="#Series折线图" data-toc-modified-id="Series折线图-1.1.1"><span class="toc-item-num">1.1.1&nbsp;&nbsp;</span>Series折线图</a></span></li><li><span><a href="#DataFrame折线图" data-toc-modified-id="DataFrame折线图-1.1.2"><span class="toc-item-num">1.1.2&nbsp;&nbsp;</span>DataFrame折线图</a></span></li></ul></li><li><span><a href="#柱形图" data-toc-modified-id="柱形图-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>柱形图</a></span><ul class="toc-item"><li><span><a href="#DataFrame柱形图" data-toc-modified-id="DataFrame柱形图-1.2.1"><span class="toc-item-num">1.2.1&nbsp;&nbsp;</span>DataFrame柱形图</a></span></li></ul></li><li><span><a href="#直方图" data-toc-modified-id="直方图-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>直方图</a></span></li><li><span><a href="#散点图" data-toc-modified-id="散点图-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>散点图</a></span></li><li><span><a href="#区域图" data-toc-modified-id="区域图-1.5"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>区域图</a></span></li></ul></li><li><span><a href="#matplotlib绘图" data-toc-modified-id="matplotlib绘图-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>matplotlib绘图</a></span><ul class="toc-item"><li><span><a href="#散点图" data-toc-modified-id="散点图-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>散点图</a></span></li><li><span><a href="#matplotlib基础知识" data-toc-modified-id="matplotlib基础知识-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>matplotlib基础知识</a></span><ul class="toc-item"><li><span><a href="#只包含单一曲线的图形" data-toc-modified-id="只包含单一曲线的图形-2.2.1"><span class="toc-item-num">2.2.1&nbsp;&nbsp;</span>只包含单一曲线的图形</a></span></li><li><span><a href="#获取画板对象" data-toc-modified-id="获取画板对象-2.2.2"><span class="toc-item-num">2.2.2&nbsp;&nbsp;</span>获取画板对象</a></span></li><li><span><a href="#设置子画布" data-toc-modified-id="设置子画布-2.2.3"><span class="toc-item-num">2.2.3&nbsp;&nbsp;</span>设置子画布</a></span></li></ul></li><li><span><a href="#设置画布属性" data-toc-modified-id="设置画布属性-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>设置画布属性</a></span><ul class="toc-item"><li><span><a href="#网格线" data-toc-modified-id="网格线-2.3.1"><span class="toc-item-num">2.3.1&nbsp;&nbsp;</span>网格线</a></span></li><li><span><a href="#坐标轴界限" data-toc-modified-id="坐标轴界限-2.3.2"><span class="toc-item-num">2.3.2&nbsp;&nbsp;</span>坐标轴界限</a></span></li><li><span><a href="#坐标轴标签" data-toc-modified-id="坐标轴标签-2.3.3"><span class="toc-item-num">2.3.3&nbsp;&nbsp;</span>坐标轴标签</a></span></li><li><span><a href="#设置标题" data-toc-modified-id="设置标题-2.3.4"><span class="toc-item-num">2.3.4&nbsp;&nbsp;</span>设置标题</a></span></li><li><span><a href="#设置图例" data-toc-modified-id="设置图例-2.3.5"><span class="toc-item-num">2.3.5&nbsp;&nbsp;</span>设置图例</a></span></li></ul></li><li><span><a href="#保存图片" data-toc-modified-id="保存图片-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>保存图片</a></span></li><li><span><a href="#设置plot的风格和样式" data-toc-modified-id="设置plot的风格和样式-2.5"><span class="toc-item-num">2.5&nbsp;&nbsp;</span>设置plot的风格和样式</a></span></li><li><span><a href="#点和线的样式" data-toc-modified-id="点和线的样式-2.6"><span class="toc-item-num">2.6&nbsp;&nbsp;</span>点和线的样式</a></span><ul class="toc-item"><li><span><a href="#颜色" data-toc-modified-id="颜色-2.6.1"><span class="toc-item-num">2.6.1&nbsp;&nbsp;</span>颜色</a></span></li><li><span><a href="#线型" data-toc-modified-id="线型-2.6.2"><span class="toc-item-num">2.6.2&nbsp;&nbsp;</span>线型</a></span></li><li><span><a href="#多参数连用" data-toc-modified-id="多参数连用-2.6.3"><span class="toc-item-num">2.6.3&nbsp;&nbsp;</span>多参数连用</a></span></li><li><span><a href="#X、Y轴坐标刻度" data-toc-modified-id="X、Y轴坐标刻度-2.6.4"><span class="toc-item-num">2.6.4&nbsp;&nbsp;</span>X、Y轴坐标刻度</a></span></li><li><span><a href="#字体设置" data-toc-modified-id="字体设置-2.6.5"><span class="toc-item-num">2.6.5&nbsp;&nbsp;</span>字体设置</a></span></li></ul></li><li><span><a href="#2D图形" data-toc-modified-id="2D图形-2.7"><span class="toc-item-num">2.7&nbsp;&nbsp;</span>2D图形</a></span><ul class="toc-item"><li><span><a href="#直方图" data-toc-modified-id="直方图-2.7.1"><span class="toc-item-num">2.7.1&nbsp;&nbsp;</span>直方图</a></span></li><li><span><a href="#条形图" data-toc-modified-id="条形图-2.7.2"><span class="toc-item-num">2.7.2&nbsp;&nbsp;</span>条形图</a></span></li></ul></li><li><span><a href="#玫瑰图/极坐标条形图" data-toc-modified-id="玫瑰图/极坐标条形图-2.8"><span class="toc-item-num">2.8&nbsp;&nbsp;</span>玫瑰图/极坐标条形图</a></span><ul class="toc-item"><li><span><a href="#饼图" data-toc-modified-id="饼图-2.8.1"><span class="toc-item-num">2.8.1&nbsp;&nbsp;</span>饼图</a></span></li><li><span><a href="#散点图" data-toc-modified-id="散点图-2.8.2"><span class="toc-item-num">2.8.2&nbsp;&nbsp;</span>散点图</a></span></li></ul></li><li><span><a href="#图形内的文字、注释、箭头" data-toc-modified-id="图形内的文字、注释、箭头-2.9"><span class="toc-item-num">2.9&nbsp;&nbsp;</span>图形内的文字、注释、箭头</a></span><ul class="toc-item"><li><span><a href="#图形内的文字" data-toc-modified-id="图形内的文字-2.9.1"><span class="toc-item-num">2.9.1&nbsp;&nbsp;</span>图形内的文字</a></span></li><li><span><a href="#注释" data-toc-modified-id="注释-2.9.2"><span class="toc-item-num">2.9.2&nbsp;&nbsp;</span>注释</a></span></li></ul></li><li><span><a href="#3D图" data-toc-modified-id="3D图-2.10"><span class="toc-item-num">2.10&nbsp;&nbsp;</span>3D图</a></span><ul class="toc-item"><li><span><a href="#曲面图" data-toc-modified-id="曲面图-2.10.1"><span class="toc-item-num">2.10.1&nbsp;&nbsp;</span>曲面图</a></span></li></ul></li></ul></li></ul></div>
# pandas

pandas中的数据结构Series和DataFrame，都有生成各类图标的`plot()`方法，默认状态下，生成的折线图。

```python
s.plot(kind='line', ax=None, figsize=None, use_index=True, title=None, grid=None, legend=False, style=None, logx=False, logy=False, loglog=False, xticks=None, yticks=None, xlim=None, ylim=None, rot=None, fontsize=None, colormap=None, table=False, yerr=None, xerr=None, label=None, secondary_y=False, **kwds)
```



Series对象的`plot()`方法，接收参数：

- kind：绘图类型
    - line：折线图（默认）
    - bar：直方图
    - barh：横直方图
    - hist：柱形图
    - box：箱型图
    - kde：kernel密度估计图，主要是对柱形图添加kernel概率密度线
    - density：same as kde
    - area：
    - pie：饼图
- ax：matplotlib axes轴对象，默认使用gca()
- figsize：画布大小
- use_index：布尔值，是否用索引作为横坐标
- title：字符串或列表，图标题
- grid：布尔值，是否显示网格线
- legend：图例
- style：列表或字典，每列数据的图形样式
- logx, logy：使用$n*10^0$来表示x、y轴坐标
- loglog：同时使用$n*10^0$来表示x、y轴坐标
- xticks、yticks：x、y轴可读标签
- xlim、ylim：x、y轴可读的取值范围
- rot：改变刻度标签（xticks, yticks）的旋转度
- fontsize：设置刻度标签（xticks, yticks）的大小
- position柱形图柱子的位置设置
- table：横坐标的值以表格形式展现出来
- yerr、xerr：带y、x轴误差线的柱形图
- lable：列的别名，作用再图例上
- secondary_y：双y轴，再右边的第二个y轴
- mark_right：双y轴时，图例中的列标签旁增加显示（right）标识

DataFrame对象的`plot()`方法和Series对象的大同小异，这里只展示不同的地方：

多接收的参数：

- kind
    - scatter：散点图，需要传入columns方向的索引
    - hexbin：三维直方图的二维表现图
- subplots：布尔值，是否有子图
- sharex、sharey：是否共享x、y轴刻度。如果有子图，默认True，如果没有子图，默认False
- layout：元组，子图的行列布局


```python
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
% matplotlib inline
```

## 折线图

一般用来表示数据的变化趋势

绘图时，y 轴表示数据大小，x轴表示Series对象的索引index，x值和y值个数必须匹配

### Series折线图


```python
x = np.linspace(0,2*np.pi, 100)
y = np.sin(x)
s = Series(data=y, index=x)
```


```python
df = DataFrame(data=np.random.randint(0,10,size=(5,7)), columns=list("ABCDEFG"))
```


```python
# 设置图例label，需要将legend设置为True
s.plot(style='-', title='title1', fontsize=20, label='line1', rot=20, colormap='Blues_r')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1ee68fdc780>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_11_1.png?raw=true)



```python
# 因为相比较刻度来说，数据量非常的大，折线图非常平滑
# 同一张图中，后设置的属性会把先设置的属性覆盖
# fontsize属性被覆盖
# grid属性显示
# 多个图形绘制，rot不能使x轴刻度值旋转
ytk = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1]
s.plot(style='-', legend=True, use_index=True, title='title1', fontsize=20, label='line1', rot=20)
(s - 1).plot(style='-.', legend=True, title='title2', fontsize=10, label='line2', color='yellow')
(s - 2).plot(style=':', legend=True, label='line3', color='red', grid=True, table=True, yticks=ytk)
```


    <matplotlib.axes._subplots.AxesSubplot at 0x1ee6794be48>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_12_1.png?raw=true)


### DataFrame折线图


```python
# x 轴表示df的index
# y 轴表示数据值的大小
# df对象有几列，就绘制几条线，每一条线的值就是每一列的值
df.plot(kind='line')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1ee67d870f0>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_14_1.png?raw=true)


## 柱形图

柱形图是一种以长方形的长度为变量的统计图表。一般用来展示横向数据的比较大小


```python
x = ["tom", 'jim', "jhon", "jerry"]
y = [90, 34, 56, 78]
s = Series(data=y, index=x)
# 纵向误差线设置为True
s.plot(kind='bar', yerr=True)
```




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_17_1.png?raw=true)




```python
# 横向柱形图
s.plot(kind='barh')
```

### DataFrame柱形图


```python
# x 轴别是df的index
# y 轴表示数据的大小
# 每一块图形表示索引index位置的一行数据
# 多重数据会产生图例，位置随机
df.plot(kind='bar', use_index=False)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1ee6b766f28>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_21_1.png?raw=true)


## 直方图

直方图又叫质量分布图，由一系列高度不等的纵向条纹或线段表示数据分布的情况。一般用横轴表示数据类型，纵轴表示分布情况。

- x轴表示一个区间，数据出现的区间
- y轴表示数据中，数据落在每个x区间的个数
- bins 表示数据分区的个数，数据中【最小-最大】值


```python
# 绘制标准正态分布曲线
x = np.linspace(-3,3,100)
# y 表示取值的个数
y = np.random.randn(100)
s = Series(data=y, index=x)
# bins 表示数据分区的个数，数据中【最小-最大】值
s.plot(kind='hist', bins=20)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1ee69aa4f98>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_25_1.png?raw=true)



```python
# bins的设置会影响图像展示
# normed=True 会将直方图的y轴由数据个数，变成出现的频率
data = [1,2,1,4,4,4,6,7,9,9]
s = Series(data=data)
s.plot(kind='hist', bins=10, normed=True)
# kernel密度估计，可以展示概率分布的趋势
s.plot(kind='kde')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x19055fc8a20>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_26_1.png?raw=true)


## 散点图

散点图是指在回归分析中，数据点在直角坐标系平面上的分布图，散点图表示因变量随自变量而变化的大致趋势，据此可以选择合适的函数对数据点进行拟合。DataFrame对象可用


```python
# 气泡散点图，设置s 属性，s的大小就是气泡的单位值大小，s 越大气泡越大
df.plot.scatter(x='A', y='B', s=df['C']*50)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1ee6b7a26a0>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_29_1.png?raw=true)



```python
# 设置colorbar为True，会显示一个色深标尺，为每个点提供颜色
# c 为df数据中一列数据，以其为标准
df.plot.scatter(x='C', y='B', c='F', colorbar=True, s=df['D']*50)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1ee6cb205c0>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_30_1.png?raw=true)


## 区域图

区域图将 Y 中的元素显示为一个或多个曲线并填充每个曲线下方的区域。如果 Y 为矩阵，则曲线堆叠在一起，显示每行元素占每个 x 区间的曲线总高度的相对量。


```python
# 接收x、y轴坐标值
df.plot.area()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1ee6b6cf470>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_33_1.png?raw=true)


# matplotlib绘图


```python
# dataframe柱行图
# x 轴别是df的index
# y 轴表示数据的大小
# 每一块图形表示索引index位置的一行数据
# 多重数据会产生图例，位置随机
df.plot(kind='bar', use_index=False)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x19052678160>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_35_1.png?raw=true)


## 散点图


```python
# 散点图，用于描述是两组数据的对应关系
heigh = [180, 178, 190, 163, 158, 160]
weight = [140, 155, 200, 160, 210, 90]
df = DataFrame(data={
    "heigh": heigh,
    "weight": weight
})
df.plot(x="weight", y="heigh", kind="scatter")
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1ee6c9ec5c0>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_37_1.png?raw=true)


Matplotlib 可能是 Python 2D-绘图领域使用最广泛的套件。它能让使用者很轻松地将数据图形化，并且提供多样化的输出格式。一般多使用matplotlib来进行绘图。

## matplotlib基础知识

Matplotlib中的基本图表包括的元素
+ x轴和y轴  axis
水平和垂直的轴线


+ 轴标签 axisLabel
水平和垂直的轴标签


+ x轴和y轴刻度  tick
刻度标示坐标轴的分隔，包括最小刻度和最大刻度


+ x轴和y轴刻度标签  tick label
表示特定坐标轴的值


+ 绘图区域（坐标系）  axes
实际绘图的区域


+ 画布 figure
呈现所有的坐标系

### 只包含单一曲线的图形


```python
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

import matplotlib.pyplot as plt
%matplotlib inline
```

1、可以使用多个plot函数（推荐），在一个图中绘制多个曲线


```python
# dataframe柱行图
# x 轴别是df的index
# y 轴表示数据的大小
# 每一块图形表示索引index位置的一行数据
# 多重数据会产生图例，位置随机
df.plot(kind='bar', use_index=False)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x19052678160>




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_44_1.png?raw=true)



```python
x = np.linspace(0,2*np.pi,100)
y = np.sin(x) + np.cos(x)
# x, y两个坐标轴
y1 = np.sin(x)
y2 = np.cos(x)
plt.plot(x, y)
plt.plot(x, y1)
plt.plot(x, y2)
```




    [<matplotlib.lines.Line2D at 0x1ee6cc92c88>]




![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_45_1.png?raw=true)

2、也可以在一个plot函数中传入多对X,Y值，在一个图中绘制多个曲线


```python
plt.plot(x, y, x,y1, x,y2)
```

### 获取画板对象


```python
# 注意获取画板对象使用小写函数
# figsize可以看成比例，不是像素
figure = plt.figure(figsize=(4, 3), facecolor='cyan')

# 向画板添加画布
# 参数，n行m列第n个
# 传入了位置的描述
ax1 = figure.add_subplot(221)
ax2 = figure.add_subplot(339)
ax3 = figure.add_subplot(233)
# 画板的划分会重叠，后绘制的会覆盖先绘制的
ax4 = figure.add_subplot(332)
```


![png](https://github.com/belingud/image/blob/master/bolg/matplotlib/output_49_0.png?raw=true)


### 设置子画布

在整个画布中分区，以展示不同的图形


```python
plt.figure(figsize=(8,4))
ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)
```

## 设置画布属性

### 网格线

使用plt.grid方法可以开启网格线，使用plt面向对象的方法，创建多个子图显示不同网格线

- lw代表linewidth，线的粗细
- alpha表示线的明暗程度
- color代表颜色
- axis显示轴向

### 坐标轴界限

格式：plt.axis([xmin,xmax,ymin,ymax])

`plt.axis('xxx')` 

参数'tight'、'off'、'equal'……

- "off" 关闭轴显示
- []  设置坐标轴的边界
- "equal","scaled" 调整轴刻度的比例


```python
plt.axis([-np.pi,3*np.pi, -1.5, 1.5])
# 分区控制坐标轴
ax1 = plt.subplot(1,2,1)
ax1.axis([-2,2,-2,2])
```

**也可以通过xlim、ylim方法来设置坐标轴界限**


```python
# 设置画布坐标界限
plt.xlim((-2,2))
plt.ylim((-3,3))
# 子画布坐标界限
ax1 = plt.subplot(1,2,1)
ax1.set_xlim([-2,2])
```

### 坐标轴标签

xlabel方法和ylabel方法  
plt.ylabel('y = x^2 + 5',rotation = 60)旋转

- color 标签颜色
- fontsize 字体大小
- rotation 旋转角度


```python
plt.xlabel("weight", color="red", fontsize=20, rotation = 90)
plt.ylabel("height", color="blue", fontsize=20, rotation = 0)
# 分区控制标签
ax2 = plt.subplot(1,2,2)
ax2.set_xlabel("weight", color="red")
ax2.set_ylabel("height", fontdict={
    "fontsize":20
})
```

### 设置标题

plt.title()方法

- loc {left,center,right}
- color 标签颜色
- fontsize 字体大小
- rotation 旋转角度


```python
plt.title("TITLE", color="red", fontsize=30)
# 分区控制
plt.figure(figsize=(10,4))
ax1 = plt.subplot(1,2,1)
ax1.set_title("axes1", fontsize=20, color="blue")
```

### 设置图例

legend方法

两种传参方法：
- 分别在plot函数中增加label参数,再调用legend()方法显示
- 直接在legend方法中传入字符串列表

loc参数

- loc参数用于设置图例标签的位置，一般在legend函数内
- matplotlib已经预定义好几种数字表示的位置

| 字符串       | 数值      | 字符串   |  数值 |
| :-------------: |:-----------:| :-----:|  :-----:|
| best        |  0        | center left   |   6 |
| upper right    | 1        | center right  |   7  |
| upper left    |  2        | lower center  |   8  |
| lower left    |  3        | upper center  |   9 |
| lower right   |  4        | center      |   10 |
| right       |  5        |

loc参数可以是2元素的元组，表示图例左下角的坐标

- [0,0] 左下
- [0,1] 左上
- [1,0] 右下
- [1,1] 右上

图例也可以超过图的界限loc = (-0.1,0.9)


```python
# 第一种写法，向legend函数中传入一个字符串列表
plt.legend(["normal","fast","slowly"])
# 第二种写法:为每一个图形添加label属性
plt.plot(x,x,label="normal")
plt.plot(x,x*2, label="fast")
plt.plot(x,x/2, label="slowly")
plt.legend(ncol=2)
# 同样可以分区控制属性
ax1 = plt.subplot(1,2,1)
ax1.set_title("axes1")
ax1.plot(x,x, x,x*2)
ax1.legend(["normal","fast"],loc=[1.0,1.0])
```

ncol参数

ncol控制图例中有几列,在legend中设置ncol,需要设置loc

linestyle、color、marker
修改线条样式  

## 保存图片

使用figure对象的savefig的函数
+ filename  
含有文件路径的字符串或Python的文件型对象。图像格式由文件扩展名推断得出，例如，.pdf推断出PDF，.png推断出PNG
（“png”、“pdf”、“svg”、“ps”、“eps”……）
+ dpi  
图像分辨率（每英寸点数），默认为100
+ facecolor  
图像的背景色，默认为“w”（白色） 


```python
figure = plt.figure(figsize=(8,6), facecolor='orange')
# 设置子画布，并画图
ax1 = figure.add_subplot(2,2,1)
ax1.plot(x, np.sin(x))
ax1.set_title("sin(x)", fontdict={
    "fontsize":16,
    "color":"red"
})
# 保存图像
figure.savefig('image.png',dpi=50)
```

## 设置plot的风格和样式

plot语句中支持除X,Y以外的参数，以字符串形式存在，来控制颜色、线型、点型等要素，语法形式为：
`plt.plot(X, Y, 'format', ...) `


```python
x = np.linspace(0,10,10)
plt.plot(x, x, color="red", linewidth=2, alpha=0.3, linestyle="-", marker="D", 
         markersize=20, markeredgecolor="blue",markeredgewidth=4,markerfacecolor="red")

# 自定义虚线，有色长度3，无色长度1，有色长度10，无色长度1，接连显式
plt.plot(x, x, dashes=[3, 1, 10, 1])

# 获取线对象，对线对象单独设置外观
lines = plt.plot(x,x, x,x*2, x,x**2)
lines[0].set_color("red")
lines[0].set_linewidth(3)

lines[1].set_color("blue")
lines[1].set_marker("D")

lines[2].set_color("green")
lines[2].set_dashes([10,2])
```

## 点和线的样式



### 颜色
参数color或c

**颜色值的方式**

+ 别名
    + color='r'

+ 合法的HTML颜色名
  
    + color = 'red'

| 颜色       | 别名      | HTML颜色名  | 颜色   |  别名 |HTML颜色名|
| :-------------: |:---------:|:-----------:| :------:|  :-----:| :-----:|
| 蓝色        | b       | blue      | 绿色   |  g   |  green  |
| 红色        | r       | red      | 黄色    |  y   |  yellow |
| 青色        | c       | cyan      | 黑色   |  k   |  black  |
| 洋红色      | m        | magenta    | 白色   |  w   |  white  |

+ HTML十六进制字符串
    + color = '#eeefff'       


+ 归一化到[0, 1]的RGB元组
    + color = (0.3, 0.3, 0.4)

+ jpg png 区别

**透明度**

alpha参数 

**背景色**

设置背景色，通过plt.subplot()方法传入facecolor参数，来设置坐标系的背景色

### 线型

参数linestyle或ls

| 线条风格     | 描述      | 线条风格 |  描述 |
| :-------------: |:------------:| :----:|  :-----:|
| '-'        | 实线     | ':'     |  虚线 |
| '--'       | 破折线    | 'steps'  |  阶梯线 |
| '-.'       | 点划线    | 'None' / '，' |  什么都不画 |

**线宽**

linewidth或lw参数

**不同宽度的破折线**

dashes参数    eg.dashes = [20,50,5,2,10,5]

**点型**

- marker 设置点形
- markersize 设置点形大小

| 标记        | 描述       | 标记   |  描述 |
| :-------------: |:-----------:| :----:|  :-----:|
| '1'         | 一角朝下的三脚架      | '3'     |  一角朝左的三脚架 |
| '2'         | 一角朝上的三脚架      | '4'     |  一角朝右的三脚架 |

| 标记        | 描述       | 标记   |  描述 |
| :-------------: |:-----------:| :----:|  :-----:|
| 's'         | 正方形   | 'p'   | 五边形     |
| 'h'         | 六边形1    | 'H'     | 六边形2    |
| '8'         | 八边形     |

| 标记        | 描述       | 标记   |  描述 |
| :-------------: |:-----------:| :----:|  :-----:|
| '.'     |  点 | 'x'   | X   |
| '\*'    |  星号  | '+'         | 加号       |
| ','         | 像素       |

| 标记        | 描述       | 标记   |  描述 |
| :-------------: |:-----------:| :----:|  :-----:|
| 'o'         | 圆圈      | 'D'         | 菱形      |
| 'd'    |  小菱形  |'','None',' ',None| 无       |

| 标记     | 描述     | 标记   |  描述 |
| :--------: |:----------:| :------:| :----:|
| '\_'     |  水平线    | '&#124;'     |  竖线   |

| 标记        | 描述       | 标记   |  描述 |
| :-------------: |:-----------:| :----:|  :-----:|
| 'v'         | 一角朝下的三角形 | '<'     |  一角朝左的三角形 |
| '^'         | 一角朝上的三角形 | '>'     |  一角朝右的三角形 |

### 多参数连用

颜色、点型、线型，可以把几种参数写在一个字符串内进行设置 'r-.o'

**更多点和线的设置**

- markeredgecolor = 'green',
- markeredgewidth = 2,
- markerfacecolor = 'purple'

| 参数        | 描述       | 参数       |  描述   |
| :-------------: |:-----------:| :-------------:|  :------:|
| color或c      | 线的颜色   | linestyle或ls  |  线型   |
| linewidth或lw   | 线宽     | marker       |  点型  |
| markeredgecolor  | 点边缘的颜色 | markeredgewidth | 点边缘的宽度 |
| markerfacecolor  | 点内部的颜色 | markersize    |  点的大小    |


**多个曲线同一设置**

属性名声明，不可以多参数连用

`plt.plot(x1, y1, x2, y2, fmt, ...)`



```python
plt.plot(x,x,'b-.o',x,x*2,'r--d')
```

**多个曲线不同设置**

多个都进行设置时，多参数连用
plt.plot(x1, y1, fmt1, x2, y2, fmt2, ...)

**三种设置方式**

1. 向方法传入关键字参数

2. 对实例使用一系列的setter方法

- plt.plot()方法返回一个包含所有线的列表，设置每一个线需要获取该线对象
  - eg: lines = plt.plot();   line = lines[0]
  - line.set_linewith()
  - line.set_linestyle()
  - line.set_color()

3. 对坐标系使用一系列的setter方法

- axes = plt.subplot()获取坐标系
  - set_title()
  - set_facecolor()
  - set_xticks、set_yticks 设置刻度值
  - set_xticklabels、set_yticklabels  设置刻度名称

### X、Y轴坐标刻度

plt.xticks()和plt.yticks()方法  

- 需指定刻度值和刻度名称  plt.xticks([刻度列表],[名称列表])
- 支持fontsize、rotation、color等参数设置


```python
plt.plot(x, np.sin(x))
# 设置刻度
plt.xticks([-np.pi,-np.pi/2,0,np.pi/2,np.pi],["-Π","-Π/2","0","Π/2","Π"])
plt.yticks([-1,0,1])
plt.grid()
```


```python
ax = plt.subplot(1,1,1)
ax.plot(x, np.sin(x))
# 设置坐标轴刻度
ax.set_xticks([-np.pi,-np.pi/2,0,np.pi/2,np.pi])
# 设置坐标轴标签
ax.set_xticklabels(["-Π","-Π/2","0","Π/2","Π"])
```

**正弦余弦**

LaTex语法，用$\pi$、$\sigma$等表达式在图表上写上希腊字母  


### 字体设置

1.全局设置

常用字体：

- 黑体 SimHei
- 仿宋 FangSong
- 楷体 KaiTi



```python
# 配置matplotlib显示中文
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# 测试
plt.title("-中文字体")
```

2.加载自定义字体，设置局部


```python
from matplotlib import font_manager
myfont = font_manager.FontProperties(fname='../辣鸡心心体.ttf')

# 测试
plt.title("-中文测试字体", fontproperties=myfont, fontsize=15)
```

## 2D图形

### 直方图

【直方图的参数只有一个x！！！不像条形图需要传入x,y】

hist()的参数

- bins  
  可以是一个bin数量的整数值，也可以是表示bin的一个序列。默认值为10
- normed  
  如果值为True，直方图的值将进行归一化处理，形成概率密度，默认值为False
- color  
  指定直方图的颜色。可以是单一颜色值或颜色的序列。如果指定了多个数据集合，颜色序列将会设置为相同的顺序。如果未指定，将会使用一个默认的线条颜色
- orientation  
  通过设置orientation为horizontal创建水平直方图。默认值为vertical

### 条形图

【条形图有两个参数x,y】

- width 纵向设置条形宽度
- height 横向设置条形高度

bar()、barh()

## 玫瑰图/极坐标条形图

创建极坐标，设置polar属性

- plt.axes(polar = True)

绘制极坐标条形图

- index = np.arange(-np.pi,np.pi,2*np.pi/6)
- plt.bar(x=index ,height = [1,2,3,4,5,6] ,width = 2*np.pi/6)

### 饼图

【饼图也只有一个参数x！】

pie()  
饼图适合展示各部分占总体的比例，条形图适合比较各部分的大小

普通各部分占满饼图

普通未占满饼图

饼图阴影、分裂等属性设置

- labels参数设置每一块的标签；
- labeldistance参数设置标签距离圆心的距离（比例值,只能设置一个浮点小数）
- autopct参数设置比例值的显示格式(%1.1f%%)；
- pctdistance参数设置比例值文字距离圆心的距离
- explode参数设置每一块顶点距圆形的长度（比例值,列表）；
- colors参数设置每一块的颜色（列表）；
- shadow参数为布尔值，设置是否绘制阴影
- startangle参数设置饼图起始角度

### 散点图

【散点图需要两个参数x,y，但此时x不是表示x轴的刻度，而是每个点的横坐标！】

scatter()  

## 图形内的文字、注释、箭头

控制文字属性的方法:  

| pyplot函数  |           API方法            |              描述              |
| :---------: | :--------------------------: | :----------------------------: |
|   text()    |     mpl.axes.Axes.text()     |  在Axes对象的任意位置添加文字  |
|  xlabel()   |  mpl.axes.Axes.set_xlabel()  |         为X轴添加标签          |
|  ylabel()   |  mpl.axes.Axes.set_ylabel()  |         为Y轴添加标签          |
|   title()   |  mpl.axes.Axes.set_title()   |       为Axes对象添加标题       |
|  legend()   |    mpl.axes.Axes.legend()    |       为Axes对象添加图例       |
|  figtext()  |   mpl.figure.Figure.text()   | 在Figure对象的任意位置添加文字 |
| suptitle()  | mpl.figure.Figure.suptitle() |  为Figure对象添加中心化的标题  |
| annnotate() |   mpl.axes.Axes.annotate()   | 为Axes对象添加注释（箭头可选） |

所有的方法会返回一个matplotlib.text.Text对象

### 图形内的文字


### 注释

annotate()

- xy参数设置箭头指示的位置

- xytext参数设置注释文字的位置  

- arrowprops参数以字典的形式设置箭头的样式  

- width参数设置箭头长方形部分的宽度

- headlength参数设置箭头尖端的长度，  

- headwidth参数设置箭头尖端底部的宽度

- shrink参数设置箭头顶点、尾部与指示点、注释文字的距离（比例值），可以理解为控制箭头的长度
  

    如下都是arrowstyle可以选择的风格样式

    ``'->'``       head_length=0.4,head_width=0.2
  
    ``'-['``       widthB=1.0,lengthB=0.2,angleB=None
  
    ``'|-|'``      widthA=1.0,widthB=1.0
  
    ``'-|>'``      head_length=0.4,head_width=0.2
  
    ``'<-'``       head_length=0.4,head_width=0.2
  
    ``'<->'``      head_length=0.4,head_width=0.2
  
    ``'<|-'``      head_length=0.4,head_width=0.2
  
    ``'<|-|>'``    head_length=0.4,head_width=0.2
  
    ``'fancy'``    head_length=0.4,head_width=0.4,tail_width=0.4
  
    ``'simple'``   head_length=0.5,head_width=0.5,tail_width=0.2
  
    ``'wedge'``    tail_width=0.3,shrink_factor=0.5

## 3D图</font>

### 曲面图  



导包  

- from mpl_toolkits.mplot3d.axes3d import Axes3D

使用mershgrid函数切割x,y轴

- X,Y = np.meshgrid(x, y)

创建3d坐标系

- axes = plt.subplot(projection='3d')

绘制3d图形

- p = axes.plot_surface(X,Y,Z,color='red',cmap='summer',rstride=5,cstride=5)

添加colorbar

- plt.colorbar(p,shrink=0.5)
