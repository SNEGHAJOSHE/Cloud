import imaplib
import email
import requests
import json
import warnings
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
urllib3.disable_warnings(InsecureRequestWarning)
warnings.simplefilter("ignore", InsecureRequestWarning)

# Proxmox server details
proxmox_host = 'https://10.184.53.226:8006'  # Replace with your Proxmox server IP/hostname
api_user = 'test@pam'  # Your API user and realm
api_token_id = 'mytoken'  # Your API token ID
api_token = '1067ea32-17b0-4ce6-8705-7bf177439492'  # Your API token value

# Email account credentials
email_user = "sneghajoseph21@gmail.com"  # Your email address
email_password = "jgct jvdk idhu gvxi"     # Your generated app password
imap_url = "imap.gmail.com"              # Gmail's IMAP server

def connect_email():
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(email_user, email_password)
        return mail
    except imaplib.IMAP4.error as e:
        print(f"Failed to connect to the email server: {e}")
        exit(1)

def fetch_user_requests(mail):
    mail.select("inbox")
    status, response = mail.search(None, 'ALL')
    email_ids = response[0].split()
    email_ids = email_ids[-10:]  # Limit to last 10 emails

    user_requests = []
    
    for num in email_ids:
        try:
            mail.sock.settimeout(5)  # Set a timeout
            status, msg_data = mail.fetch(num, "(RFC822)")
            if status != 'OK':
                print(f"Failed to fetch email ID {num}: {status}")
                continue
            
            msg = email.message_from_bytes(msg_data[0][1])
            subject = msg.get('subject', 'No Subject')
            sender = msg['from']
            user_requests.append((subject, sender))
        
        except Exception as e:
            print(f"Error fetching email ID {num}: {e}")

    return user_requests

def add_user_to_proxmox(new_user, new_password):
    url = f"{proxmox_host}/api2/json/access/users"
    
    headers = {
        "Authorization": f"PVEAPIToken={api_user}!{api_token_id}={api_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "userid": new_user,
        "password": new_password,
        "groups": "Admin"  # Ensure this group exists in Proxmox
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        
        # Check for successful response
        if response.status_code == 200:
            print(f"User {new_user} added successfully!")
        else:
            # Provide more detailed logging
            print(f"Failed to add user {new_user}: {response.status_code}, Response: {response.text}")
            if response.status_code == 500:
                print("Internal Server Error. Please check the Proxmox server logs for more details.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while adding user: {e}")


def process_requests():
    mail = connect_email()
    user_requests = fetch_user_requests(mail)
    
    # Process user requests
    for subject, sender in user_requests:
        print(f"Processing request from {sender}: {subject}")  # Debugging line
        
        if "Add user:" in subject:
            try:
                parts = subject.split(';')
                if len(parts) != 2:
                    print(f"Invalid format for email from {sender}: {subject}")
                    continue
                
                new_user = parts[0].split(':')[1].strip()  # Extract username
                new_password = parts[1].split(':')[1].strip()  # Extract password

                # Call function to add the user to Proxmox
                add_user_to_proxmox(new_user, new_password)

            except IndexError as e:
                print(f"Error processing request from {sender}: Invalid email format.")
            except Exception as e:
                print(f"Error processing request from {sender}: {e}")
        else:
            print(f"Ignoring email from {sender} due to format: {subject}")

    mail.logout()


if __name__ == "__main__":
    process_requests()
