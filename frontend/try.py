import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login("inmyveinspetrol@gmail.com", "Petrolinmyveins1234")

# message to be sent
message = "hello"

# sending the mail
s.sendmail("inmyveinspetrol@gmail.com", "inmyveinspetrol@gmail.com", message)

# terminating the session
s.quit()
