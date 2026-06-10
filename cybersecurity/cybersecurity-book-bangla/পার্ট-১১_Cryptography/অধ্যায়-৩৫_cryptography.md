# অধ্যায় ৩৫: Cryptography

## সহজ কথায়

Cryptography মানে হলো **গুপ্তলিপি** — ডাটা এমনভাবে পরিবর্তন করা যে শুধু যাকে দিচ্ছো, সেই পড়তে পারে। মনে করো তুমি বন্ধুকে চিঠি লিখলে, কিন্তু পথে যদি কেউ পড়ে ফেলে? তাই তুমি এমনভাবে লিখবে যে শুধু তোমার বন্ধু বুঝতে পারে। এই জাদুটাই করে **Cryptography**।

> **মজার Analogy:** Cryptography হলো আপনার গোপন ডায়েরির তালার মতো। সিমেট্রিক এনক্রিপশন মানে একই চাবি দিয়ে তালা বন্ধ করো আর খোলো। অ্যাসিমেট্রিক মানে — সবার জন্য একটা পাবলিক বাক্স রাখলে (যাতে সবাই চিঠি ফেলতে পারে), কিন্তু বাক্স খোলার চাবি শুধু তোমার কাছে। আর হ্যাশিং হলো জুসার মতো — তুমি আপেল (ডাটা) দিলে জুস (হ্যাশ) পাবে, কিন্তু জুস থেকে আর আপেল ফেরত পাবে না!

---

## ১. Symmetric vs Asymmetric Encryption

### সিমেট্রিক এনক্রিপশন (Secret Key)

একই চাবি দিয়ে এনক্রিপ্ট + ডিক্রিপ্ট।

```
সিমেট্রিক:
তুমি (লিখছো) → 🔑 "secret123" → [এনক্রিপ্ট] → 𐄷𐄷𐄷𐄷𐄷 → [ডিক্রিপ্ট] → 🔑 "secret123" → বন্ধু (পড়ছে)
```

```python
# # সিমেট্রিক এনক্রিপশন — AES (সবচেয়ে জনপ্রিয়)
from cryptography.fernet import Fernet  # pip install cryptography

# # কী জেনারেট করা
key = Fernet.generate_key()
print(f"গোপন চাবি (এইটা শেয়ার করো না!): {key.decode()}")

cipher = Fernet(key)

# # আসল মেসেজ
plain_text = b"এই মেসেজ কেউ পড়তে পারবে না! গোপন! 🤫"

# # এনক্রিপ্ট
encrypted = cipher.encrypt(plain_text)
print(f"এনক্রিপ্টেড: {encrypted}")

# # ডিক্রিপ্ট (একই চাবি দিয়ে!)
decrypted = cipher.decrypt(encrypted)
print(f"ডিক্রিপ্টেড: {decrypted.decode()}")
```

### অ্যাসিমেট্রিক এনক্রিপশন (Public/Private Key)

দুইটা চাবি — পাবলিক (সবাই জানে) + প্রাইভেট (শুধু তুমি জানো)।

```
অ্যাসিমেট্রিক:
তুমি → [বন্ধুর পাবলিক কী] → এনক্রিপ্ট → 𐄷𐄷𐄷𐄷𐄷 → [বন্ধুর প্রাইভেট কী] → বন্ধু (শুধু সেও পড়তে পারে)

সিগনেচার:
তুমি → [তোমার প্রাইভেট কী] → সাইন → 𐄷𐄷𐄷𐄷𐄷 → [তোমার পাবলিক কী] → বন্ধু (ভেরিফাই করে — "হ্যাঁ, এটা তুমিই লিখেছো!")
```

