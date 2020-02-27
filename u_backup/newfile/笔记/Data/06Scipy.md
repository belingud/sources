<h1>Scipy图像处理<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#二维图像处理" data-toc-modified-id="二维图像处理-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>二维图像处理</a></span></li><li><span><a href="#三维图像的处理" data-toc-modified-id="三维图像的处理-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>三维图像的处理</a></span></li><li><span><a href="#可以使用的颜色映射参数" data-toc-modified-id="可以使用的颜色映射参数-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>可以使用的颜色映射参数</a></span></li><li><span><a href="#图片灰度处理" data-toc-modified-id="图片灰度处理-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>图片灰度处理</a></span></li><li><span><a href="#数值积分，求解圆周率" data-toc-modified-id="数值积分，求解圆周率-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>数值积分，求解圆周率</a></span></li><li><span><a href="#Scipy文件输入/输出" data-toc-modified-id="Scipy文件输入/输出-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Scipy文件输入/输出</a></span></li><li><span><a href="#使用scipy.ndimage图片处理" data-toc-modified-id="使用scipy.ndimage图片处理-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>使用scipy.ndimage图片处理</a></span></li></ul></div>
本文主要用到的图像处理的方法：

- plt.imread()
- plt.imshow()
- misc.imread()
- misc.save()
- scio.savemat()
- misc.imrotate()
- misc.imresize()
- misc.imfilter()
- scipy.ndimage图片处理

# 二维图像处理

使用scipy.fftpack模块来计算快速傅里叶变换，速度比传统傅里叶变换快，是对之前算法的改进。

灰度图片是二维数据，处理使用的是fftpack的二维转变方法。


```python
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
%matplotlib inline

# 处理傅里叶变换的函数
from scipy.fftpack import ifft2, fft2, ifft, fft
```

*numpy也提供了fft/ifft函数，但是执行效率没有scipy的高*

这里引入一个概念，时域和频域：

时域：是真实世界，是惟一实际存在的域。因为我们的经历都是在时域中发展和验证的，已经习惯于事件按时间的先后顺序地发生。而评估数字产品的性能时，通常在时域中进行分析，因为产品的性能最终就是在时域中测量的。

频域：它不是真实的，而是一个数学构造。时域是惟一客观存在的域，而频域是一个遵循特定规则的数学范畴，正弦波是频域中唯一存在的波形。

对于二维图片的处理主要分为以下几个步骤：

1. 首先是加载图片，使用imread()方法，加载出来的灰度图像数据，是一个二维数组，没有rgb颜色数据，每个像素点用一个数来表示，就是这个像素点的灰度
2. 将时域空间的图片数据，映射到频域空间，得到的是一组复数的二维数组
3. 将频域空间的图片数据，进行滤波操作
4. 再将频域空间滤波完成的数据，转换回时域空间
5. 获取二维数组数据中的实数部分，使用imshow()方法展示图像


```python
# 读取灰度图片
moon = plt.imread('moonlanding.png')
# 展示图片使用imshow()方法，传入一个cmap属性来添加各种风格
plt.imshow(moon, cmap='gray')
```

获取到数据是一组`float32`类型的0~1之间的浮点数


```python
# 将读取的图片数据，映射到频域空间
fft_moon = fft2(moon)
# 获取的是一组复数数据，用j来表示虚数部分
```

实现过滤操作使用了一个方法`where()`，它接收三个参数：

- condition：过滤条件
- x：满足过滤条件，填充的值
- y：不满足过滤条件，填充的值


```python
filted_fft_moon = np.where(np.abs(fft_moon) > 1e4, 0, fft_moon)
```


```python
# 再把滤波完成的数据转化回时域空间
ifft_moon = ifft2(filted_fft_moon)
```

转换完的数据依然是一个复数数组，我们需要取实数部分，才能实现对它的展示


```python
# 对复数数组取数值的实数部分
real_moon = np.real(ifft_moon)
# 展示
plt.imshow(real_moon, cmap="gray")
```

# 三维图像的处理

三维图像就是一个使用三维数组数据存储的图像，除了灰度二维之外，还存有颜色的rgb数据。

这里处理三维图像，使用了python的图像处理模块PIL，在python中，进行图像处理一般都会用到这个库，pillow模块也是根据PIL模块编写的。

三维图像的处理与二维图像处理的步骤，大致相同。


```python
# 引入PIL模块中的Image方法来处理彩色图像
from PIL import Image
```


