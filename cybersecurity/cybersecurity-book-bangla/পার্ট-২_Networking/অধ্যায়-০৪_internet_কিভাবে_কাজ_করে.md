# অধ্যায় ৪: Internet কীভাবে কাজ করে

## সহজ কথায়:
Internet হলো বিশাল একটা ডাকবিভাগ। তুমি চিঠি পাঠাও (data packet), পোস্টম্যান (router) ঠিকানায় পৌঁছে দেয়, আর উত্তর আসে। IP address হলো তোমার ঠিকানা।

---

## ৪.১ IP Address: Public vs Private, Static vs Dynamic

### IP Address (Internet Protocol Address)
প্রতিটি ডিভাইসের একটি **ইউনিক নাম্বার** থাকে internet-এ — এটাই IP address।

**ঠিক যেমন:** তোমার বাড়ির ঠিকানা। কেউ যদি তোমাকে চিঠি দিতে চায়, ঠিকানা লাগবে। ডেটা পাঠাতেও IP লাগে।

### IP Address-এর দুই ভার্শন:

| ভার্শন | ফরম্যাট | উদাহরণ | মোট address |
|---------|---------|---------|------------|
| **IPv4** | xxx.xxx.xxx.xxx | 192.168.1.1 | ৪.৩ বিলিয়ন (ফুরিয়ে যাচ্ছে) |
| **IPv6** | xxxx:xxxx:xxxx:... | 2001:db8::1 | অসীম (প্রায়) |

### Public vs Private IP

| টাইপ | কী | উদাহরণ | কে দেখে? |
|------|-----|---------|---------|
| **Public IP** | Internet-এ visible | 103.25.xx.xx | সবাই দেখতে পারে |
| **Private IP** | লোকাল network-এর ভিতর | 192.168.1.x | শুধু তুমি ও তোমার router |

**Real life analogy:**
- Public IP = তোমার বিল্ডিং এর ঠিকানা (বাইরে থেকে দেখা যায়)
- Private IP = তোমার ফ্ল্যাট নাম্বার (বিল্ডিং এর ভিতরেই বলা হয়)

### Static vs Dynamic IP

| টাইপ | পরিবর্তন হয়? | খরচ | কে ব্যবহার করে? |
|------|--------------|------|----------------|
| **Static** | না, কখনো বদলায় না | বেশি (~500 টাকা/মাস) | Server, website, company |
| **Dynamic** | সময়ে সময়ে বদলায় | ফ্রি (ISP দেয়) | সাধারণ user |

---

## ৪.২ IP Tracking — কীভাবে হয়, কীভাবে বাঁচবে

### IP Tracking কীভাবে হয়?
```
তুমি ওয়েবসাইট Visite করলে → তোমার IP server-এ log হয়
সার্ভার অপারেটর → ISP-কে বলে "এই IP কে ব্যবহার করছে?"
ISP → তোমার তথ্য দেয় (পুলিশের আদেশ থাকলে)
```

### তোমার IP দিয়ে কী কী জানা যায়?
```
✅ তোমার শহর / এলাকা (approx)
✅ তোমার ISP (Grameenphone, Robi, ইত্যাদি)
✅ তোমার OS ও browser (browser fingerprinting)

❌ তোমার সঠিক বাড়ির ঠিকানা (directly না)
❌ তোমার নাম (না)
❌ তোমার ফোন নাম্বার (না)
```

### 🔐 কীভাবে বাঁচবে (Anonymity Techniques):
1. **VPN** — তোমার IP লুকিয়ে VPN server-এর IP দেখায়
2. **Tor** — আরো বেশি anonymous (৩ layer encryption)
3. **Proxy** — basic hiding (VPN-এর চেয়ে কম secure)
4. **Public WiFi** — অন্য network-এ connect করলে IP বদলায়

> ভাই সাবধান! VPN সবার জন্য ভালো না। ফ্রি VPN ডেটা চুরি করে! ভালো paid VPN ব্যবহার করো।

---

## ৪.৩ MAC Address — কী, কীভাবে Track করে