```python
# # RSA — অ্যাসিমেট্রিক এনক্রিপশন
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

# # কী পেয়ার জেনারেট
private_key = rsa.generate_private_key(
    public_exponent=65537,   # # এই সংখ্যা সব RSA-তে একই থাকে
    key_size=2048,           # # 2048 নিচে হলে INSECURE!
)

public_key = private_key.public_key()

# # পাবলিক কী দিয়ে এনক্রিপ্ট (যে কেউ পারে)
message = b"AI Agent: গোপন নির্দেশনা — সিরিয়াল নম্বর ২০২৬-এক্স"
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print(f"🔐 পাবলিক কী দিয়ে এনক্রিপ্টেড: {ciphertext.hex()[:50]}...")

# # প্রাইভেট কী দিয়ে ডিক্রিপ্ট (শুধু মালিক পারে)
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print(f"🔑 প্রাইভেট কী দিয়ে ডিক্রিপ্টেড: {plaintext.decode()}")
```

### পার্থক্য

| বৈশিষ্ট্য | Symmetric (AES) | Asymmetric (RSA/ECC) |
|-----------|----------------|---------------------|
| **চাবি** | ১ টা (Shared Secret) | ২ টা (Public + Private) |
| **গতি** | 🚀 খুব দ্রুত (হার্ডওয়্যার অ্যাক্সিলারেটেড) | 🐢 ধীর (গণিত জটিল) |
| **ব্যবহার** | বড় ফাইল এনক্রিপ্ট | কী এক্সচেঞ্জ, সিগনেচার |
| **নিরাপত্তা** | AES-256 = অটুট (কোয়ান্টাম ছাড়া) | RSA-2048 = ভালো, কিন্তু কোয়ান্টাম ভঙ্গুর |
| **কী শেয়ার** | সমস্যা — কী পাঠাতে গেলে ইন্টারসেপ্ট হতে পারে | পাবলিক কী শেয়ার করা নিরাপদ |

---

## ২. AES, DES, RSA, ECC — বিস্তারিত

### DES (Data Encryption Standard) — পুরনো, আর ব্যবহার করো না!

```python
# # DES — ৫৬-বিট কী (আজকের কম্পিউটারে ১ দিনে ভেঙে ফেলা যায়!)
# # WARNING: DES কখনো ব্যবহার করবেন না — এটা BROKEN!

from Crypto.Cipher import DES

# # DES কী (৫৬ বিট = ৮ বাইট) — খুবই দুর্বল!
key = b'8bytkey'  # # মাত্র ৮ অক্ষর! 쉽게 ভাঙা যায়!

cipher = DES.new(key, DES.MODE_ECB)
plaintext = b"AES ১২৮-বিটও ভাঙা যায় না, DES তো ৫৬-বিট!"

# # প্যাডিং যোগ করে encrypt
from Crypto.Util.Padding import pad
padded_text = pad(plaintext, DES.block_size)
encrypted = cipher.encrypt(padded_text)
print(f"DES এনক্রিপ্টেড (ভালো করে দেখো না — দুর্বল!): {encrypted.hex()[:40]}...")
```

### AES (Advanced Encryption Standard) — বর্তমানের বিশ্বমান

```python
# # AES — বর্তমানে সবচেয়ে নিরাপদ সিমেট্রিক এনক্রিপশন
# # কী-সাইজ: ১২৮, ১৯২, ২৫৬ বিট (যত বেশি, তত নিরাপদ)

from Crypto.Cipher import AES
import os

# # ১২৮-বিট AES কী (আসল প্রজেক্টে secrets বা secure RNG ব্যবহার করো!)
key = os.urandom(16)   # # 128 bits = 16 bytes (সেফ!)
iv = os.urandom(16)    # # IV (Initialization Vector) — এলোমেলো!

cipher = AES.new(key, AES.MODE_CBC, iv)

message = b"""
এটি একটি গোপন বার্তা যা AES-১২৮ দিয়ে এনক্রিপ্ট করা হয়েছে।
শুধু সঠিক কী থাকলেই কেউ পড়তে পারবে। বাকি সবাই — 𐄷𐄷𐄷𐄷𐄷!
"""

# # প্যাডিং দিয়ে এনক্রিপ্ট
from Crypto.Util.Padding import pad, unpad
ciphertext = cipher.encrypt(pad(message, AES.block_size))

print(f"AES-CBC এনক্রিপ্টেড: {ciphertext.hex()[:80]}...")
print(f"IV (Initialization Vector): {iv.hex()}")

# # ডিক্রিপ্ট
cipher_dec = AES.new(key, AES.MODE_CBC, iv)
decrypted = unpad(cipher_dec.decrypt(ciphertext), AES.block_size)
print(f"ডিক্রিপ্টেড: {decrypted.decode()}")
```

