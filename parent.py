from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io
import json

# read API keys
with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

params = {
    'term': 'Blueberry Cheese Cake',
    'lang': 'en',
    'limit': 5
}

response = client.search('San Francisco', **params)

print response.businesses[0].name
print response.businesses[0].url.partition("?")[0]
print response.businesses[0].rating
print response.businesses[0].display_phone
print " "
print response.businesses[1].name
print response.businesses[1].url.partition("?")[0]
print response.businesses[1].rating
print response.businesses[1].display_phone
