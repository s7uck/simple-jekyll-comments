import os
import requests
import yaml
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import urlparse

PORT = 9090
COMMENTS_DIR = os.path.abspath(".")
COMMENTS_FILENAME = "%s_%s.yaml"

class Comment:
    def make_comment_file(self):
        return f"""
author: {self.author}
time: {self.time}
reply_to: {self.reply_to}
email: {self.email}
content: |
  {self.content}
"""

    def __init__(self, author, time, content, reply_to, email=""):
        self.author = author
        self.time = time
        self.content = content
        self.reply_to = reply_to
        self.email = email
        self.id = len(lambda f: f.endswith(".yaml"), os.listdir(COMMENTS_DIR))

    def write_comment(self):
        self.path = os.path.join(COMMENTS_DIR, COMMENTS_FILENAME % (self.id, self.time))
        with open(self.path, 'w') as file:
            file.write(self.make_comments_file())
        file.close()

class CommentsServer(BaseHTTPRequestHandler):
    def do_POST(self):
        pass #gtg finish this later

def run():
    print("Avvio del server...")
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, CommentsServer)
    httpd.serve_forever()

run()
