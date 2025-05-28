# Enscan_Script

适用于大批量资产导出，快速筛选Enscan输出结果中的domain和ip，利用hunter快速批量导出资产，让你在红蓝攻防中快人一步。

## 声明

不建议给脚本加上并发，可能会导致账号被封，该项目仅用于合法信息查询，请勿用于非法用途

## 为什么使用该项目

直接使用Enscan常常会有的一个痛点，还没导出几条资产就触发安全验证

![image-20250528093329169](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20250528093329169.png)

aqc安全验证现在变得鸡贼了，使用Enscan触发安全验证，你手动打开aqc去解验证的时候发现一切正常，但是使用Enscan仍然存在安全验证

![image-20250528093659295](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20250528093659295.png)

曾经也设想过，多开几个账号，共同去导出目标，但是也存在同样问题，跑不了多少个目标就触发安全验证了，即使加上sleep延迟也还是可能会触发安全验证。用代理池去并发跑，一下子就容易封掉账号，所以还是直接用热点开关飞行模式切换ip会比较好。或者直接舍弃并发，每20秒切换一次代理池应该也可以(不确定这样会不会封号)。个人目前使用热点切换ip的方式，暂时还没有被封号。

![image-20250528092706084](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20250528092706084.png)



## 如何使用

下载enscan放到当前目录下，重命名为“enscan”，windows用户命名为“enscan.exe”。下载好后根据enscan项目，配置好config.yaml文件

![image-20250528094910615](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20250528094910615.png)

帮助信息

```
python3 enscan_script.py -h
```

![image-20250528095212683](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20250528095212683.png)

targets.txt填入导出目标单位

```
python3 enscan_script.py -m 1
```

![image-20250528100231052](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20250528100231052.png)

出现如下提示，按照提示开关飞行模式切换ip

![image-20250528095649225](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20250528095649225.png)

待Enscan查询完毕后，使用如下命令整合导出资产

```
python3 enscan_script.py -m 2
```

![image-20250528101005251](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20250528101005251.png)

如果查询目标命令和查询结果不符，则不导出对应资产，重新确认修改资产名字后重新运行enscan

![image-20250528100435480](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20250528100435480.png)

![image-20250528101041533](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20250528101041533.png)

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

2025.05.28 更新项目Enscan_Script，修复存在的多个问题

## 待更新内容

暂时也想不到要更新什么内容
