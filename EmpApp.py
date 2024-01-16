from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *
from datetime import datetime
from botocore.client import Config
 
app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'

# Home
@app.route('/')
def home():
    return render_template('index.html')

# About Us
@app.route('/aboutUs')
def new_home():
    return render_template('AboutUs.html')

# Add Employee
@app.route("/addnewemp", methods=['GET', 'POST'])
def addEmployee():
    return render_template('AddEmp.html')

#about page
@app.route("/about", methods=['GET'])
def about():
    return render_template('https://youtu.be/ih9zBLDr_ro')

#add employee
@app.route("/addemp", methods=['POST'])
def AddEmp():
    name = request.form['name']
    location = request.form['location']
    age = request.form['age']
    technology = request.form['technology']
    emp_image_file = request.files['emp_image_file']

    insert_sql = "INSERT INTO employees (name, location, age, technology) VALUES (%s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:
        cursor.execute(insert_sql, (name, location, age, technology))
        db_conn.commit()
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-" + name + "-" + location + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=name)

#edit employee
@app.route("/editemp", methods=['GET','POST'])
def EditEmp():
    emp_id = request.form['emp_id']
    name = request.form['name']
    location = request.form['location']
    age = request.form['age']
    technology = request.form['technology']

    update_sql = "UPDATE employees SET name = %s, location = %s, age = %s, technology = %s WHERE emp_id = %s"
    cursor = db_conn.cursor()

    try:
        changefield = (name, location, age, technology, emp_id)
        cursor.execute(update_sql, (changefield))
    
    except Exception as e:
        return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('EditEmpOutput.html', name=name)

#get edit data
@app.route("/geteditemp/<string:id>", methods=['GET','POST'])
def GetEditData(id):
    emp_id = id
    mycursor = db_conn.cursor()
    getempdata = "select * from employees WHERE emp_id = %s"
    mycursor.execute(getempdata,(emp_id))
    result = mycursor.fetchall()
    (emp_id, name, age, location, technology) = result[0]   
    return render_template('EditEmp.html', emp_id=emp_id, name=name, location=location, age=age, technology=technology, result=result)
    
#delete employee
@app.route("/delemp/<string:id>", methods=['GET','POST'])
def DeleteEmp(id):
    emp_id = id
    mycursor = db_conn.cursor()
    del_emp_sql = "DELETE FROM employees WHERE emp_id = %s"
    mycursor.execute(del_emp_sql, (emp_id))
    db_conn.commit()

    return render_template('DeleteEmpOutput.html', emp_id=emp_id)
    
#get employee
@app.route("/staffDet", methods=['GET','POST'])
def GetEmpData(): 
    mycursor = db_conn.cursor()
    getempdata = "select * from employees"
    mycursor.execute(getempdata)
    employee = mycursor.fetchall()
    return render_template('DetailsOutput.html', employee=employee)

#get SINGLE employee
@app.route("/getemp", methods=['GET'])
def GetSingleEmpData():
    emp_id = request.args['emp_id']
    mycursor = db_conn.cursor()
    getempdata = "select * from employees WHERE emp_id = %s"
    mycursor.execute(getempdata,(emp_id))
    result = mycursor.fetchall()
    if not result:
        return render_template('EmpLookup.html', err='Employee with id %s does not exist' % emp_id)
    (emp_id, name, age, location, technology) = result[0]   
    image_url = showimage(bucket, name, location)
    return render_template('GetEmpOutput.html', emp_id=emp_id, name=name, location=location, age=age, technology=technology, image_url=image_url)

# Load EmployeeLookup Page
@app.route("/employeeLookup")
def LoadEmployeeLookup():
    return render_template('EmpLookup.html')

#Get Employee ID
@app.route("/empattid", methods=['GET','POST'])
def GetEmpId(): 
    #create a cursor
    mycursor = db_conn.cursor()
    getempdata = "select * from employees"
    mycursor.execute(getempdata)
    emps = mycursor.fetchall()
    #render template and send the set of tuples to the HTML file for displaying
    return render_template("attendance.html",emps=emps )

def showimage(bucket, name, location):
    s3_client = boto3.client('s3', region_name=customregion, config=boto3.session.Config(signature_version='s3v4', s3={'signature_version': 's3v4', 'use_accelerate_endpoint': False}))
    public_urls = []
    emp_image_file_name_in_s3 = "emp-" + name + '-' + location + "_image_file"
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': emp_image_file_name_in_s3}, ExpiresIn = 100)
            print(presigned_url)
            public_urls.append(presigned_url)
    except Exception as e:
        pass
    # print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
