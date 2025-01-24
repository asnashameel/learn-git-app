from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# In-memory storage
data_store = {}
next_id = 1

class SimpleCRUDHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
    
   
if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleCRUDHandler)
    print("Starting server on port 8080...")
    httpd.serve_forever()