```python
# 读取图片，读取到的数据依然是一个图片
img = Image.open("th.jpg")
```

将图片数据，转化为数组形式需要经过两步：

1. 图片数据转化为字节数据
2. 将字节数据，转化为一维数组

这个数组既是我们需要处理的数据


```python
# 将图片数据转化为字节
# tobytes(): Return image as a bytes object.
b_img = img.tobytes()

# 将字节，转化为数组数据
# np.frombuffer(): 将缓冲区的数据解释为一维数组
img_data = np.frombuffer(b_img, dtype=np.uint8)
```

至此，我们完成了图片数据的预处理，得到了需要转换过滤的数组数据，下面是数据的转换和过滤。和上文中二维图像的处理相同


```python
# 将时域数据映射为频域数据
fft_img = fft(img)
# 将频域数据进行过滤处理
filted_fft_img = np.where(np.abs(fft_img) < 1e2, 0, fft_img)
# 将处理过后的频域数据转换回时域数据
ifft_img = ifft(filted_fft_img)
```


```python
# 然后取数据的实数部分，并用uint8编码
data_to_show = np.uint8(np.real(ifft_img))
```

最后，将数组的数据加载为缓冲区的图片缓冲


```python
img_to_show = Image.frombytes(mode=img.mode, size=img.size, data=data_to_show)
```

# 可以使用的颜色映射参数

Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Vega10, Vega10_r, Vega20, Vega20_r, Vega20b, Vega20b_r, Vega20c, Vega20c_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spectral, spectral_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, viridis, viridis_r, winter, winter_r

# 图片灰度处理

所谓的图片灰度处理，就是把彩色图片数据中，第三维表示rgb颜色的数据，转换成表示灰度的数据。主要通过几个方式：

1. 取最大值|最小值
2. 取平均值
3. 使用权重


```python
# 读取图片数据
img = plt.imread('th.jpg')
# 取最大值，实现灰度处理
plt.imshow(img.max(axis=2), cmap='gray')

# 取平均值，实现灰度处理
plt.imshow(img.mean(axis=2), cmap='gray')

# 使用权重，实现灰度处理
plt.imshow(np.dot(img, np.array([0.5, 0.3, 0.2])), cmap='gray')
```

`dot(a, b, out=None)`方法，是数组的点承方法，相当于$arr1·arr2$，接收三个参数，两个数组，和一个输出格式

# 数值积分，求解圆周率

求解圆周率  

integrate
对函数$(1-x^2)^{0.5}$进行积分 


```python
# 使用linspace生成一个等差数列，用来绘制图像上的点
x = np.linspace(-1,1,num=100)
# 使用lambda匿名函数来定义需要绘制的函数
f = lambda x: (1-x**2)**0.5
# 定义y为函数的调用，也是我们需要绘制的图形
y = f(x)
```

为了便于理解，我们将这个函数的图形绘制出来，然后再求解其积分。

这是一个半圆，y取正负，可以绘制成一个圆，更加直观

使用plt进行图像的绘制，再新的笔记中详解。


```python
# 生成画布
plt.figure(figsize=(4,4))
# 定义画图方向
plt.axis("equal")
# 绘制图形
plt.plot(x, y)
plt.plot(x, -y)
```

使用`scipy.integrate`进行积分，调用`quad()`方法


```python
from scipy.integrate import quad
```

`quad()`方法接收三个参数：

1. 参数 1 接收不规则曲线的表达式
2. 参数 2、3 接收不规则曲线的左右边界

有两个返回值：

1. 不规则图形的面积
2. 积分求解的偏差


```python
# 用area和err来接收这两个参数
area, err = quad(f, -1, 1)
```


```python
# 圆周率就是面积的二倍
area*2
```

# Scipy文件输入/输出

import scipy.io as io
随机生成数组，使用scipy中的io.savemat()保存  
文件格式是.mat，标准的二进制文件

`scio()`方法的参数：

- file_name：要保存的图片的文件名
- mdic：传入保存的mat文件的字典数据
- appendmat：布尔值，是否添加may后缀，默认添加，
- format：字符串，'5'或'4'，分别表示MATLAB5以上到7.2，或4一下版本的mat文件
- long_field_names：布尔值，为`True`时兼容MATLAB7.6以上，文件名最长63个字节
- oned_as：'row'或'column'，保存为横向或纵向向量


```python
import scipy.io as scio
```

