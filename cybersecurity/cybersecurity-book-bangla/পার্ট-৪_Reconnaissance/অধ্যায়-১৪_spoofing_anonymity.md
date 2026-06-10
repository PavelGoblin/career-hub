# অধ্যায় ১৪: IP Spoofing, MAC Spoofing, Anonymity

## সহজ কথায়:
যখন তুমি匿名 (anonymous) থাকো, তখন কেউ জানে না তুমি কে। IP spoofing মানে নিজের IP লুকিয়ে অন্য IP দেখানো — যেন তুমি ছদ্মবেশ ধারণ করলে।

---

## ১৪.১ IP Spoofing — কীভাবে হয়

IP Spoofing = তোমার প্যাকেটের header-এ **Source IP বদলে দাও** যাতে মনে হয় অন্য কেউ পাঠাচ্ছে।

### কীভাবে কাজ করে:

```
আসল প্যাকেট:
[Source: তোমার IP] → [Dest: Target IP]

Spoofed প্যাকেট:
[Source: ভিকটিমের IP] → [Dest: Target IP]
```

### কোড উদাহরণ (Python — Scapy):
```python
#!/usr/bin/env python3
# IP spoofing demonstration — শুধু educational

from scapy.all import *

# target IP তে spoofed packet পাঠাও
target_ip = "192.168.1.10"     # target server
spoofed_ip = "10.0.0.1"        # fake source IP (ভিকটিম)

# IP layer spoofed
ip = IP(src=spoofed_ip, dst=target_ip)

# TCP SYN packet
tcp = TCP(sport=12345, dport=80, flags="S")

# Packet send
send(ip/tcp, verbose=0)

print(f"📦 Spoofed packet sent: {spoofed_ip} → {target_ip}:80")
```

### ⚠️ IP Spoofing-এর সীমাবদ্ধতা:
```
১. Response তোমার কাছে আসবে না (ভিকটিমের কাছে যাবে)
২. ISP-level filtering (many ISPs block spoofed packets)
৩. Modern networks use Ingress Filtering (BCP 38)
৪. TCP handshake complete করা যায় না (unless you're MITM)
```

### IP Spoofing যে ক্ষেত্রে কাজ করে:
```
✅ SYN Flood attack (response চাই না)
✅ DNS amplification (spoofed source)
✅ Non-IP-critical attacks
❌ Session hijacking (TCP sequence number লাগে)
```

---

## ১৪.২ MAC Spoofing — Practical কোড

MAC Spoofing = তোমার network card-এর MAC address বদলে দেওয়া।

### কেন দরকার?
```
- WiFi network block/ban → MAC change করে reconnect
- Network anonymity
- Bypass MAC filtering
- Impersonate another device
```

### Linux-এ MAC Spoofing:

```bash
# Step 1: Interface down
sudo ip link set eth0 down

# Step 2: MAC change
sudo ip link set eth0 address 00:11:22:33:44:55

# Step 3: Interface up
sudo ip link set eth0 up

# Step 4: Verify
ip link show eth0
```

### Using Macchanger (Kali-তে pre-installed):
```bash
# Install:
sudo apt install macchanger

# Random MAC:
sudo macchanger -r eth0

# Specific MAC:
sudo macchanger -m 00:11:22:33:44:55 eth0

# Original MAC back:
sudo macchanger -p eth0

# দেখো:
macchanger -s eth0
# Current MAC: 00:11:22:33:44:55
# Permanent MAC: aa:bb:cc:dd:ee:ff (original)
```

### Windows-এ MAC Spoofing:
```powershell
# Device Manager → Network Adapter
# Properties → Advanced → Network Address
# Value → নতুন MAC লিখো (12 digits, no dashes)
```

### Python Script — MAC Spoofer:
```python
#!/usr/bin/env python3
# MAC spoofing tool
import subprocess
import random
import re

def get_random_mac():
    """র্যান্ডম MAC address generate করো"""
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: f"{x:02x}", mac))

def change_mac(interface, new_mac):
    """MAC address change"""
    print(f"[+] Changing MAC for {interface} to {new_mac}")
    subprocess.run(["sudo", "ip", "link", "set", interface, "down"])
    subprocess.run(["sudo", "ip", "link", "set", interface, "address", new_mac])
    subprocess.run(["sudo", "ip", "link", "set", interface, "up"])

def get_current_mac(interface):
    """বর্তমান MAC বের করো"""
    result = subprocess.run(["ip", "link", "show", interface],
                           capture_output=True, text=True)
    mac_search = re.search(r"ether ([0-9a-f:]{17})", result.stdout)
    return mac_search.group(1) if mac_search else None

# ব্যবহার:
interface = "eth0"
original_mac = get_current_mac(interface)
print(f"[+] Original MAC: {original_mac}")

new_mac = get_random_mac()
change_mac(interface, new_mac)

current_mac = get_current_mac(interface)
print(f"[+] New MAC: {current_mac}")
```

---

## ১৪.৩ Psiphon ও VPN — কতটুকু নিরাপদ

### VPN কীভাবে কাজ করে:
```
তোমার PC → Encrypted Tunnel → VPN Server → Internet

VPN server তোমার real IP লুকায় → VPN server-এর IP দেখায়
```

### VPN-এর সীমাবদ্ধতা (যা VPN companies বলে না):
```
❌ VPN company তোমার traffic দেখতে পারে (logs রাখে?)
❌ কিছু VPN malware আছে (data sell করে)
❌ VPN ≠ anonymity (government VPN company-কে order দিতে পারে)
❌ DNS leak হতে পারে
❌ WebRTC leak (browser তোমার real IP leak করতে পারে)
❌ Free VPN → Almost always sells your data
```

