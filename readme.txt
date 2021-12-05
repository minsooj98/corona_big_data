프로젝트 실행 전 사전 작업!

MariaDB 이용



1. 데이터 베이스 생성!

데이터 베이스는 fproject 이용

MariaDB [(none)]> create database fproject;
MariaDB [(none)]> use fproject;





2. 테이블 생성 !
회원 테이블과 그래프 테이블 생성!

1) 회원 테이블
create table members(userid varchar(20) primary key,
		passwd varchar(20), username varchar(20),
		birth varchar(20) NULL, gender varchar(10) NULL);


2) 그래프 테이블
create table graph(	image varchar(50) primary key,
		userid VARCHAR(20) NOT NULL);