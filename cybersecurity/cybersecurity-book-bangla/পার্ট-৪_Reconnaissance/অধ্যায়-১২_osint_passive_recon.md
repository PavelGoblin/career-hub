# অধ্যায় ১২: Passive Reconnaissance (OSINT)

## সহজ কথায়:
তুমি চুরি করার আগে বাড়িটার চারপাশ ঘুরে দেখো — কখন কে থাকে, ক্যামেরা কোথায়, দরজা কেমন। এইটাই reconnaissance। আর **passive** মানে তুমি শুধু দেখছো, কাউকে ছুঁয়ে দেখছো না।

---

## ১২.১ OSINT কী?

OSINT = Open Source Intelligence। পাবলিকলি available তথ্য সংগ্রহ — যেমন Google search, social media, public database।

**কী কী পাওয়া যায়:**
- Email address
- Subdomains
- Technology stack (কোন CMS, server)
- Exposed documents
- Employee information
- API endpoints
- IP ranges

---

## ১২.২ Google Dorks (হ্যাকারদের জন্য Google)

Google Dork = বিশেষ search operator যা Google-এ hidden তথ্য বের করে।

### Basics:
| Operator | কাজ | উদাহরণ |
|----------|-----|---------|
| **site:** | নির্দিষ্ট site-এ search | `site:example.com` |
| **filetype:** | নির্দিষ্ট ফাইল টাইপ | `filetype:pdf` |
| **inurl:** | URL-এ keyword | `inurl:admin` |
| **intitle:** | Title-এ keyword | `intitle:"index of"` |
| **intext:** | Body text-এ search | `intext:password` |
| **cache:** | Google cache দেখা | `cache:example.com` |
| **link:** | কোন site লিংক করেছে | `link:example.com` |
| **-** | বাদ দেওয়া | `site:example.com -www` |
| **" "** | Exact phrase | `"admin login"` |
| **\|** | OR | `password \| passwd \| secret` |

### হ্যাকারদের favorite Google Dorks:

```bash
# 🔴 Critical Information Exposure:

# যেখানে password লেখা আছে (সাবধান!)
intext:"password" filetype:log
intext:"mysql password" filetype:txt
"password" "config.php" ext:php

# Directory listing (সব file দেখা যাচ্ছে)
intitle:"index of" "parent directory"
intitle:"index of" /etc/
intitle:"index of" "backup"

# Database files exposed
filetype:sql "INSERT INTO" "password"
filetype:sql "CREATE TABLE" "users"
filetype:env "DB_PASSWORD"

# Camera exposed
intitle:"webcamXP" inurl:8080
intitle:"Live View / - AXIS"
intitle:"EvoCam" inurl:"webcam.html"

# Admin panels
inurl:admin intitle:login
inurl:"/wp-admin/" intitle:"login"
inurl:"/administrator/" intitle:"login"

# Config files exposed
filetype:conf inurl:httpd.conf
filetype:config "connectionString"
filetype:xml "connectionString"

# Backup files
filetype:bak "backup" "sql"
filetype:old "password"
```

---

## ১২.৩ Shodan — Internet of Things search engine

Shodan = Google for devices। IoT device, CCTV, server, router খুঁজে বের করে।

### Basic Search:
```bash
# Browser এ: shodan.io

# কোন দেশের CCTV খুঁজো:
country:BD port:554 has_screenshot:true

# Open SSH server:
port:22 country:BD

# Apache server:
apache country:BD

# MongoDB (no password):
product:MongoDB port:27017

# Webcam:
webcamxp country:BD
```

### Shodan দিয়ে কী কী পাওয়া যায়:
```
- CCTV camera (live stream দেখাও যায়!)
- Industrial control system (ICS)
- Database (MongoDB, MySQL — password ছাড়া)
- Default credential device
- Server with open ports
- Router, printer, smart TV
```

### শিখে রাখো — Shodan Filters:

| Filter | কাজ | উদাহরণ |
|--------|-----|---------|
| `country:` | দেশ | `country:BD` |
| `city:` | শহর | `city:Dhaka` |
| `port:` | পোর্ট | `port:22` |
| `os:` | Operating System | `os:Windows` |
| `product:` | Service name | `product:OpenSSH` |
| `org:` | ISP/Organization | `org:Google` |
| `net:` | IP range | `net:103.25.0.0/16` |
| `hostname:` | Hostname | `hostname:example.com` |

---

## ১২.৪ theHarvester — Email ও Subdomain Collection

Kali Linux-এ pre-installed tool।

```bash
# Basic — domain দিয়ে email + subdomain খুঁজো
theHarvester -d example.com -b google

# Multiple sources:
theHarvester -d example.com -b google,bing,yahoo,linkedin

# Output save:
theHarvester -d example.com -b all -f results.html
```

**Payload:**
```bash
# ব্যবহার:
theHarvester -d microsoft.com -b google

# Sample Output:
# *******************
# * Emails *
# *******************
# admin@microsoft.com
# info@microsoft.com
#
# *******************
# * Hosts *
# *******************
# www.microsoft.com
# mail.microsoft.com
```

---

## ১২.৫ Maltego Basics

Maltego = OSINT visualization tool। Graph আকারে সম্পর্ক দেখায়।

