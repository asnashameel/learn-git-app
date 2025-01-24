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

    def do_GET(self):
        global data_store
        if self.path == "/items":
            self._set_headers()
            self.wfile.write(json.dumps(data_store).encode())
        elif self.path.startswith("/items/"):
            item_id = self.path.split("/")[-1]
            if item_id.isdigit() and int(item_id) in data_store:
                self._set_headers()
                self.wfile.write(json.dumps(data_store[int(item_id)]).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Item not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Invalid endpoint"}).encode())
    
   
if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleCRUDHandler)
    print("Starting server on port 8080...")
    httpd.serve_forever()
