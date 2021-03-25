const http = require("http");
const url = require("url");
const path = require("path");
const fs = require("fs");

function requestHandler(request, response)
{
    let rootDirectory = "/web_server/root";
    // Replace deprecated function
    let requestUri = rootDirectory + url.parse(request.url).pathname;
    console.log(requestUri);
    let filename = path.join(process.cwd(), requestUri);
    console.log(process.cwd())

    function contentHandler(error, stats)
    {
        if (error)
        {
            // Write proper 404 response
            response.writeHead(404, {"Content-Type": "text/plain"});
            response.write("404 Not found! Error code: " + error.code + "\n");
            response.end();
        }
        else
        {
            if (stats.isDirectory())
            {
                filename += "index.html";
            }
            function fileHandler(error, file)
            {
                if (error)
                {
                    response.writeHead(500, {"Content-Type": "text/plain"});
                    response.write("Error code: " + error.code + "\n");
                    response.end();
                }
                else
                {
                    let contentTypesByExtension =
                    {
                        '.html': "text/html",
                        '.css':  "text/css",
                        '.js':   "text/javascript",
                        ".jpeg": "image/jpeg",
                        ".png": "image/png"
                    };
                    let content_type = contentTypesByExtension[path.extname(filename)];
                    response.writeHead(200, {"Content-Type": content_type});
                    response.write(file, "binary");
                    response.end();
                }
            }
            fs.readFile(filename, "binary", fileHandler);
        }
    }

    fs.stat(filename, contentHandler);
}
let port = 8080
const server = http.createServer(requestHandler);
server.listen(port);
console.log("Server listening on port " + port)