import os
import re
import xlwt
import yaml
import time
import json
import base64
import shutil
import requests
import argparse
import threading
import subprocess
from rich import print
from rich.text import Text
from rich.console import Console
from rich.progress import Progress

localtime = time.localtime(time.time())
make_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

make_check_stop = threading.Event()

def gradient_text(text, start_color, end_color):
    """
    创建渐变颜色文本

    :param text: 要渲染的文本
    :param start_color: 起始颜色 (十六进制, 如 "#FF0000")
    :param end_color: 结束颜色 (十六进制, 如 "#0000FF")
    :return: 渐变效果的Text对象
    """

    # 将十六进制颜色转换为RGB元组
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)

    # 创建Text对象
    gradient = Text()

    # 为每个字符计算插值颜色
    for i, char in enumerate(text):
        # 计算当前字符位置的比例 (0.0 - 1.0)
        ratio = i / max((len(text) - 1), 1)  # 避免除以零

        # 计算插值RGB值
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)

        # 创建RGB颜色字符串
        color = f"rgb({r},{g},{b})"

        # 添加带颜色的字符
        gradient.append(char, style=color)

    return gradient

def banner():
    ascii_art = """
     ______                              _____           _       _
    |  ____|                            / ____|         (_)     | |
    | |__   _ __  ___  ___ __ _ _ __   | (___   ___ _ __ _ _ __ | |_
    |  __| | '_ \\/ __|/ __/ _` | '_ \\   \\___ \\ / __| '__| | '_ \\| __|
    | |____| | | \\__ \\ (_| (_| | | | |  ____) | (__| |  | | |_) | |_
    |______|_| |_|___/\\___\\__,_|_| |_| |_____/ \\___|_|  |_| .__/ \\__|
                                   ______                 | |
                                  |______|                |_|
    Version: Enscan_Script v1.3
    Author: Abbbbbqvq
    Github: https://github.com/Abbbbbqvq
    """
    console = Console()
    text = gradient_text(ascii_art, "#00FF00", "#800080")
    console.print(text)

def remove_duplicates():
    ip_file_list = []
    url_file_list = []
    ip_file = open("result/ip.txt", "r", encoding='utf-8')
    for i in ip_file:
        if i in ip_file_list:
            continue
        else:
            ip_file_list.append(i)
    ip_file = open("result/ip.txt", "w", encoding='utf-8')
    for i in ip_file_list:
        ip_file.write(i)
    url_file = open("result/url.txt", "r", encoding='utf-8')
    for i in url_file:
        if i in url_file_list:
            continue
        else:
            url_file_list.append(i)
    url_file = open("result/url.txt", "w", encoding='utf-8')
    for i in url_file_list:
        url_file.write(i)

def hunter_scan(api_key):
    check = open("result/check.txt", "a+", encoding='utf-8')
    check.write(time.asctime() + "\n")
    check.write("已跳过hunter搜索的资产：\n")
    global res
    is_null = ["hunter提取为空或是失败的资产："]
    number = 1
    # print("正在使用hunter提取domain，请稍等")
    hunter_create_xls()
    # api_key = ""
    with open("result/domain.txt", 'r', encoding='utf-8') as domain_read:
        for line in domain_read.readlines():
            line = line.replace('\n', '')
            print("[green][INFO] 正在使用hunter提取：" + line)
            while True:
                try:
                    hunter_num = check_hunter_num(line, api_key)
                    print(f'[green][INFO] 查询到资产数量为：{hunter_num}')
                    break
                except:
                    print("[red bold][ERROR] 请求繁忙，正在重新请求")
            if hunter_num > args.max_number:
                print("[yellow][WARN] 目标："+line+"的资产总数为："+str(hunter_num)+"，已超过设定的最大限制(当前最大限制："+str(args.max_number)+")")
                print("[yellow][WARN] 已跳过当前目标，跳过目标已保存在result/check,txt文件中")
                check.write(f'{line}\n')
                continue
                # flag = 0
                # while flag == 0:
                #     user = input("是否继续使用hunter导出('Y'或'N'，默认'N')>>>>>>")
                #     if user == "" or user == "N":
                #         flag = 1
                #     elif user == "Y":
                #         flag = 2
                # if flag == 1:
                #     continue
            query_sentence = 'domain.suffix="' + line + '" + and ip.country=="中国"'
            search = base64.urlsafe_b64encode(query_sentence.encode("utf-8"))
            search = str(search, 'utf8')
            is_page = 1
            while True:
                url = 'https://hunter.qianxin.com/openApi/search?api-key=' + str(api_key) + '&search=' + str(search) + '&page=' + str(is_page) + '&page_size=100&is_web=3'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
                }
                print("[green][INFO] 正在使用hunter提取：" + line + "，当前正在导出第" + str(is_page) + "页")
                resp = requests.get(url=url, headers=headers)
                res = json.loads((resp.content).decode('utf-8'))
                try:
                    if res["code"] != 200:
                        if res["code"] == 429:
                            continue
                        is_null.append(line)
                        print("[red bold][ERROR] 错误信息：", end = "")
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
                    print(f"[red bold][ERROR] 错误信息：{res}")
                time.sleep(3)
                is_page += 1
    check.write('\n\n')
    err_file = open("result/err.txt", "a+", encoding='utf-8')
    for i in is_null:
        err_file.write(i + "\n")
    print("[green][INFO] 提取完毕，正在" + "result目录下生成xls，提取到的ip已经筛选好放入ip.txt")
    workbook_for_hunter.save('result/hunter.xls')

