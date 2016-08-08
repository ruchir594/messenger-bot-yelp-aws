var port = process.env.PORT || 3500,
    http = require('http'),
    fs = require('fs');

var spawn = require("child_process").spawn;
var PythonShell = require('python-shell');
var https = require('https');
var util = require('util');
var PAGE_TOKEN = "EAACe5CsbT1oBAAvUT3lphTCAlWMP1wfVZC41k5uHO8LwdtRmgLNq6KrOxJmVxBZCU7Np9LEQOZCk5c9LzedzeJQr1IZBWFuSBxbWxUxwXaylyYxe31vbisHKvygQqkuEsS0h2TodmzCZBF1hjFBYMwRgEIiRCEohHn7d4AKQ5AAZDZD";
var VERIFY_TOKEN = "newtonIsTheGreatestManEverLived";

    server = https.createServer( function(event, context, callback) {

        console.dir(event.param);

        if (event.method == 'POST') {
            console.log("got POST");
            var body = '';
            event.on('data', function (data) {
                body += data;
                console.log("Partial body: " + body);
            });
            event.on('end', function () {
                var tempostr = body.substring(5, body.length)
                var decode = decodeURI(tempostr)
                console.log("Body: " + decode);
                if (decode != "fuckshit321b0") {
                /*var process = spawn('python',["../kgb.py", body.substring(5, body.length)]);

                process.stdout.on('data', function (data){
                    console.log('back in app.js')
                    console.log(data)
                  });*/
                  var options = {
                    mode: 'text',
                    args: [decodeURI(body.substring(5, body.length))]
                  };
                PythonShell.run("./kgb.py" , options,function (err, results) {
                  if (err) throw err;
                  //console.log('result: %j', results);
                  console.log('back in app.js')
                  console.log(results)
                  var results = String(results)
                  var respon = ""
                  res.writeHead(200, {'Content-Type': 'text/html'});
                  res.end(results);
                }); }
            });
            //res.writeHead(200, {'Content-Type': 'text/html'});
            //res.end('post received ');
        }
        else
        {
            console.log("GET");
            var queryParams = event.params.querystring;

            var rVerifyToken = queryParams['hub.verify_token']

            if (rVerifyToken === VERIFY_TOKEN) {
              var challenge = queryParams['hub.challenge']
              callback(null, parseInt(challenge))
            }else{
              callback(null, 'Error, wrong validation token');
            }
            //var html = '<html><body><form method="post" action="http://localhost:3000">Name: <input type="text" name="name" /><input type="submit" value="Submit" /></form></body>';
            //var html = fs.readFileSync('p1.html');
            //res.writeHead(200, {'Content-Type': 'text/html'});
            //res.end(html);
        }

    });

// Listen on port 3000, IP defaults to 127.0.0.1
server.listen(port);

// Put a friendly message on the terminal
console.log('Server running at ' + port + '/');
