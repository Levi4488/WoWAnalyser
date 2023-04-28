import os
import requests
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

data = {
    'grant_type': 'client_credentials',
}

response = requests.post('https://www.warcraftlogs.com/oauth/token', data=data, auth=(CLIENT_ID, CLIENT_SECRET)).json()

access_token = response['access_token']