### RSA vs ECC — দুই অ্যাসিমেট্রিক জায়ান্ট

```python
# # RSA 2048 বনাম ECC — ECC কম শক্তিতে বেশি নিরাপত্তা দেয়!

# # RSA কী সাইজ বনাম ECC সুরক্ষা লেভেল
key_comparison = {
    "Security Level": ["৮০-বিট (দুর্বল)", "১১২-বিট (মাঝারি)", "১২৮-বিট (নিরাপদ)", "২৫৬-বিট (খুব নিরাপদ)"],
    "RSA কী-সাইজ": ["১০২৪", "২০৪৮", "৩০৭২", "১৫৩৬০"],
    "ECC কী-সাইজ": ["১৬০", "২২৪", "২৫৬", "৫১২"],
    "বয়স": ["পুরনো (RSA)", "বর্তমান (RSA)", "আদর্শ (ECC)", "ভবিষ্যৎ (PQC)"]
}

for i in range(4):
    print(f"{key_comparison['Security Level'][i]:20} | "
          f"RSA: {key_comparison['RSA কী-সাইজ'][i]:6} | "
          f"ECC: {key_comparison['ECC কী-সাইজ'][i]:6} | "
          f"{key_comparison['বয়স'][i]}")

# # ECC ২৫৬-বিট = RSA ৩০৭২-বিটের সমান নিরাপত্তা — কিন্তু ১০ গুণ ছোট কী!
```

---

## ৩. Hashing — একমুখী রাস্তা

হ্যাশিং মানে — ডাটা নিয়ে একটা ছোট, ফিক্সড সাইজের **ফিঙ্গারপ্রিন্ট** বানানো। রাস্তা শুধু একমুখী — হ্যাশ থেকে আসল ডাটা বের করা যায় না।

```python
# # বিভিন্ন হ্যাশিং অ্যালগরিদম তুলনা
import hashlib

data = b"আমার নাম কি?"  # # ১৮ বাইটের ডাটা

# # MD5 (১২৮ বিট) — NEVER USE! পুরনো, collision পাওয়া গেছে
md5_hash = hashlib.md5(data).hexdigest()
print(f"MD5 (ভাঙা!):    {md5_hash}  ({len(md5_hash)*4} বিট)")

# # SHA-1 (১৬০ বিট) — ভাঙা! Google ২০১৭ সালে collision দেখিয়েছে
sha1_hash = hashlib.sha1(data).hexdigest()
print(f"SHA-1 (ভাঙা!):  {sha1_hash}  ({len(sha1_hash)*4} বিট)")

# # SHA-256 (২৫৬ বিট) — বর্তমানে নিরাপদ
sha256_hash = hashlib.sha256(data).hexdigest()
print(f"SHA-256 (সেফ):  {sha256_hash}  ({len(sha256_hash)*4} বিট)")

# # bcrypt — পাসওয়ার্ড হ্যাশিং-এর জন্য সবচেয়ে ভালো
import bcrypt  # pip install bcrypt

password = b"my_secure_password_123"

# # bcrypt salt + hash (প্রতি হ্যাশে salt এলোমেলো!)
salt = bcrypt.gensalt()  # # rounds=১২ (ডিফল্ট) — যত বেশি, ধীর, কিন্তু সুরক্ষিত
hashed = bcrypt.hashpw(password, salt)
print(f"\nbcrypt হ্যাশ (পাসওয়ার্ডের জন্য): {hashed.decode()}")

# # পাসওয়ার্ড ভেরিফাই করা
check = bcrypt.checkpw(password, hashed)
print(f"পাসওয়ার্ড মিলেছে? {check}")

# # ভুল পাসওয়ার্ড দিলে:
wrong = bcrypt.checkpw(b"wrong_password", hashed)
print(f"ভুল পাসওয়ার্ড? {wrong}")
```

