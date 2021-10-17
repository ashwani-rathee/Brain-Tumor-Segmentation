const express = require('express')
const app = express()
// set the port of our application
// process.env.PORT lets the port be set by Heroku
var port = process.env.PORT || 3000;
var multipart = require('connect-multiparty');
var multipartMiddleware = multipart();
const bodyParser = require("body-parser");

var potrace = require('potrace'),
fs = require('fs');
 
//Here we are configuring express to use body-parser as middle-ware.
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

var trace = new potrace.Potrace();
app.post('/tosvg', multipartMiddleware, function(request, response) {
    trace.loadImage(request.files["file"]["path"], function(err) {
      if (err) throw err;
      console.log(trace.getPathTag()); // will return just <path> tag
      response.json({"output": trace.getPathTag()});
    });
    
  })

app.listen(port, function() {
	console.log('Our app is running on http://localhost:' + port);
});