def check_hunter_num(domain, api_key):
    # api_key = ""
    query_sentence = f'domain.suffix="{domain}" + and ip.country=="中国"'
    search = base64.urlsafe_b64encode(query_sentence.encode("utf-8"))
    search = str(search, 'utf8')
    is_page = 1
    url = 'https://hunter.qianxin.com/openApi/search?api-key=' + str(api_key) + '&search=' + str(
        search) + '&page=' + str(is_page) + '&page_size=1&is_web=3'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    }
    resp = requests.get(url=url, headers=headers)
    res = json.loads((resp.content).decode('utf-8'))
    return res['data']['total']
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
    ip_file = open("result/ip.txt", "a+", encoding='utf-8')
    url_file = open("result/url.txt", "a+", encoding='utf-8')
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

def enscan_domain():
    domain_list = []
    icp_list = []
    wechat = []
    app = []
    l = []
    is_null = []
    check = open("result/check.txt", "a+", encoding='utf-8')
    err = open("result/err.txt", "a+", encoding='utf-8')
    check.write(time.asctime() + "\n")
    check.write("检查是否存在输入有误的资产：\n")
    err.write(time.asctime() + "\n")
    err.write("检查是否存在输入有误的资产：\n")
    for file_name in os.listdir("./outs"):
        not_null = 0
        if os.path.isfile(os.path.join("./outs", file_name)):
            if ".json" in file_name:
                with open("./outs/" + file_name, 'r', encoding='utf-8') as f:
                    try:
                        p = f.read()
                        r = json.loads(p)
                        extra = r['enterprise_info'][0]['extra']
                        extra = extra.replace("aqc⌈", "").replace("⌋", "")
                        name = r['enterprise_info'][0]['name']
                        f.seek(0)
                        if extra != name:
                            print(
                                "[red bold][ERROR] 错误信息：输入的资产与查询结果不符，请重新检查确认！！！错误资产已输出到rusult目录err.txt文件中")
                            check.write(f"{extra}\n")
                            err.write(f"{extra}\n")
                            continue

                        if len(r['icp']) > 0:
                            l.append(file_name.replace("【合并】","").replace(".json","："))
                        for i in range(len(r['icp'])):
                            domain = r['icp'][i]['domain']
                            domain_list.append(domain)
                            l.append("    " + r['icp'][i]['domain'])
                            not_null = 1
                    except:
                        not_null = 0
                    try:
                        for i in r['wechat']:
                            wechat.append(i['name'])
                            l.append("    " + i['name'])
                            not_null = 1
                    except:
                        not_null = 0
                    try:
                        for i in r["app"]:
                            app.append(i['name'])
                            l.append("    " + i['name'])
                            not_null = 1
                    except:
                        not_null = 0
                    try:
                        for i in range(len(r['icp'])):
                            icp = r['icp'][i]['icp']
                            if ("    " + icp) in l:
                                continue
                            else:
                                icp_list.append(icp)
                                l.append("    " + icp)
                                not_null = 1
                    except:
                        not_null = 0
                    if not_null == 0:
                        is_null.append(file_name)

    check.write("\n\n")

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

    result_file = open("result/result.txt", "a+", encoding='utf-8')
    ip_file = open("result/ip.txt", "a+", encoding='utf-8')
    domain_file = open("result/domain.txt", "a+", encoding='utf-8')
    icp_file = open("result/icp.txt", "a+", encoding='utf-8')
    wechat_file = open("result/wechat.txt", "a+", encoding='utf-8')
    app_file = open("result/app.txt", "a+", encoding='utf-8')

    result_file.write(time.asctime() + "\n")
    result_file.write("找到的ip资产如下：\n")
    if len(ip) == 0:
        result_file.write("aqc未查询到ip\n")
        print("[yellow][WARN] aqc未查询到ip")
    else:
        for i in ip:
            result_file.write(i + "\n")
            ip_file.write(i + "\n")
    result_file.write("\n")
    result_file.write("找到的domain资产如下：\n")
    if len(domain) == 0:
        result_file.write("aqc未查询到domain\n")
        print("[yellow][WARN] aqc未查询到domain")
    else:
        for i in domain:
            result_file.write(i + "\n")
            domain_file.write(i + "\n")
    result_file.write("\n")
    result_file.write("找到的公众号如下：\n")
    if len(wechat) == 0:
        result_file.write("aqc未查询到公众号\n")
        print("[yellow][WARN] aqc未查询到公众号")
    else:
        for i in wechat:
            result_file.write(i + "\n")
            wechat_file.write(i + "\n")
    result_file.write("\n")
    result_file.write("找到的app如下：\n")
    if len(wechat) == 0:
        result_file.write("aqc未查询到APP\n")
        print("[yellow][WARN] aqc未查询到APP")
    else:
        for i in app:
            result_file.write(i + "\n")
            app_file.write(i + "\n")
    result_file.write("\n")
    result_file.write("找到的icp资产如下：\n")
    if len(icp_list) == 0:
        result_file.write("aqc未查询到Icp备案\n")
        print("[yellow][WARN] aqc未查询到Icp备案")
    else:
        for i in icp_list:
            result_file.write(i + "\n")
            icp_file.write(i + "\n")
    result_file.write("\n")
    result_file.write("存在错误的域名：\n")
    if len(other) == 0:
        result_file.write("未发现错误域名\n")
        print("[green][INFO] 未发现错误域名")
    else:
        result_file.write("请手动处理如下资产：\n")
        print("[red bold][ERROR] 请手动处理如下资产：")
        for i in other:
            result_file.write(i + "\n")
            print("[red bold][ERROR] " + i)
    if len(is_null) == 0:
        print("[green][INFO] aqc查询资产不为空，查询正常")
    else:
        print("[red bold][ERROR] aqc查询资产为空，可手动确认资产是否为空")
        result_file.write("\n下面这些资产没东西：\n")
        for i in is_null:
            result_file.write(i + "\n")
            print("[red bold][ERROR] " + i)
    check = open("result/check.txt", "a+", encoding='utf-8')
    check.write(time.asctime() + "\n")
    if len(l) == 0:
        check.write("未发现outs目录下的enscan输出文件，请自查\n")
        print("[red bold][ERROR] 未发现outs目录下的enscan输出文件，请自查")
    else:
        if len(is_null) != 0:
            check.write("aqc查询资产为空的资产：\n")
            for i in is_null:
                check.write(i + "\n")
            check.write("\n\n")
        check.write("aqc查询资产分类：\n")
        for i in l:
            check.write(i + "\n")
    check.write("\n\n")
    result_file.write("\n\n")

    print("[green][INFO] 结果都将导出在result里哦，请注意查收！")

