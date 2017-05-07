#!/usr/bin/env python3

"""

Simple Web Server for communicating with MagnusFlora modules

"""

import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

import http.server
import http.client
import cgi
import subprocess
import json

# Magnus Flora Server Handler
class MagnusFloraHandler(http.server.BaseHTTPRequestHandler):

    # For now, hard code
    PORTS = {
        "tecthulu": {
            "host": "localhost",
            "port": 5050,
            "ops": {
                "hello": { "type": "GET", "url": "/" },
                "delay": { "type": "GET", "url": "/delay" },
                "faction": { "type": "GET", "url": "/status/faction" },
                "health": { "type": "GET", "url": "/status/health" },
                "status": { "type": "GET", "url": "/status/json" }
            }
        },
        "sound": {
            "host": "localhost",
            "port": 2003,
            "ops": {
                "hello": { "type": "GET", "url": "/" },
                "health": { "type": "GET", "url": "/health" },
                "portal": { "type": "POST", "url": "/portal" }
            }
        },
        "led": {
            "host": "localhost",
            "port": 2001,
            "ops": {
                "hello": { "type": "GET", "url": "/" },
                "health": { "type": "GET", "url": "/health" },
                "portal": { "type": "POST", "url": "/portal" }
            }
        },
        "servo": {
            "host": "localhost",
            "port": 2004,
            "ops": {
                "hello": { "type": "GET", "url": "/" },
                "health": { "type": "GET", "url": "/health" },
                "portal": { "type": "POST", "url": "/portal" }
            }
        },
        "jarvis": {
            "host": "localhost",
            "port": 2005,
            "ops": {
                "hello": { "type": "GET", "url": "/" },
                "health": { "type": "GET", "url": "/health" },
                "status": { "type": "GET", "url": "/status/json" }
            }
        }
    }

    DOC_ROOT = "/home/pi/MagnusFlora/web/DocRoot"
    SNAPSHOT = "/home/pi/MagnusFlora/web/current_snapshot"

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("doing GET")

        self.send_file()


    def do_POST(self):
        print("doing POST - ", self.path)

        if self.path.startswith("/MagnusFlora/"):
            api_objs = self.path.split('/')    
            module = api_objs[2]
            operation = api_objs[3]

            print("module = ", module)
            print("operation = ", operation)

            try:
                jsonStr = self.parse_POST()
                print("request jsonStr = ", jsonStr)
                status, response = self.processRequest(module, operation, jsonStr)
            except:
                response = {}
                status = "Error"

            jsonStr = json.dumps({'status':status,'response':response})
            print("response jsonStr = ", jsonStr)

            self._set_headers()
            self.wfile.write(jsonStr.encode("utf-8"))
        else:
            self.send_response(404)

    def parse_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        data = '{}'

        if ctype == "multipart/form-data":
            postvars = cgi.parse_multipart(self.rfile, pdict)
            if 'request' in postvars:
                data = postvars['request'][0].decode("utf-8")
        elif ctype == "application/x-www-form-urlencoded":
            length = int(self.headers['Content-Length'])
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            if 'request' in postvars:
                data = postvars['request'][0].decode("utf-8")
        elif ctype == "application/json":
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length).decode("utf-8")

        return data

    def send_file(self):
        if self.path == "" or self.path == "/":
            self.path = "/index.html"

        full_path = self.DOC_ROOT + self.path

        print(full_path)

        try: 
            with open(full_path, "rb") as f:
                self.send_response(200)
                self.send_header("Content-Type", self.getContentType(self.path))
                self.end_headers()
                self.wfile.write(f.read())
        except IOError:
            self.send_response(404)

    def processRequest(self, module, operation, request):
        vars = json.loads(request)
        status = "Error"
        data = {}

        try:
            if module in self.PORTS:
                host = self.PORTS[module]["host"]
                port = self.PORTS[module]["port"]
                if operation in self.PORTS[module]["ops"]:
                    type = self.PORTS[module]["ops"][operation]["type"]
                    url = self.PORTS[module]["ops"][operation]["url"]

                    data = self.sendCommand(host, port, url, type, request)
                    status = "OK"
        except:
            data = {}
            status = "Error"

        return status, data

    def sendCommand(self, host, port, url, type, request):
        data = {}

        print("sendCommand: " + type + " http://" + host + ":" + str(port) + url + " - " + request)

        try:
            httpServ = http.client.HTTPConnection(host, port)
            httpServ.connect()

            httpServ.request(type, url, request)
            response = httpServ.getresponse()
            val = response.read().decode("utf-8")

            print("Response = ", val)
            try:
                data = json.loads(val)
            except:
                data = json.loads('"' + val + '"')
        finally:
            httpServ.close()

        return data

    def getContentType(self, path):
        if path.endswith(".jpeg"):
            return "img/jpeg"
        elif path.endswith(".png"):
            return "img/png"
        elif path.endswith(".gif"):
            return "img/gif"
        elif path.endswith(".js"):
            return "text/javascript"
        elif path.endswith(".html"):
            return "text/html"
        elif path.endswith(".css"):
            return "text/css"

        return "text/plain"

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', 9000), MagnusFloraHandler)

    print("Listening on port 9000")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

