import os
import webbrowser
import requests
import json
import prettytable

user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)" +
              "AppleWebKit/537.36 (KHTML, like Gecko)" +
              "Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66")


def get_problem_info(pid: str) -> dict:
    """Get information about a problem."""
    url = "https://api.loj.ac.cn/api/problem/getProblem"
    payload = {
        "displayId": int(pid),
        "localizedContentsOfLocale": "zh_CN",
        "tagsOfLocale": "zh_CN",
        "samples": False,
        "judgeInfo": True,
        "judgeInfoToBePreprocessed": False,
        "statistics": True,
        "discussionCount": True,
        "permissionOfCurrentUser": True,
        "lastSubmissionAndLastAcceptedSubmission": True
    }
    r = requests.post(url, json=payload)
    f = json.loads(r.text)
    tags = [i["name"] for i in f["tagsOfLocale"]]
    tag_ids = [i["id"] for i in f["tagsOfLocale"]]
    info = {}
    info["题目名称"] = f["localizedContentsOfLocale"]["title"]
    if 73 not in tag_ids:
        info["时间限制"] = f["judgeInfo"]["timeLimit"]
        info["空间限制"] = f["judgeInfo"]["memoryLimit"]
    info["通过情况"] = "%d/%d" % (f["meta"]["acceptedSubmissionCount"],
                              f["meta"]["submissionCount"])
    info["标签　　"] = ', '.join(tags)
    return info


def get_search_info(key: str) -> (list, list):
    """Search `key` and get information from the results"""
    url = "https://api.loj.ac.cn/api/problem/queryProblemSet"
    payload = {
        "keyword": key,
        "locale": "zh_CN",
        "skipCount": 0,
        "takeCount": 50
    }
    r = requests.post(url=url, json=payload)
    f = json.loads(r.text)
    field_names = ["题目编号", "题目名称", "通过情况"]
    table = [[i["meta"]["displayId"], i["title"],
              "%d/%d" % (i["meta"]["acceptedSubmissionCount"],
                         i["meta"]["submissionCount"])]
             for i in f["result"]]
    return (field_names, table)


def handle(opt: list):
    """Handle the arguments passed in."""
    if opt["-b"]:
        if "-p" in opt:
            p: str = opt["-p"]
            webbrowser.open("https://loj.ac/p/"+p)
            exit(0)
        if "-s" in opt:
            key: str = opt["-s"]
            webbrowser.open("https://loj.ac/p?keyword=%s" % key)
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
            if len(content) > height:
                content = content[:height]
            tb = prettytable.PrettyTable()
            tb.field_names = field_names
            tb.add_rows(content)
            tb.align = "l"
            print(tb)
            exit(0)
