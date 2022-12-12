import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

#Initiates connection with gmail server and sends email
def send_email(address, message, subject):
    sender = "sigmagrindset110@gmail.com"
    receiver = address

    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    # Create html version of the body
    body = MIMEText(message, 'html')

    # Combine all in the message container
    msg.attach(body)

    try:
        # Send the message via local SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(sender, 'fgbqrmbcnlfdkkju')
        mail.sendmail(sender, receiver, msg.as_string())
        mail.quit()

        print('Email sent!')
    except:
        print('Error')


#Creates HTML body/format for email that will be sent
#RETURNS formatted message
def profile_edit_mail_message(name, dates, scenario):
    message = """\
    <html>
      <div style="display: flex; width: 100%; height: 60px; background-color: #d1c4e9; align-items: center; justify-content: center;">
      <p><strong>RottenPotatoes</strong></p>
      </div>
        <head></head>
        <body style="border:3px; border-style:solid; border-color:#b39ddb; padding: 1em;">
            <p ><font face="Trebuchet MS" color="#474B50">
                Hi {name}<br>
                <br>
                    &nbsp; &nbsp; This is a warning email, your {scenario} part of the profile has been edited on <strong>{dates}</strong>.<br>
                    &nbsp; &nbsp; <br>
                    &nbsp; &nbsp; Click <strong><a href="http://localhost:3000/profile/{name}">here</a></strong> to view your updated profile.<br>
                    &nbsp; &nbsp; <br>
                Best Regards,<br>
                <font color="#b39ddb"; border-style: >RottenPotatoes Team</font>
                </font>
            </p>
        </body>
    </html>
    """.format(name=name, dates=dates, scenario = scenario)

    return message

#Creates HTML body/format for email that will be sent
#RETURNS formatted message
def email_confirmation_message(code):
    message = """\
    <html>
      <div style="display: flex; width: 100%; height: 60px; background-color: #d1c4e9; align-items: center; justify-content: center;">
      <p> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <strong>RottenPotatoes</strong></p>
      </div>
        <head></head>
        <body style="border:3px; border-style:double; border-color:#b39ddb; padding: 1em;">
            <p ><font face="Trebuchet MS" color="#474B50">
                <br>
                    &nbsp; &nbsp; This is your verification code {code}.<br>
                <br>
                <br>
                Best Regards,<br>
                <font color="#3081EA">RottenPotatoes Team</font>
                </font>
            </p>
        </body>
    </html>
    """.format(code=code)

    return message
