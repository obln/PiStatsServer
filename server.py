from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json

from vcgencmd import Vcgencmd


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        found = False
        payload = {}
        if path == "/temp":
            temp = vcgm.measure_temp()
            payload = {"temperature": temp}
            found = True
        elif path == "/voltage":
            voltage = vcgm.measure_volts("core")
            payload = {"voltage": voltage}
            found = True
        elif path == "/throttled":
            throttled = vcgm.get_throttled()
            payload = {"throttled": throttled}
            found = True

        if found:
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            payload_json = json.dumps(payload).encode('utf-8')
            self.wfile.write(payload_json)
        else:
            self.send_response(404)
            self.end_headers()

vcgm = Vcgencmd()
HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
