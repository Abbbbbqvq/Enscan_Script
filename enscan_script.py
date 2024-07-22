# -*- coding: utf-8 -*-

import argparse
from time import sleep
import time
import subprocess
import re
import os
import requests
import base64
import json
import xlwt
from bs4 import BeautifulSoup

def enscan_domain():
    domain_list = []
    icp_list = []
    wechat = []
    app = []
    l = []
    is_null = []
    for file_name in os.listdir("./" + args.running_dir):
        not_null = 0
        if os.path.isfile(os.path.join("./" + args.running_dir, file_name)):
            if ".json" in file_name:
                with open("./" + args.running_dir + "/" + file_name, 'r', encoding='utf-8') as f:
                    t = re.compile('"domain":"(.*?)",')
                    p = f.read()
                    r = t.findall(p)
                    if len(r) > 0:
                        l.append(file_name.replace("【合并】","").replace(".json","："))
                    for i in r:
                        domain_list.append(i)
                        l.append("    " + i)
                        not_null = 1
                    try:
                        d = json.loads(p)
                    except:
                        not_null = 0
                    try:
                        for i in d["wechat"]:
                            wechat.append(i['name'])
                            l.append("    " + i['name'])
                            not_null = 1
                    except:
                        not_null = 0
                    try:
                        for i in d["app"]:
                            app.append(i['name'])
                            l.append("    " + i['name'])
                            not_null = 1
                    except:
                        not_null = 0
                    t = re.compile('"icp":"(.*?)",')
                    r = t.findall(p)
                    for i in r:
                        if ("    " + i) in l:
                            continue
                        else:
                            icp_list.append(i)
                            l.append("    " + i)
                            not_null = 1
                    if not_null == 0:
                        is_null.append(file_name)

    def is_ip_address(text):
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        return re.match(ip_pattern, text) is not None

    def is_domain(text):
        domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
        return re.match(domain_pattern, text) is not None

    ip = []
    domain = []
    other = []
    for i in domain_list:
        if is_ip_address(i):
            ip.append(i)
        elif is_domain(i):
            domain.append(i)
        else:
            other.append(i)

    result_file = open(args.output_dir + "/result.txt", "a+", encoding='utf-8')
    ip_file = open(args.output_dir + "/ip.txt", "a+", encoding='utf-8')
    domain_file = open(args.output_dir + "/domain.txt", "a+", encoding='utf-8')
    icp_file = open(args.output_dir + "/icp.txt", "a+", encoding='utf-8')
    wechat_file = open(args.output_dir + "/wechat.txt", "a+", encoding='utf-8')
    app_file = open(args.output_dir + "/app.txt", "a+", encoding='utf-8')

    result_file.write(time.asctime() + "\n")
    result_file.write("找到的ip资产如下：\n")
    if len(ip) == 0:
        result_file.write("嘤嘤嘤，没找到ip捏(*꒦ິ⌓꒦ີ)\n")
        print("嘤嘤嘤，没找到ip捏(*꒦ິ⌓꒦ີ)")
    else:
        for i in ip:
            result_file.write(i + "\n")
            ip_file.write(i + "\n")
    result_file.write("\n")
    result_file.write("找到的domain资产如下：\n")
    if len(domain) == 0:
        result_file.write("嘤嘤嘤，没找到domain捏(*꒦ິ⌓꒦ີ)\n")
        print("嘤嘤嘤，没找到domain捏(*꒦ິ⌓꒦ີ)")
    else:
        for i in domain:
            result_file.write(i + "\n")
            domain_file.write(i + "\n")
    result_file.write("\n")
    result_file.write("找到的公众号如下：\n")
    if len(wechat) == 0:
        result_file.write("嘤嘤嘤，没找到公众号捏(*꒦ິ⌓꒦ີ)\n")
        print("嘤嘤嘤，没找到公众号捏(*꒦ິ⌓꒦ີ)")
    else:
        for i in wechat:
            result_file.write(i + "\n")
            wechat_file.write(i + "\n")
    result_file.write("\n")
    result_file.write("找到的app如下：\n")
    if len(wechat) == 0:
        result_file.write("嘤嘤嘤，没找到app捏(*꒦ິ⌓꒦ີ)\n")
        print("嘤嘤嘤，没找到A屁屁捏(*꒦ິ⌓꒦ີ)")
    else:
        for i in app:
            result_file.write(i + "\n")
            app_file.write(i + "\n")
    result_file.write("\n")
    result_file.write("找到的icp资产如下：\n")
    if len(icp_list) == 0:
        result_file.write("嘤嘤嘤，没找到icp捏(*꒦ິ⌓꒦ີ)\n")
        print("嘤嘤嘤，没找到icp捏(*꒦ິ⌓꒦ີ)")
    else:
        for i in icp_list:
            result_file.write(i + "\n")
            icp_file.write(i + "\n")
    result_file.write("\n")
    result_file.write("找到正则匹配外的资产：\n")
    if len(other) == 0:
        result_file.write("桀桀桀桀，确认没有正则匹配外的资产，程序无误，nice！\n")
        print("桀桀桀桀，确认没有正则匹配外的资产，程序无误，nice！")
    else:
        result_file.write("omg，出现了一些问题，请手动处理如下资产：\n")
        print("omg，出现了一些问题，请手动处理如下资产：")
        for i in other:
            result_file.write(i + "\n")
            print(i)
    if len(is_null) == 0:
        print("targets里的资产都有东西，安服仔永不空军！！！")
    else:
        print("这些资产不争气，啥都没有！")
        result_file.write("\n下面这些资产没东西：\n")
        for i in is_null:
            result_file.write(i + "\n")
            print(i)
    check = open(args.output_dir + "/check.txt", "a+", encoding='utf-8')
    check.write(time.asctime() + "\n")
    if len(l) == 0:
        check.write("检查一下你他喵的是不是没放资产！\n")
        print("检查一下你他喵的是不是没放资产！")
    else:
        if len(is_null) != 0:
            check.write("无内容资产：\n")
            for i in is_null:
                check.write(i + "\n")
            check.write("\n\n")
        check.write("资产分类：\n")
        for i in l:
            check.write(i + "\n")
    check.write("\n\n")
    result_file.write("\n\n")

    print("结果都将导出在" + args.output_dir + "里哦，请注意查收！")


