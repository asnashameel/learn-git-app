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

    def do_POST(self):
        global data_store, next_id
        if self.path == "/items":
            content_length = int(self.headers["Content-Length"])
            post_data = json.loads(self.rfile.read(content_length).decode())

            data_store[next_id] = post_data
            response = {"id": next_id, "data": post_data}
            next_id += 1

            self._set_headers(201)
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Invalid endpoint"}).encode())

    def do_PUT(self):
        global data_store
        if self.path.startswith("/items/"):
            item_id = self.path.split("/")[-1]
            if item_id.isdigit() and int(item_id) in data_store:
                content_length = int(self.headers["Content-Length"])
                put_data = json.loads(self.rfile.read(content_length).decode())

                data_store[int(item_id)] = put_data
                self._set_headers()
                self.wfile.write(json.dumps({"id": int(item_id), "data": put_data}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Item not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Invalid endpoint"}).encode())

    def do_DELETE(self):
        global data_store
        if self.path.startswith("/items/"):
            item_id = self.path.split("/")[-1]
            if item_id.isdigit() and int(item_id) in data_store:
                del data_store[int(item_id)]
                self._set_headers(204)
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
