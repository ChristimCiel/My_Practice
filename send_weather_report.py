import smtplib
import email.message
import schedule
import time

my_email = "xxx@yahoo.com"
password = "Your_password"

i = 1

def send_email():
    global i
    localtime = time.localtime()
    now = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
    msg = email.message.Message()
    msg["Form"] = my_email
    msg["To"] = "xxx@gmail.com"
    msg["Subject"] = f"The first email ever"
    msg.set_content(now)

    #Get fromt the mail provider's server
    connection = smtplib.SMTP_SSL("smtp.mail.yahoo.com")
    connection.login(my_email, password)
    connection.send_message(msg)
    connection.close()
    print(f"{i} email {now} has been successfully sent!")
    i += 1 

schedule.every().minute.do(send_email)

while True:
     schedule.run_pending()
     time.sleep(1)
