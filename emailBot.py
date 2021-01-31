import smtplib, ssl, email

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def send_email(filename):

	port = 465  # For SSL
	smtp_server = "smtp.gmail.com"
	sender_email = "roetger.bot@gmail.com"  # Enter your address
	receiver_email = "andreroetger@yahoo.com.br"  # Enter receiver address
	password = '*****************'

	subject = f"{os.path.basename(filename)}"
	body = "Envio atuomático!"

	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Subject"] = subject


	message.attach(MIMEText(body, "plain"))

	with open(filename, "rb") as attachment:
	    # Add file as application/octet-stream
	    # Email client can usually download this automatically as attachment
	    part = MIMEBase("application", "octet-stream",name=os.path.basename(filename))
	    part.set_payload(attachment.read())

	# Encode file in ASCII characters to send by email    
	encoders.encode_base64(part)
	print(os.path.basename(filename))

	# Add header as key/value pair to attachment part
	part.add_header(
	    'Content-Disposition' ,
	    'attachment; filename="%s"' % os.path.basename(filename)
	)
	print( "attachment; filename='%s'" % os.path.basename(filename),)

	# Add attachment to message and convert message to string
	message.attach(part)
	text = message.as_string()




	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, text)


