# Enscan_Script

快速筛选Enscan输出结果中的domain，让你在红蓝攻防中快人一步



直接Enscan导出大批量资产失败率太高了，所以干脆写个脚本，实测跑1500+个资产没问题，这次是加了个hunter的功能，用来查找domain.txt中的资产，导出信息为url.txt和ip.txt，用于直接工具梭哈，这里推荐工具为dddd。hunter和fofa导出功能可能会耗费大量积分，各位师傅们酌情使用，特别是fofa查询，不仅消耗点数，而且每天还有查询次数限制。

脚本主要实现功能是和Enscan功能重复的，所以这个脚本的使用看个人喜好，有问题和建议可以提Issues，共同完善这个懒狗脚本。

## 声明

使用程序可能导致账号被封，仅用于信息收集用途，请勿用于非法用途

## 环境配置

首先下载enscan到本地，生成配置文件，配置好需要的api，详细的配置请移步enscan_go项目

[wgpsec/ENScan_GO: 一款基于各大企业信息API的工具，解决在遇到的各种针对国内企业信息收集难题。一键收集控股公司ICP备案、APP、小程序、微信公众号等信息聚合导出。 (github.com)](https://github.com/wgpsec/ENScan_GO)

红队工具dddd下载，详细配置请移步dddd项目

[SleepingBag945/dddd: dddd是一款使用简单的批量信息收集,供应链漏洞探测工具，旨在优化红队工作流，减少伤肝的机械性操作。支持从Hunter、Fofa批量拉取目标 (github.com)](https://github.com/SleepingBag945/dddd)

## 如何使用

hunter功能点懒得截图了，师傅们自己测试吧！

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

hunter输出结果示例

![image-20240516064119071](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/1.png)

![image-20240516064119071](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/2.png)

![image-20240516064119071](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/3.png)

![image-20240516064119071](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/4.png)

![image-20240516064119071](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/5.png)

## 更新日志

2024.04.14 创建项目Enscan_Script。

2024.04.24 更新项目Enscan_Script，将多个py脚本整合到一个py文件中。

2024.05.07 更新项目Enscan_Script，将提取内容优化。

2024.05.16 更新项目Enscan_Script，修复一系列乱七八糟的bug，将提取内容优化，新增提取公众号和App。

2024.05.24 更新项目Enscan_Script，联合hunter查询，导出url和ip，可直接放入dddd和fscan快速梭哈。

2024.05.25 更新项目Enscan_Script，增加100%控股子公司输出。

2024.07.22 更新项目Enscan_Script，增加fofa查询功能。

## 待更新内容

暂时也想不到要更新什么内容
