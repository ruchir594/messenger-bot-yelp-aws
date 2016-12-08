from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io
import json
import re
import sys
import urllib
import six
sys.path.insert(0, './bot')
import natasha_chat
from geotext import GeoText
from crf_location import crf_exec
from natasha_chat import eliza_chat
from ssvwo import prod

##############################################################################
# --- userful functions
##############################################################################
def getWords(data):
    return re.compile(r"[\w']+").findall(data)

def getWords_special_location(data):
    return re.compile(r"[\w'/.,-@]+").findall(data)
##############################################################################
# ---- JSON Database lib functions
##############################################################################
def oldner(event, userid):
    with open('data.json', 'r') as f:
         data = json.load(f)
    flag = False
    for i in data["people"]:
        if i["userid"] == userid:
            #i["count"] = i["count"] + 1
            flag = True
            with open('data.json', 'w') as f:
                 json.dump(data, f)
            return i
    if flag == False:
        killbill = {
              "userid": userid,
              "location":"",
              "food":"",
              "generated":"False",
              "flag":"",
              "count":0,
              "text":"first time event"
              }
        data["people"].append(killbill)
        with open('data.json', 'w') as f:
             json.dump(data, f)
        return killbill

    #print len(data['people'])
    # Writing JSON data
def updatejson(person):
    with open('data.json', 'r') as f:
         data = json.load(f)
    for i in data['people']:
        if i['userid'] == person['userid']:
            i['location'] = person['location']
            i['text'] = person['text']
            i['count'] = i['count'] + 1
            break
    with open('data.json', 'w') as f:
         json.dump(data, f)
##############################################################################
# ---- the main function
##############################################################################
def lambda_handler(event, userid, context):
    # Reading data back
    person = oldner(event, userid)
    c = getWords(event)
    lust = getWords_special_location(event)
    #print (lust)
    d1 = ['i', 'live', 'in', 'please', 'hi', 'give', 'find', 'who', 'what', 'my', 'hungry', 'near', 'me', 'thank', 'you', \
            'want', 'to', 'eat', 'like','liked', 'I', 'can', 'you', 'suggest', 'of', 'is', 'are', 'near', 'there', 'some', \
            'little', 'now', 'wanna', 'want', 'at', 'on', 'in', 'near', 'area', 'next', 'and', 'how', 'about', 'or', \
            'the', 'a', 'an', 'about', 'for', 'with', 'should', 'could', 'would', 'out','time','person','year','way','day',\
            'thing','man','world','life','hand','part','child','eye','woman','place','work','week', 'doing',\
            'case','point','government','company','number','group','problem','fact','be','have','do','say',\
            'get','make','go','know','take','see','come','think','look','give','use','find','tell', 'telling',\
            'ask','work','seem','feel','try','leave','call','good','new','first','last','long','great','little','own','other',\
            'old','right','big','high','different','small','large','next','early','young','important','few',\
            'public','bad','same','able','to','of','in','for','on','with','at','by','from','up','about','into',\
            'over','after','beneath','under','above','the','and','a','that','I','it','not','he','as','you', \
            'this','but','his','they','her','she','or','an','will','my','one','all','would','there','their', 'talk', \
            'talking', 'love', 'loved', 'hello', 'help', 'helping', 'helped', 'pleasure', 'bye', 'goodbye', 'care', 'later', \
            'no','nothing', 'thanks', 'welcome', 'something', 'hey', 'am', 'me', 'need', 'bot', 'droid', 'ai', 'smart', 'super',\
            'moron', 'dumb', 'fuck', 'fucking', 'sex', 'indeed', 'sure', 'enough', 'man', 'show', 'showing', 'then', 'than',\
            'ok', 'okay', 'alright', 'cool', 'dude', 'lady', 'girl']
    #d1 = []
    kiss = ''
    bang = ''
    bump_last = ['.', ',', ';', ':', '(', ')', '?', '!']
    for c_cmall in lust:
        if c_cmall[-1] not in bump_last:
            if c_cmall not in d1:
                kiss = kiss + c_cmall.title() + ' '
                bang = bang + c_cmall.title() + ' '
            else:
                kiss = kiss + c_cmall + ' '
                bang = bang + c_cmall + ' '
        else:
            if c_cmall not in d1:
                kiss = kiss + c_cmall[:-1].title() + ' '
                bang = bang + c_cmall[:-1].title() + ' ' + c_cmall[-1] + ' '
            else:
                kiss = kiss + c_cmall[:-1] + ' '
                bang = bang + c_cmall[:-1] + ' ' + c_cmall[-1] + ' '
    ##############################################################################
    # --- find cities from python open source lib
    #################################################################################
    c = getWords_special_location(event)
    a = ''
    for c_cmall in c:
        if c_cmall not in d1:
            a = a + c_cmall.title() + ' '
        else:
            a = a + c_cmall + ' '
    #print a
    potentiav = GeoText(a)
    b1 = potentiav.cities
    ##############################################################################
    # ----- use CRF for NER
    #################################################################################
    a = crf_exec(bang, 0)
    i=0
    data_ayrton=[]
    b=[]
    drop_char = ['.', ',', ';']
    for i in a:
        if i[0][-1] in drop_char:
            j = i[0][:-1]
        else:
            j = i[0]
        data_ayrton.append([str(j), str(i[1]), str(i[2]), str(i[3])])
    c = data_ayrton
    ##############################################################################
    # --- find location from CRF -----
    ##############################################################################
    data_ayrton = []
    i=0
    p_loc = ''
    p_loc_ref = []
    for atom in c:
        if atom[2][-3:] == 'LOC' and atom[0] not in p_loc_ref:
            p_loc = p_loc + atom[0] + ' '
            p_loc_ref.append(atom[0])
            data_ayrton.append(p_loc)
            p_loc = ''
        i = i + 1
            #p_loc_ref = []
    j=''
    for i in data_ayrton:
        j = j + i
    j=j.replace(' ','')
    k=''
    for i in b1:
        k = k + i
    k=k.replace(' ','')
    if j!=k:
        data_ayrton = data_ayrton + b1
    #print data_ayrton
    b = []
    j = ''
    for i in data_ayrton:
        j = j + i + ' '
    b = j
    #print b
    #return
    #############################################################################
    # checking if something important is found in here
    a = ''
    c = getWords(event)
    for c_cmall in c:
        if c_cmall.lower() not in d1:
            a = a + c_cmall + ' '
    if a == '':
        #######
        ####### ---- calling ssv-wo.py
        #######
        similarity = prod(person['text'], event.lower())
        #print person['text'], event.lower(), similarity
        person['text'] = event.lower()
        updatejson(person)
        if similarity > 0.8:
            print 'jankiap50@ ' + eliza_chat('similarityhigh')
            return
        if similarity > 0.55:
            print 'jankiap50@ ' + eliza_chat('similaritycall')
            return
        event = event.lower()
        print 'jankiap50@ ' + eliza_chat(event)
        return
    # we remember their location.
    # The very first thing the bot does is that it will keep asking you about
    # the location until it is satisfied
    ##############################################################################
    # ------- location of USER
    ##############################################################################
    if b == '' and person["location"] == "":
        a = 'jankiap50@ Hmmm.... If you tell me your city, i can help you find food.'
        print a
        return
    else:
        c = getWords(event)
        flag = False
        # ----- flag_city_this remembers if we got location from this incoming text
        # ----- or from JSONDB
        # we receive location from JSON Database of USER
        if b == '':
            flag = True
            b = person["location"]
            flag_city_this = False
        # The location is found using NER which is a CRF model
        # and the JSON is updated
        else:
            person["location"] = b
            flag_city_this = True
            updatejson(person)
        ##############################################################################
        # ----- see if he wants to eat some food
        ##############################################################################
        d2 = getWords(b)
        for i in range(len(d2)):
            d2[i] = d2[i].lower()
        #print d2
        # the variable "a" will store what he may want to eat
        a = ''
        for c_cmall in c:
            if c_cmall.lower() not in d1 and c_cmall.lower() not in d2:
                a = a + c_cmall + ' '
        #print 'a ', a
        #print len(a), type(a)
        ##############################################################################
        if a == '' and flag_city_this == True:
            print 'jankiap50@ I think your location is ' + b + ' . What are you looking for?'
            return
        elif a == '' and flag_city_this == False:
            event = event.lower()
            print 'jankiap50@ ' + eliza_chat(event)
            #print 'SIMPLE NLG MODULE'
            return
        else:
            a = api_callee({ 'item': a, 'location': b}, 0)
        if a == 'jankiap50':
            print 'jankiap50@ Aha!, I can only help you find food. I searched at location: ' + b
            return
        elif a == 'jankiap50_error_yelp':
            print 'jankiap50@ Yelp! is unavailable in your location ' + b
            return
        else:
            if flag == True:
                a = a + "I remember you were looking for food in " + b + " @ @ @ @ @"
            else:
                a = a + " @ @ @ @ @"
            print a.encode('ascii', 'ignore')
            return
