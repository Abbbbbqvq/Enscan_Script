#coding=utf-8
import os
import re
import time

domain_list = []
current_dir = os.getcwd()
for file_name in os.listdir(current_dir):
  if os.path.isfile(os.path.join(current_dir, file_name)):
    if ".json" in file_name:
      with open(file_name, 'r', encoding='utf-8') as f:
        t = re.compile('"domain":"(.*?)",')
        p = f.read()
        r = t.findall(p)
        for i in r:
          domain_list.append(i)

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

result = open("result.txt","a+")
result.write(time.asctime() + "\n")
print(time.asctime())
result.write("找到的ip资产如下：\n")
print("找到的ip资产如下：")
if len(ip) == 0:
  result.write("嘤嘤嘤，没找到ip捏(*꒦ິ⌓꒦ີ)\n")
  print("嘤嘤嘤，没找到ip捏(*꒦ິ⌓꒦ີ)")
else:
  for i in ip:
    result.write(i + "\n")
    print(i)
result.write("\n")
result.write("找到的domain资产如下：\n")
print("找到的domain资产如下：")
if len(domain) == 0:
  result.write("嘤嘤嘤，没找到domain捏(*꒦ິ⌓꒦ີ)\n")
  print("嘤嘤嘤，没找到domain捏(*꒦ິ⌓꒦ີ)")
else:
  for i in domain:
    result.write(i + "\n")
    print(i)
result.write("\n")
result.write("找到正则匹配外的资产：\n")
print("找到正则匹配外的资产：")
if len(other) == 0:
  result.write("桀桀桀桀，确认没有正则匹配外的资产，程序无误，nice！\n")
  print("桀桀桀桀，确认没有正则匹配外的资产，程序无误，nice！")
else:
  result.write("omg，出现了一些问题，请手动处理如下资产：\n")
  print("omg，出现了一些问题，请手动处理如下资产：")
  for i in ip:
    result.write(i + "\n")
    print(i)
result.write("\n\n")
print("运行结果在当前目录下的result.txt文件里了喔，请注意查收！")