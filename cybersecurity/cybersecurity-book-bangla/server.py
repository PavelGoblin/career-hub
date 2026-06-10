#!/usr/bin/env python3
"""
সাইবার নিরাপত্তা বই — ওয়েবসার্ভার
Run: python server.py
Open: http://localhost:3000
"""

import http.server
import socketserver
import os
import urllib.parse
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PORT = 3000
BOOK_DIR = os.path.dirname(os.path.abspath(__file__))
WEBSITE_DIR = os.path.join(BOOK_DIR, 'website')

class BookHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Parse path
        parsed = urllib.parse.urlparse(path)
        path = parsed.path

        # /book/ → serve from book root directory
        if path.startswith('/book/'):
            rel_path = path[6:]  # Remove '/book/'
            full_path = os.path.join(BOOK_DIR, rel_path)
            return os.path.normpath(full_path)

        # Everything else → website/ directory
        full_path = os.path.join(WEBSITE_DIR, path.lstrip('/'))
        if os.path.exists(full_path):
            return os.path.normpath(full_path)

        # SPA fallback → index.html for non-file routes
        if not os.path.isfile(full_path) and '.' not in path:
            return os.path.join(WEBSITE_DIR, 'index.html')

        return os.path.normpath(full_path)

    def log_message(self, format, *args):
        # Colorize output
        msg = format % args
        if '200' in msg or '304' in msg:
            print(f"\033[92m✓ {msg}\033[0m")
        elif '404' in msg:
            print(f"\033[91m✗ {msg}\033[0m")
        else:
            print(f"\033[93m→ {msg}\033[0m")

if __name__ == '__main__':
    os.chdir(BOOK_DIR)
    
    print(f"""
{'='*50}
[Books] Cybersecurity Book Server
{'='*50}
Server: http://localhost:{PORT}
Open browser -> http://localhost:{PORT}
Book directory: {BOOK_DIR}
Website files: {WEBSITE_DIR}
{'='*50}
Press Ctrl+C to stop
""")
    
    with socketserver.TCPServer(("", PORT), BookHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped.")
            httpd.server_close()
