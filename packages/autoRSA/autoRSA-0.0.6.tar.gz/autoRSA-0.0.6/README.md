# autoRSA

autoRSA是一个半自动预测RSA术式中**入钉角度**，**导板形状**的Python库。

## 依赖库一览

autoRSA依赖于以下Python库：

- `open3D`，通过以下代码安装：
```
pip install open3d
```
- `numpy`，通过以下代码安装：
```
pip install numpy
```
- `tqdm`，通过以下代码安装：
```
pip install tqdm
```
- `pyvista`，通过以下代码安装：
```
pip install pyvista
```
- `torch`和`sko`，可选（`find_nail2()`函数所需）。

借助
```cmd
pip install autoRSA
```
可以自动安装依赖库。

## 计算流程一览

1. 函数初始化。`filename`是肩胛骨模型文件的位置，建议使用已计算法向量和三角面片的`.stl`格式文件。
```python
s = scapula(filename)
```
2. 函数选点。选点采用的是**最佳拟合圆**的方式，用户选点应先选取关节盂下缘的点，再选取关节盂前后缘的点。`select_points1()`函数提供了一个基于点云选取所需点的窗口。`select_points2()`函数需要用户或其他程序自己输入选取的点在文件中的索引。`picked_id_pcd`应是一个列表，其中储存了选择点的索引。
```python
s.select_points1()
s.select_points2(picked_id_pcd)
```
3. 计算最佳拟合圆圆心。
```python
s.computer_circle()
```
4. 移动模型以便于计算。
```python
s.move_center_to_O()
s.find_vector()
```
5. 钉长计算。其中`theta1`，`theta2`，`num_point`这三个参数是可选的，默认为5/8度，360/40度，400点。
```python
s.find_nail(theta1=..., theta2=..., num_point=...)
print (s.location)
# 输出举例：[array([38.44197149]), [], array([ 13.74876639, 205.71172213])]
# 输出解释：第一个数字代表求的钉长，第二个参数目前无用，第三个参数的两个值代表钉和法向量夹角以及沿着法向量旋转的角度。
```
6. 计算把手位置。`filename`代表把手文件的位置，建议使用`.stl`格式。我们提供了一个[把手文件](https://pan.baidu.com/s/1fifUMRuVYlnPZexv8Sp41Q?pwd=2022)。用户也可以自己绘制。
```python
s.find_handle(filename)
```
7. 计算导板形状。
```python
s.find_guide()
```
8. 放置基座。`filename`代表基座文件的位置，建议使用`.stl`格式。我们提供了一个[基座文件](https://pan.baidu.com/s/1GasR0yxYqnsesIwlbMCPAw?pwd=2022)。用户也可以自己绘制。
```python
s.find_jizuo(filename)
```
9. 将步骤4中移动所带来的变化复原。
```python
s.go_back()
```
10. 保存文件。输出包括肩胛骨模型文件`mesh.stl`，把手文件`handle.stl`，导板文件`guide.stl`，钉子文件`nail.stl`，基座文件`jizuo.stl`。其他程序可以读入这些文件进行后续操作，用户也可以借助`Mimics`或其他软件进行后续处理。
```python
s.save()
```

## 效果参考
![](https://cdn.luogu.com.cn/upload/image_hosting/vvs8chsn.png)