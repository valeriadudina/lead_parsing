from flask import Flask, request
import json
app = Flask(__name__)
from PipedriveHandler import create_deal, create_person, create_note
from DiscordHandler import send_discord_message
from config import discord_webhook_yelp, discord_webhook_gmd
@app.route('/yelp', methods=['POST'])
def yelp():
    print(request.data.decode('UTF-8'))
    data = json.loads(request.data.decode('UTF-8'))
    #Google my business
    if data.get('from').get('address') == 'googlemybusiness-noreply@google.com':
        source_code = 258
        name = data.get('subject').split('Message from')[1]
        print('name = ', name)
        text = data.get('text').strip()
        respond_link = text.split('Respond')[1].split('Details')[0]
        respond_link_formatted = respond_link[2:len(respond_link) - 4]
        details = text.split('Respond')[1].split('Details')[1].split(
            '*This information has been supplied directly by the customer.')[0]
        print(respond_link_formatted)
        print(details)
        person_id = create_person(name)
        deal_id = create_deal(person_id, source_code, "Google My Business")
        details = details.replace("\n\n", "\n")
        details = details.replace("\n\n\n", "\n")
        create_note(details, respond_link_formatted, deal_id)
        send_discord_message(deal_id, 'Google My Business', discord_webhook_gmd)
    #Yelp
    elif yelp:
        source_code = 257
        text = data.get('text')
        questions_1 = text.split("Hi there, please respond with a price and availability estimate. Here are my answers to Yelp's questions regarding my project:")
        if len(questions_1)==1:
            questions_1 = text.split("Hi there, please respond with a price estimate. Here are my answers to Yelp's questions regarding my project: ")
            print('q2 = ', questions_1)
        questions = questions_1[1].split("[ Respond Now ]")[0]
        questions = questions.split('''
    ---  
    ---  
    |''')[0][3:]
        print(questions)

        respond_link_2 = questions_1[1].split("[ Respond Now ]")
        print('2 = ', respond_link_2)
        respond_link = respond_link_2[1].split("---")[0]
        respond_link = respond_link[1:len(respond_link)-2]
        print(respond_link)
        name = data.get('subject').split('New Message: ')[1].split('is requesting a quote from MAINDUCT INC.')[0]
        print(name)
        person_id = create_person(name)
        deal_id = create_deal(person_id, source_code, "Yelp")
        create_note(questions, respond_link, deal_id)
        send_discord_message(deal_id, 'Yelp', discord_webhook_yelp)
    return('Success!!!')



if __name__=='__main__':
    app.run(port=8000)