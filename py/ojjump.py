import sys
import getopt
import luogu
import uoj
import loj


def show_help():
    """Show the help"""
    print("""oj name_of_the_OJ [-s keyword] [-p problem_id] [-b]
详细用法参见 README.md
""")


opts = {}
try:
    opt, arg = getopt.getopt(sys.argv[2:], "hbp:s:", [
        "help", "in_browser", "problem_id=", "search="])

    print(opt, arg)
    opts["-b"] = False
    oj = sys.argv[1]
    if oj == "-h" or oj == "--help":
        show_help()
        exit(0)
    for i in opt:
        if i[0] == "-b" or i[0] == "--browser":
            opts["-b"] = True
        if i[0] == "-p" or i[0] == "--problem_id":
            opts["-p"] = i[1]
        if i[0] == "-s" or i[0] == "--search":
            opts["-s"] = i[1]
except SystemExit:
    exit(0)
except:
    show_help()
    exit(0)

online_judges = {
    "luogu": luogu, 
    "lg": luogu, 
    "loj": loj, 
    "l": loj, 
    "uoj": uoj.Uoj("uoj.ac"),
    "u": uoj.Uoj("uoj.ac"),
    "bzoj": uoj.Uoj("darkbzoj.tk"),
    "darkbzoj": uoj.Uoj("darkbzoj.tk"),
    "bz": uoj.Uoj("darkbzoj.tk"),
    "db": uoj.Uoj("darkbzoj.tk"),
}
if not oj in online_judges:
    raise Exception("OJ not supported")
online_judges[oj].handle(opts)
