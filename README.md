Ubuntu Setup:
=============
#!/bin/bash </br>
apt update </br>
apt install git -y </br>
git clone https://github.com/norman0402/aws-live.git </br>
cd aws-live </br>
pip3 install flask </br>
pip3 install pymysql </br>
pip3 install boto3 </br>
python3 EmpApp.py </br>

Setting up mysql table in EC2:
===============================
>> mysql -h <rds_db_instance>.ap-south-1.rds.amazonaws.com -u admin -p </br>
mysql> create database <db_name>; </br>
Query OK, 1 row affected (0.01 sec) </br>
</br>
mysql> use <db_name>; </br>
Database changed </br>
</br>

mysql> create table employees(emp_id int(20) auto_increment, name varchar(20), age int(20), location varchar(20), technology varchar(20), PRIMARY KEY (emp_id)); </br>
Query OK, 0 rows affected, 2 warnings (0.03 sec) </br>
</br>
mysql> alter table employees AUTO_INCREMENT=2024001; </br>
Query OK, 0 rows affected (0.01 sec) </br>
Records: 0  Duplicates: 0  Warnings: 0 </br>
</br>
mysql> </br> 
mysql> </br>
mysql> select * from employees; </br>
Empty set (0.00 sec) </br>
</br>
mysql> describe employees; </br>
+------------+-------------+------+-----+---------+----------------+ </br>
| Field      | Type        | Null | Key | Default | Extra          | </br>
+------------+-------------+------+-----+---------+----------------+ </br>
| emp_id     | int         | NO   | PRI | NULL    | auto_increment | </br>
| name       | varchar(20) | YES  |     | NULL    |                | </br>
| age        | int         | YES  |     | NULL    |                | </br>
| location   | varchar(20) | YES  |     | NULL    |                | </br>
| technology | varchar(20) | YES  |     | NULL    |                | </br>
+------------+-------------+------+-----+---------+----------------+ </br>
5 rows in set (0.01 sec)</br>







