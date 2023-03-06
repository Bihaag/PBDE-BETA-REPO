from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

currentlocation = os.path.dirname(os.path.abspath(__file__))

##CREATING TABLE(JOBS) IN DB
"""import sqlite3
conn = sqlite3.connect('Login.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT, usertype TEXT)')
conn.commit()
conn.close()"""

##CREATING TABLE(JOBS) IN DB
"""import sqlite3
conn = sqlite3.connect('Login.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE jobs (JobId INTEGER PRIMARY KEY, Job_Title TEXT, Job_Description TEXT, Faculty TEXT)')
conn.commit()
conn.close()
"""

##INSERT INTO TABLE (USERS)
"""'''sqlconnection = sqlite3.Connection(currentlocation + "\Login.db")'''
sqlconnection = sqlite3.connect('Login.db')
cursor = sqlconnection.cursor()
'''query1 = "INSERT INTO users (name, password, email, usertype) VALUES(?,?,?)",("Vaish", "123", "vaish@gmail.com", "admin")
cursor.execute(query1)'''
cursor.execute("INSERT INTO users (username, password, email, usertype) VALUES(?,?,?,?)",('Vaish', '123', 'vaish@gmail.com', 'Admin'))
sqlconnection.commit()
sqlconnection.close()"""

##INSERT INTO TABLE (JOBS)
"""sqlconnection = sqlite3.connect('Login.db')
cursor = sqlconnection.cursor()
cursor.execute("INSERT INTO jobs (Job_Title, Job_Description, Faculty) VALUES(?,?,?)",('Data Analyst', 'You will be required to analyse data', 'IT'))
sqlconnection.commit()
sqlconnection.close()"""

##DELETE SPECIFIC RECORDS
'''sqlconnection = sqlite3.connect('Login.db')
cursor = sqlconnection.cursor()
cursor.execute("DELETE FROM jobs WHERE Job_Title = 'Data Analyst'")
sqlconnection.commit()
sqlconnection.close()'''

##DELETE SPECIFIC RECORDS
'''sqlconnection = sqlite3.connect('Login.db')
cursor = sqlconnection.cursor()
cursor.execute("DELETE FROM users WHERE username = 'Vaish'")
sqlconnection.commit()
sqlconnection.close()'''

##DELETE ALL RECORDS
'''import sqlite3
# Connect to the database
conn = sqlite3.connect('Login.db')
c = conn.cursor()
# Execute the delete command
c.execute('DELETE FROM jobs')
# Commit the changes
conn.commit()
# Close the connection
conn.close()'''


myapp = Flask(__name__)


@myapp.route("/")
def homepage():
    return render_template("Homepage.html")

##LOGIN
@myapp.route("/", methods = ["POST"])
def checklogin():
    UN = request.form['username']
    PW = request.form['password']
    UT = request.form['usertype']

    '''sqlconnection = sqlite3.Connection(currentlocation + "\Login.db")'''
    sqlconnection = sqlite3.connect('Login.db')
    cursor = sqlconnection.cursor()
    '''query1 = "SELECT Username, Password from users WHERE Username = {un} AND Password = {pw}".format(un = UN, pw = PW)'''

    query1 = "SELECT username, password FROM users WHERE username = ? AND password = ? AND usertype = ?"
    params = (UN, PW, UT)
    
    rows = cursor.execute(query1,params)
    rows = rows.fetchall()
    
    if len(rows) == 1 and UT == "Admin":
        return render_template("LoggedIn.html")
    elif len(rows) == 1 and UT == "Applicant":
        return render_template("LoggedInApplicant.html")
    else:
        '''return redirect("/profilenotfound")'''
        return render_template("ProfileNotFound.html")

##REGISTER
@myapp.route("/register", methods = ["GET", "POST"])
def registerpage():
    if request.method == "POST":
        dUN = request.form['username']
        dPW = request.form['password']
        Uemail = request.form['email']
        Uusertype = request.form['usertype']
        
        '''sqlconnection = sqlite3.Connection(currentlocation + "\Login.db")'''
        sqlconnection = sqlite3.connect('Login.db')
        cursor = sqlconnection.cursor()
        '''query1 = "INSERT users VALUES('{u}','{p}','{e}')".format(u = dUN, p=dPW, e=Uemail)'''
        query1 = "INSERT INTO users (username, password, email, usertype) VALUES(?, ?, ?, ?)"
        values = (dUN, dPW, Uemail, Uusertype)
        cursor.execute(query1,values)
        sqlconnection.commit()
        '''return redirect("/")'''
        return render_template("SuccessfulRegistration.html")
    return render_template("Register.html")

##ADD JOB
@myapp.route("/addjob", methods = ["GET", "POST"])
def addjob():
    if request.method == "POST":
        jTitle = request.form['jobtitle']
        jDes = request.form['jobdescription']
        fAc = request.form['faculty']
    

        sqlconnection = sqlite3.connect('Login.db')
        cursor = sqlconnection.cursor()
    
        query1 = "INSERT INTO jobs (Job_Title, Job_Description, Faculty) VALUES(?, ?, ?)"
        values = (jTitle, jDes, fAc)
        cursor.execute(query1,values)
        sqlconnection.commit()
        '''return redirect("/")'''
        return render_template("SuccessfulJobAdded.html")
    return render_template("AddJob.html")

## VIEW DATABASE
'''@myapp.route('/availablejobs')'''
@myapp.route('/selectedFile')
def index():
    conn = sqlite3.connect('Login.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Job_Title, Job_Description, Faculty FROM jobs')
    jobs = cursor.fetchall()
    conn.close()
    return render_template('selectedFile.html', jobs=jobs)
'''return render_template('AvailableJobs.html', jobs=jobs)
'''

##SELECT RECORD - TO EDIT JOBS
import sqlite3

@myapp.route('/selectedFile', methods=['GET', 'POST'])
def select_record_from_database():
    if request.method == 'POST':
        # Get the selected ID value from the form data
        selected_id = request.form['selected_job']
        
        conn = sqlite3.connect('Login.db')
        c = conn.cursor()

        # Execute the SELECT statement using the selected ID value
        c.execute("SELECT * FROM jobs WHERE JobId=?", (selected_id,))

        # Fetch the selected record
        selected_record = c.fetchone()

        # Close the database connection
        conn.close()

        # Return the selected record
        return render_template('UpdateJob.html', job=selected_record, selected_job=selected_id)

    else:
        return "Error: Invalid request method."


##Update Record
@myapp.route('/updateJob', methods=['POST'])
def update_job():
    # Get the form data
    job_Id = request.form['JobId']
    job_title = request.form['Job_Title']
    job_description = request.form['Job_Description']
    faculty = request.form['Faculty']

    # Connect to the database
    conn = sqlite3.connect('Login.db')
    c = conn.cursor()

    # Execute the UPDATE statement to update the job record
    c.execute("UPDATE jobs SET Job_Title=?, Job_Description=?, Faculty=? WHERE JobId=?", (job_description, faculty, job_title))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Redirect to the jobs page
    return render_template('/selectedFile.html')


if __name__ == "__main__":
   myapp.run(port=8082, debug=True)
