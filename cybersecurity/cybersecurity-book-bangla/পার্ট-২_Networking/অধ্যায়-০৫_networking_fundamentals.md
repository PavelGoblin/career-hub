# অধ্যায় ৫: Networking Fundamentals

## সহজ কথায়:
Networking হলো দুই বা ততোধিক কম্পিউটারের মধ্যে কথা বলার সিস্টেম। যেমন দুই বন্ধু ফোনে কথা বলে — তেমনি কম্পিউটার network-এ data share করে।

---

## ৫.১ OSI Model (৭ Layer)

OSI (Open Systems Interconnection) model হলো networking-এর **বাইবেল** — ৭টা layer যেখানে প্রতিটি layer-এর আলাদা কাজ।

**Real life analogy:** তুমি একটি পিজ্জা অর্ডার করো:

| Layer | নাম | কাজ | পিজ্জা analogy |
|-------|-----|------|----------------|
| **৭** | **Application** | User-এর সাথে interface | তুমি অ্যাপে পিজ্জা অর্ডার করো |
| **৬** | **Presentation** | Data format, encryption | অ্যাপ তোমার অর্ডার ঠিক format-এ লেখে |
| **৫** | **Session** | Connection তৈরি/শেষ | Restart-এর সময় অর্ডার ID save রাখে |
| **৪** | **Transport** | Reliable delivery,TCP/UDP | পিজ্জা ঠিকভাবে পৌঁছায় কিনা চেক করে |
| **৩** | **Network** | Routing, IP addressing | পিজ্জা কোন পথে আসবে ঠিক করে |
| **২** | **Data Link** | MAC address, framing | লোকাল delivery guy-র কাছে পৌঁছে |
| **১** | **Physical** | Cables, signals, bits | পিজ্জা actual physical-এ যায় |

### Layer বিস্তারিত:

#### Layer 1: Physical Layer
- কাজ: **বিট** (0/1) ট্রান্সমিট করা
- মাধ্যম: Copper wire, fiber optic, radio wave
- Devices: Hub, Repeater, Cable
- ডেটা: Bits

#### Layer 2: Data Link Layer  
- কাজ: **Frame** তৈরি, MAC address, error detection
- Devices: Switch, Bridge
- ডেটা: Frame
- Sub-layers: LLC + MAC
- MAC address দিয়ে device identify করে

**হ্যাকারদের জন্য গুরুত্ব:** ARP spoofing এই layer-এ হয়। MAC address manipulation।

#### Layer 3: Network Layer
- কাজ: **Routing**, IP addressing
- Devices: Router
- ডেটা: Packet
- প্রোটোকল: IP, ICMP, ARP

**হ্যাকারদের জন্য গুরুত্ব:** IP spoofing, traceroute, routing attacks।

#### Layer 4: Transport Layer
- কাজ: End-to-end delivery, reliability
- ডেটা: Segment (TCP) / Datagram (UDP)
- প্রোটোকল: TCP, UDP
- Port numbers এই layer-এ work করে

#### Layer 5: Session Layer
- কাজ: Session management (start, stop, maintain)
- উদাহরণ: API authentication, session cookies

#### Layer 6: Presentation Layer
- কাজ: Data format translation, encryption/decryption
- উদাহরণ: SSL/TLS encryption starts here, JPEG, ASCII

#### Layer 7: Application Layer
- কাজ: User-এর closest layer
- প্রোটোকল: HTTP, FTP, SMTP, DNS, SSH

---

## ৫.২ TCP/IP Model — OSI-এর সাথে তুলনা

TCP/IP Model বর্তমান Internet-এর **actual model**। ৪ টা layer:

| OSI Model (৭ Layer) | TCP/IP Model (৪ Layer) | উদাহরণ প্রোটোকল |
|---------------------|----------------------|------------------|
| ৭.Application | → **Application** | HTTP, FTP, SMTP, DNS |
| ৬.Presentation | → (একসাথে) | |
| ৫.Session | → | |
| ৪.Transport | → **Transport** | TCP, UDP |
| ৩.Network | → **Internet** | IP, ICMP, ARP |
| ২.Data Link | → **Network Access** | Ethernet, WiFi |
| ১.Physical | → (একসাথে) | |

