import smtplib
import email
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

s = smtplib.SMTP('smtp.gmail.com:587') #smtp.gmx because it has to login to gmx mailing service. it will be gmail for gmail and yahoo for yahoo etc
s.starttls()
print "logging in:"
s.login('fullfake11@gmail.com','fakepassword11')
print "logged in"

for i in range(2):
    msg = email.mime.Multipart.MIMEMultipart()
    msg['Subject'] = "Motion detected"
    msg['From'] = 'fullfake11@gmail.com'
    msg['To'] = 'ts.sharath18@gmail.com'

    # PDF attachment
    filename = "image.jpg"
    fp=open(filename,'rb')
    img = MIMEImage(fp.read())
    #att = email.mime.application.MIMEApplication(fp.read(),_subtype="jpg")
    fp.close()
    #att.add_header('Content-Disposition','attachment',filename = "image.jpg" + '.jpg')
    msg.attach(img)
    print "File one attached"

    # send via Gmail server
    # NOTE: my ISP, Centurylink, seems to be automatically rewriting
    # port 25 packets to be port 587 and it is trashing port 587 packets.
    # So, I use the default port 25, but I authenticate. 
    #       s = smtplib.SMTP('smtp.gmail.com')
    #       s.starttls()

    s.sendmail('fullfake11@gmail.com',['ts.sharath18@gmail.com'], msg.as_string())
    print "sent"
#except:
#       print "Sorry, couldn't mail, try again."
