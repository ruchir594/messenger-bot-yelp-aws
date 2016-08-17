<<<<<<< HEAD
Yelp Bot.
=======
<b>Yelp Bot for Facebook Messenger. </b>
>>>>>>> 49df4abe0cfab9d5dc7c5e90fe684da5628bc7b6

A bot to parse english text in order to generate queries using Yelp API.

Talk to the Bot at https://www.facebook.com/Yelp-Bot-1750022258569181/

Here is a step by step guide.

It uses Amazon AWS EC2 Ubuntu (free tier) instance

Step 1.

follow all the steps from the following. Which will help you set up a basic bot which will echo your responses.

https://github.com/guillaumeteillet/create-your-own-facebook-messenger-bot-platform-ec2-aws

guillaumeteillet has done a great job and it will help you set up your EC2 instance and Messenger Webhook.

Step 2.

make a developer account on Yelp to receive your credentials.

{
    "consumer_key": "",
    "consumer_secret": "",
    "token": "",
    "token_secret": ""
}

Add your credentials into ./config-secret.json

CODE:

There is a fair bit of Python code that goes into understanding natural language. As you will go through the code, you will realize it is more of a smart hack than actually "understanding" the english langauge. But you know what? That hack is exactly what natural laguage processing is all about. There are more rigorous ways to do it, but none more faster.

We have used a JSON file as database. It is pretty awesome eeh.
