import re,requests,os,argparse
parser = argparse.ArgumentParser(description="抖音图片下载器")
parser.add_argument('--url',type=str,help='视频链接')
parser.add_argument('--file_path',type=str,help='保存图片的路径')
parser.add_argument('--cookie',type=str,help='设置cookie,若cookie错误请自行删除当前目录下的cookie.txt文件')
args = parser.parse_args()
if not args.url:
    args.url = input('请输入url:')
if args.url == '':
    print('url不能为空')
    exit()
if not args.file_path:
    args.file_path = input('请输入保存路径 (默认为当前目录下images文件夹): ') or './images'
if args.cookie:
    with open("./cookie.txt",'w') as f:
        f.write(args.cookie)    
if not os.path.isfile("./cookie.txt"):
    print('请先设置cookie')
    if not args.cookie:
        args.cookie = input('请输入cookie:')
        with open("./cookie.txt","w") as f:
            f.write(args.cookie)
url = args.url
path = args.file_path
headers = {
    "Cookie":f"{open("./cookie.txt","r").read()}",
    'Referer':url,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'    
}
response = requests.get(url, headers=headers)
r = response.text
a_list = re.findall(r'"https://p3-pc-sign.douyinpic.com(.*?)"', r)
all_url = []
for a in a_list:
    if a[-1] == '\\':
        a = a[:-1]
        a = str('https://p3-pc-sign.douyinpic.com' + a).replace(r'\u0026', '&')
        all_url.append(a)
seen = {}
for urls in all_url:
    parts = urls.split('ce/')
    if len(parts) > 1:
        key = parts[-1][:10]
        if key in seen:
            if len(urls) < len(seen[key]):
                seen[key] = urls
        else:
            seen[key] = urls
    else:
        seen[urls] = urls
deduplicated_list = list(seen.values())
for i in deduplicated_list:
    print(i)
    response = requests.get(i)
    type(i)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f'{path}/'+str(re.findall(r'ce/(.*?)~',i)).replace("['",'').replace("']",'')+'.jpg', 'wb') as f:
        f.write(response.content)
    try:
        os.remove(f".{path}/[].jpg")
    except:
        pass
print('Done！')