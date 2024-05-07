import argparse
from time import sleep
import time
import subprocess
import re
import os

def enscan_domain():
    domain_list = []
    icp_list = []
    l = []
    for file_name in os.listdir("./" + args.running_dir):
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
                    t = re.compile('"icp":"(.*?)",')
                    r = t.findall(p)
                    for i in r:
                        if ("    " + i) in l:
                            continue
                        else:
                            icp_list.append(i)
                            l.append("    " + i)

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

    os.makedirs(args.output_dir)
    result_file = open(args.output_dir + "/result.txt", "a+")
    ip_file = open(args.output_dir + "/ip.txt", "a+")
    domain_file = open(args.output_dir + "/domain.txt", "a+")
    icp_file = open(args.output_dir + "/icp.txt", "a+")
    result_file.write(time.asctime() + "\n")
    print(time.asctime())
    result_file.write("找到的ip资产如下：\n")
    print("找到的ip资产如下：")
    if len(ip) == 0:
        result_file.write("嘤嘤嘤，没找到ip捏(*꒦ິ⌓꒦ີ)\n")
        print("嘤嘤嘤，没找到ip捏(*꒦ິ⌓꒦ີ)")
    else:
        for i in ip:
            result_file.write(i + "\n")
            ip_file.write(i + "\n")
            print(i)
    result_file.write("\n")
    result_file.write("找到的domain资产如下：\n")
    print("找到的domain资产如下：")
    if len(domain) == 0:
        result_file.write("嘤嘤嘤，没找到domain捏(*꒦ິ⌓꒦ີ)\n")
        print("嘤嘤嘤，没找到domain捏(*꒦ິ⌓꒦ີ)")
    else:
        for i in domain:
            result_file.write(i + "\n")
            domain_file.write(i + "\n")
            print(i)
    result_file.write("\n")
    result_file.write("找到的icp资产如下：\n")
    print("找到的icp资产如下：")
    if len(icp_list) == 0:
        result_file.write("嘤嘤嘤，没找到icp捏(*꒦ິ⌓꒦ີ)\n")
        print("嘤嘤嘤，没找到domain捏(*꒦ິ⌓꒦ີ)")
    else:
        for i in icp_list:
            result_file.write(i + "\n")
            icp_file.write(i + "\n")
            print(i)
    result_file.write("\n")
    result_file.write("找到正则匹配外的资产：\n")
    print("找到正则匹配外的资产：")
    if len(other) == 0:
        result_file.write("桀桀桀桀，确认没有正则匹配外的资产，程序无误，nice！\n")
        print("桀桀桀桀，确认没有正则匹配外的资产，程序无误，nice！")
    else:
        result_file.write("omg，出现了一些问题，请手动处理如下资产：\n")
        print("omg，出现了一些问题，请手动处理如下资产：")
        for i in ip:
            result_file.write(i + "\n")
            print(i)
    check = open(args.output_dir + "/check.txt", "a+")
    check.write(time.asctime() + "\n")
    check.write("资产分类：\n")
    if len(l) == 0:
        check.write("检查一下你他喵的是不是没放资产！\n")
        print("检查一下你他喵的是不是没放资产！")
    else:
        for i in l:
            check.write(i + "\n")
    check.write("\n\n")
    result_file.write("\n\n")

    print("结果都将导出在" + args.output_dir + "里哦，请注意查收！")


def enscan_run():
    with open('targets.txt', 'r', encoding='utf-8') as f:
        for line in f:
            print(line, end="")
            line = line.replace('\n', '')
            output = subprocess.call([
                './enscan',
                '-n', line,
                '-o', args.running_dir,
                '-json'
            ])
            sleep(5)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-m", "--mode", dest='running_mode', help="运行模式：\n例如：python3 main.py -m 1\n1、运行完enscan然后提取出资产域名信息。\n2、只运行enscan。\n3、只提取资产域名信息。")
    parser.add_argument("-d", "--dir", dest='running_dir', help="指定enscan输出目录\n例如：python3 main.py -d outs(不加-d参数默认提取outs目录下的导出结果)")
    parser.add_argument("-o", "--output", dest='output_dir', help="保存结果到xxx文件夹\n例如：python3 main.py -o result(不加-o参数默认保存在result文件夹下)")
    args = parser.parse_args()
    if args.running_dir == None:
        args.running_dir = "outs"
    if args.output_dir == None:
        args.output_dir = "result"
    if args.running_mode == "1":
        enscan_run()
        enscan_domain()
    elif args.running_mode == "2":
        enscan_run()
    elif args.running_mode == "3":
        enscan_domain()
