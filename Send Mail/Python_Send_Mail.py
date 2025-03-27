import smtplib
import email.message
import schedule
import time

my_email = "email_account"
password = "password_you_get"
i = 1

def send_email():
    global i
    localtime = time.localtime()
    now = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
    msg = email.message.EmailMessage()
    msg["From"] = my_email
    msg["To"] = "receiver email"
    msg["Subject"] = "Hi !"
    msg.set.content(f"{now}")


    #寄出前要先連線，去查找要使用 Email 的伺服器
    connection = smtplib.SMTP_SSL("smtp.mail.yahoo.com")
    connection.login(my_email,password)
    connection.send_message(msg)
    connection.close()

    print(f"第{i}封信件，{now}，發送成功")
    i += 1

schedule.every().minute.do(send_email)
while True:
    schedule.rum_pending()
    time.sleep(1)
