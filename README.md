# Lord of SQL Injection Write Up

Write Ups for [Lord of SQL Injection](http://los.eagle-jump.org/)

Visual Studio Code를 이용하여 작성

iTerm2 + Git Command Line Tools와 Visual Studio Code 소스 제어 창을 함께 이용하여 버전 관리

[**1번 문제 - Gremlin**](https://gitlab.com/dsm-highschool/sql-injection-writeup/blob/master/12_%EC%9D%B4%EC%9E%AC%EC%84%9D/los_no1_gremlin.md) / [**2번 문제 - Cobolt**](https://gitlab.com/dsm-highschool/sql-injection-writeup/blob/master/12_%EC%9D%B4%EC%9E%AC%EC%84%9D/los_no2_cobolt.md) / [**3번 문제 - Goblin**](https://gitlab.com/dsm-highschool/sql-injection-writeup/blob/master/12_%EC%9D%B4%EC%9E%AC%EC%84%9D/los_no3_goblin.md) / [**4번 문제 - Orc**](https://gitlab.com/dsm-highschool/sql-injection-writeup/blob/master/12_%EC%9D%B4%EC%9E%AC%EC%84%9D/los_no4_orc.md) / [**5번 문제 - Wolfman**](https://gitlab.com/dsm-highschool/sql-injection-writeup/blob/master/12_%EC%9D%B4%EC%9E%AC%EC%84%9D/los_no5_wolfman.md)

[**6번 문제 - Darkelf**](https://gitlab.com/dsm-highschool/sql-injection-writeup/blob/master/12_%EC%9D%B4%EC%9E%AC%EC%84%9D/los_no6_darkelf.md) / [**7번 문제 - Orge**](https://gitlab.com/dsm-highschool/sql-injection-writeup/blob/master/12_%EC%9D%B4%EC%9E%AC%EC%84%9D/los_no7_orge.md) / [**8번 문제 - Troll**](https://gitlab.com/dsm-highschool/sql-injection-writeup/blob/master/12_%EC%9D%B4%EC%9E%AC%EC%84%9D/los_no8_troll.md)

# Lord of SQL Injection

## 소개

* Lord of SQL Injection은 2015년 제작된 SQL Injection Wargame 사이트이다.
* 총 25문제로 구성되어 있으나 2017년 9월 4일 기준 23번 hell_fire 문제와 24번 evil_wizard 문제가 broken 되어 그냥 넘겨진다
* SQL Injection의 기초적인 원리부터 Blind SQL Injection의 방법까지 다양한 지식을 필요로 하며 접할 수 있다.

## 특징

* Lord of SQL Injection의 모든 문제는 php 소스 코드를 공개해 준다.

    ![code](images/code.png)

* 또, 25번 Umaru 문제를 제외한 모든 문제는 다음과 같이 query를 공개해 준다.

    ![query](images/query.png)

* 이를 이용하여 각 문제의 solve("[문제 이름]") 함수를 실행시키면 문제가 풀린다.