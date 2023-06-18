import requests
from config import discord_webhook
from config import  PIPEDRIVE_URL
def send_discord_message(deal_id, source):

    payload = {'content' : f'New lead from {source}\n\n {PIPEDRIVE_URL}deal/{deal_id}'}
    response = requests.request("POST", discord_webhook,  data=payload)
    print(response.text)