def enscan_run(deep=' '):
    run_null = []
    err_file = open(args.output_dir + "/err.txt", "a+", encoding='utf-8')
    err_file.write(time.asctime() + "\n")
    err_file.write("查询失败目标资产名单：\n")
    if deep != ' ':
        deep = '-invest 100 -deep ' + deep
    with open('targets.txt', 'r', encoding='utf-8') as f:
        current_line = 0
        all_line = len(f.readlines())
        f.seek(0)
        for line in f:
            current_line += 1
            print("正在运行enscan，当前正在导出：" + line.replace("\n", "") + "，目前进度：" + "{:.2%}".format(current_line / all_line))
            line = line.replace('\n', '')
            commond = './enscan -n ' + line + ' -json ' + deep
            print(commond)
            output = subprocess.run(commond, shell=True, capture_output=True, text=True, encoding='utf-8')
            if "无法解析信息错误信息" in output.stdout:
                print("网络错误，已将" + line + "添加到err.txt文件中，请手动打开爱企查检查情况。")
                err_file.write(line + "\n")
            elif "没有查询到关键词" in output.stdout:
                print("没有查询到目标资产：" + line + "，已添加到err.txt文件中")
                run_null.append(line)
            sleep(5)
    err_file.write("\n\n未查询到的资产：\n")
    for i in run_null:
        err_file.write(i + "\n")

localtime = time.localtime(time.time())
make_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