### পার্থক্য:
- OSI = **Theoretical** (শিখতে ভালো, শেখানো হয় পরীক্ষার জন্য)
- TCP/IP = **Practical** (বাস্তবে internet এই model-এ চলে)

---

## ৫.৩ TCP vs UDP — কোনটা কখন, কেন

### TCP (Transmission Control Protocol)
নির্ভরযোগ্য, কিন্তু ধীর। চিঠির মতো — Reply confirm করবে।

**বৈশিষ্ট্য:**
- ✅ Reliable (প্যাকেট নিশ্চিত পৌঁছায়)
- ✅ Ordered (sequence maintain করে)
- ✅ Error checking
- ❌ Slow (overhead বেশি)
- Three-way handshake: SYN → SYN-ACK → ACK

**কখন ব্যবহার হয়:**
- ওয়েব ব্রাউজিং (HTTP/HTTPS)
- Email (SMTP, IMAP)
- File transfer (FTP)
- SSH

### UDP (User Datagram Protocol)
দ্রুত, কিন্তু নির্ভরযোগ্য নয়। WhatsApp message চলে গেলে confirm চায় না — পৌঁছালে ভালো, না পৌঁছালেও OK।

**বৈশিষ্ট্য:**
- ✅ Fast
- ✅ Low latency
- ❌ Unreliable (প্যাকেট হারালেও বলে না)
- ❌ No ordering

**কখন ব্যবহার হয়:**
- Video streaming (YouTube, Netflix)
- VoIP (Zoom, Google Meet)
- DNS queries
- Gaming
- DHCP

### TCP vs UDP তুলনা:

| বৈশিষ্ট্য | TCP | UDP |
|-----------|-----|-----|
| Connection | Connection-oriented | Connection-less |
| Reliability | ১০০% | না |
| Speed | Slow | Fast |
| Use case | File transfer, web | Video, voice, gaming |
| 헤더 크기 | ২০ bytes | ৮ bytes |

---

## ৫.৪ LAN, MAN, WAN — পার্থক্য ও ব্যবহার

### LAN (Local Area Network)
ছোট এলাকা — যেমন বাসা, অফিস, স্কুল।
- **Area:** ১ কিমি পর্যন্ত
- **Speed:** খুব দ্রুত (1 Gbps - 100 Gbps)
- **Ownership:** Private (তোমার নিজের)
- **Technology:** Ethernet, WiFi

### MAN (Metropolitan Area Network)
শহর-ব্যাপী network।
- **Area:** ১০-৫০ কিমি
- **Speed:** Fast
- **Ownership:** Public/Private
- **Technology:** Fiber optic

### WAN (Wide Area Network)
বিশ্বব্যাপী network — Internet নিজেই **বিশাল WAN**।
- **Area:** যে কোনো জায়গা
- **Speed:** তুলনামূলক ধীর
- **Ownership:** Public (ISP-দের)
- **Technology:** Fiber, Satellite

### Comparison:

```
LAN (ঘর/অফিস)
    ↓
MAN (শহর)
    ↓
WAN (দেশ/বিশ্ব) ← Internet
```

---

## ৫.৫ Ports — কী, কেন গুরুত্বপূর্ণ

Port হলো **ডিজিটাল দরজা** যা দিয়ে নির্দিষ্ট service-এ ঢোকা যায়।

**Real life analogy:** একটি বিল্ডিং এর বিভিন্ন ফ্ল্যাট:
- IP = বিল্ডিং এর ঠিকানা
- Port = ফ্ল্যাট নাম্বার

### Common Port Numbers (হ্যাকারদের জন্য মনে রাখা জরুরি):

