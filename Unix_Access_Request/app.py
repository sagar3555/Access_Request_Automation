from flask import Flask, render_template,flash, request ,session ,redirect ,url_for,g
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import subprocess
import re
from functools import wraps
from  insertintodatabase import Insert_Into_Database ,Get_Data_From_Database,Update_Status , Get_Request_For_Approval ,My_Requests
from mails import Request_raised , Request_Approved_Or_Rejected
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class LoginForm(Form):
    login_id = TextField('Name:', validators=[validators.required()])
    password = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])


class Access_Request_Form(Form):
    access = TextField('access:', validators=[validators.required(), validators.Length(min=1, max=1)])
    server_list = TextField('server_list:', validators=[validators.required(), validators.Length(min=6, max=35)])
    application_user = TextField('application_user :', validators=[validators.required(), validators.Length(min=1, max=1)])
    application_user_names  = TextField('application_user_names:' ,validators=[validators.required(), validators.Length(min=3, max=200)])
    reason = TextField('reason:',  validators=[validators.required(), validators.Length(min=3, max=500)])
    contact = TextField('contact:', validators=[validators.required(), validators.Length(min=9, max=13)])
    specific_group = TextField('specific_group:', validators=[validators.required(), validators.Length(min=1, max=1)])
    specific_group_names = TextField('specific_group_names:', validators=[validators.required(), validators.Length(min=3, max=200)])

class ApproveReject (Form) :
    approve_or_reject = TextField('approved/rejected:')