def ip_c_search():
    print("正在查询ip C段")
    ip_c_file = open(args.output_dir + "/ip_c.txt", "a+", encoding='utf-8')
    ip_file = open(args.output_dir + "/ip.txt", "r", encoding='utf-8')
    for ip in ip_file.readlines():
        t = re.compile(r'\.(\d+)\n')
        r = t.findall(ip)[0]
        url = "https://chapangzhan.com/" + ip.replace(r + "\n", "0") + "/24"
        # 定义header
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }
        # 发起请求
        req = requests.get(url, headers=header)
        bs = BeautifulSoup(req.text, "html.parser")
        body = str(bs.body)
        t = re.compile('<a href="https://ipchaxun.com/(.*?)/" rel="nofollow" target="_blank">')
        r = t.findall(body)
        for c_ip in r:
            print("当前正在查询：" + c_ip)
            ip138_run(c_ip)
            sleep(1)

def ip138_run(ip):
    url = "https://site.ip138.com/" + ip + "/"
    # 定义header
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    # 发起请求
    req = requests.get(url, headers=header)
    bs = BeautifulSoup(req.text, "html.parser")
    body = str(bs.body)
    t = re.compile('<ul id="list">(.*?)</ul>', re.DOTALL)
    r = t.findall(body)
    t = re.compile('target="_blank">(.*?)</a></li>', re.DOTALL)
    domain = t.findall(r[0])
    for i in domain:
        print(i)

def hunter_scan():
    global res
    is_null = ["hunter提取为空或是失败的资产："]
    number = 1
    print("正在使用hunter提取domain，请稍等")
    hunter_create_xls()
    api_key = ""
    with open("./" + args.output_dir + "/domain.txt", 'r', encoding='utf-8') as domain_read:
        for line in domain_read.readlines():
            line = line.replace('\n', '')
            print("正在使用hunter提取：" + line)
            query_sentence = 'domain.suffix="' + line + '" + and ip.country=="中国"'
            search = base64.urlsafe_b64encode(query_sentence.encode("utf-8"))
            search = str(search, 'utf8')
            is_page = 1
            while True:
                url = 'https://hunter.qianxin.com/openApi/search?api-key=' + str(api_key) + '&search=' + str(search) + '&page=' + str(is_page) + '&page_size=100&is_web=3'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
                }
                print("正在使用hunter提取：" + line + "，当前正在导出第" + str(is_page) + "页")
                try:
                    resp = requests.get(url=url, headers=headers)
                    res = json.loads((resp.content).decode('utf-8'))
                    if res["code"] != 200:
                        if res["code"] == 429:
                            continue
                        is_null.append(line)
                        print("错误信息：", end = "")
                        print(res)
                    elif res["data"]["arr"] == None and res["code"] != 400:
                        if is_page == 1:
                            is_null.append(line)
                        else:
                            break
                    elif res["data"]["arr"] != None and res["code"] != 400:
                        number = hunter_write_xls(number)
                except:
                    is_null.append(line)
                    print("错误信息：", end="")
                    print(res)
                sleep(3)
                is_page += 1
    err_file = open(args.output_dir + "/err.txt", "a+", encoding='utf-8')
    for i in is_null:
        err_file.write(i + "\n")
    print("提取完毕，正在" + args.output_dir + "目录下生成xls，提取到的ip已经筛选好放入ip.txt")
    workbook_for_hunter.save(args.output_dir + '/hunter.xls')

def hunter_create_xls():
    global workbook_for_hunter
    workbook_for_hunter = xlwt.Workbook(encoding='utf-8')
    global worksheet_for_hunter
    worksheet_for_hunter = workbook_for_hunter.add_sheet('鹰图查询结果')
    # 创建颜色
    pattern = xlwt.Pattern()  # 创建模式对象
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 5  # 设置模式颜色为黄色
    style = xlwt.XFStyle()  # 创建样式对象
    style.pattern = pattern  # 将模式加入到样式对象
    # 设置单元格的宽度
    worksheet_for_hunter.col(0).width = 400 * 20
    worksheet_for_hunter.col(1).width = 200 * 20
    worksheet_for_hunter.col(2).width = 100 * 20
    worksheet_for_hunter.col(3).width = 400 * 20
    worksheet_for_hunter.col(4).width = 150 * 20
    worksheet_for_hunter.col(5).width = 400 * 20
    worksheet_for_hunter.col(6).width = 400 * 20
    worksheet_for_hunter.col(7).width = 400 * 20
    # 写第一行的标题
    worksheet_for_hunter.write(0, 0, '网址', style)
    worksheet_for_hunter.write(0, 1, 'IP地址', style)
    worksheet_for_hunter.write(0, 2, '端口', style)
    worksheet_for_hunter.write(0, 3, '网站标题', style)
    worksheet_for_hunter.write(0, 4, '域名', style)
    worksheet_for_hunter.write(0, 5, '状态码', style)
    worksheet_for_hunter.write(0, 6, '公司名称', style)
    worksheet_for_hunter.write(0, 7, '备案号', style)

