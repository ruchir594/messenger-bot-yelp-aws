'use strict';
var https = require('https');
var util = require('util');
var PAGE_TOKEN = "EAAD9yzla62gBAAf3dnLhVd0z3O8lEa1HM5g4uEZAVpFfX3sri84QFZC3G86qIZBCG1gbC7CXy8LHkzRehOCF3UauGRWv2ZCy5ZB0qKioDnDZAsAd27jlw9rRcsAA57TkvZBSrc8rXE1JtBqcnvUJZCZBALjZCz4utfprbiLt6wy2YTqgZDZD";
//var PAGE_TOKEN = "EAACe5CsbT1oBAAvUT3lphTCAlWMP1wfVZC41k5uHO8LwdtRmgLNq6KrOxJmVxBZCU7Np9LEQOZCk5c9LzedzeJQr1IZBWFuSBxbWxUxwXaylyYxe31vbisHKvygQqkuEsS0h2TodmzCZBF1hjFBYMwRgEIiRCEohHn7d4AKQ5AAZDZD";
var VERIFY_TOKEN = "newtonIsTheGreatestManEverLived";

var aws = require('aws-sdk');
var lambda = new aws.Lambda({
  region: 'us-west-2' //change to your region
});

exports.handler = (event, context, callback) => {
  // process GET request
  if(event.params && event.params.querystring){
    var queryParams = event.params.querystring;

    var rVerifyToken = queryParams['hub.verify_token']

    if (rVerifyToken === VERIFY_TOKEN) {
      var challenge = queryParams['hub.challenge']
      callback(null, parseInt(challenge))
    }else{
      callback(null, 'Error, wrong validation token');
    }

  // process POST request
  }else{

    var messagingEvents = event.entry[0].messaging;
    for (var i = 0; i < messagingEvents.length; i++) {
      var messagingEvent = messagingEvents[i];

      var sender = messagingEvent.sender.id;
      if (messagingEvent.message && messagingEvent.message.text) {
        var text = messagingEvent.message.text;
        console.log("Receive a message: " + text);
        //sendTextMessage(sender, "you sent this: "+text);
        //var playwith = text.split("\n");
        //sendTextMessage(sender, "so you want to eat "+playwith[0]+" at "+playwith[1]);

        //if (typeof(playwith[1]) != typeof("hello")) {
        //    sendTextMessage(sender, "I can't tell where exactly you are, help me by using following until I get smarter... \n\n<What you want to eat>\n<Beautiful city/town/neighbourhood you are in>\n for example \n\nThai Food\nDartmouth College, Hanover");
        //    playwith[1]="san francisco";
        //    continue;
        //}
        /////////////////////////////////////////////////////////////////////////////////////////

                var d1 = [];
                d1.push('i', 'live', 'in', 'please', 'hi', 'give', 'find', 'who', 'what', 'my', 'hungry', 'near', 'me', 'thank', 'you');
                d1.push('want', 'to', 'eat', 'like','liked', 'I', 'can', 'you', 'suggest', 'of', 'is', 'are', 'near', 'there', 'some');
                d1.push('little', 'now', 'wanna', 'want', 'at', 'on', 'in', 'near', 'area', 'next', 'and', 'how', 'about', 'or');
                d1.push('the', 'a', 'an', 'about', 'for', 'with', 'should', 'could', 'would', 'out','time','person','year','way','day');
                d1.push('thing','man','world','life','hand','part','child','eye','woman','place','work','week', 'doing');
                d1.push('case','point','government','company','number','group','problem','fact','be','have','do','say');
                d1.push('get','make','go','know','take','see','come','think','look','want','give','use','find','tell', 'telling');
                d1.push('ask','work','seem','feel','try','leave','call','good','new','first','last','long','great','little','own','other');
                d1.push('old','right','big','high','different','small','large','next','early','young','important','few');
                d1.push('public','bad','same','able','to','of','in','for','on','with','at','by','from','up','about','into');
                d1.push('over','after','beneath','under','above','the','and','a','that','I','it','not','he','as','you');
                d1.push('this','but','his','they','her','she','or','an','will','my','one','all','would','there','their', 'talk');
                d1.push('talking', 'love', 'loved', 'hello', 'help', 'helping', 'helped', 'pleasure', 'bye', 'goodbye', 'care', 'later');
                d1.push('no','nothing', 'thanks', 'welcome', 'something', 'smart', 'dumb', 'poor', 'am', 'hey');

                var text2 = text.replace(/\?/g,'');
                text2 = text2.replace(/!/g,'');
                text2 = text2.replace(/\./g,'');
                text2 = text2.replace(/,/g,'');
                text2 = text2.replace(/:/g,'');

                console.log("Receive a message2: " + text2);

                var words_text = text2.split(' ');

                var i = 0
                var flag = false
                var hasher = -1
                while(i<words_text.length){
                  hasher = d1.indexOf(words_text[i].toLowerCase())
                  if(hasher == -1){
                    flag = true
                    console.log("Flag true on: " + words_text[i]);
                  }
                  i = i + 1
                }
                if(flag == false){

                  if(words_text[0].toLowerCase() == 'hi' || words_text[0].toLowerCase() == 'hello'){
                    sendTextMessage(sender, "Hello, I am Natasha.")
                  }
                  else if(words_text[0].toLowerCase() == 'who'){
                    sendTextMessage(sender, "Hi there, My name is Natasha and I am a smart AI.")
                  }
                  else if(words_text[0].toLowerCase() == 'what'){
                    sendTextMessage(sender, "I am smart bot that uses Yelp API to help you find food in your area. Please tell me your city and what you want to eat. I will soon be smarter than I am, please come back in a week.")
                    sendTextMessage(sender, "Meanwhile, please please like my page.")
                  }
                  else if(words_text[0].toLowerCase() == 'how'){
                    sendTextMessage(sender, "Let's just say I am smart...")
                    sendTextMessage(sender, "Meanwhile, please please like my page.")
                  }
                  else if(words_text[0].toLowerCase() == 'goodbye' || words_text.indexOf('bye') != -1){
                    sendTextMessage(sender, "Bye, thank you for dropping by.")
                    sendTextMessage(sender, "Meanwhile, please please like my page.")
                  }
                  else if(words_text[0].toLowerCase() == 'thank' || words_text[0].toLowerCase() == 'thanks'){
                    sendTextMessage(sender, "You are welcome.")
                    sendTextMessage(sender, "Meanwhile, please please like my page.")
                  }
                  else if(words_text[0].toLowerCase() == 'you'){
                    sendTextMessage(sender, "Well, you have strong opinions about me.")
                    sendTextMessage(sender, "Meanwhile, please please like my page.")
                  }
                  else if(words_text[0].toLowerCase() == 'i' && words_text[1].toLowerCase() == 'want'){
                    sendTextMessage(sender, "I cannot tell what you want, please be more specific and give me your location as well.  I will soon be smarter than I am, please come back in a week.")
                  }
                  else if(words_text[0].toLowerCase() == 'i' && words_text[1].toLowerCase() == 'am'){
                    sendTextMessage(sender, "Sure, you are!")
                    sendTextMessage(sender, "Meanwhile, please please like my page.")
                  }
                  else if(words_text[0].toLowerCase() == 'i'){
                    sendTextMessage(sender, "Okay, maybe!")
                  }
                  else {
                    sendTextMessage(sender, "I am just front end Yelp API integration, I am not allowed to do anything else. Give me the food you want and city/town you are in. I will soon be smarter than I am, please come back in a week. I just got a but smarter. ")
                    sendTextMessage(sender, "Meanwhile, please please like my page.")
                  }

                  //sendTextMessage(sender, "Nothing to Process...")


                } else { //else zero begin
                  sendTextMessage(sender, "processing...")
                  /////////////////////////////////////////////////////////////////////////

            var params = {
                FunctionName: 'makeYelpApi', // the lambda function we are going to invoke
                InvocationType: 'RequestResponse',
                LogType: 'Tail',
                Payload: '"' + text + '"'
            };

            // the following lambda function invokes the makeYelpApi
            // which is a python code which uses Official Yelp API
            // to get food in 53 countries

            lambda.invoke(params, function(err, data) {
                if (err) {
                context.fail(err);
                console.log(err);
                //sendTextMessage(sender, err);
                } else {

                var str = data.Payload
                //console.log(data.Payload);
                //console.log(typeof(data.Payload));
                var places = str.split("@");
                //console.log(places)
                if (places[0] == '"jankiap50') {
                    sendTextMessage(sender, places[1]);
                    sendTextMessage(sender, "sorry, but i will soon be a lot smarter. Please come back in a week. Meanwhile, please please like the page.")
                    //sendTextMessage(sender, places[2]);
                    //sendTextMessage(sender, places[3])
                }
                else {


                var aplace = [];
                var aplacea="";
                var i = 0;
                var increment = 5;
                while (i < places.length){
                    //aplacea = places[i]+"\n"+places[i+1]+"\n"+places[i+3]+"\n"+places[i+4];
                    aplace.push(places[i]+"^"+places[i+1]+"^"+places[i+2]+"^"+places[i+3]+"^"+places[i+4]);
                    if (typeof(places[i+1]) == typeof("hello")){
                    //sendTextMessage(sender, aplacea);
                    i=i+increment;
                    }
                    else {
                    i=i+increment;
                    }
                }
                sendGenericMessage(sender, aplace);
                //sendYelpPower(sender);
                }
                }
                console.log(data);
            });

      } //Else Zero ends


        callback(null, "Done");
      }
    }

    callback(null, event);
  }
};
//////////////////////////////////////////////////////////////////////////////////
function sendTextMessage(senderFbId, text) {
  var json = {
    recipient: {id: senderFbId},
    message: {text: text},
  };
  var body = JSON.stringify(json);
  var path = '/v2.6/me/messages?access_token=' + PAGE_TOKEN;
  var options = {
    host: "graph.facebook.com",
    path: path,
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
  };
  var callback = function(response) {
    var str = ''
    response.on('data', function (chunk) {
      str += chunk;
    });
    response.on('end', function () {

    });
  }
  var req = https.request(options, callback);
  req.on('error', function(e) {
    console.log('problem with request: '+ e);
  });

  req.write(body);
  req.end();
}
////////////////////////////////////////////////////////////////////////////////////
function sendGenericMessage(recipientId, places) {
  var textual0 = places[0].split('^')
  var textual1 = places[1].split('^')
  var textual2 = places[2].split('^')
  //var textual9 = places[9].split('^')
  //console.log(typeof(textual0), typeof(textual0[1]), textual0[1])
  var messageData = {
    recipient: {
      id: recipientId
    },
    message: {
      attachment: {
        type: "template",
        payload: {
          template_type: "generic",
          elements: [{
            title: textual0[0],
            subtitle: textual0[3] + textual0[4],
            item_url: textual0[1],
            image_url: textual0[2],
            buttons: [{
              type: "web_url",
              url: textual0[1],
              title: "Open in Yelp"
            }],
          }, {
            title: textual1[0],
            subtitle: textual1[3] + textual1[4],
            item_url: textual1[1],
            image_url: textual1[2],
            buttons: [{
              type: "web_url",
              url: textual2[1],
              title: "Open in Yelp"
            }],
          },{
            title: textual2[0],
            subtitle: textual2[3] + textual2[4],
            item_url: textual2[1],
            image_url: textual2[2],
            buttons: [{
              type: "web_url",
              url: textual2[1],
              title: "Open in Yelp"
            }],
          },{
            title: "Powered by yelp",
            subtitle: "Powered by http://tonatasha.com",
            item_url: "http://tonatasha.com",
            image_url: "http://tonatasha.com/img/yelp/bigbutton.png",
            buttons: [{
              type: "web_url",
              url: "http://tonatasha.com",
              title: "Go to Natasha"
            }],
          }]
        }
      }
    }
  };

  var body = JSON.stringify(messageData);
  var path = '/v2.6/me/messages?access_token=' + PAGE_TOKEN;
  var options = {
    host: "graph.facebook.com",
    path: path,
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
  };
  var callback = function(response) {
    var str = ''
    response.on('data', function (chunk) {
      str += chunk;
    });
    response.on('end', function () {

    });
  }
  var req = https.request(options, callback);
  req.on('error', function(e) {
    console.log('problem with request: '+ e);
  });

  req.write(body);
  req.end();
}
///////////////////////////////////////////////////////////////////////////////////
function sendYelpPower(senderFbId) {
    var m1="image"
    var m2="http://tonatasha.com/img/yelp/bigbutton.png"
  var json = {
    recipient: {id: senderFbId},
    message: {
        attachment:{
                    type: m1,
                    payload: {
                        url: m2
                    }
        }
    }
  };
  //var body = "{recipient: {id:}"+String(senderFbId)+", message: {text:"+String(text)+"}}"
  //attachment:{type:'image', payload:{url:'http://tonatasha.com/img/yelp/yelp_powered_btn_red.png'}}},
  var body = JSON.stringify(json);
  var path = '/v2.6/me/messages?access_token=' + PAGE_TOKEN;
  var options = {
    host: "graph.facebook.com",
    path: path,
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
  };
  var callback = function(response) {
    var str = '';
    response.on('data', function (chunk) {
      str += chunk;
    });
    response.on('end', function () {

    });
  }
  var req = https.request(options, callback);
  req.on('error', function(e) {
    console.log('problem with request: '+ e);
  });

  req.write(body);
  req.end();
}
