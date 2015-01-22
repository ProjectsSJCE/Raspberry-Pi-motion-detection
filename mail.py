import smtplib
try:
#       block to mail
# Create a text/plain message
        msg = email.mime.Multipart.MIMEMultipart()
        msg['Subject'] = str(day)
        msg['From'] = 'sitechecker@gmx.com'
        msg['To'] = 'comperio@gmx.com'

# The main body is just another attachment
#body = email.mime.Text.MIMEText("""Hello, how are you? I am fine.
#This is a rather nice letter, don't you think?""")
#msg.attach(body)

# PDF attachment
        filename = str(day) + '.csv'
        fp=open(filename,'rb')
        att = email.mime.application.MIMEApplication(fp.read(),_subtype="csv")
        fp.close()
        att.add_header('Content-Disposition','attachment',filename = str(day) + '.csv')
        msg.attach(att)
        print "File one attached"

        filename = "Changes-" + str(day) + '.csv'
        fp=open(filename,'rb')
        att = email.mime.application.MIMEApplication(fp.read(),_subtype="csv")
        fp.close()
        att.add_header('Content-Disposition','attachment',filename = "Changes-" + str(day) + ".csv")
        msg.attach(att)
        print "File two attached"

        filename = "Time-" + str(day) + ".csv"
        fp=open(filename,'rb')
        att = email.mime.application.MIMEApplication(fp.read(),_subtype="csv")
        fp.close()
        att.add_header('Content-Disposition','attachment',filename = "Time-" + str(day) + ".csv")
        msg.attach(att)
        print "File three attached"

# send via Gmail server
# NOTE: my ISP, Centurylink, seems to be automatically rewriting
# port 25 packets to be port 587 and it is trashing port 587 packets.
# So, I use the default port 25, but I authenticate. 
#       s = smtplib.SMTP('smtp.gmail.com')
#       s.starttls()
        s = smtplib.SMTP('smtp.gmx.com:587') #smtp.gmx because it has to login to gmx mailing service. it will be gmail for gmail and yahoo for yahoo etc
        s.starttls()
#       print "smtplib"
        print "logging in:"
        s.login('sitechecker@gmx.com','12345password')
        print "logged in"
        s.sendmail('sitechecker@gmx.com',['comperio@gmx.com'], msg.as_string())
        print "sent"
        s.quit()
except:
       print "Sorry, couldn't mail, try again."