def hunter_write_xls(number):
    global l
    l =0
    ip_file = open(args.output_dir + "/ip.txt", "a+", encoding='utf-8')
    url_file = open(args.output_dir + "/url.txt", "a+", encoding='utf-8')
    for l in range(len(res["data"]["arr"])):
        its_url = res["data"]["arr"][l]["url"]  # 网址
        url_file.write(its_url + "\n")
        ip = res["data"]["arr"][l]["ip"]  # IP地址
        ip_file.write(ip + "\n")
        port = res["data"]["arr"][l]["port"]  # 端口
        web_title = res["data"]["arr"][l]["web_title"]  # 网站标题
        domain = res["data"]["arr"][l]["domain"]  # 域名
        status_code = res["data"]["arr"][l]["status_code"]  # 状态码
        company = res["data"]["arr"][l]["company"]  # 公司名称
        record_number = res["data"]["arr"][l]["number"]  # 备案号

        # 写入数据
        worksheet_for_hunter.write(number, 0, its_url)
        worksheet_for_hunter.write(number, 1, ip)
        worksheet_for_hunter.write(number, 2, port)
        worksheet_for_hunter.write(number, 3, web_title)
        worksheet_for_hunter.write(number, 4, domain)
        worksheet_for_hunter.write(number, 5, status_code)
        worksheet_for_hunter.write(number, 6, company)
        worksheet_for_hunter.write(number, 7, record_number)
        number += 1
    return number

def fofa_scan():
    global res
    number = 1
    fofa_create_xls()
    fofa_key = ''
    with open("./" + args.output_dir + "/domain.txt", 'r', encoding='utf-8') as domain_read:
        for line in domain_read.readlines():
            line = line.replace('\n', '')
            print("正在使用fofa提取：" + line)
            query_sentence = 'domain="' + line + '"'
            # query_sentence = 'domain = "jsydzb.com"'
            fofa_search = base64.urlsafe_b64encode(query_sentence.encode("utf-8"))
            fofa_search = str(fofa_search, 'utf8')
            fofa_is_page = 1
            while True:
                url = 'https://fofa.info/api/v1/search/all?&key=' + str(fofa_key) + '&qbase64=' + str(fofa_search) + "&page=" + str(fofa_is_page) + "&full=true"
                print(url)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
                }
                print("正在使用fofa提取：" + line + "，当前正在导出第" + str(fofa_is_page) + "页")
                try:
                    resp = requests.get(url=url, headers=headers)
                    res = json.loads((resp.content).decode('utf-8'))
                    print(res)
                    if len(res['results']) == 0:
                        break
                    number = fofa_write_xls(number)
                except:
                    print("导出出现错误，请自查：")
                    print(res)
                sleep(3)
                fofa_is_page += 1
            fofa_for_workbook.save(args.output_dir + "/fofa.xls")

def fofa_create_xls():
    global fofa_for_workbook
    fofa_for_workbook = xlwt.Workbook(encoding='utf-8')
    global worksheet_for_fofa
    worksheet_for_fofa = fofa_for_workbook.add_sheet('fofa查询结果')
    # 创建颜色
    pattern = xlwt.Pattern()  # 创建模式对象
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 5  # 设置模式颜色为黄色
    style = xlwt.XFStyle()  # 创建样式对象
    style.pattern = pattern  # 将模式加入到样式对象
    # 设置单元格的宽度
    worksheet_for_fofa.col(0).width = 400 * 20
    worksheet_for_fofa.col(1).width = 200 * 20
    worksheet_for_fofa.col(2).width = 100 * 20
    # 写第一行的标题
    worksheet_for_fofa.write(0, 0, '网址', style)
    worksheet_for_fofa.write(0, 1, 'IP地址', style)
    worksheet_for_fofa.write(0, 2, '端口', style)

