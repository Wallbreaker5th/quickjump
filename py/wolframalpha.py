import sys
import urllib.parse
import webbrowser
s=urllib.parse.quote(sys.argv[1])
webbrowser.open('https://www.wolframalpha.com/input/?i='+s)