### Trusted VPNs (২০২৫):
```
🟢 Mullvad — No logs, anonymous payment (cash/crypto)
🟢 ProtonVPN — Switzerland based, no logs
🟢 IVPN — No logs, open source clients
🟢 ExpressVPN — Fast, but more expensive
```

### Psiphon:
```bash
# Psiphon = circumvention tool (VPN + SSH + proxy)
# ভালো: Free, কাজ করে Bangladesh-এ
# খারাপ: Slow, no privacy guarantee
# Uses: Blocked content access (not for hacking)
```

### VPN Leak Test:
```bash
# VPN connect করার পর test করো:
# Browser এ:
https://ipleak.net
https://browserleaks.com/webrtc

# Check করো:
✓ IP changed? (তোমার দেশ না অন্য দেশ?)
✓ DNS leak? (ISP-র DNS দেখা যাচ্ছে?)
✓ WebRTC leak? (real IP browser-এ visible?)
```

---

## ১৪.৪ Tor Network — কীভাবে কাজ করে

Tor = The Onion Router। তিন layer encryption + three random nodes.

### Tor Architecture:
```
তোমার PC → Entry Node (গার্ড) → Middle Node → Exit Node → Target Website

প্রতি layer:
Layer 1: Encrypted to Entry Node (knows your IP, not destination)
Layer 2: Encrypted to Middle Node (knows neither)
Layer 3: Encrypted to Exit Node (knows destination, not your IP)
```

### Tor Browser ব্যবহার:
```bash
# Download: https://www.torproject.org/
# Extract → Start Tor Browser
```

### Command Line Tor:
```bash
# Install:
sudo apt install tor torsocks

# Start:
sudo systemctl start tor

# Tor দিয়ে curl:
torsocks curl ifconfig.me

# Tor দিয়ে nmap:
torsocks nmap -sT target.com

# Tor service status:
sudo systemctl status tor
```

### Onion Services (.onion):
```bash
# নিজের hidden service বানাও:
# /etc/tor/torrc — এডিট করো:

HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 80 127.0.0.1:80

# Restart tor:
sudo systemctl restart tor

# তোমার .onion address:
sudo cat /var/lib/tor/hidden_service/hostname
# Output: xyz123abc456.onion
```

### Tor Limitations:
```
❌ Slow (3 hops → latency বেশি)
❌ Exit node traffic monitor করা যায়
❌ Some sites block Tor exit nodes
❌ Not 100% anonymous (timing attacks possible)
❌ Don't download files via Tor (DNS leak)
```

---

## ১৪.5 Anonymity Setup — Complete Guide

### Maximum Anonymity Setup:

```
Step 1: Whonix (Two VM setup)
         - Gateway (Tor proxy) + Workstation (isolated)
         - সব traffic Tor-এর মাধ্যমে forced

Step 2: Tails OS (USB boot)
         - Amnesic (কিছু save থাকে না)
         - Boot → Use → Shutdown (কিছুই থাকে না)

Step 3: VPN + Tor (ঐচ্ছিক)
         - VPN → Tor (ISP দেখে VPN, Tor দেখে না)
         - Tor → VPN (VPN sees Tor, not your IP)
         - Controversial — some say less anonymous
```

### OPSEC (Operations Security) Rules:

```
✅ Use Whonix/Tails for sensitive work
✅ Never login to personal accounts
✅ Disable JavaScript (NoScript)
✅ Disable WebRTC (in browser)
✅ Use different identities for different tasks
✅ Clean metadata from files (exiftool)
✅ Use dedicated anonymous email
✅ Pay with crypto/Monero, never card

❌ Don't use same username across platforms
❌ Don't post recognizable information
❌ Don't upload photos with geolocation
❌ Don't use personal social media
```

### Check Your Anonymity:

```bash
# Terminals চেক:
# চেকলিস্ট:

1. whatismyip.com → IP changed?
2. ipleak.net → DNS leak?
3. browserleaks.com → WebRTC leak?
4. tor check: check.torproject.org → "Congratulations!"
5. whoer.net → anonymity score
```

---

## 💡 ল্যাব এক্সারসাইজ

```
🔰 MAC Spoofing (তোমার নিজের নেটওয়ার্কে):
১. তোমার current MAC বের করো: ip link show
২. Random MAC set করো: sudo macchanger -r eth0
৩. MAC change হয়েছে কিনা check করো
৪. Original MAC-এ ফিরে যাও

🔰 VPN Test:
৫. VPN connect করো (যদি থাকে)
৬. ipleak.net → check IP + DNS leak

🔰 Tor Browser:
৭. Tor Browser download + start
৮. check.torproject.org → "Congratulations" দেখো?
৯. Tor browser দিয়ে নিচের সাইট Visite করো:
    http://facebookcorewwwi.onion (Facebook onion)

🔰 Bonus:
১০. Whois anonymity check করো:
    তুমি কি complete anonymous? হ্যাঁ/না — কারণসহ।
```

---

## 📌 মনে রাখো

| Concept | কীভাবে কাজ করে | Level |
|---------|---------------|-------|
| **IP Spoofing** | Source IP change | ⚠️ Limited |
| **MAC Spoofing** | Network card ID change | ✅ Effective locally |
| **VPN** | Encrypted tunnel, IP change | ✅ Good, not 100% |
| **Tor** | 3-layer encryption, 3 nodes | ✅ Better anonymity |
| **Whonix/Tails** | Highest anonymity | 🥇 Best |
| **Psiphon** | Circumvention only | ❌ Not for privacy |

**পরবর্তী পার্ট — Attack Techniques! 🎯**