### MAC Address (Media Access Control)
প্রতি নেটওয়ার্ক ডিভাইসের (WiFi card, Ethernet port) একটি **হার্ডওয়্যার ঠিকানা** থাকে — একে MAC address বলে।

```
MAC address এর ফরম্যাট: 00:1A:2B:3C:4D:5E
                         6 জোড়া হেক্সাডেসিমেল নাম্বার
```

### IP vs MAC:

| জিনিস | পরিবর্তনযোগ্য? | কী কাজে লাগে? |
|-------|----------------|---------------|
| IP Address | ✅ সহজে change করা যায় | ইন্টারনেটে রাউটিং |
| MAC Address | ❌ Hardware-এ burned-in (কিন্তু software-এ change করা যায়) | লোকাল network-এ Identification |

### MAC Address Tracking:
- তোমার WiFi network-এ router তোমার MAC address জানে
- Coffee shop, airport-এর WiFiও MAC address track করে
- **MAC spoofing** — MAC address change করে anonymity maintain

---

## ৪.৪ DNS, Domain, Server

### Domain Name
মানুষ মনে রাখতে পারে না 103.25.x.x এর মত নাম্বার। তাই আমরা ব্যবহার করি **domain name**।

```
google.com          → IP: 142.250.xx.xx
facebook.com        → IP: 31.13.xx.xx
youtube.com         → IP: 173.194.xx.xx
```

### DNS (Domain Name System)
DNS হলো **ফোনবুক** — domain name → IP address অনুবাদ করে।

**Real life analogy:** তুমি বলো "আমি রহিমকে কল করতে চাই" — ফোনবুক খুঁজে রহিমের নাম্বার বের করো। DNS-ও তেমন — তুমি বলো "google.com", DNS খুঁজে IP বের করে দেয়।

### DNS কীভাবে কাজ করে (step by step):
```
তুমি browser-এ লেখো: www.google.com
         ↓
1. Browser first checks local cache (আগে জানলে)
         ↓
2. Recursive DNS resolver (ISP / Google DNS 8.8.8.8)
         ↓
3. Root DNS server (কে .com manage করে?)
         ↓
4. TLD DNS server (.com server বলে "google.com যায় কোথায়")
         ↓
5. Authoritative DNS server (Google-র নিজের DNS)
         ↓
6. IP পেয়ে গেলে → browser-এ load হয়
```

### DNS Record Types:
| টাইপ | কী ধারণ করে | উদাহরণ |
|------|------------|--------|
| **A** | IPv4 address | google.com → 142.250.80.46 |
| **AAAA** | IPv6 address | google.com → 2a00:1450:4001:82b::200e |
| **CNAME** | Canonical name (alias) | www.google.com → google.com |
| **MX** | Mail server | @google.com → mail server |
| **TXT** | Text data (verification) | SPF, DKIM records |

### Server কী?
Server = একটা কম্পিউটার যা ২৪/৭ চলে, আর অন্যদের service দেয়।

```
তুমি → google.com request পাঠালে
         ↓
Google-র server → response হিসেবে webpage পাঠায়
         ↓
তুমি browser-এ webpage দেখো
```

---

## ৪.৫ How Internet Works: ISP → Router → তোমার ডিভাইস

### সম্পূর্ণ চিত্র:

```
তুমি (ল্যাপটপ/ফোন)
    ↕ WiFi/Ethernet
Router (ঘরে)
    ↕
ISP (Grameenphone/Robi/Airtel)
    ↕ Fiber/Optical cable / 4G Tower
Internet Backbone (বিশাল ফাইবার অপটিক কেবল)
    ↕
Google Server (যেখানে data রাখা)
```

### Step-by-step:
```
1. তুমি browser এ লেখো "facebook.com"
2. Router router-এ যায়
3. Router ISP-তে পাঠায়
4. ISP DNS-এ জিজ্ঞেস করে "facebook.com কোথায়?"
5. DNS বলে "IP: 31.13.71.36"
6. তোমার request internet backbone দিয়ে Facebook server-এ যায়
7. Facebook server তোমার request process করে
8. Facebook profile page এর data (HTML, CSS, JS, images) 
   → packet আকারে ভাগ হয়
9. সব packet internet দিয়ে ফিরে আসে
10. Router packet গুলো তোমার ল্যাপটপে দেয়
11. Browser সব packet জুড়ে webpage দেখায়
```

