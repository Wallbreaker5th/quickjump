import os
import webbrowser
import json
import requests
import urllib
import re
import prettytable

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


def get_problem_info(pid: str) -> dict:
    """Get information about a problem."""
    url = "https://www.luogu.com.cn/problem/"+pid
    r = requests.get(url, headers={"User-Agent": user_agent})
    f = get_info(r.text)["currentData"]["problem"]
    info = {}
    info["题目名称"] = f["title"]
    info["难度　　"] = difficulties[f["difficulty"]]
    info["时间限制"] = "%d ms ~ %d ms" % (
        min(f["limits"]["time"]),
        max(f["limits"]["time"]))
    info["内存限制"] = "%d KB ~ %d KB" % (
        min(f["limits"]["time"]),
        max(f["limits"]["time"]))
    info["通过情况"] = "%d/%d" % (
        f["totalAccepted"],
        f["totalSubmit"])

    if 104 in f["tags"]:
        info["题目类型"] = "提交答案"
    if 103 in f["tags"]:
        info["题目类型"] = "交互题"
    return info


def get_search_info(key: str) -> (list, list):
    """Search `key` and get information from the results"""
    url = "https://www.luogu.com.cn/problem/list?keyword=%s&page=1" % key
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
        if p[0].isdigit():
            p = "P"+p
        p = p.upper()
        opt["-p"] = p
    if opt["-b"]:
        if "-p" in opt:
            p: str = opt["-p"]
            webbrowser.open("https://www.luogu.com.cn/problem/"+p)
            exit(0)
        if "-s" in opt:
            key: str = opt["-s"]
            webbrowser.open(
                "https://www.luogu.com.cn/problem/list?keyword=%s&page=1" % key)
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
