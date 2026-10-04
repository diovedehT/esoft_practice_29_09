import os
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        token = os.environ.get("APP_API_TOKEN", "")
        masked = token[:2] + "*" * (len(token) - 2) if len(token) > 2 else "<не задан>"
        body = f"APP_API_TOKEN получен: {masked}\n".encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
