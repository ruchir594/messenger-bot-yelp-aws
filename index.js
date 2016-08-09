'use strict';

// Getting started with Facebook Messaging Platform
// https://developers.facebook.com/docs/messenger-platform/quickstart

const express = require('express');
const request = require('superagent');
const bodyParser = require('body-parser');
const https = require('https');

var spawn = require("child_process").spawn;
var PythonShell = require('python-shell');

// Variables
let pageToken = "EAACe5CsbT1oBAAvUT3lphTCAlWMP1wfVZC41k5uHO8LwdtRmgLNq6KrOxJmVxBZCU7Np9LEQOZCk5c9LzedzeJQr1IZBWFuSBxbWxUxwXaylyYxe31vbisHKvygQqkuEsS0h2TodmzCZBF1hjFBYMwRgEIiRCEohHn7d4AKQ5AAZDZD";
const verifyToken = "newtonIsTheGreatestManEverLived";
const privkey = "/etc/letsencrypt/live/yelper.tonatasha.com/privkey.pem";
const cert = "/etc/letsencrypt/live/yelper.tonatasha.com/cert.pem";
const chain = "/etc/letsencrypt/live/yelper.tonatasha.com/chain.pem";

const app = express();
const fs = require('fs');

app.use(bodyParser.json());

app.get('/webhook', (req, res) => {
    if (req.query['hub.verify_token'] === verifyToken) {
        return res.send(req.query['hub.challenge']);
    }
    res.send('Error, wrong validation token');
});
app.post('/webhook', (req, res) => {
    const messagingEvents = req.body.entry[0].messaging;

    messagingEvents.forEach((event) => {
        const sender = event.sender.id;

        if (event.postback) {
            const text = JSON.stringify(event.postback).substring(0, 200);
            sendTextMessage(sender, 'Postback received: ' + text);
        } else if (event.message && event.message.text) {
            const text = event.message.text.trim().substring(0, 200);

                sendTextMessage(sender, 'Text received, so gtfo?: ' + text);
                var options = {
                  mode: 'text',
                  args: [text]
                };
                PythonShell.run("./lambda_function.py" , options,function (err, results) {
                  if (err) throw err;
                  //console.log('result: %j', results);
                  console.log('back in app.js')
                  console.log(results)
                  var results = String(results)
                  var places = results.split("@");
                  //console.log(places)
                  if (places[0] == 'jankiap50') {
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
                  }
                });

        }
    });

    res.sendStatus(200);
});

function sendMessage (sender, message) {
    request
        .post('https://graph.facebook.com/v2.6/me/messages')
        .query({access_token: pageToken})
        .send({
            recipient: {
                id: sender
            },
            message: message
        })
        .end((err, res) => {
            if (err) {
                console.log('Error sending message: ', err);
            } else if (res.body.error) {
                console.log('Error: ', res.body.error);
            }
        });
}

function sendTextMessage (sender, text) {
    sendMessage(sender, {
        text: text
    });
}

function sendGenericMessage (sender, places) {
  var textual0 = places[0].split('^')
  var textual1 = places[1].split('^')
  var textual2 = places[2].split('^')
    sendMessage(sender, {
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
    });
}

app.post('/token', (req, res) => {
    if (req.body.verifyToken === verifyToken) {
        pageToken = req.body.token;
        return res.sendStatus(200);
    }
    res.sendStatus(403);
});
app.get('/token', (req, res) => {
    if (req.body.verifyToken === verifyToken) {
        return res.send({token: pageToken});
    }
    res.sendStatus(403);
});

 https.createServer({
      key: fs.readFileSync(privkey),
      cert: fs.readFileSync(cert),
      ca: fs.readFileSync(chain)
    }, app).listen(3500, function () {
  console.log('App is ready on port 3500');
});
