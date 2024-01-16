Ubuntu Setup:
=============
#!/bin/bash
apt update
apt install git -y
git clone https://github.com/norman0402/aws-live.git
cd aws-live
pip3 install flask
pip3 install pymysql
pip3 install boto3
python3 EmpApp.py

config.py:
==========
customhost = "<rds_db_instance>.ap-south-1.rds.amazonaws.com"
customuser = "admin"
custompass = "password"
customdb = "<db_name>"
custombucket = "<s3 bucket>"
customregion = "ap-south-1"

Setting up mysql table in EC2:
===============================
mysql -h <rds_db_instance>.ap-south-1.rds.amazonaws.com -u admin -p
mysql> create database <db_name>;
Query OK, 1 row affected (0.01 sec)

mysql> use <db_name>;
Database changed


mysql> create table employees(emp_id int(20) auto_increment, name varchar(20), age int(20), location varchar(20), technology varchar(20), PRIMARY KEY (emp_id));
Query OK, 0 rows affected, 2 warnings (0.03 sec)

mysql> alter table employees AUTO_INCREMENT=2024001;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> 
mysql> 
mysql> select * from employees;
Empty set (0.00 sec)

mysql> describe employees;
+------------+-------------+------+-----+---------+----------------+
| Field      | Type        | Null | Key | Default | Extra          |
+------------+-------------+------+-----+---------+----------------+
| emp_id     | int         | NO   | PRI | NULL    | auto_increment |
| name       | varchar(20) | YES  |     | NULL    |                |
| age        | int         | YES  |     | NULL    |                |
| location   | varchar(20) | YES  |     | NULL    |                |
| technology | varchar(20) | YES  |     | NULL    |                |
+------------+-------------+------+-----+---------+----------------+
5 rows in set (0.01 sec)







