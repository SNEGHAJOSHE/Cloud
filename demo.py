# import requests
# url = "https://10.184.53.226:8006/api2/json/access/users"
# headers = {
#     "Authorization": "PVEAPIToken=root@pam\!mytoken=1067ea32-17b0-4ce6-8705-7bf177439492"
# }
# data = {
#     "userid": "demo@pve",
#     "password": "demo@1234",
#     "groups": "Admin"
# }

# response = requests.post(url, headers=headers, data=data, verify=False)
# print(response.json())


import os
import warnings
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings and capture them
urllib3.disable_warnings(InsecureRequestWarning)
warnings.simplefilter("ignore", InsecureRequestWarning)

# Proxmox server details
proxmox_host = 'https://10.184.53.226:8006'  # Replace with your Proxmox server IP/hostname
api_user = 'test@pam'  # Your API user and realm
api_token_id = 'mytoken'  # Your API token ID
api_token = '1067ea32-17b0-4ce6-8705-7bf177439492'  # Your API token value

# New user details
new_user = 'demo1@pve'  # New username
new_password = 'demo@1234'  # New user's password
new_group = 'Admin'  # Optional: Group for the new user

# Construct the API URL
url = f"{proxmox_host}/api2/json/access/users"

# Set the authorization header
headers = {
    "Authorization": f"PVEAPIToken={api_user}!{api_token_id}={api_token}",
    "Content-Type": "application/json"  # Ensure you're sending data as JSON
}

# Prepare the data for the new user
data = {
    "userid": new_user,
    "password": new_password,
    "groups": new_group
}

try:
    # Make the POST request to add the new user
    response = requests.post(url, headers=headers, json=data, verify=False)

    # Print the status code and response text for debugging
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    # Check if the response is empty
    if not response.text:
        print("Error: The server returned an empty response.")
    else:
        # Try parsing the JSON response
        try:
            json_response = response.json()
            print("JSON Response:", json_response)
        except ValueError:
            print("Error: The response is not valid JSON.")
            print("Raw Response:", response.text)

    # Check for successful response
    if response.status_code == 200:
        print("User added successfully!")
    else:
        print(f"Failed to add user: {response.status_code}, Response: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
