# -*- coding: utf-8 -*-

def PrintLogo():
    print(r'''
.__                .__                   __                .__   
|__|_____   ______ |__| ____    ____   _/  |_  ____   ____ |  |  
|  \____ \  \____ \|  |/    \  / ___\  \   __\/  _ \ /  _ \|  |  
|  |  |_> > |  |_> >  |   |  \/ /_/  >  |  | (  <_> |  <_> )  |__
|__|   __/  |   __/|__|___|  /\___  /   |__|  \____/ \____/|____/
   |__|     |__|           \//_____/    by KnightFang    v0.1    
''')
    
import csv
import json
import locale
import re
import subprocess
import urllib.request

#example
URL		= "http://www.baidu.com"
HOST	= "111.63.65.247" #baidu.com
PORT	= 80

# file
INPUT = "./in.csv"
OUTPUT = "./out.csv"
HEADER = "./header.json"

# 建议：Windows 下 CSV 常见为 utf-8 / utf-8-sig / gbk
ENCODING = "utf-8"


def ExtractIpPortFromUrl(url: str):
    """从 URL/文本中提取 IP 地址和端口号。

    入参：url（URL 字符串或包含 IP 的任意文本）
    返回：(ip, port)；若未找到则返回 (None, None)
    """

    if not url:
        return None, None

    ip_match = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", url)
    if not ip_match:
        return None, None

    ip = ip_match.group(1)

    # 尝试在 IP 后面找 :port
    port_match = re.search(rf"{re.escape(ip)}:(\d{{1,5}})", url)
    port = port_match.group(1) if port_match else None

    return ip, port

def ExtractIpFromUrl(url):
    '''
    从 URL 中提取 IP 地址。
    入参：URL 字符串
    返回：IP 地址；若未找到则返回 None
    '''
    ip, _port = ExtractIpPortFromUrl(url)
    return ip

def WindowsPing(HOST):
    '''
    使用 Windows 系统 ping 测试目标是否可达。
    入参：目标 IP/域名
    返回：可执行且有输出则 True，否则 False
    '''
    cmd = ["ping", "-n", "1", HOST]
    preferred = locale.getpreferredencoding(False) or "utf-8"
    out = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding=preferred,
        errors="ignore",
    ).stdout
    return bool(out)

def LoadCsv(Path, Encoding='utf-8'):
    '''
    读取 CSV 文件。
    入参：csv 文件路径
    返回：每行一个 dict（key 为表头，value 为对应值）。
    '''
    data = []
    fieldnames = []

    try:
        try_encodings = [Encoding]
        if Encoding.lower() not in {"utf-8-sig", "utf-8", "gbk"}:
            try_encodings += ["utf-8-sig", "utf-8", "gbk"]
        else:
            # 常见顺序：优先 utf-8-sig（兼容 BOM），再 utf-8，再 gbk
            try_encodings = ["utf-8-sig", "utf-8", "gbk"]

        last_error = None
        for enc in try_encodings:
            try:
                with open(Path, mode="r", encoding=enc, newline="") as f:
                    reader = csv.DictReader(f)
                    print("[info]dict:", reader.fieldnames)

                    fieldnames = list(reader.fieldnames) if reader.fieldnames else []

                    for col in ["ip", "url", "port"]:
                        if col not in fieldnames:
                            fieldnames.append(col)

                    for row in reader:
                        for col in fieldnames:
                            if col not in row:
                                row[col] = ""

                        url_value = row.get("url")
                        if url_value:
                            ip, port = ExtractIpPortFromUrl(url_value)
                            row["ip"] = ip or ""
                            row["port"] = port or ""

                        data.append(row)

                last_error = None
                break
            except UnicodeDecodeError as e:
                last_error = e
                data = []
                continue

        if last_error is not None:
            raise last_error

    except FileNotFoundError:
        print(f"Error: Cannot Open File {Path}")
        return []
    except Exception as e:
        print(f"Error: Handling {e}")
        return []

    return data
		

def main():
    LoadCsv(INPUT, ENCODING)
    print(ExtractIpFromUrl(URL))
    print(WindowsPing(HOST))

		
if __name__ == "__main__":
    PrintLogo()
    main()