### হ্যাশিং কখন ব্যবহার করো

| Scenario | অ্যালগরিদম | কারণ |
|----------|------------|------|
| পাসওয়ার্ড সংরক্ষণ | **bcrypt / Argon2** | ধীর — ব্রুট-ফোর্স কঠিন করে |
| ফাইল ইন্টিগ্রিটি চেক | **SHA-256 / SHA-512** | দ্রুত + collision-resistant |
| Digital Signature | **SHA-256 + RSA/ECC** | PKI স্ট্যান্ডার্ড |
| ডাটা ইন্টিগ্রিটি (Blockchain) | **SHA-256** | Bitcoin-ও SHA-২৫৬ ব্যবহার করে |
| **❌ আর কখনো না** | **MD5, SHA-1** | Collision attack — বিশ্বাস করো না |

---

## ৪. PKI ও Certificate Authority

PKI পুরো সিস্টেম যেটা SSL/TLS-এর পেছনে কাজ করে — পাবলিক কী কাকে বলে সেটা ভেরিফাই করে।

```
PKI — কারা আছে:

1. CA (Certificate Authority) — বিশ্বস্ত সংস্থা (DigiCert, Let's Encrypt)
   ↓ ইস্যু করে
2. Certificate — তোমার পাবলিক কী + পরিচয় (ডিজিটাল পাসপোর্ট)
   ↓ ভেরিফাই করে
3. Browser — সার্টিফিকেট চেক করে — "এটা আসল Facebook!"
```

```bash
# # সার্টিফিকেট চেক করার কমান্ড
# # একটি ওয়েবসাইটের SSL সার্টিফিকেট দেখা
echo | openssl s_client -connect google.com:443 -servername google.com 2>/dev/null | openssl x509 -text -noout | head -50

# # সার্টিফিকেটের মেয়াদ শেষ কবে?
echo | openssl s_client -connect github.com:443 2>/dev/null | openssl x509 -noout -dates

# # নিজের Self-Signed সার্টিফিকেট বানানো
openssl req -x509 -newkey rsa:2048 -keyout mykey.pem -out mycert.pem -days 365 -nodes
```

```python
# # SSL সার্টিফিকেট চেক করার পাইথন কোড
import ssl
import socket

def check_certificate(hostname):
    """একটি সাইটের SSL সার্টিফিকেট চেক করি"""
    context = ssl.create_default_context()
    
    with socket.create_connection((hostname, 443), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            
            print(f"সাইট: {hostname}")
            print(f"ইস্যু করেছে: {cert['issuer'][0][0][1]}")
            print(f"মেয়াদ শেষ: {cert['notAfter']}")
            print(f"সাবজেক্ট: {cert['subject'][0][0][1]}")
            
            # # SAN (Subject Alternative Names) — সব ডোমেইন লিস্ট
            print("সকল ডোমেইন:")
            for entry in cert['subjectAltName']:
                print(f"  • {entry[1]}")

check_certificate("github.com")
```

### Certificate Chain

```
Root CA (সর্বোচ্চ — বিশ্বাস করা হয়, অফলাইন রাখা হয়)
   ↓ সাইন করে
Intermediate CA (মাঝারি — Root-এর পক্ষে কাজ করে)
   ↓ সাইন করে
Server Certificate (তোমার ওয়েবসাইটের সার্টিফিকেট)

# # ব্রাউজারে প্যাডলক চিহ্ন → Certificate দেখলে এই চেইন দেখাবে
```

