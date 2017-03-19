`项目说明：`

本项目是使用开源的宽客库tquant，获取股票信息，并挖掘股票的有用信息。

**_20170320_**

1.计算股票日均线数据线程
2.重构股票日K数据处理线程，讲全量和增量复用一份代码
3.优化日志打印显示

**_20170318_**

1.增加已经获取股票的增量日K数据处理，即随着时间的往后推移，先前获取的股票日K数据已经不是最新的了，需要单独的线程处理最近几日的日K数据

2.优化线程进度打印字符显示，更友好

3.修改配置文件后缀为cfg，cfg格式内容更清晰明了

**_20170317_**

1.增加获取证券交易日功能代码

**_20170316_**

1.优化线程执行进度显示方式

2.增加股票日K数据处理断点续传功能

3.增加异常捕获，防止异常后线程终断

**_20170315_**

1.增加获取A股日K数据入库代码

**_20170314_**

1.本项目是使用开源的tquant库获取证券信息；

2.目前只支持落库MySQL；

3.当前支持国内A股列表信息落库

4.使用方式：先配置MySQL数据库连接信息；执行sqlscript目录下的所有的sql脚本文件，并保证成功；然后运行bootstrap目录下的BootStrap.py即可。

5.tquant库安装使用教程http://www.tquant.trade/
