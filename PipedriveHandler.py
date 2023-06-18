from config import API_KEY, PIPEDRIVE_URL
import requests
import json

def search_deal_existing_person(person_id):
    url = f"{PIPEDRIVE_URL}v1/persons/{person_id}/deals?api_token={API_KEY}"
    headers = {
        'Accept': 'application/json',
        'Cookie': '__cf_bm=SEBhuUQkyFS_4i1k5d20sxWc06FekEgoHHb.Di92S9w-1661292457-0-AfuRx7KUzO5rTfMojjvboBVfRfvmfnB8+LcRMABvJzhFA8DMHCQ+g17828zqambI33ilEAZ9UG2UK45f+ZTwZks='
    }
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)

def create_deal(person_id, source_code, deal_from):
    url = f"{PIPEDRIVE_URL}v1/deals?api_token={API_KEY}"

    payload = json.dumps({
        "title": f"New deal from {deal_from}",
        "person_id": person_id,
        "pipeline_id": 1,
        "stage_id": 2,
        "ee5381ef93a3eb81a405bbdcc03b08408bdc4d76": source_code
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return json.loads(response.text).get('data').get('id')

def get_deal_id(person_id):
    search_deal = search_deal_existing_person(person_id)
    if search_deal.get('data'):
        return search_deal.get('data')[0].get('id')
    else:
        create = create_deal(person_id)
        return create.get('data').get('id')


def search_item(item):

    url = f"{PIPEDRIVE_URL}v1/persons/search?term={item}&api_token={API_KEY}"
    response = requests.request("GET", url)
    print(response.text)
    return response.text

def search_person(email):

    if email:
        resp=json.loads(search_item(email))
        print("resp  = ", resp.get('data'))
        if resp.get('data').get('items')!=[] and resp.get('data').get('items')!=[] and resp.get('data').get('items')!=None :
            return resp.get('data').get('items')[0].get('item').get('id')

    return 'not found'


def set_address_area(address, area, person_id):
    url = f"{PIPEDRIVE_URL}v1/persons/{person_id}?api_token={API_KEY}"

    payload = json.dumps({
        "4377527eea25024cbf4ee5b5ffcba244fe0f5921": address,
        "da4443addaa862771a853d8d261bf0c7b2b26331": area
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cookie': '__cf_bm=EU8RgV2SqWNhOROwjY9T1BpGNKVWtL5h.wxollBGFwo-1661287360-0-AT6w90hAsdw9SW+qiODlqtxNeMtXMV+T4BUMxFY1UajnI/hLcmYfSzbudPqt5JI2RK5B9hmLzzjjq/4Mdrjqu2s='
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    return response.text

def create_person(name):
    url = f"{PIPEDRIVE_URL}v1/persons?api_token={API_KEY}"
    payload = {
  "name": name
}
    #print('create person data = ', payload)
    response = requests.request("POST", url, data=payload)
    print("create_person_ ",response.text)
    return json.loads(response.text).get('data').get('id')


def get_person_id(data):
    search = search_person(data.get('email'), data.get('primaryPhone'), data.get('secondaryPhone'))
    print("search = ", search)
    if search == 'not found':
        person_id = create_person(data)
        set_address_area(data.get('address'), data.get('stateProvince'), person_id)
        print(person_id)
        return person_id
    else:
        return search


def create_note(questions,respond_link, deal_id):

    url = f'{PIPEDRIVE_URL}v1/notes?api_token={API_KEY}'
    payload = {
        "content":questions+"\n"+respond_link,
        "deal_id": deal_id

    }
    response = requests.request("POST", url, data=payload)
    print(response.text)
