# অধ্যায় ২৩: Web Application Security Basics

## সহজ কথায়:
Web application = website-এর পেছনের engine। আর web security = সেই engine-এ দুর্বলতা খুঁজে বের করা। বুঝলে তুমি ১০০+ site hack করতে পারবে (legal)।

---

## ২৩.১ HTTP কীভাবে কাজ করে

HTTP = Browser ↔ Server-এর মধ্যে communication protocol।

### HTTP Request Structure:

```
তুমি browser-এ লেখো: https://example.com/login

Browser নিচের request পাঠায়:
```

```http
GET /login HTTP/1.1                    ← Method, Path, Version
Host: example.com                       ← Target website
User-Agent: Mozilla/5.0 (Windows NT)    ← Browser info
Accept: text/html                       ← কি ধরনের response চায়
Cookie: session=abc123                  ← Session token
Authorization: Basic dXNlcjpwYXNz      ← Authentication header
```

### HTTP Response Structure:

```http
HTTP/1.1 200 OK                        ← Status code
Content-Type: text/html                ← Content type
Set-Cookie: session=xyz789              ← New cookie
Content-Length: 1234                    ← Response size

<html>
  <body>
    <h1>Welcome!</h1>
  </body>
</html>
```

### HTTP Methods:

| Method | কাজ | উদাহরণ |
|--------|-----|---------|
| **GET** | Data দেখা | View profile |
| **POST** | Data পাঠানো | Login form |
| **PUT** | Update করা | Update profile |
| **DELETE** | মুছে ফেলা | Delete account |
| **PATCH** | Partial update | Edit one field |
| **OPTIONS** | কি method allowed দেখো | CORS preflight |

### HTTP Status Codes:

```
1xx: Informational (101 Switching Protocols)
2xx: Success
    200 OK — সব ঠিক আছে
    201 Created — নতুন resource create
    204 No Content — success, কিন্তু কিছু ফেরত নেই

3xx: Redirection
    301 Moved Permanently — permanently সরেছে
    302 Found — temporarily সরেছে
    304 Not Modified — cache ব্যবহার করো

4xx: Client Error
    400 Bad Request — ভুল request
    401 Unauthorized — login করো
    403 Forbidden — permission নেই
    404 Not Found — পেজ নেই
    405 Method Not Allowed — wrong method

5xx: Server Error
    500 Internal Server Error — server crash
    502 Bad Gateway — upstream problem
    503 Service Unavailable — overload
```

---

## ২৩.২ Burp Suite — Setup ও ব্যবহার

Burp Suite = Web pentesting-এর সবচেয়ে গুরুত্বপূর্ণ tool।

### Install:

```bash
# Kali/Parrot তে:
sudo apt install burpsuite

# Or download from:
https://portswigger.net/burp/communitydownload
```

### Setup (Browser Proxy):

```
Burp Suite → Proxy → Proxy Settings
→ Listen on: 127.0.0.1:8080

Browser setup:
Firefox → Settings → Network → Connection Settings
→ Manual proxy → HTTP Proxy: 127.0.0.1, Port: 8080
→ Also proxy for HTTPS

CA Certificate install (for HTTPS):
Browser → http://burpsuite → Download CA Certificate
→ Import into browser (Trust this CA for websites)
```

### Burp Suite Tools:

```
🟢 Proxy — Intercept HTTP/HTTPS traffic
🟢 Repeater — Modify & resend requests
🟢 Intruder — Automated attack (brute force, fuzzing)
🟢 Decoder — Decode/encode data
🟢 Comparer — Compare two requests
🟢 Sequencer — Session token randomness check
🟢 Extender — BApp store (community extensions)
```

### Proxy — Traffic Intercept:

```
1. Burp Proxy → Intercept → Intercept is on
2. Browser-এ target site খোলো
3. Request freeze! modify করো
4. Forward → Server-এ যায়
5. Response দেখো
```

### Repeater — Request Modify:

```
1. কোনো request-এ Right click → Send to Repeater
2. Repeater tab → Modify request
3. Send button → Response দেখো
4. বারবার modify + send → vulnerability খুঁজো
```

### Intruder — Automation:

```
1. Request → Send to Intruder
2. Positions → Payload position চিহ্নিত করো (§)
3. Payloads → Wordlist / Numbers / Brute force
4. Options → Grep match (success indicator)
5. Start attack → Results দেখো
```

---

## ২৩.৩ DVWA ও WebGoat Setup

Vulnerable web apps = intentionally insecure website -> legal hack practice.

### DVWA (Damn Vulnerable Web Application):

```bash
# Kali তে:
sudo apt install dvwa

# Or Docker:
docker run --rm -it -p 80:80 vulnerables/web-dvwa

# Browser → http://localhost
# Login: admin / password

# Setup:
# DVWA Security → Low (for learning)
```

### WebGoat (OWASP):

```bash
# Docker:
docker run -p 8080:8080 webgoat/goatandwolf

# Browser → http://localhost:8080/WebGoat

# Lessons:
# → Injection
# → Broken Auth
# → Sensitive Data
# → XXE
# → Broken Access Control
```

### Other Vuln Apps:

```bash
# bWAPP (buggy web app):
docker run -p 80:80 raesene/bwapp

# Juice Shop (OWASP):
docker run -p 3000:3000 bkimminich/juice-shop

# Hackademic:
# Damn Vulnerable Node (DVNA)
```

---

## ২৩.4 HTTP Headers Security

### Security Headers Checklist:

```bash
Strict-Transport-Security: max-age=31536000    # HTTPS强制
X-Frame-Options: DENY                          # Clickjacking protect
X-Content-Type-Options: nosniff                # MIME sniffing protect
Content-Security-Policy: default-src 'self'     # XSS protect
X-XSS-Protection: 1; mode=block                # XSS filter (deprecated)
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=()
```

### Check Headers:

```bash
# curl command:
curl -v https://example.com
# দেখো Headers টা safe কিনা

# Online checker:
https://securityheaders.com
```

---

## 💡 ল্যাব এক্সারসাইজ

```
১. একটি ওয়েবসাইটের HTTP request/response দেখো:
   curl -v http://example.com
   → Headers বুঝো

২. Burp Suite setup করো:
   - Proxy setup
   - CA certificate install
   - কিছু traffic intercept করো

৩. DVWA install করো:
   - http://localhost/dvwa
   - Login → DVWA Security → Low
   - SQL injection tab → practice ready!

৪. একটি সাইটের security headers যাচাই করো:
   securityheaders.com — score কত?
```

---

## 📌 মনে রাখো

| Concept | Key Point |
|---------|-----------|
| **HTTP Methods** | GET (read), POST (create), DELETE (remove) |
| **Status Codes** | 200(OK), 404(না), 500(server error) |
| **Burp Suite** | Web hacking এর সবচেয়ে দরকারি tool |
| **DVWA** | Safe practice environment |
| **Security Headers** | CSP, HSTS, X-Frame-Options |

**পরবর্তী — OWASP Top 10 (প্রতিটি vulnerability code সহ)! ⚠️**