def fofa_write_xls(number):
    ip_file = open(args.output_dir + "/ip.txt", "a+", encoding='utf-8')
    url_file = open(args.output_dir + "/url.txt", "a+", encoding='utf-8')
    for l in range(len(res['results'])):
        its_url = res['results'][l][0]  # 网址
        url_file.write(its_url + "\n")
        ip = res['results'][l][1]  # IP地址
        ip_file.write(ip + "\n")
        port = res['results'][l][2]  # 端口

        # 写入数据
        worksheet_for_fofa.write(number, 0, its_url)
        worksheet_for_fofa.write(number, 1, ip)
        worksheet_for_fofa.write(number, 2, port)
        number += 1
    return number


def remove_duplicates():
    ip_file_list = []
    url_file_list = []
    ip_file = open(args.output_dir + "/ip.txt", "r", encoding='utf-8')
    for i in ip_file:
        if i in ip_file_list:
            continue
        else:
            ip_file_list.append(i)
    ip_file = open(args.output_dir + "/ip.txt", "w", encoding='utf-8')
    for i in ip_file_list:
        ip_file.write(i)
    url_file = open(args.output_dir + "/url.txt", "r", encoding='utf-8')
    for i in url_file:
        if i in url_file_list:
            continue
        else:
            url_file_list.append(i)
    url_file = open(args.output_dir + "/url.txt", "w", encoding='utf-8')
    for i in url_file_list:
        url_file.write(i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-m", "--mode", dest='running_mode',
                        help="运行模式：\n例如：python3 main.py -m 1\n1、运行完enscan然后使用hunter提取出资产域名信息。\n"
                             "2、只运行enscan。\n"
                             "3、只提取资产域名信息。\n"
                             "4、只运行hunter(默认提取result/domain.txt，不是默认目录需要-o指定目录)\n"
                             "5、只运行fofa(默认提取result/domain.txt，不是默认目录需要-o指定目录)")
    parser.add_argument("-d", "--dir", dest='running_dir',
                        help="指定enscan输出目录\n例如：python3 main.py -d outs(不加-d参数默认提取outs目录下的导出结果)")
    parser.add_argument("-o", "--output", dest='output_dir',
                        help="保存结果到xxx文件夹\n例如：python3 main.py -o result(不加-o参数默认保存在result文件夹下)")
    parser.add_argument("-sub", "--subsidiary", dest='subsidiary', default=' ',
                        help="搞子公司\n例如：python3 main.py -m 2 -sub 3 (百分百控股往下摸三级子公司)")

    args = parser.parse_args()
    if args.running_dir == None:
        args.running_dir = "outs"
    if args.output_dir == None:
        args.output_dir = "result"
    if args.running_mode == "1":
        if os.path.isdir(args.output_dir):
            print(args.output_dir + "文件夹已存在，不再继续创建")
        else:
            os.makedirs(args.output_dir)
        enscan_run(args.subsidiary)
        enscan_domain()
        hunter_scan()
        remove_duplicates()
    elif args.running_mode == "2":
        if os.path.isdir(args.output_dir):
            print(args.output_dir + "文件夹已存在，不再继续创建")
        else:
            os.makedirs(args.output_dir)
        enscan_run(args.subsidiary)
    elif args.running_mode == "3":
        if os.path.isdir(args.output_dir):
            print(args.output_dir + "文件夹已存在，不再继续创建")
        else:
            os.makedirs(args.output_dir)
        enscan_domain()
    elif args.running_mode == "4":
        hunter_scan()
        remove_duplicates()
    elif args.running_mode == "5":
        fofa_scan()
        remove_duplicates()
