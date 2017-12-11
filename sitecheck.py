# import requests to check webpages
import requests

# import datetime for showing the date and time
import datetime

# import time for scheduling
import time

# Import smtplib for the actual sending function
import smtplib

# Import the email modules needed
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import the websites list from websites.py
from websites import websites

# how many seconds to repeat the script
MANY_SEC 		= 4 * 60 * 60

# email variables
EMAIL_SUBJECT 	= 'Awesome Websites Report '
MY_ADDRESS 		= 'from@gmail.com'
PASSWORD 		= 'password' # specify the password for the from email address
MY_NAME			= 'Awesome Sites Check'
SEND_TO 		= 'to@gmail.com'
HOST 			= 'smtp.gmail.com'
HTML_HEAD 		= '<html><body><ul>'
HTML_FOOT 		= '</ul></body></html>'

# main function
def theEmailHandler():

	print '********************************************'
	print '************ Checking Websites *************'
	print '********************************************'

	# empty variable to hold all the messages
	message = ''

	# checking websites and adding the message up
	for name, website in websites.iteritems():
		timenow = datetime.datetime.now().strftime('%-H:%M:%S ')
		try:
			request = requests.get(website)
			if request.status_code == 200:
				message += '<li><a href="'+website+'" target="_blank">'+name+'</a>: <span style="color:green">is working at '+timenow+'</span></li>'
				print name + ' is Working at '+timenow
			else:
				message += '<li><a href="'+website+'" target="_blank">'+name+'</a>: <span style="color:red"> is down at '+timenow+'</span></li>'
				print name + ' is down at '+timenow+'  <-------- is down'
		except requests.ConnectionError:
			message += '<li><a href="'+website+'" target="_blank">'+name+'</a>: <span style="color:orange"> has a connection error '+timenow+'</span></li>'
			print name + ' is down at '+timenow+'  <-------- has a connection error'

	msg = MIMEMultipart('alternative')

	# setup the parameters of the message
	msg['From'] = MY_NAME
	msg['To'] = SEND_TO
	msg['Subject'] = EMAIL_SUBJECT + datetime.datetime.now().strftime('%A, %B %d, %Y %-H:%M:%S ')

	# Adding the message body
	msg.attach(MIMEText(HTML_HEAD + message + HTML_FOOT, 'html'))

	# set up the SMTP server
	s = smtplib.SMTP_SSL(HOST)
	s.login(MY_ADDRESS, PASSWORD)

	print 'Sending message at '+timenow
	print '********************************************'
	
	# send the message via the server set up earlier.
	s.sendmail(MY_ADDRESS, SEND_TO, msg.as_string())
	del msg
		
	# Terminate the SMTP session and close the connection
	s.quit()

	time.sleep(MANY_SEC)
	
while True:
	theEmailHandler()