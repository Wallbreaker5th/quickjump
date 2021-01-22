import os
import webbrowser
import requests
import json
import prettytable
import re
import urllib
from bs4 import BeautifulSoup


user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)" +
              "AppleWebKit/537.36 (KHTML, like Gecko)" +
              "Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66")

difficulties = ["暂无评定", "入门", "普及-", "普及/提高-",
                "普及+/提高", "提高+/省选-", "省选/NOI-", "NOI/NOI+/CTSC"]


def get_info(text: str) -> dict:
    """Get information from HTML"""
    search_result = re.search(
        "decodeURIComponent\\(\"(.*)\"\\)\\);window\\._feConfigVersion", text)
    search_result = search_result.group(1)
    decoded_result = urllib.parse.unquote(search_result)
    result = json.loads(decoded_result)
    return result


def get_problem_info(pid: tuple) -> dict:
    """Get information about a problem."""
    url = "https://codeforces.com/problemset/problem/%s/%s" % (pid[0], pid[1])
    r = requests.get(url)
    html = r.content.decode('utf-8')
    bs = BeautifulSoup(html, features="html.parser")
    info = {}
    info["题目名称"] = bs.find(class_="title").string
    time_limit: str = bs.find(class_="time-limit").get_text()
    info["时间限制"] = time_limit.replace("time limit per test", "")
    memory_limit: str = bs.find(class_="memory-limit").get_text()
    info["空间限制"] = memory_limit.replace("memory limit per test", "")
    bs_tags = bs.find_all(class_="tag-box")
    tags = [i.string.strip("\n\r\t ") for i in bs_tags if not i.string.strip(
        "\n\r\t ").startswith('*')]
    info["标签　　"] = ", ".join(tags)
    info["难度　　"] = bs.find(title="Difficulty").string.strip("\n\r\t* ")
    info["来源　　"] = bs.th.string.strip("\n\r\t* ")
    return info


def get_search_info(key: str) -> (list, list):
    """Search `key` and get information from the results"""
    url = "https://www.luogu.com.cn/problem/list?type=CF&keyword=%s&page=1" % key
    r = requests.get(url, headers={"User-Agent": user_agent})
    f = get_info(r.text)["currentData"]
    field_names = ["题目编号", "题目名称", "通过情况", "难度"]
    table = [[i["pid"], i["title"],
              "%d/%d" % (i["totalAccepted"], i["totalSubmit"]),
              difficulties[i["difficulty"]]]
             for i in f["problems"]["result"]]
    return (field_names, table)


def handle(opt: list):
    """Handle the arguments passed in."""
    if "-p" in opt:
        p: str = opt["-p"]
        if p[-1].isalpha:
            opt["-p"] = (p[:-1], p[-1].upper())
        else:
            print("题目编号格式错误")
            exit(1)
        if not p[0].isdigit():
            print("题目编号格式错误")
            exit(1)
    if opt["-b"]:
        if "-p" in opt:
            p: tuple = opt["-p"]
            webbrowser.open(
                "https://codeforces.com/problemset/problem/%s/%s" % (p[0], p[1]))
            exit(0)
        if "-s" in opt:
            print("Codeforces 不支持搜索题目，此处使用洛谷搜索。")
            key: str = opt["-s"]
            webbrowser.open(
                "https://www.luogu.com.cn/problem/list?type=CF&keyword=%s&page=1" % key)
            exit(0)
    else:
        if "-p" in opt:
            p: str = opt["-p"]
            info = get_problem_info(p)
            for i in info:
                print(i, ":\t", info[i])
            print("使用 -b 参数在浏览器打开以获取题目详细信息。")
            exit(0)
        if "-s" in opt:
            print("Codeforces 不支持搜索题目，此处使用洛谷搜索。")
            field_names, content = get_search_info(opt["-s"])
            height = os.get_terminal_size().lines-5
            print("h", height)
            if len(content) > height:
                content = content[:height]
            tb = prettytable.PrettyTable()
            tb.field_names = field_names
            tb.add_rows(content)
            tb.align = "l"
            print(tb)
            exit(0)