def fix_config_yaml(file_path, spaces_per_indent=2):
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 将所有制表符替换为相应数量的空格
        fixed_content = content.replace('\t', ' ' * spaces_per_indent)

        # 将修正后的内容写回原文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(fixed_content)
        print("[green][SUCCESS] YAML 文件中的 Tab 已替换为 " + str(spaces_per_indent) + " 空格。")

    except Exception as e:
        print(f"[red bold][ERROR] 处理文件时出现错误: {e}")

def read_config_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)  # 读取并解析 YAML 内容
            return data
    except FileNotFoundError:
        print(f"[red bold][ERROR] 错误：文件 {file_path} 不存在")
    except yaml.YAMLError as e:
        print(f"[red bold][ERROR] YAML 解析错误: {e}")
        fix_config_yaml(file_path)
    except Exception as e:
        print(f"[red bold][ERROR] 发生错误: {e}")
    return None

def baidu_security_verification(cookie):
    url = 'https://aiqicha.baidu.com/s?q=123'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'Cookie': cookie,
    }
    resp = requests.get(url=url, headers=headers)

    # print(resp.content.decode('utf-8'))
    if "百度安全验证" in resp.content.decode('utf-8'):
        return False
    else:
        return True

def enscan_run(deep):
    run_null = []
    err_file = open("result/err.txt", "a+", encoding='utf-8')
    err_file.write(time.asctime() + "\n")
    err_file.write("查询失败目标资产名单：\n")
    if deep != '':
        deep = '-invest 100 -deep ' + deep
    with open('targets.txt', 'r', encoding='utf-8') as f:
        all_line = len(f.readlines())
        f.seek(0)
        with Progress() as progress:
            task = progress.add_task("[green][INFO] 正在运行enscan...", total=all_line)
            for line in f:
                line = line.replace('\n', '')
                if os.name == "nt":
                    commond = 'enscan.exe -n "' + line + '" -json ' + deep
                elif os.name == "posix":
                    commond = './enscan -n "' + line + '" -json ' + deep
                # print(commond)
                output = subprocess.run(commond, shell=True, capture_output=True, text=True, encoding='utf-8')
                # print(output.stderr)
                if "无法解析页面数据" in output.stdout:
                    print("[red bold][ERROR] 网络错误，已将" + line + "添加到err.txt文件中，请手动打开爱企查检查情况。")
                    err_file.write(line + "\n")
                elif "没有查询到关键词" in output.stdout:
                    print("[yellow][WARN] 没有查询到目标资产：" + line + "，已添加到err.txt文件中")
                    run_null.append(line)
                progress.update(task, advance=1)
                time.sleep(5)
        print("[green][INFO] enscan运行结果已保存至outs文件夹")
        make_check_stop.set()
    err_file.write("\n\n未查询到的资产：\n")
    for i in run_null:
        err_file.write(i + "\n")

