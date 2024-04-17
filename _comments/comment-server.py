import os
import requests
import yaml
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import logging
import time

PORT = 9090
COMMENTS_DIR = os.path.abspath(".")
COMMENTS_FILENAME = "%s_%s.md"

def comments_list(directory=COMMENTS_DIR):
    return list(
        filter(lambda f: f.endswith(".md"), os.listdir(directory))
    )

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
        self.id = len(comments_list())

    def write_comment(self):
        self.path = os.path.join(COMMENTS_DIR, self.reply_to.strip("/"), COMMENTS_FILENAME % (self.id, self.time))
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        print(self.make_comment_file())
        with open(self.path, 'w+') as file:
            file.write(self.make_comment_file())
        file.close()
        print(f"saved to {self.path}")

class CommentsServer(BaseHTTPRequestHandler):
    def respond(self, status, status_text, body=""):
        self.send_response(status, status_text)
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

    def respond_OK(self, body=""):
        self.respond(200, 'OK', body)

    def get_payload(self):
        length = int(self.headers['Content-Length'])
        payload = self.rfile.read(length).decode('utf-8')
        data = {}
        for item in payload.split('&'):
            key, value = item.split('=')
            data[key] = value
        return data

    def do_POST(self):
        payload = self.get_payload()
        print(payload)
        comment_data = payload

        for att in ['author', 'time', 'content', 'reply_to', 'email']:
            if att not in comment_data:
                if att in ['author', 'content']:
                    self.respond(400, 'Missing attribute: %' % att)
                    break
                elif att == 'time': comment_data['time'] = time.time()
                else: comment_data[att] = ''

        comment = Comment(
            comment_data['author'],
            int(comment_data['time']),
            comment_data['content'],
            comment_data['reply_to'],
            email=comment_data['email'],
        )
        comment.write_comment()

def run(port=PORT):
    logging.basicConfig(level=logging.INFO)
    print("Avvio del server...")
    server_address = ('', port)
    httpd = HTTPServer(server_address, CommentsServer)
    logging.info('Starting server...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Closing server...\n')

if __name__ == '__main__':
    from sys import argv
    run(*argv[1:])
