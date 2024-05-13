# Enscan_Script

快速筛选Enscan输出结果中的domain，让你在红蓝攻防中快人一步

## 声明

个人感觉吧，直接Enscan导出大批量资产失败率太高了，所以干脆写个脚本，实测跑1500+个资产没问题。

脚本主要实现功能是和Enscan功能重复的，所以这个脚本的使用看个人喜好，有问题和建议可以提Issues，共同完善这个懒狗脚本。





脚本用于安全渗透测试，请勿用于非法渗透测试。

## 环境配置

首先下载enscan到本地，生成配置文件，配置好需要的api，详细的配置请移步enscan_go项目

[wgpsec/ENScan_GO: 一款基于各大企业信息API的工具，解决在遇到的各种针对国内企业信息收集难题。一键收集控股公司ICP备案、APP、小程序、微信公众号等信息聚合导出。 (github.com)](https://github.com/wgpsec/ENScan_GO)

目录结构大概是这样

![image-20240507045734257](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240507045734257.png)

Enscan的名字定义可以在py文件中修改，直接全局搜索可以搜到，targets.txt放的是目标资产名

## 如何使用

帮助信息

```
python3 enscan_script.py -h
```

![image-20240507050618405](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240507050618405.png)

运行enscan然后提取资产域名信息

![image-20240507050938889](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240507050938889.png)

默认导出在result文件夹下

![image-20240507051029301](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240507051029301.png)

分别导出多个结果txt，方便利用导出结果

![image-20240507051306725](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/images/image-20240507051306725.png)

## 更新日志

2024.4.14 创建项目Enscan_Script。

2024.4.24 更新项目Enscan_Script，将多个py脚本整合到一个py文件中。

2024.5.  7 更新项目Enscan_Script，将提取内容优化。

## 待更新内容

1、提取公众号名和小程序名。

2、提取结果联动扫描器一条龙服务。

3、联合hunter查询，导出url和ip，可直接放入dddd和fscan快速梭哈。

4、enscan运行失败的重新运行机制。
