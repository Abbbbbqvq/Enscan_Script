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

    result_file = open(args.output_dir + "/result.txt", "a+")
    ip_file = open(args.output_dir + "/ip.txt", "a+")
    domain_file = open(args.output_dir + "/domain.txt", "a+")
    icp_file = open(args.output_dir + "/icp.txt", "a+")
    wechat_file = open(args.output_dir + "/wechat.txt", "a+")
    app_file = open(args.output_dir + "/app.txt", "a+")

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
    check = open(args.output_dir + "/check.txt", "a+")
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


def enscan_run():
    run_null = []
    err_file = open(args.output_dir + "/err.txt", "a+")
    err_file.write(time.asctime() + "\n")
    err_file.write("查询失败目标资产名单：\n")
    with open('targets.txt', 'r', encoding='utf-8') as f:
        current_line = 0
        all_line = len(f.readlines())
        f.seek(0)
        for line in f:
            current_line += 1
            print("正在运行enscan，当前正在导出：" + line.replace("\n","") + "，目前进度：" + "{:.2%}".format(current_line / all_line))
            line = line.replace('\n', '')
            output = subprocess.run('./enscan -n ' + line + ' -o ' + args.running_dir + ' -json', shell=True, capture_output=True, text=True)
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

def hunter_scan():
    global res
    number = 1
    print("正在使用hunter提取domain，请稍等")
    hunter_write_to_xls()
    api_key = "289d0affd492d7d37edfa29f7a5a93c52192a365ef99eba95d7f261851d20632"
    with open("./" + args.output_dir + "/domain.txt", 'r', encoding='utf-8') as domain_read:
        for line in domain_read.readlines():
            line = line.replace('\n', '')
            print("正在提取：" + line)
            query_sentence = 'domain.suffix="' + line + '"'
            search = base64.urlsafe_b64encode(query_sentence.encode("utf-8"))
            search = str(search, 'utf8')
            url = 'https://hunter.qianxin.com/openApi/search?api-key=' + str(api_key) + '&search=' + str(
                search) + '&page=1&page_size=10&is_web=3'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
            }
            resp = requests.get(url=url, headers=headers)
            res = json.loads((resp.content).decode('utf-8'))
            if res["data"]["arr"] != None:
                number = hunter_scan_and_write(number)
            sleep(2)
    print("提取完毕，正在" + args.output_dir + "目录下生成xls，提取到的ip已经筛选好放入ip.txt")
    workbook.save(args.output_dir + '/hunter.xls')

def hunter_write_to_xls():
    global workbook
    workbook = xlwt.Workbook(encoding='utf-8')
    global worksheet
    worksheet = workbook.add_sheet('鹰图查询结果')
    # 创建颜色
    pattern = xlwt.Pattern()  # 创建模式对象
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 5  # 设置模式颜色为黄色
    style = xlwt.XFStyle()  # 创建样式对象
    style.pattern = pattern  # 将模式加入到样式对象
    # 设置单元格的宽度
    worksheet.col(0).width = 400 * 20
    worksheet.col(1).width = 200 * 20
    worksheet.col(2).width = 100 * 20
    worksheet.col(3).width = 400 * 20
    worksheet.col(4).width = 150 * 20
    worksheet.col(5).width = 400 * 20
    worksheet.col(6).width = 400 * 20
    worksheet.col(7).width = 400 * 20
    # 写第一行的标题
    worksheet.write(0, 0, '网址', style)
    worksheet.write(0, 1, 'IP地址', style)
    worksheet.write(0, 2, '端口', style)
    worksheet.write(0, 3, '网站标题', style)
    worksheet.write(0, 4, '域名', style)
    worksheet.write(0, 5, '状态码', style)
    worksheet.write(0, 6, '公司名称', style)
    worksheet.write(0, 7, '备案号', style)

def hunter_scan_and_write(number):
    global l
    l =0
    ip_file = open(args.output_dir + "/ip.txt", "a+")
    url_file = open(args.output_dir + "/url.txt", "a+")
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
        worksheet.write(number, 0, its_url)
        worksheet.write(number, 1, ip)
        worksheet.write(number, 2, port)
        worksheet.write(number, 3, web_title)
        worksheet.write(number, 4, domain)
        worksheet.write(number, 5, status_code)
        worksheet.write(number, 6, company)
        worksheet.write(number, 7, record_number)
        number += 1
    return number

def remove_duplicates():
    ip_file_list = []
    url_file_list = []
    ip_file = open(args.output_dir + "/ip.txt", "r")
    for i in ip_file:
        if i in ip_file_list:
            continue
        else:
            ip_file_list.append(i)
    ip_file = open(args.output_dir + "/ip.txt", "w")
    for i in ip_file_list:
        ip_file.write(i)
    url_file = open(args.output_dir + "/url.txt", "r")
    for i in url_file:
        if i in url_file_list:
            continue
        else:
            url_file_list.append(i)
    url_file = open(args.output_dir + "/url.txt", "w")
    for i in url_file_list:
        url_file.write(i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-m", "--mode", dest='running_mode', help="运行模式：\n例如：python3 main.py -m 1\n1、运行完enscan然后使用hunter提取出资产域名信息。\n2、只运行enscan。\n3、只提取资产域名信息。\n4、只运行hunter(默认提取result/domain.txt，不是默认目录需要-o指定目录)")
    parser.add_argument("-d", "--dir", dest='running_dir', help="指定enscan输出目录\n例如：python3 main.py -d outs(不加-d参数默认提取outs目录下的导出结果)")
    parser.add_argument("-o", "--output", dest='output_dir', help="保存结果到xxx文件夹\n例如：python3 main.py -o result(不加-o参数默认保存在result文件夹下)")
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
        enscan_run()
        enscan_domain()
        #hunter_scan()
        #remove_duplicates()
    elif args.running_mode == "2":
        if os.path.isdir(args.output_dir):
            print(args.output_dir + "文件夹已存在，不再继续创建")
        else:
            os.makedirs(args.output_dir)
        enscan_run()
    elif args.running_mode == "3":
        if os.path.isdir(args.output_dir):
            print(args.output_dir + "文件夹已存在，不再继续创建")
        else:
            os.makedirs(args.output_dir)
        enscan_domain()
    elif args.running_mode == "4":
        hunter_scan()
        remove_duplicates()
