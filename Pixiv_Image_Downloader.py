import requests,os,urllib3,argparse
parser = argparse.ArgumentParser(description="Pixiv图片下载器")
parser.add_argument('--id',type=str,help='画师id')
parser.add_argument('--file_path',type=str,help='保存图片的路径')
parser.add_argument('--cookie',type=str,help='设置cookie,若cookie错误请自行删除当前目录下的cookie.txt文件')
args = parser.parse_args()
if not args.id:
    args.id = input('请输入画师id:')
if args.id == '':
    print('画师id不能为空')
    exit()
if not args.file_path:
    args.file_path = input('请输入保存路径 (默认为 H:/): ') or 'H:/'
if args.cookie:
    with open("./cookie.txt",'w') as f:
        f.write(args.cookie)    
if not os.path.isfile("./cookie.txt"):
    print('请先设置cookie')
    if not args.cookie:
        args.cookie = input('请输入cookie:')
        with open("./cookie.txt","w") as f:
            f.write(args.cookie)
id = args.id
path = args.file_path
get_url = 'https://www.pixiv.net/ajax/user/'+id+'/profile/all'
print(get_url)
print('！！！欢迎使用！！！')
headers = {
    'cookie':f"{open("./cookie.txt","r").read()}",
    'Referer': 'https://i.pximg.net/',
    'Referer': 'https://www.pixiv.net/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
}
urllib3.disable_warnings()
ids_json = requests.get(url=get_url,headers= headers,verify=False).json()
ids = ids_json["body"]["illusts"]
dirname = "猫猫"
if not os.path.exists(path + dirname):
    os.mkdir(path + dirname)
if not os.path.exists(path + '猫猫'+ '/' +  '画师' + id ):
    os.mkdir(path + '猫猫'+ '/' +  '画师' + id )
if not os.path.exists(path + '猫猫' + '/' + id + '.txt'):
    with open(path + '猫猫' + '/' + id + '.txt','w',encoding='utf-8') as f:
        f.write('')
ids = str(ids)
ids = ids.replace(': None','')
ids = ids.replace('{','[')
ids = ids.replace('}',']')
print(ids)
no = open(path + '猫猫' + '/' + id + '.txt','r',encoding='utf-8').read()
ids = ids.replace(no,'')    
ids = eval(ids)
print(ids)
for real_id in ids:
    urls = 'https://www.pixiv.net/ajax/illust/'+ real_id +'/pages?'
    responses = requests.get(url=urls,headers=headers,verify=False).json()
    print(real_id)
    for realurls in responses['body']:
        real_urls = realurls['urls']['original']
        real_urls = str(real_urls)
        filenames = real_urls.split('/')[-1]
        print(real_urls)
        responses2 = requests.Session().get(url=real_urls,headers=headers,verify=False).content
        print('编号为'+filenames+'的图片下载完成')
        with open(path + '猫猫' + '/' + '画师' + id + '/' + filenames,'wb') as fp:
            fp.write(responses2)
        real_id = str(real_id)
    with open(path + '猫猫' + '/' + id + '.txt','a',encoding='utf-8') as f:
        f.write("'"+real_id+"', ")          
print('画师id:'+id)