```bash
# Kali-তে:
maltego
```

### Basic Transform:
```
1. Maltego খোলো
2. New → Blank Graph
3. Palette → Domain → Drag করো
4. Domain নাম লেখো: example.com
5. Right-click → Run Transform → To DNS Name → DNS to IP
6. Right-click → Run Transform → To Email Address
7. দেখো কত connection!
```

---

## ১২.৬ Whois ও DNS Lookup

### Whois — Domain owner info:
```bash
whois example.com

# Output:
# Domain Name: EXAMPLE.COM
# Registrar: INTERNET CORPORATION FOR ASSIGNED NAMES AND NUMBERS
# Creation Date: 1992-01-01
# Name Server: A.IANA-SERVERS.NET, B.IANA-SERVERS.NET
# Organization: Internet Assigned Numbers Authority
```

### DNS Record Check:
```bash
# A record (IPv4):
dig example.com A

# MX record (Mail server):
dig example.com MX

# NS record (Name server):
dig example.com NS

# All records:
dig example.com ANY

# Short output:
dig example.com +short

# Alternative:
nslookup example.com
nslookup -type=mx example.com  # MX only
```

---

## ১২.৭ Social Media OSINT

### Facebook OSINT:
```
- Public post from target
- Facebook Graph Search (যদি কাজ করে)
- Facebook page info
- Friends list (যদি public)
- Photos → location, tag
```

### LinkedIn OSINT:
```
- Employee list
- Technology stack (what they use)
- Job posting (কোন tech লাগে)
- Organization structure
```

### Twitter OSINT:
```bash
# Twitter advanced search browser:
https://twitter.com/search-advanced

# Tools:
twint -u username --email      # Email find
twint -u username --following   # Follow list
twint -u username --location    # Location based
```

### Instagram OSINT:
```bash
# Browser tools (online):
https://instasave.io/
instagram.com/{username}/?__a=1  # JSON data
```

---

## ১২.৮ Email Header Analysis — Fake Email ধরার উপায়

### Email Header কীভাবে দেখবে:

**Gmail:**
```
Open email → Three dots → Show original
```

**Outlook:**
```
Open email → ... → View → View message details
```

### Header-এ কী কী চেক করবে:

| Field | কী বলে | কী চেক করবে |
|-------|--------|-------------|
| **Received:** | কোন server দিয়ে এসেছে | Path mismatch? |
| **From:** | পাঠানোর ঠিকানা | Display name vs actual email |
| **Reply-To:** | উত্তর কোথায় যাবে | Different from From? |
| **Return-Path:** | Bounce কোথায় যাবে | Mismatch? |
| **SPF** | Domain verification | Pass/Fail? |
| **DKIM** | Digital signature | Pass/Fail? |
| **DMARC** | Policy | Pass/Fail? |

### Spoofed Email Detection:

```
# Fake email header example:
From: "CEO" <ceo@company.com>
Reply-To: hacker@gmail.com   ← দেখো! Reply-To আলাদা!
Return-Path: <bounce@hacker.com>  ← Suspicious!
Authentication-Results: spf=softfail  ← SPF fail!

# Real email header:
From: "CEO" <ceo@company.com>
Reply-To: ceo@company.com     ← Same as From
Authentication-Results: spf=pass dkim=pass  ← Pass!
```

---

## ১২.৯ Additional OSINT Tools

### Have I Been Pwned:
```bash
# Check if your email leaked in data breach:
# Browser: https://haveibeenpwned.com/
```

### Wayback Machine:
```bash
# Old version of website দেখো:
# Browser: https://web.archive.org/web/*
```

### BuiltWith:
```bash
# Website technology stack:
# Browser: https://builtwith.com/example.com
```

### DNSDumpster:
```bash
# DNS recon + visualization:
# Browser: https://dnsdumpster.com/
```

---

## 💡 ল্যাব এক্সারসাইজ

```
🔰 Beginner Level:
১. Google Dork চালাও: intitle:"index of" "parent directory"
   কী পেলে? কমপক্ষে ৩টা directory listing site খুঁজো।

২. Shodan-এ যাও → country:BD search করো
   কতগুলো device পাওয়া গেল?

৩. theHarvester চালাও একটি domain-এ:
   theHarvester -d example.com -b google

🚀 Advanced Level:
৪. Maltego → Domain → Transform → Visualization
   Email, IP, DNS relationship দেখো।

৫. একটি সন্দেহজনক email-এর header analysis করো।
   কোন field mismatch দেখতে পাচ্ছো?

৬. wayback machine-এ target site-এর পুরনো version দেখো।
   নতুন version-এর সাথে পার্থক্য কী?
```

---

## 📌 মনে রাখো

| Tool/Technique | কী খুঁজে পাবে |
|---------------|---------------|
| **Google Dorks** | Password, config, backup, camera |
| **Shodan** | Devices, IoT, CCTV, server |
| **theHarvester** | Email, subdomain |
| **Maltego** | Relationship graph |
| **Whois** | Domain owner info |
| **Dig** | DNS records |
| **Email Header** | Spoof detect |
| **Wayback Machine** | Old website version |

**পরবর্তী অধ্যায় — Active Reconnaissance (Nmap Bible)! 🔍**
