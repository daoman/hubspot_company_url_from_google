import hubspot
import requests
from bs4 import BeautifulSoup
from search_engine_parser import GoogleSearch
from random import randint
from time import sleep
from hubspot import HubSpot
from hubspot.crm.companies import ApiException
from hubspot.crm import contacts, companies, deals
from hubspot.crm.companies import SimplePublicObjectInput, ApiException
from hubspot.crm.associations import (
    BatchInputPublicAssociation,
    PublicAssociation,
    PublicObjectId,
)

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def google2(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)

    soup = BeautifulSoup(r.text, "html.parser")
    return soup.find_all('div', {'class':'g'})[0].find('a')['href']

api_client = HubSpot(api_key='')

all_contacts = api_client.crm.companies.get_all()

mis_contacts = [contact for contact in all_contacts if contact.properties['domain'] == None]

for mis_contact in mis_contacts:
    try:
        properties = {
                    "domain": google2(mis_contact.properties['name']),
            }   
        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        api_client.crm.companies.basic_api.update(company_id=mis_contact.id, simple_public_object_input=simple_public_object_input)
    except ApiException as e:
            print("Exception when requesting contact by id: %s\n" % e)