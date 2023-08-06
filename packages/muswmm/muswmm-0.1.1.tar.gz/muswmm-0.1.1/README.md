muswmm是一个可以管理SWMM项目、设计SWMM模拟器、过程实时控制模拟的Python开发工具库。

### 引擎版本
SWMM 5.2.000

### 如何安装
```
pip install muswmm
```

### 如何使用
#### 项目设置
##### 打开、保存、另存为
```
from muswmm.project import *

# 打开项目输入文件
prj = Project('example.inp')
# 保存输入文件
prj.save()
# 输入文件另存为
prj.save_as('example1.inp')
```
##### 模拟选项
```
from muswmm.project import *

prj = Project('example.inp')
options = prj.options
print(options.infil)    # 读取采用的入渗方法
options.route_step = 10.0    # 修改演算步长
```
#### 可视化对象操作
##### 可视化对象集合提取
```
from muswmm.project import *

prj = Project('example.inp')
gages = prj.gages    # 雨量计集合
subcatchs = prj.subcatchments    # 子汇水区集合
junctions = prj.junctions # 检查井集合
outfalls = prj.outfalls    # 排口集合
storages = prj.storages    # 调蓄单元集合
dividers = prj.dividers    # 分流器集合
conduits = prj.conduits    # 管渠集合
pumps = prj.pumps    # 水泵集合
orifices= prj.orifices    # 孔口集合
weirs = prj.weirs    # 堰集合
outlets = prj.outlets    # 出水口集合
```
##### 可视化对象集合元素操作
- 获取集合元素数量
- 根据名称查询元素
- 添加、删除元素
- 迭代器
- 元素属性读写

以子汇水区为例：
```
from muswmm.project import *

prj = Project('example.inp')
subcatchs = prj.subcatchments    # 子汇水区集合
print(len(subcatchs))    # 子汇水区集合元素数量

subcatch = subcatchs['S1']    # 读取名称为S1的子汇水区
print(subcatch.area)    # 子汇水区面积
polygon = subcatch.polygon    # 子汇水区多边形
# 读取多边形拐点坐标
for point in polygon:
    print('{},{}'.format(point.x,point.y))

# 添加子汇水区元素
new_polygon = Points()
new_polygon.add(Point(0.0,0.0))
new_polygon.add(Point(0.0, 1000.0))
new_polygon.add(Point(1000.0, 1000.0))
new_polygon.add(Point(1000.0,0.0))
new_polygon.add(Point(0.0, 0.0))
new_subcatch = Subcatchment.new(prj, new_polygon)

# 删除子汇水区元素
subcatch.remove()

# 清空子汇水区元素
subcatchs.clear()
```

#### 应用程序接口
SWMM引擎提供若干用于模拟器设计、过程控制、模拟结果读取等。
##### 模拟器设计
###### 方式1
```
from muswmm.simulator import *

inp = r'example.inp'    # 输入文件
rpt = r'example.rpt'    # 报告文件
out = r'example.out'    # 输出文件
sim = Simulator(inp, rpt, out)    # 新建模拟器
err_code = sim.open()    # 打开模拟器
err_code = sim.start(1)    # 开始模拟
while(err_code == 0):
    err_code, elapsed_time = sim.step()    # 逐步模拟
    print(sim.getCurrentTime().strftime('%Y-%m-%d %H:%M:%S'))    # 报告当前时间
    if elapsed_time == 0:
        break
sim.end()    # 结束模拟
sim.close()    # 关闭模拟器
```
###### 方式2
```
from muswmm.simulator import *

inp = r'example.inp'    # 输入文件
rpt = r'example.rpt'    # 报告文件
out = r'example.out'    # 输出文件
sim = Simulator(inp, rpt, out)    # 新建模拟器
err_code = sim.run()    # 直接运行模拟器
```
##### 过程控制
SWMM5.2较SWMM5.1增加了用于在模拟过程中获取状态变量和参数（swmm_getValue）并修改设施控制量和边界条件（swmm_setValue）的接口。
swmm_getValue可获取的状态变量和参数及其对应的索引号如下：
###### 系统（SYSTEM）
- SWMM_STARTDATE = 0
- SWMM_CURRENTDATE = 1
- SWMM_ELAPSEDTIME = 2
- SWMM_ROUTESTEP = 3
- SWMM_MAXROUTESTEP = 4
- SWMM_REPORTSTEP = 5
- SWMM_TOTALSTEPS = 6
- SWMM_NOREPORT = 7
- SWMM_FLOWUNITS = 8

###### 雨量计(GAGE)
- SWMM_GAGE_RAINFALL = 100

