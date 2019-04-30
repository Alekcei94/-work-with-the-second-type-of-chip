import smtplib
import time

def start():
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
	print(smtpObj.starttls())
	smtpObj.login('alekcei940421@gmail.com', 'fnnkbvgzxm9n7')
	smtpObj.sendmail('alekcei940421@gmail.com', 'alekcei940421@gmail.com', 'test')
	smtpObj.quit()