---

## ৫. SSL/TLS — HTTPS কীভাবে নিরাপদ করে?

### SSL/TLS হ্যান্ডশেক — ৪ ধাপে কীভাবে নিরাপদ সংযোগ হয়

```python
# # SSL/TLS হ্যান্ডশেক — ধাপে ধাপে
class TLSHandshake:
    """HTTPS সংযোগের পেছনের জাদু"""
    
    def connect_to_https(self, website):
        print(f"""
========== TLS হ্যান্ডশেক শুরু: {website} ==========

[১] Client Hello
    └─ আমি {website}-এ HTTPS-এ কানেক্ট করতে চাই
    └─ আমি AES-256-GCM, TLS 1.3 বুঝি
    └─ আমার এলোমেলো নম্বর: 0xA1B2C3D4...

[২] Server Hello
    └─ চলো AES-256-GCM ব্যবহার করি, TLS 1.3
    └─ আমার সার্টিফিকেট নাও:
        ├─ ইস্যুকারী: Let's Encrypt
        ├─ মেয়াদ: ৩ মাস
        └─ আমার পাবলিক কী: [RSA 2048-bit]
    └─ আমার এলোমেলো নম্বর: 0xE5F6G7H8...

[৩] Key Exchange (Diffie-Hellman)
    └─ ক্লায়েন্ট: আমার DH প্যারামিটার পাঠায় → 🔑
    └─ সার্ভার: তার DH প্যারামিটার পাঠায় → 🔑
    └─ উভয়েই Session Key ক্যালকুলেট করে (একই!)
    └─ এই Session Key দিয়ে বাকি সব এনক্রিপ্ট হবে

[৪] Secure Connection Established! ✅
    └─ এখন থেকে সব ডাটা AES-256-GCM দিয়ে এনক্রিপ্টেড
    └─ HTTP → HTTPS (নিরাপদ তলে)
    
        """)
        return "SECURE 🔒"

tls = TLSHandshake()
tls.connect_to_https("https://github.com")
```

```bash
# # TLS ভার্শন চেক করা
nmap --script ssl-enum-ciphers -p 443 github.com

# # পুরনো TLS ভার্শন বন্ধ আছে কিনা চেক
nmap -sV --script ssl-enum-ciphers -p 443 example.com | grep -E "TLSv1.0|TLSv1.1|SSLv3"

# # সার্টিফিকেট চেইন ডাউনলোড
openssl s_client -connect google.com:443 -showcerts
```

### HTTPS বনাম HTTP — পার্থক্য

```
HTTP:  http://example.com/login?user=admin&pass=12345
      ⬇️ PLAIN TEXT — যে কেউ পড়তে পারে!
      ⬇️ Man-in-the-Middle করতে ২ সেকেন্ড

HTTPS: https://example.com/login
      ⬇️ 𐄷𐄷𐄷𐄷𐄷𐄷𐄷 (এনক্রিপ্টেড — কেউ পড়তে পারবে না)
      ⬇️ Man-in-the-Middle করলে 𐄷𐄷𐄷𐄷 দেখা যাবে, আসল ডাটা না!
```

---

## ৬. কীভাবে বাঁচবে — Cryptography Best Practices

| ✅ করণীয় | ❌ বর্জনীয় |
|-----------|------------|
| AES-256-GCM বা ChaCha20-Poly1305 ব্যবহার করো | ❌ DES, RC4, MD5, SHA-1 — ভুলেও ব্যবহার করো না |
| পাসওয়ার্ডের জন্য bcrypt/Argon2 ব্যবহার করো | ❌ পাসওয়ার্ড plain text বা MD5-এ রাখো না |
| HTTPS everywhere — Let's Encrypt ফ্রি সার্ট দেয় | ❌ HTTP-তে লগইন ফর্ম রাখো না |
| RSA ন্যূনতম ২০৪৮-বিট, ECC হলে ২৫৬-বিট | ❌ RSA ১০২৪-বিট — সেটা ২০০০-এর দশকের! |
| SSL/TLS সঠিকভাবে কনফিগার করো (TLS 1.3) | ❌ SSLv3, TLSv1.0, TLSv1.1 — এগুলো ডিপ্রিকেটেড |
| Key দীর্ঘমেয়াদী রাখতে HSM বা Key Vault ব্যবহার করো | ❌ সোর্স কোডে হার্ডকোডেড কী রাখো না |