### ব্যাখ্যা (ডাক বিভাগ analogy):
```
তুমি বন্ধুকে চিঠি লিখলে:
① চিঠি লিখো → Data (তোমার request)
② খামে দিয়ে ঠিকানা লেখো → IP + Port
③ পোস্ট অফিসে দিয়ে দাও → Router
④ পোস্ট অফিস সর্ট করে → ISP routing
⑤ ট্রেন/প্লেনে করে পাঠায় → Internet backbone
⑥ বন্ধুর পোস্ট অফিস → Destination router
⑦ বন্ধু পায় → Server
⑧ বন্ধু উত্তর দেয় → Response
```

---

## ৪.6 Packet Switching (Internet-এর ম্যাজিক)

Internet-এ ডেটা একসাথে যায় না। **প্যাকেট** আকারে ভাগ হয়।

```
তুমি ১০০ পৃষ্ঠার বই পাঠাতে চাও:
→ ১০০ পাতা আলাদা করে → প্রতিটা আলাদা খামে → আলাদা পথে → গন্তব্যে জোড়া
```

**Packet-এ কী থাকে:**
```
┌─────────────────────────────────┐
│         Header                  │
│  Source IP: তোমার IP           │
│  Dest IP: Facebook Server       │
│  Sequence Number: প্যাকেট নং    │
│  TTL (Time To Live)             │
├─────────────────────────────────┤
│         Data                    │
│  তোমার request/data-র অংশ      │
└─────────────────────────────────┘
```

---

## ৪.7 Traceroute — Packet-এর পথ দেখা

তোমার packet কোন পথে যায় — সেটা traceroute দিয়ে দেখা যায়।

**কমান্ড (তোমার কম্পিউটারে):**
```bash
# Windows-এ CMD তে:
tracert google.com

# Linux/Mac-এ terminal-এ:
traceroute google.com
```

**Output কেমন হবে:**
```
tracert google.com

  1     1ms     2ms     1ms  192.168.1.1 (router)
  2    10ms    12ms    10ms  103.25.x.x (ISP gateway)
  3    15ms    15ms    14ms  103.x.x.x (ISP backbone)
  4    40ms    42ms    41ms  72.14.x.x (Google network)
  5    42ms    41ms    42ms  google.com (142.250.xx.xx)
```

প্রতি line-এ হলো **একটি router** যার মাধ্যমে packet গেছে। latency দেখা যায় প্রতিটা hop-এ কত সময় নিচ্ছে।

---

## 💡 ল্যাব এক্সারসাইজ

```
১. তোমার নিজের IP বের করো:
   Windows: CMD → ipconfig
   Linux:   terminal → ip a

২. Public IP বের করো:
   browser → whatismyip.com

৩. DNS resolution test:
   website: https://dns.google/
   search: "google.com"
   দেখো কত IP আসে

৪. Traceroute চালাও:
   Windows: tracert google.com
   Linux:   traceroute google.com
   দেখো কতগুলো hop আছে
```

---

## 📌 মনে রাখো

| Concept | সারমর্ম |
|---------|---------|
| **IP Address** | Internet-এ তোমার ঠিকানা |
| **Public IP** | বাইরে থেকে দেখা যায় |
| **Private IP** | শুধু বাসার ভিতর |
| **MAC Address** | Hardware ID (Network card-এর) |
| **DNS** | Domain → IP translator |
| **Server** | ২৪/৭ চলা service-giving computer |
| **Packet** | ছোট ছোট ভাগে data ভ্রমণ |
| **TTL** | প্যাকেট কতক্ষণ বাঁচবে |

**পরবর্তী অধ্যায়ে আমরা networking fundamentals-এ ডুব দেব — OSI model, TCP/IP, ports, protocols! 🌐**
