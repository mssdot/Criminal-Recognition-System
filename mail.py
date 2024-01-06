# app.py
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os
import glob

app = Flask(__name__)

# Flask-Mail configuration
app.config['SECRET_KEY'] = "tsfyguaistyatuis589566875623568956"

app.config['MAIL_SERVER'] = "smtp.googlemail.com"

app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = "mss182311@gmail.com"

app.config['MAIL_PASSWORD'] = "wrpk quwf jzbz vdyq"

mail = Mail(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def send_email(to_email, subject, body, attachment_paths):
	msg = Message(subject, recipients=[to_email], sender=app.config['MAIL_USERNAME'])
	msg.body = body

	 

	#...................................file ttachment.....................................
	image_directory = attachment_paths
	 

	file_count = sum(1 for file in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, file)))
	 
	
	for filename in os.listdir(image_directory): 
		 
		if filename.endswith(('.jpg', '.jpeg', '.png')):
			image_path = os.path.join(image_directory, filename)
			with app.open_resource(image_path) as fp:
			    #msg.attach(filename, 'image/jpg', fp.read(), 'inline', headers=[('Content-ID', f'a{c}')])
				msg.attach(filename, 'image/jpg', fp.read()  )
	 
	if(file_count==0):
		print("no files are found . so criminal is detected")
	try:
		mail.send(msg)
		return True
	except Exception as e:
		return str(e)

@app.route('/send_email', methods=['POST'])
def send_email_route():
	data = request.form
	to_email = data.get('to_email')
	subject = data.get('subject')
	body = data.get('body') 
	attachment_paths = data.get('dirlist') 
	 
	result = send_email(to_email, subject, body, attachment_paths)

	if result is True:
		return jsonify({"status": "success", "message": "Email sent successfully!"})
	else:
		return jsonify({"status": "error", "message": f"Failed to send email. Error: {result}"})

if __name__ == "__main__":
    app.run(debug=True)