@app.route("/unixcaccessrequest", methods=['GET', 'POST'])
def hello1():
        ##contactno = "sagar"
        if g.user :


            fh = open("getreportee.ps1", "w+")
            fh.write(
                "import-module activedirectory \n Get-ADUser -Filter ('manager -eq " + '"' + g.user + '"' + "')|foreach { $_.SamAccountName }")
            fh.close()

            ch = subprocess.Popen(
                [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe', '-ExecutionPolicy', 'Unrestricted',
                 r"E:\Unix_Access_Request\getreportee.ps1"], shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = ch.communicate()
            #print(stdout)
            #print(stderr)
            temp2 = stdout.decode()
            #print(temp2, "temp2", type(temp2))

            if temp2 == '':
                ismanager = False
                reporteelist = [g.user]

            elif temp2 != '':
                ismanager = True
                reporteelist = temp2.replace('\r', '')
                reporteelist = reporteelist.split('\n')
                reporteelist = [x.upper() for x in reporteelist]
                print(reporteelist)

            fh = open("getcontactno.ps1", "w+")
            fh.write(
                "import-module activedirectory \n Get-ADUser -Id " + g.user + " -Properties *|  foreach { $_.mobile }")
            fh.close()

            ch = subprocess.Popen(
                [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe', '-ExecutionPolicy', 'Unrestricted',
                 r"E:\Unix_Access_Request\getcontactno.ps1"], shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = ch.communicate()
            contactno = stdout.decode()




            form = Access_Request_Form(request.form)
            if request.method == 'POST':
                requested_for  = request.form['user']
                access = request.form['access']
                if access.lower() == 'y':
                    access = "yes"
                else:
                    access = "No"

                #server_list = request.form['server_list']
                application_user = request.form['application_user']
                if application_user.lower() == 'y':
                    application_user = "yes"
                else :
                    application_user = "No"

                application_user_names = request.form['application_user_names']
                reason = request.form['reason']
                contact = request.form['contact']
                specific_group = request.form['specific_group']
                if specific_group.lower() == 'y':
                    specific_group = "yes"
                else:
                    specific_group = "No"
                specific_group_names = request.form['specific_group_names']
                count  = request.form['count']
                server_list_final = request.form['server_list_final']
                print (server_list_final)
                ch = subprocess.Popen(
                    [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe', '-ExecutionPolicy', 'Unrestricted',
                     r'E:\Unix_Access_Request\get_reqester_details.ps1', "-requestername " +requested_for]
                    , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = ch.communicate()
                requester_details  = stdout.decode()
                requester_details = requester_details.split("\n")
                print(requester_details)

                requested_for_email_id = requester_details[0].replace("\r","")
                manager_id = requester_details[1].replace("\r","")
                manager_email_id = requester_details[2].replace("\r","")



                if ismanager and  g.user == manager_id :
                    request_id  = Insert_Into_Database(requested_for ,requested_for_email_id , manager_id ,manager_email_id ,access ,server_list_final ,application_user,application_user_names,reason ,contact,specific_group ,specific_group_names,'approved'  )
                    Request_Raised_Approved(request_id,requested_for,requested_for_email_id,manager_email_id,reason)
                    #flash("Sucess request raised : request id - " + str(
                    #    request_id) + "and auto approved" )

                else  :
                    #manager_id = "extsdd"
                    request_id = Insert_Into_Database(requested_for, requested_for_email_id, manager_id, manager_email_id, access,
                                         server_list_final, application_user, application_user_names, reason, contact,
                                         specific_group, specific_group_names, 'Sent for approval')

                    Request_raised(request_id ,requested_for ,requested_for_email_id,manager_email_id,reason)

                    #flash("Sucess request raised : request id - " + str(request_id) + " and Sent for approval to your manger " + manager_id + "(" + manager_email_id + ")")
                    return  render_template("requestraised.html" , request_id = request_id ,manager_email_id = manager_email_id ,status="Sent For Approval")
            return render_template("requestpage-new.html", form=form ,contactno = contactno ,reporteelist=reporteelist)
        return redirect(url_for("login"))




@app.route('/request/id/<int:request_id>' ,methods=['GET','POST'])
def profile(request_id):
    try  :
        if g.user :
            request_data = Get_Data_From_Database(request_id)
            if request_data[0] == g.user or request_data[9] == g.user :
                form = ApproveReject(request.form)
                if request.method == 'POST':
                    approve_or_reject = request.form['approved/rejected']
                    print (approve_or_reject)
                    Update_Status(request_id , approve_or_reject)
                    request_data = Get_Data_From_Database(request_id)
                    Request_Approved_Or_Rejected (request_id , request_data[11] ,request_data[1],approve_or_reject)
                    print (request_data[11])
                    return render_template('approverejectrequest.html', requested_for_id=request_data[0],
                                           manager_email_id=request_data[1], \
                                           server_list_final=request_data[2], application_user=request_data[3],
                                           application_user_names=request_data[4], \
                                           reason=request_data[5], specific_group=request_data[6],
                                           specific_group_names=request_data[7], status=request_data[8],
                                           manager_id=request_data[9], datetime=request_data[10])


                return render_template('approverejectrequest.html',requested_for_id = request_data[0],manager_email_id=request_data[1], \
                                       server_list_final=request_data[2],application_user= request_data[3],application_user_names = request_data[4],\
                                       reason=request_data[5],specific_group = request_data[6] , specific_group_names=request_data[7],status=request_data[8],manager_id= request_data[9],datetime = request_data[10])
            return ("You are not authorised !")
        print (request.url ,"requested url ")
        return redirect(url_for("login" , next = request.url))

    except  :
        return  "Reqest does not exists"






@app.before_request
def before_request() :
    g.user = None
    if 'user' in session :
        g.user  = session['user']


@app.route("/login",methods=['GET', 'POST'])
def login() :
    form = LoginForm(request.form)
    if request.method == 'POST':
        session.pop('user',None)


        loginid = request.form['login_id']
        password = request.form['password']
        #print(loginid , password)

        password_formatted = """{0}"""
        password_formatted = password_formatted.format(password)
        print (password_formatted)
        fh = open("VerifyCredentials.ps1", "w+")
        fh.write("function Test-ADCredential {\n \
                [CmdletBinding()]\n \
                 Param\n \
                (\n \
                    [string]$UserName,\n\
                    [string]$Password \n\
                )\n\
                if (!($UserName) -or !($Password)) {\n\
                Write-Warning 'Test-ADCredential: Please specify both user name and password'\n\
                } else {\n\
                Add-Type -AssemblyName System.DirectoryServices.AccountManagement\n\
                $DS = New-Object System.DirectoryServices.AccountManagement.PrincipalContext('domain')\n\
                $DS.ValidateCredentials($UserName, $Password)\n\
                }\n\
                } \n ")
        fh.write("Test-ADCredential -username "+ loginid +"  -password "+ password)
        fh.close()

        powerShellPath = r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe'
        powershellfile = r'E:\Unix_Access_Request\VerifyCredentials.ps1'
        p = subprocess.Popen([powerShellPath, '-ExecutionPolicy', 'Unrestricted', powershellfile,
                              "Test-ADCredential -username " + loginid + " " + " -Password " + " " + password_formatted],
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        temp1 = stdout.decode()
        temp2  = stderr.decode()
        #print (temp2 , password ,loginid)


        if "True" in temp1 :
            session['user'] = loginid

            return redirect(url_for("Home"))

        else :
            flash("Login Id or Password is Incorrect")

    return render_template("login.html", form=form)


@app.route("/home",methods=['GET', 'POST'])
def Home () :
    if g.user :
        return render_template("home.html")
    return redirect(url_for("login"))

@app.route("/requestforapproval",methods=['GET', 'POST'])
def Request_Approval () :
    if g.user :
        requests = Get_Request_For_Approval(g.user)
        print (requests ,"requests")
        return render_template("reqestsforapproval.html" ,requests=requests)
    return redirect(url_for("login"))

@app.route("/myrequests",methods=['GET', 'POST'])
def MyRequests () :
    if g.user :
        requests = My_Requests(g.user)
        print (requests ,"requests")
        return render_template("myrequests.html" ,requests=requests)
    return redirect(url_for("login"))



@app.route("/adminlogin",methods=['GET', 'POST'])
def Admin_login() :
    if  g.user :
        return render_template("adminloginpage.html")
    else  :
        return redirect(url_for("login"))

@app.route("/userlogin",methods=['GET', 'POST'])
def Normal_User_login() :
        if g.user:
            return render_template("normaluserlogin.html")
        else:
            return redirect(url_for("login"))


@app.route("/logout",methods=['GET', 'POST'])
def logout() :
    session.pop('user', None)


    return redirect(url_for("login"))






if __name__ == "__main__":
    app.run( host = "10.102.112.150", port=80,threaded = True)