---

## ল্যাব এক্সারসাইজ

> **ল্যাব ১:** AES-২৫৬-CBC দিয়ে একটি টেক্সট ফাইল এনক্রিপ্ট করে ডিক্রিপ্ট করো। দেখাও যে সঠিক কী ও IV ছাড়া ডিক্রিপ্ট করা অসম্ভব।

> **ল্যাব ২:** RSA-২০৪৮ কী পেয়ার জেনারেট করো। তারপর পাবলিক কী দিয়ে এনক্রিপ্ট করে প্রাইভেট কী দিয়ে ডিক্রিপ্ট করো।

> **ল্যাব ৩:** MD5, SHA-1, SHA-২৫৬ — তিনটি দিয়ে একই মেসেজের হ্যাশ বের করো এবং দৈর্ঘ্যের পার্থক্য দেখাও। দেখাও যে SHA-1 collision সম্ভব (Google SHAttered example)।

> **ল্যাব ৪:** bcrypt দিয়ে একটি পাসওয়ার্ড হ্যাশ করো। rounds=৪, rounds=১২, rounds=২০ — সময়ের পার্থক্য মেপে দেখাও। ব্যাখ্যা করো কেন ধীর = ভালো।

> **ল্যাব ৫:** OpenSSL দিয়ে একটি Self-Signed সার্টিফিকেট জেনারেট করো। তারপর Nginx-এ এটি বসিয়ে লোকাল HTTPS সার্ভার চালাও। ব্রাউজার থেকে কানেক্ট করে "Not Secure" দেখাও — তারপর বুঝিয়ে বলো কেন Root CA দরকার।

---

## মনে রাখো

| টপিক | মূল পয়েন্ট |
|-------|------------|
| Symmetric (AES) | এক চাবি — দ্রুত — বড় ডাটার জন্য |
| Asymmetric (RSA/ECC) | দুই চাবি — ধীর — কী এক্সচেঞ্জ ও সিগনেচারের জন্য |
| AES Key Sizes | AES-১২৮ (নিরাপদ), AES-১৯২ (নিরাপদ), AES-২৫৬ (খুব নিরাপদ) |
| DES/RSA 1024 | পুরনো — ২০২৬-এ আর ব্যবহার করবে না |
| Hashing (SHA-256) | একমুখী — পাসওয়ার্ড স্টোরেজ → bcrypt/Argon2 |
| MD5/SHA-1 | BROKEN — collision attack সম্ভব |
| PKI | CA + Certificate + Browser — পাবলিক কী ভেরিফিকেশন সিস্টেম |
| TLS Handshake | ৪ ধাপ: Hello → Cert → Key Exchange → Secure |
| HTTPS ≠ HTTP | HTTPS-এ সব এনক্রিপ্টেড — MITM impossible |

> **শেষ কথা:** ভাই, ক্রিপ্টোগ্রাফির মজাই হলো — তুমি অংক আর লজিক দিয়ে এমন কিছু সৃষ্টি করতে পারো যা পুরো দুনিয়ার কম্পিউটারও ভাঙতে পারে না। কিন্তু মাথায় রাখবে — সবচেয়ে শক্তিশালী এনক্রিপশনও অকেজো যদি **তুমি নিজেই পাসওয়ার্ড শেয়ার করে দাও**। প্রযুক্তির চেয়ে মানুষের দুর্বলতাই আসল ঝুঁকি!
