def Request_raised (id , requested_for,requested_for_email, manager_email ,reason) :

    SMTPserver = 'smtp-relay.ica.ia-hc.net'
    sender =     'sagar.debadwar@ica.se'
    destination = [requested_for_email]
    #requested_for_email = 'sagar.debadwar@ica.se'

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'


    content= "PFB details for Unix access request waiting for your Approval  "+"\n" \
             " Request Id : "+str(id)+"\n" \
             "\n Requested For :"+str(requested_for)+"\n " \
            "Reason For request : "+reason+"\n " \
            "Link for Approval :  http://10.102.112.150/login (best Viewed In chrome) "

    subject= "Unix Access reques waiting your Approval"

    import sys
    import os
    import re

    #from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
    from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

    # old version
    # from email.MIMEText import MIMEText
    from email.mime.text import MIMEText


    msg = MIMEText(content)
    msg['Subject']=       subject
    msg['From']   = sender # some SMTP servers will do this automatically, not all
    msg['To'] = manager_email
    msg['CC'] = requested_for_email
    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    #conn.login(USERNAME, PASSWORD)

    conn.sendmail(sender, destination, msg.as_string())
    conn.quit()

#First_mail("a","2018-02-03","sagar.debadwar@ica.se")

def Request_Raised_Approved (id , requested_for,requested_for_email, manager_email ,reason) :
    SMTPserver = 'smtp-relay.ica.ia-hc.net'
    sender = 'sagar.debadwar@ica.se'
    destination = [requested_for_email]
    #requested_for_email = 'sagar.debadwar@ica.se'

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'

    content = "Access request has been approved ."

    subject = "Unix Access Request Approved (Request Id ) : " +str(id)

    import sys
    import os
    import re

    # from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
    from smtplib import SMTP  # use this for standard SMTP protocol   (port 25, no encryption)

    # old version
    # from email.MIMEText import MIMEText
    from email.mime.text import MIMEText

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = sender  # some SMTP servers will do this automatically, not all
    msg['CC'] = manager_email
    msg['To'] = manager_email
    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    # conn.login(USERNAME, PASSWORD)

    conn.sendmail(sender, destination, msg.as_string())
    conn.quit()


def Request_Approved_Or_Rejected(id ,requested_for_email, manager_email ,approveorreject) :
    SMTPserver = 'smtp-relay.ica.ia-hc.net'
    sender = 'sagar.debadwar@ica.se'
    destination = [requested_for_email]
    #requested_for_email = 'sagar.debadwar@ica.se'

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'

    content = "Access request has been approved ."

    subject = "Unix Access Request  (Request Id ) : " +str(id) + " has been "+approveorreject

    import sys
    import os
    import re

    # from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
    from smtplib import SMTP  # use this for standard SMTP protocol   (port 25, no encryption)

    # old version
    # from email.MIMEText import MIMEText
    from email.mime.text import MIMEText

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = sender  # some SMTP servers will do this automatically, not all
    msg['CC'] = manager_email
    msg['To'] = requested_for_email
    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    # conn.login(USERNAME, PASSWORD)

    conn.sendmail(sender, destination, msg.as_string())
    conn.quit()
