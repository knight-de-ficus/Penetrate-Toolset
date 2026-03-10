def PrintLogo():
	print(r'''
.__                .__                   __                .__   
|__|_____   ______ |__| ____    ____   _/  |_  ____   ____ |  |  
|  \____ \  \____ \|  |/    \  / ___\  \   __\/  _ \ /  _ \|  |  
|  |  |_> > |  |_> >  |   |  \/ /_/  >  |  | (  <_> |  <_> )  |__
|__|   __/  |   __/|__|___|  /\___  /   |__|  \____/ \____/|____/
   |__|     |__|           \//_____/    by KnightFang    v0.1    
''')

#example
URL		= "http://www.baidu.com"
HOST	= "111.63.65.247" #baidu.com
PORT	= 80

#file
INPUT	= "./in.csv"
OUTPUT	= "./out.csv"
HEADER	= "./header.json"

import urllib.request
import subprocess
import re
import json
import csv

def UrlExtract(url):
	match = re.search(r'(\d{1,3}(?:\.\d{1,3}){3})', url)
	if match:
		return match.group(1)
	else:
		return None

def WindowsPing(HOST):
	cmd = ["ping","-n","1",HOST]
	out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='gbk', errors='ignore').stdout
	if out is None:
		return False
	else:
		return True

def LoadCsv(Path):
    data = []
    fieldnames = []

    try:
        with open(Path, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames) if reader.fieldnames else []

            for col in ['ip', 'url', 'port']:
                if col not in fieldnames:
                    fieldnames.append(col)

            for row in reader:
                for col in fieldnames:
                    if col not in row:
                        row[col] = ""

                url_value = row.get('url')
                if url_value:
                    ip, port = UrlExract(url_value)
                    row['ip'] = ip
                    row['port'] = port
                
                data.append(row)

    except FileNotFoundError:
        print(f"Error: Cannot Open File {Path}")
        return []
    except Exception as e:
        print(f"Error: Handling {e}")
        return []

    return data
		

def main():
	#LoadCsv(INPUT)	

		
if __name__ == "__main__":
	PrintLogo()
	main()