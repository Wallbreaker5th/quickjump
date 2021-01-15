import os
import webbrowser
import requests
import json
import prettytable
import re
from bs4 import BeautifulSoup


class Uoj:
    """Support all OJs that are based on UOJ (I hope so)"""
    domain = ""

    def __init__(self, domain: str = "uoj.ac"):
        self.domain = domain

    def get_problem_info(self, pid: str) -> dict:
        """Get information about a problem."""
        url = "https://%s/problem/%s" % (self.domain, pid)
        r = requests.get(url)
        html = r.content.decode('utf-8')
        bs = BeautifulSoup(html, features="html.parser")
        info = {}
        info["题目名称"] = bs.find(class_="page-header").string
        re_time_limit = re.search(
            "<p>(?:<strong>)?时间限制：?(?:</strong>)?：?"
            + "\\$(\\d*) *\\\\texttt\\{(\\w*)\\}\\$",
            html)
        re_memory_limit = re.search(
            "<p>(?:<strong>)?(?:空间|内存)限制：?(?:</strong>)?：?"
            + "\\$(\\d*) *\\\\texttt\\{(\\w*)\\}\\$",
            html)
        if re_time_limit:
            info["时间限制"] = "%s %s" % (
                re_time_limit.group(1), re_time_limit.group(2))
        if re_memory_limit:
            info["空间限制"] = "%s %s" % (
                re_memory_limit.group(1), re_memory_limit.group(2))
        return info
    def get_search_info(self, key: str) -> dict:
        """Search `key` and get information from the results"""
        url = "https://%s/problems?search=%s" % (self.domain, key)
        r = requests.get(url)
        html = r.content.decode('utf-8')
        field_names = ["题目编号", "题目名称"]
        re_result=re.findall("<a href=\"/problem/(\\d+)\">(.+?)</a>",html)
        table=[[i[0],i[1]] for i in re_result]
        return (field_names,table)

    def handle(self, opt: list):
        """Handle the arguments passed in."""
        if opt['-b']:
            if '-p' in opt:
                p: str = opt['-p']
                webbrowser.open('https://uoj.ac/problem/'+p)
                exit(0)
            if '-s' in opt:
                key: str = opt['-s']
                webbrowser.open('https://uoj.ac/problems?search=%s' % key)
                exit(0)
        else:
            if "-p" in opt:
                p: str = opt["-p"]
                info = self.get_problem_info(p)
                for i in info:
                    print(i, ":\t", info[i])
                print("使用 -b 参数在浏览器打开以获取题目详细信息。")
                exit(0)
            if "-s" in opt:
                field_names, content = self.get_search_info(opt["-s"])
                height = os.get_terminal_size().lines-5
                if len(content) > height:
                    content = content[:height]
                tb = prettytable.PrettyTable()
                tb.field_names = field_names
                tb.add_rows(content)
                tb.align = "l"
                print(tb)
                exit(0)
