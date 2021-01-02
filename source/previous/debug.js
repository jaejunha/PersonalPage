var http = require('http');
var fs = require('fs');

function onRequest(request, response){
 
	if(request.method == "GET" && request.url == "/"){
		response.writeHead(200, {"Content-Type": "text/html"});
		fs.createReadStream("./index.html").pipe(response);
 
	} else {
		response.writeHead(200, {"Content-Type": "text/html"});
		fs.createReadStream(__dirname+request.url).pipe(response); 
	}
}
 
http.createServer(onRequest).listen(8000);
console.log("Server is working...");