| Port | Service | প্রোটোকল | কেন গুরুত্বপূর্ণ |
|------|---------|-----------|-----------------|
| **20/21** | FTP | TCP | File transfer (anonymous login vulnerability) |
| **22** | SSH | TCP | Secure shell (brute force attack) |
| **23** | Telnet | TCP | Unencrypted (dangerous, sniff করা যায়) |
| **25** | SMTP | TCP | Email sending (spam relay) |
| **53** | DNS | TCP/UDP | DNS poisoning |
| **80** | HTTP | TCP | Web server (base website) |
| **110** | POP3 | TCP | Email receiving |
| **143** | IMAP | TCP | Email receiving (modern) |
| **443** | HTTPS | TCP | Secure web (SSL/TLS) |
| **445** | SMB | TCP | Windows file sharing (EternalBlue exploit) |
| **3306** | MySQL | TCP | Database (SQL injection target) |
| **3389** | RDP | TCP | Windows remote desktop (brute force) |
| **5432** | PostgreSQL | TCP | Database |
| **8080** | HTTP-Alt | TCP | Alternative web port |
| **8443** | HTTPS-Alt | TCP | Alternative secure web |

### হ্যাকাররা Port কীভাবে ব্যবহার করে:

```bash
# প্রথমে scan করবে কোন port open আছে
nmap -p- target.com

# Open port পেলে, সেটার service version check করবে
nmap -sV -p 22,80,443 target.com

# তারপর exploit খুঁজবে
searchsploit openssh 7.2
```

---

## ৫.৬ Protocols: HTTP, HTTPS, FTP, SSH, SMTP, DNS

### HTTP (HyperText Transfer Protocol)
- **পোর্ট:** 80
- **কাজ:** Web page পরিবহন
- **বৈশিষ্ট্য:** Plain text (encrypted না)

```bash
# HTTP request দেখো (terminal এ):
curl -v http://example.com

# Output দেখাবে:
# > GET / HTTP/1.1
# > Host: example.com
# < HTTP/1.1 200 OK
# < Content-Type: text/html
```

### HTTPS (HTTP Secure)
- **পোর্ট:** 443
- **কাজ:** Encryption-সহ web page
- **বৈশিষ্ট্য:** SSL/TLS encryption

```bash
# HTTPS connection check:
curl -v https://google.com

# Certificate details দেখো:
openssl s_client -connect google.com:443
```

### FTP (File Transfer Protocol)
- **পোর্ট:** 21 (control), 20 (data)
- **কাজ:** File transfer
- **বৈশিষ্ট্য:** Old, insecure (password plain text যায়)
- **SFTP/FTPS** — secure version (SSH-এর উপর)

```bash
# FTP connection:
ftp 192.168.1.10
# username: anonymous
# password: (empty or email)
```

### SSH (Secure Shell)
- **পোর্ট:** 22
- **কাজ:** Remote secure login
- **বৈশিষ্ট্য:** Encrypted

```bash
# SSH দিয়ে remote server-এ login:
ssh user@192.168.1.10

# SSH key generate:
ssh-keygen -t rsa -b 4096
```

### SMTP (Simple Mail Transfer Protocol)
- **পোর্ট:** 25
- **কাজ:** Email পাঠানো

### DNS (Domain Name System)
- **পোর্ট:** 53
- **কাজ:** Domain → IP resolution

```bash
# DNS query:
nslookup google.com

# Alternative:
dig google.com
```

---

## 💡 ল্যাব এক্সারসাইজ

```
১. তোমার কম্পিউটারের open port চেক করো:
   Windows: netstat -an | findstr LISTEN
   Linux:   ss -tln

২. একটি website-এর IP বের করো:
   ping google.com
   nslookup facebook.com

৩. TCP vs UDP বুঝতে:
   - Streaming video দেখো (UDP)
   - File download করো (TCP)
   - পার্থক্য অনুভব করো

৪. Common port scan করো নিজের local machine-এ:
   nmap localhost (যদি nmap থাকে)
```
---

## 📌 মনে রাখো

| Concept | মূল কথা |
|---------|---------|
| **OSI ৭ Layer** | Physical → Data Link → Network → Transport → Session → Present → Application |
| **TCP** | নির্ভরযোগ্য, ধীর | 
| **UDP** | দ্রুত, অনির্ভরযোগ্য |
| **Port** | নির্দিষ্ট service-এর দরজা |
| **LAN/MAN/WAN** | ছোট থেকে বড় network |
| **Common Ports** | 80(HTTP), 443(HTTPS), 22(SSH), 21(FTP), 3306(MySQL) |

**পরবর্তী অধ্যায়ে advanced networking concepts নিয়ে কথা বলব — ARP, DHCP, Firewall, Proxy! 🚀**