借用上文中加载的`img`图像信息，示例图像保存方法


```python
scio.savemat(file_name="img", mdict={"data": img})
```

使用scio.loadmat()读取数据，读取到的数据是一个字典，图片信息存储再`data`键的值里面


```python
plt.imshow(scio.loadmat("img.mat")["data"])
```

读写图片使用scipy中misc.imread()/imsave()


```python
import scipy.misc as misc
```


```python
# 读取图片
mm = misc.imread("th.jpg")
```


```python
# 保存图片
misc.imsave("mm.jpg", mm)
```

misc的imrotate（旋转）、imresize（缩放）、imfilter（过滤）操作


```python
# 旋转
plt.imshow(misc.imrotate(mm, angle=30))
```

缩放函数`imrotate()`接收的参数：

- arr：需要进行缩放的图片数据，是一个nparray
- size：缩放大小
    - int：百分比
    - float：比例
    - tuple：按照元组里面的整数进行缩放
- interp：插值方法，('nearest'最近, 'lanczos'兰索斯算法, 'bilinear'双线性插值,'bicubic'立方 or 'cubic'平方)
- mode：字符串，保存的模式

返回缩放之后的数组数据。


```python
plt.imshow(misc.imresize(mm, 0.3))
```

`imfilter()`图像数据过滤，过滤方式ftype 'blur'模糊, 'contour'轮廓, 'detail'细节, 'edge_enhance'边缘增强, 'edge_enhance_more'边缘增强提高,'emboss'浮雕, 'find_edges'边界, 'smooth'平滑, 'smooth_more'平滑提高, 'sharpen'锐化.


```python
plt.imshow(misc.imfilter(mm, "find_edges"))
```

# 使用scipy.ndimage图片处理


```python
from scipy import ndimage
```

使用scipy.misc.face(gray=True)获取图片，使用ndimage移动坐标、旋转图片、切割图片、缩放图片

`face()`方法描述：Get a 1024 x 768, color image of a raccoon face.获取一个浣熊的脸


```python
# misc.face(gray=True)是一个预加载图片
plt.imshow(misc.face(gray=True), cmap="gray")
```


```python
face = misc.face(gray=True)
```

- shift移动坐标


```python
# float表示延两个轴要移动的像素个数
# 列表  表示分别沿着不同的轴移动
plt.imshow(ndimage.shift(face, [50, 80], mode="mirror"))
```

- rotate旋转图片


```python
plt.imshow(ndimage.rotate(face, angle=90), cmap="gray")
```

- zoom缩放图片


```python
# float 表示沿着两个轴的压缩比例
# 列表表示沿着两个轴以不同比例缩放
plt.imshow(ndimage.zoom(face, zoom=5), cmap="gray")
```

使用切片切割图片


```python
plt.imshow(face, cmap="gray")
```


```python
# 切割图片
data = face[70:700, 650:780]
plt.imshow(data, cmap="gray")
```

图片进行过滤   
添加噪声，对噪声图片使用ndimage中的高斯滤波、中值滤波、signal中维纳滤波进行处理  
使图片变清楚

加载图片，使用灰色图片misc.face()添加噪声


```python
# 生成噪声数据，因为图片数据是用uint8 彩色数据来存储的，所以噪声数据也要定义成uint8格式
# 并且，噪声数据应该和图片切片数据的形状相同
noise_data = np.uint8(np.random.randint(0,250,size=data.shape)*0.2).reshape(130*630)
# 获取噪声数据的索引
random_index = np.random.randint(0,noise_data.size, 1000)
# 根据图片数据的形状，重捏噪声数据形状
noise = noise_data.reshape(data.shape)
# 将噪声数据添加到图片数据中
data += noise
# 展示添加噪声之后的图片
plt.imshow(data, cmap="gray")
```

gaussian高斯滤波参数sigma：高斯核的标准偏差


```python
plt.imshow(ndimage.gaussian_filter(data, sigma=2), cmap="gray")
```

median中值滤波参数size：给出在每个元素上从输入数组中取出的形状位置，定义过滤器功能的输入

signal维纳滤波参数mysize：滤镜尺寸的标量


```python
import scipy.signal as signal
```


```python
# size数值越大模糊效果越明显
plt.imshow(signal.wiener(data, mysize=10), cmap="gray")

moon = plt.imread("moonlanding.png")
plt.imshow(signal.wiener(moon, mysize=10), cmap="gray")
```
