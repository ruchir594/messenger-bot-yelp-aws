from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io
import json
import re
import sys
sys.path.insert(0, './bot')
import natasha_chat
from geotext import GeoText

####################################################################
def getWords(data):
    return re.compile(r"[\w']+").findall(data)

def lambda_handler(event, context):
    c = getWords(event)
    d1 = ['i', 'live', 'in', 'please', 'hi', 'give', 'find', 'what', 'my', 'hungry', 'near', 'me', 'thank', 'you', \
            'want', 'to', 'eat', 'like', 'I', 'can', 'you', 'suggest', 'of', 'is', 'are', 'near', 'there', 'some', \
            'little', 'now', 'wanna', 'want', 'at', 'on', 'in', 'near', 'area', 'next', 'and', 'how', 'about', 'or', \
            'the', 'a', 'an']
    a = ''
    for c_cmall in c:
        if c_cmall not in d1:
            a = a + c_cmall.title() + ' '
        else:
            a = a + c_cmall + ' '
    #print a
    potentiav = GeoText(a)
    b = potentiav.cities
    #print 'b',b
    if b == []:
        g = 'jankiap50@' + natasha_chat.eliza_chat(event) + ' @ I cant find the city from your text, @ please specify both food and city/town/neighbourhood'
        return g
    else:
        d2 = getWords(b[0])
        #print d2
        a = ''
        for c_cmall in c:
            if c_cmall not in d1 and c_cmall not in d2:
                a = a + c_cmall + ' '
        #print a
        #print b[0]
        #return 0
        return api_callee({ 'item': a, 'location': b[0]}, 0)

def api_callee(event, context):
    # read API keys
    with io.open('config_secret.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)

    params = {
        'term': event['item'],
        'lang': 'en',
        'limit': 5
    }

    response = client.search(event['location'], **params)
    placesYelp = ""

    placesYelp = str(response.businesses[0].name) +'@'+ \
                str(response.businesses[0].mobile_url.partition("?")[0]) +'@' + \
                str(response.businesses[0].image_url) +'@' + \
                str(response.businesses[0].rating) +'@' + \
                str(response.businesses[0].display_phone)+'@' + \
                str(response.businesses[1].name)+'@' + \
                str(response.businesses[1].mobile_url.partition("?")[0])+'@' + \
                str(response.businesses[1].image_url) +'@' + \
                str(response.businesses[1].rating)+'@' + \
                str(response.businesses[1].display_phone)+'@' + \
                str(response.businesses[2].name)+'@' + \
                str(response.businesses[2].mobile_url.partition("?")[0])+'@'+ \
                str(response.businesses[2].image_url) +'@' + \
                str(response.businesses[2].rating)+'@' + \
                str(response.businesses[2].display_phone)+'@'

    #return response.businesses[0].name, response.businesses[0].url.partition("?")[0], response.businesses[0].rating, response.businesses[0].display_phone
    #print str(placesYelp)
    return placesYelp
    #print str(response.businesses[0].name)
    #return str(response.businesses[0].name)

#print type(lambda_handler({ 'item': 'blueberry cheesecake', 'location': 'san francisco'}, 0))
#print lambda_handler({ 'item': 'blueberry cheesecake', 'location': 'san francisco'}, 0)
#print lambda_handler("I would like to live in new york city, or in lake forest area.", 0)
lambda_handler(str(sys.argv[1]), 0)