def check_baidu_security_verification():
    while True:
        time.sleep(8)
        if baidu_security_verification(read_config_yaml("config.yaml")['cookies']['aiqicha']) == False:
            print("[red bold][ERROR] 触发爱企查防爬机制，无需中断程序，切换成热点网络，开关飞行模式进行ip切换")
        if make_check_stop.is_set():
            break

def check_city(city):
    if city == "":
        return
    else:
        black_list = ['.DS_Store', 'backup']
        check_folder('./outs/backup')
        for file_name in os.listdir("./outs"):
            if file_name not in black_list:
                shutil.copyfile(f"./outs/{file_name}",f"./outs/backup/{file_name}")
                with open(f"./outs/{file_name}", 'r', encoding='utf-8') as f:
                    p = f.read()
                    d = json.loads(p)
                    n = 1
                    if len(d["enterprise_info"]) > 1:
                        for i in range(1, len(d["enterprise_info"])):
                            if city not in d["enterprise_info"][n]["address"]:
                                del d["enterprise_info"][n]
                                with open(f"./outs/{file_name}", 'w+', encoding='utf-8') as f:
                                    json.dump(d, f, ensure_ascii=False)
                            else:
                                n += 1

def check_folder(folder):
    if os.path.isdir(f"{folder}"):
        print(f"[green][INFO] {folder}文件夹已存在，不再继续创建")
    else:
        os.makedirs(f"{folder}")

if __name__ == '__main__':
    banner()
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-m", "--mode", dest='running_mode',
                        help="运行模式：\n例如：python3 main.py -m 1\n"
                             "1、运行enscan。\n"
                             "2、提取资产域名信息。\n"
                             "3、运行hunter(默认提取result/domain.txt)\n")
    parser.add_argument("-sub", "--subsidiary", dest='subsidiary', default='',
                        help="查询子公司\n例如：python3 main.py -m 1 -sub 3 (百分百控股往下摸三级子公司)")
    parser.add_argument("-c", "--city", dest='city', default='',
                        help="限定子公司范围\n例如：python3 main.py -m 1 -sub 3 -c '杭州市' (查询地区为杭州市的资产)")
    parser.add_argument("-max", "--maxnumber", dest='max_number', default=1000,
                        help="限制hunter最大查询数量：默认1000\n例如：python3 main.py -m 3 -max 1000")
    args = parser.parse_args()
    try:
        if args.running_mode == "1":
            if os.path.isfile("enscan") or os.path.isfile("enscan.exe"):
                if args.subsidiary == "" and args.city != "":
                    print("[red bold][ERROR] -sub参数未设置，请检查！--help")
                    exit()
                check_folder("result")
                run1 = threading.Thread(target=enscan_run, args=(args.subsidiary,))
                run2 = threading.Thread(target=check_baidu_security_verification)

                run1.start()
                run2.start()

                run1.join()
                run2.join()
                check_city(args.city)
            else:
                print("[red bold][ERROR] 未发现当前目录下存在enscan可执行文件，请将enscan下载到当前目录，并重命名为enscan")
                print("[red bold][ERROR] 下载链接：https://github.com/wgpsec/ENScan_GO/releases")
        elif args.running_mode == "2":
            check_folder("result")
            enscan_domain()
            check_city(args.city)
        elif args.running_mode == "3":
            if os.path.isfile("api_key.json"):
                with open('api_key.json', 'r', encoding='utf-8') as f:
                    hunter_scan(f.read())
                    try:
                        remove_duplicates()
                    except:
                        print("[red bold][ERROR] 出现错误或url.txt数据为空!!!")
            else:
                with open('api_key.json', 'w', encoding='utf-8') as f:
                    key = input("请输入hunter api key >>>")
                    f.write(f'{key}')
                    print('[green][INFO] hunter api key已保存至api_key.json')
        else:
            print("[red bold][ERROR] 参数有误，请检查！--help")
    except KeyboardInterrupt:
        print(f"[yellow][WARN] 再次Ctrl+C退出程序.")
