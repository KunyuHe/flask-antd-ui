# Flask web服务器

## 建库

```sql
drop TABLE if EXISTS tb_income;
CREATE TABLE tb_income(
	id serial PRIMARY key,
	value float,
	customer_id INTEGER,
	date DATE
);

drop TABLE if EXISTS tb_customer;
CREATE TABLE tb_customer(
	id serial PRIMARY key,
	name VARCHAR(255),
	email VARCHAR(255)
);




drop TABLE if EXISTS tb_user;
CREATE TABLE tb_user (
id serial PRIMARY key,
username VARCHAR(20),
password VARCHAR(255),
phone VARCHAR(255),
email VARCHAR(255),
address VARCHAR(255)
);


drop TABLE if EXISTS tb_trade;
CREATE TABLE tb_trade (
id serial PRIMARY key,
customer_id INTEGER,
feedback INTEGER DEFAULT 0
);

--SELECT * FROM tb_customer

drop TABLE if EXISTS user_customer;
CREATE TABLE user_customer (
customer_id INTEGER,
user_id INTEGER
);


SELECT * from tb_trade ORDER BY id desc 

```