###### 子汇水区（SUBCATCHMENT）
- SWMM_SUBCATCH_AREA = 200
- SWMM_SUBCATCH_RAINGAGE = 201
- SWMM_SUBCATCH_RAINFALL = 202
- SWMM_SUBCATCH_EVAP = 203
- SWMM_SUBCATCH_INFIL = 204
- SWMM_SUBCATCH_RUNOFF = 205
- SWMM_SUBCATCH_RPTFLAG = 206

###### 节点（NODE）
- SWMM_NODE_TYPE = 300
- SWMM_NODE_ELEV = 301
- SWMM_NODE_MAXDEPTH = 302
- SWMM_NODE_DEPTH = 303
- SWMM_NODE_HEAD = 304
- SWMM_NODE_VOLUME = 305
- SWMM_NODE_LATFLOW = 306
- SWMM_NODE_INFLOW = 307
- SWMM_NODE_OVERFLOW = 308
- SWMM_NODE_RPTFLAG = 309

###### 链接（LINK）
- SWMM_LINK_TYPE = 400
- SWMM_LINK_NODE1 = 401
- SWMM_LINK_NODE2 = 402
- SWMM_LINK_LENGTH = 403
- SWMM_LINK_SLOPE = 404
- SWMM_LINK_FULLDEPTH = 405
- SWMM_LINK_FULLFLOW = 406
- SWMM_LINK_SETTING = 407
- SWMM_LINK_TIMEOPEN = 408
- SWMM_LINK_TIMECLOSED = 409
- SWMM_LINK_FLOW = 410
- SWMM_LINK_DEPTH = 411
- SWMM_LINK_VELOCITY = 412
- SWMM_LINK_TOPWIDTH = 413
- SWMM_LINK_RPTFLAG = 414

swmm_setValue可修改的设施控制值和边界条件如下：
- SWMM_GAGE_RAINFALL = 100
- SWMM_SUBCATCH_RPTFLAG = 206
- SWMM_NODE_LATFLOW = 306
- SWMM_NODE_HEAD = 307
- SWMM_NODE_RPTFLAG = 309
- SWMM_LINK_SETTING = 407
- SWMM_LINK_RPTFLAG = 414
- SWMM_ROUTESTEP = 3
- SWMM_REPORTSTEP = 5
- SWMM_NOREPORT = 7
以水泵的简单控制为例，当然这里可以在输入文件中基于规则进行控制（RBC），但对于条件或动作复杂的情况，或利用优化算法实现设施控制，RBC则无法实现，需采用这里的过程实时控制（RTC）。
```
from muswmm.simulator import *

inp = r'example.inp'
rpt = r'example.rpt'
out = r'example.out'
sim = Simulator(inp, rpt, out)
err_code = sim.open()
err_code = sim.start(1)
while(err_code == 0):
    # 获取名称为SU1的调蓄单元的水深
    depth = sim.getValue(sim.SWMM_NODE_DEPTH, sim.getIndex(sim.SWMM_NODE, 'SU1'))
    # 当调蓄单元的水深超过2.0m，名称为P1的水泵启动
    if depth > 2.0:
        sim.setValue(sim.SWMM_LINK_SETTING, sim.getIndex(sim.SWMM_LINK, 'P1'), 1.0)
    err_code, elapsed_time = sim.step()
    print(sim.getCurrentTime().strftime('%Y-%m-%d %H:%M:%S'))
    if elapsed_time == 0:
        break
sim.end()
sim.close()
```
##### 模拟结果读取
SWMM提供swmm_getSavedValue接口，用于在模拟结束（swmm_end）之后和模拟器关闭(swmm_close)之前读取模拟过程线结果。
```
from muswmm.simulator import *

inp = r'example.inp'
rpt = r'example.rpt'
out = r'example.out'
sim = Simulator(inp, rpt, out)
err_code = sim.open()
err_code = sim.start(1)
while(err_code == 0):
    err_code, elapsed_time = sim.step()
    print(sim.getCurrentTime().strftime('%Y-%m-%d %H:%M:%S'))
    if elapsed_time == 0:
        break
sim.end()
# 获取总步长数
total_step = sim.getValue(sim.SWMM_TOTALSTEP,0)
# 获取名称为S1的子汇水区的径流过程线
for i in range(1, total_step + 1):
    value = sim.getSavedValue(sim.SWMM_SUBCATCH_RUNOFF, sim.getIndex(sim.SWMM_SUBCATCH, "S1", i)
    print(value)
sim.close()
```
#### 二进制结果文件读取
```
from muswmm.output import *

output = Output()
output.open('example.out')
# 获取名称为S1的子汇水区的径流过程线
results = output.get_results(output.SUBCATCH, 'S1', output.SUBCATCH_RUNOFF)
print(results)
output.close()
```