##############################################################################
# ----- Calling YELP API ----
##############################################################################
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

    #print event['item']
    #print event['location']
    response = client.search(event['location'], **params)
    #print response
    placesYelp = ""
    #print response.businesses[0]
    if response.businesses == None:
        placesYelp = 'jankiap50_error_yelp'
    elif len(response.businesses) == 0:
        placesYelp = 'jankiap50'
    else:
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
                    str(response.businesses[2].display_phone)+'@' + \
                    str(response.businesses[3].name)+'@' + \
                    str(response.businesses[3].mobile_url.partition("?")[0])+'@' + \
                    str(response.businesses[3].image_url) +'@' + \
                    str(response.businesses[3].rating)+'@' + \
                    str(response.businesses[3].display_phone)+'@' + \
                    str(response.businesses[4].name)+'@' + \
                    str(response.businesses[4].mobile_url.partition("?")[0])+'@'+ \
                    str(response.businesses[4].image_url) +'@' + \
                    str(response.businesses[4].rating)+'@' + \
                    str(response.businesses[4].display_phone)+'@'

    #return response.businesses[0].name, response.businesses[0].url.partition("?")[0], response.businesses[0].rating, response.businesses[0].display_phone
    #print str(placesYelp)
    result=placesYelp.encode('ascii', 'ignore')
    return result

#print type(lambda_handler({ 'item': 'blueberry cheesecake', 'location': 'san francisco'}, 0))
#print lambda_handler("I would like to live in new york city, or in lake forest area.", 0)
jdblove = urllib.unquote_plus(urllib.unquote_plus(str(sys.argv[1])))
lambda_handler(str(jdblove), sys.argv[2], 0)
