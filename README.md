# Enscan_Script

快速筛选Enscan输出结果中的domain，让你在红蓝攻防中快人一步

## 如何使用

首先下载enscan到本地，生成配置文件，配置好需要的api，详细的配置请移步enscan_go项目

[wgpsec/ENScan_GO: 一款基于各大企业信息API的工具，解决在遇到的各种针对国内企业信息收集难题。一键收集控股公司ICP备案、APP、小程序、微信公众号等信息聚合导出。 (github.com)](https://github.com/wgpsec/ENScan_GO)

![image-20240413113310675](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/image-20240413113310675.png)

enscan文件命名要跟run.py中的一致，和run.py文件放置在当前目录下。

domain.py要放在enscan输出的目录下(enscan默认输出目录为outs)。

资产添加在targets.txt中

![image-20240413113736806](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/image-20240413113736806.png)

run.py用于启动enscan，省去输命令的时间，同时sleep(5)能够降低爱企查网站的防御机制，目前只用过爱企查，其他网站得要自己手动更改绕过方法。

enscan查询完所有资产结果后，直接运行domain.py，即可输出导出资产中的domain，输出结果会在终端和outs文件夹下的result.txt文件中显示。

![image-20240413115335671](https://github.com/Abbbbbqvq/Enscan_Script/blob/main/image-20240413115335671.png)
