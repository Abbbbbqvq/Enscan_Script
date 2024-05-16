# Enscan_Script

快速筛选Enscan输出结果中的domain，让你在红蓝攻防中快人一步



直接Enscan导出大批量资产失败率太高了，所以干脆写个脚本，实测跑1500+个资产没问题，本来打算加了个hunter的功能，用来导出url和ip用的，但是很不辛，功能在5月10日写好，hunter就公告5月10日到5月26日维护，日你妈退钱。功能大概测了一下，调用hunter api会因为网络问题会查不到或者是出现报错，这点要等hunter维护完了再去进行修改。

脚本主要实现功能是和Enscan功能重复的，所以这个脚本的使用看个人喜好，有问题和建议可以提Issues，共同完善这个懒狗脚本。

## 声明

使用程序可能导致账号被封，仅用于信息收集用途，请勿用于非法用途

## 环境配置

首先下载enscan到本地，生成配置文件，配置好需要的api，详细的配置请移步enscan_go项目

[wgpsec/ENScan_GO: 一款基于各大企业信息API的工具，解决在遇到的各种针对国内企业信息收集难题。一键收集控股公司ICP备案、APP、小程序、微信公众号等信息聚合导出。 (github.com)](https://github.com/wgpsec/ENScan_GO)

## 如何使用

hunter功能点使用存在点小问题，等hunter维护完就进行修改完善，这里暂不演示。

帮助信息

```
python3 enscan_script.py -h
```

![image-20240516055358937](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516055358937.png)

运行enscan然后提取资产域名信息

```
python3 enscan_script.py -m 1
```

若是不加“-o”参数默认导出在result文件夹下

![image-20240516061056580](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516061056580.png)

如果超过10秒没反应，可能是触发了爱企查的安全验证

![image-20240516060638729](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516060638729.png)

出现如下情况，打开爱企查通过安全验证即可，出现网络错误报错，解决方法也一样

![image-20240516060748013](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516060748013.png)

![image-20240516060830333](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516060830333.png)

分别导出多个结果txt，方便利用扫描器一键梭哈

![image-20240516061753320](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516061753320.png)

app资产

![image-20240516063624024](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516063624024.png)

icp备案

![image-20240516063705832](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516063705832.png)

ip地址

![image-20240516063815426](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516063815426.png)

公众号

![image-20240516063835139](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516063835139.png)

输出结果

![image-20240516064051788](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516064051788.png)

用于资产审查

![image-20240516064119071](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240516064119071.png)

## 更新日志

2024.04.14 创建项目Enscan_Script。

2024.04.24 更新项目Enscan_Script，将多个py脚本整合到一个py文件中。

2024.05.07 更新项目Enscan_Script，将提取内容优化。

2024.05.16 更新项目Enscan_Script，修复一系列乱七八糟的bug，将提取内容优化，新增提取公众号和App。

## 待更新内容

1、联合hunter查询，导出url和ip，可直接放入dddd和fscan快速梭哈。