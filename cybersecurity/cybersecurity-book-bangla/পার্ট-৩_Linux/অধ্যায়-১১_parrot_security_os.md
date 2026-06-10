# অধ্যায় ১১: Parrot Security OS

## সহজ কথায়:
Kali যদি AK-47 হয়, Parrot হলো স্নাইপার রাইফেল — হালকা, দ্রুত, আর anonymity-তে ভালো।

---

## ১১.১ Parrot OS কী?

Parrot Security OS হল Debian-ভিত্তিক Linux distribution যা **cybersecurity, anonymity, ও privacy**-র জন্য তৈরি।

**মূল বৈশিষ্ট্য:**
- Lightweight (MATE desktop — ১ GB RAM-এ চলে)
- ৪০০+ pre-installed security tools
- বিল্ট-ইন anonymity tools (Tor, Anonsurf, Firefox privacy)
- Forensic mode (বুট করার সময় forensic mode select)
- Full disk encryption support

---

## ১১.২ Kali-র সাথে তুলনা

| ফিচার | Kali Linux | Parrot OS |
|--------|-----------|-----------|
| **Base** | Debian Stable | Debian Testing (newer packages) |
| **Desktop** | Xfce (heavy) | MATE (lightweight) |
| **RAM Usage** | ~2 GB | ~1 GB |
| **Tools** | 600+ (heavy) | 400+ (curated, focused) |
| **Anonymity** | Optional | Built-in (Anonsurf) |
| **Forensic mode** | Yes (ডিফল্ট) | Yes (বুট মেনুতে) |
| **Tor pre-configured** | না | হ্যাঁ |
| **Update cycle** | Rolling (daily) | Rolling (weekly) |
| **Community** | 🥇 Largest | Smaller but active |
| **Best for** | Professional pentesting | Anonymity + pentesting |

### Performance Test (1 GB RAM):
```
Kali Boot:    2-3 মিনিট
Parrot Boot:  1-2 মিনিট
Kali Desktop: ২ GB লাগে smooth
Parrot Desktop: ১ GB-তেও চলে
```

---

## ১১.৩ কখন Parrot, কখন Kali

### Parrot ব্যবহার করো যখন:
```
✅ তোমার পুরনো ল্যাপটপ (4 GB RAM-ও)
✅ Anonymity প্রধান প্রয়োজন (default Tor)
✅ Pentest + daily driver (একই OS-এ সব)
✅ Lightweight environment চাও
✅ ডার্ক ওয়েব রিসার্চ
```

### Kali ব্যবহার করো যখন:
```
✅ সবচেয়ে বেশি tools লাগে
✅ Professional corporate pentesting
✅ সম্পূর্ণ toolset প্রয়োজন
✅ Latest exploits/test tools লাগে
✅ সমতা জন্য CTF
✅ তোমাকে OSCP দিতে হবে (Kali recommended)
```

### আমার Recommendation:
```
New users → Parrot (easy, lightweight)
একটু advanced → Kali (complete)
Anonymity চাইলে → Parrot
Daily OS চাইলে → Parrot (Kali daily driver হিসাবে heavy)
```

---

## ১১.৪ Parrot OS-এর বিশেষ Tools

### Anonsurf (One-click anonymity):
```bash
# Anonymity চালু:
sudo anonsurf start

# Tor circuit change:
sudo anonsurf change

# Stop anonymity:
sudo anonsurf stop

# Check status:
sudo anonsurf status
```

### Parrot-এর Unique Tools:
```
• Anonsurf      → System-wide Tor routing
• Firefox Privacy → Pre-configured privacy settings
• Onion Circuits → Tor circuit manager
• Tor Browser    → Pre-installed
• Cryptography tools → Full disk encryption
• Forensic Tools → Guymager, Foremost
```

### Wifiphase (WiFi auditing simplified):
```bash
# Parrot-এ WiFi audit tools সহজ করা
# একটি GUI tool যা aircrack-ng-এর wrapper
```

---

## ১১.৫ Parrot OS Install

Kali-র মতোই, কিন্তু আরো সহজ:

```bash
# 1. Download from:
https://parrotsec.org/download/

# 2. VirtualBox:
# New → Type: Linux, Version: Debian 64-bit
# RAM: 2048 MB (minimum 1024)
# Hard disk: 40 GB

# 3. Boot ISO → Graphical Install
# Steps similar to Kali

# 4. Update:
sudo apt update
sudo apt full-upgrade -y
```

### Install Security Tools (যদি কম লাগে):
```bash
# Metasploit:
sudo apt install metasploit-framework

# Nmap (already there):
sudo apt install nmap

# Burp Suite:
sudo apt install burpsuite

# Wireshark:
sudo apt install wireshark
```

---

## 💡 ল্যাব এক্সারসাইজ

```
১. Parrot OS দিয়ে VirtualBox-এ setup করো (যদি সময় থাকে)
২. Anonsurf চালাও → IP check করো (whatismyip.com)
৩. Anonsurf stop করো → IP check করো (পার্থক্য দেখো)
৪. কমান্ড চালাও:
   sudo anonsurf start
   curl ifconfig.me
   sudo anonsurf stop
   curl ifconfig.me
```

---

## 📌 মনে রাখো

| পার্থক্য | Kali | Parrot |
|----------|------|--------|
| **Tools** | 600+ | 400+ |
| **RAM** | 2 GB | 1 GB |
| **Desktop** | Xfce | MATE |
| **Anonymity** | Manual | Built-in |
| **Best use** | Pentesting | Anonymity + Pentesting |

**পার্ট ৪ শুরু হচ্ছে — Reconnaissance (তথ্য সংগ্রহ)! 🕵️**
