import json

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from argparse import ArgumentParser

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


if __name__ == "__main__":
    parser = ArgumentParser(description="Pi Stats HTTP Server")
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    vcgm = Vcgencmd()
    server = HTTPServer((args.host, args.port), Handler)
    print(f"Starting server at http://{args.host}:{args.port}")
    server.serve_forever()
