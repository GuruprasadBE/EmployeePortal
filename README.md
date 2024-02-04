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
mysql -h <rds_db_instance>.ap-south-1.rds.amazonaws.com -u admin -p </br>
mysql> create database <db_name>; </br>
mysql> use <db_name>; </br>

mysql> create table employees(emp_id int(20) auto_increment, name varchar(20), age int(20), location varchar(20), technology varchar(20), PRIMARY KEY (emp_id)); </br>
mysql> alter table employees AUTO_INCREMENT=2024001; </br>
mysql> select * from employees; </br>
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

Lambda Function and Trigger:
=============================
https://awstip.com/s3-upload-lambda-trigger-5afd9e9be819 </br>
https://beabetterdev.com/2022/12/04/aws-s3-file-upload-lambda-trigger-tutorial/ </br>

https://stackoverflow.com/questions/64566908/aws-cloudwatch-log-group-does-not-exist </br>

SNS Topic:
==========
https://medium.com/@ernestosafo11/creating-and-subscribing-to-sns-topics-and-adding-sns-event-for-s3-bucket-df2e9cfb9d5d </br>
https://www.geeksforgeeks.org/amazon-web-services-amazon-s3-notifications-to-sns/ </br>

Create a SNS Topic. </br>
Create Subscription and give it as Email. </br>
Now go to S3 bucket -> Properties -> EventNotifications </br>
Create Event Notification and Choose the Destination as the SNS Topic </br>
This will send out a json email notification when a object is uploaded to the S3 bucket. </br>
To get a custom email message, create a lambda function and add the trigger as SNS topic. </br>
Now you will receive the SNS event in the lambda function. Parse based on your need and publish it to SNS topic to send out as email. </br>
For this lambda function, you need to attach a inline policy, sns:Publish from Lambda -> Configuration -> Permissions -> Execution Role -> click on 'Role Name'. </br>
This will navigate to the IAM page where you can create the inline policy, by searching for SNS and Publish keyword. And here you can restrict the ARNs to the sns topic ARN which we are using. </br>



