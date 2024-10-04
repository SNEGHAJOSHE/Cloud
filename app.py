from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Admin's email address
admin_email = 'sneghajoseph21@gmail.com'  # Replace with the admin's actual email

# Email configuration (SMTP settings for Gmail)
SMTP_SERVER = "smtp.gmail.com"  # SMTP server (Gmail in this case)
SMTP_PORT = 587  # SMTP port for TLS
EMAIL_USER = "sneghajoseph21@gmail.com"  # Your email address
EMAIL_PASS = "jgct jvdk idhu gvxi"  # Your email password or app-specific password
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        try:
            # Create the email message
            subject = f"Add user: {username}; password: {password}"
            body = "A new user request has been submitted. Please review and add the user to the system."

            # Construct the email
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = admin_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            # Connect to the email server and send the email
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, admin_email, msg.as_string())
            server.quit()

            return jsonify({"message": "Email sent to admin successfully!"}), 200

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"message": "Failed to send email."}), 500
    else:
        return jsonify({"message": "Invalid data provided!"}), 400

if __name__ == '__main__':
    app.run(debug=True) 