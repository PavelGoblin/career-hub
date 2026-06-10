# অধ্যায় ১০: Kali Linux Setup ও প্রথম ব্যবহার

## সহজ কথায়:
Kali Linux হলো হ্যাকারের অস্ত্রাগার। এটা Install করার মানে ৬০০+ hacking tool একসাথে পাওয়া।

---

## ১০.১ VirtualBox-এ Kali Linux Install

VirtualBox দিয়ে তোমার Windows/Mac-এর **ভিতরে** আরেকটা কম্পিউটার চালাতে পারো।

### Step-by-Step:

**Step 1: VirtualBox Install**
```bash
# Browser-এ যাও:
https://www.virtualbox.org/
# Windows hosts → Download → Install
```

**Step 2: Kali Linux ISO Download**
```bash
# Browser-এ যাও:
https://www.kali.org/get-kali/
# Kali Linux 64-bit Installer → Download
# Size: ~3.5 GB
```

**Step 3: Virtual Machine Setup**
```
VirtualBox → New
নাম: Kali Linux
টাইপ: Linux
ভার্শন: Debian 64-bit
RAM: 4096 MB (মিনিমাম ২GB)
Hard Disk: 60 GB (Dynamic)
```

**Step 4: Install Kali**
```
১. VM Select → Start
২. ISO file select → Start
৩. Graphical Install → Enter
৪. Language: English → Continue
৫. Location: Bangladesh → Continue
৬. Hostname: kali → Continue
৭. Domain: (empty) → Continue
৮. Root password: (strong password) → Continue
৯. Partition: Guided - use entire disk → Continue
১০. All files in one partition → Continue
১১. Finish → Yes
১২. Network mirror: Yes → Continue
১৩. GRUB boot loader: Yes
১৪. Install complete → Reboot
```

**Step 5: Login**
```
Username: root
Password: (তোমার password)
```

### Post-Install Setup:
```bash
# System update
apt update && apt upgrade -y

# Guest Additions (better performance)
apt install -y virtualbox-guest-x11

# Kali tools install (full)
apt install -y kali-linux-headless

# Reboot
reboot
```

---

## ১০.২ Metasploitable2 Install (Target Machine)

Metasploitable2 = intentionally vulnerable Linux machine। এটাই হবে তোমার **practice target**। এতে hack করে শিখবে।

### Setup:
```bash
# 1. Download Metasploitable2:
# Browser: https://sourceforge.net/projects/metasploitable/
# File: Metasploitable2.zip (~800 MB)

# 2. Extract zip

# 3. VirtualBox:
# New → Name: Metasploitable2
# Type: Linux, Version: Ubuntu 64-bit
# RAM: 1024 MB
# Hard disk: Use existing → Metasploitable2.vmdk select

# 4. Network setting (গুরুত্বপূর্ণ):
# Settings → Network → Adapter 1:
# Attached to: Host-only Adapter
```

### দুই মেশিনের network setup:
```
তোমার PC (Windows): 192.168.56.1
Kali VM:             192.168.56.101 (DHCP)
Metasploitable VM:   192.168.56.102 (DHCP)

তিনটা device একই host-only network-এ আছে
```

### Test Connection:
```bash
# Kali-তে log in
# Metasploitable-কে ping দাও:
ping 192.168.56.102

# Output:
# PING 192.168.56.102 (192.168.56.102) 56(84) bytes of data.
# 64 bytes from 192.168.56.102: icmp_seq=1 ttl=64 time=1.02 ms
```

---

## ১০.৩ Android-এ Kali NetHunter (Root ছাড়া)

Kali NetHunter = Android phone-এ Kali।

### Requirements:
- Android phone (Android 9+)
- 4 GB+ RAM
- 64-bit processor
- কমপক্ষে ৫ GB ফ্রি স্পেস

### Termux দিয়ে Setup (Root ছাড়া):
```bash
# 1. Termux install করো Google Play থেকে

# 2. Termux-এ:
pkg update && pkg upgrade -y
pkg install -y wget curl git

# 3. NetHunter install:
apt install -y kali-nethunter

# 4. Start:
nethunter
```

### Root থাকলে (Full NetHunter):
```bash
# Official image download:
# https://www.kali.org/get-kali/#kali-mobile

# Custom ROM প্রয়োজন হতে পারে
# OnePlus, Pixel devices ভালো support করে
```

**সীমাবদ্ধতা:** Root ছাড়া WiFi hacking (monitor mode) কাজ করে না।

---

## ১০.৪ WSL-এ Kali Linux (Windows-এ)

Windows Subsystem for Linux (WSL) — Windows-এ সরাসরি Linux চালাও, VM ছাড়া!

### Setup:
```powershell
# PowerShell (Admin) এ:
# Step 1: WSL চালু করো
wsl --install

# Step 2: Kali install
wsl --install -d kali-linux

# Step 3: Restart

# Step 4: প্রথমবার open করলে username/password দেবে

# Step 5: Update
sudo apt update && sudo apt upgrade -y

# Step 6: Tools install (যদিও অনেক tool GUI ছাড়া কাজ করে না)
sudo apt install -y nmap metasploit-framework hydra john
```

### WSL Limitations for Hacking:
```
❌ No GUI (X server লাগবে)
❌ No monitor mode (WiFi)
❌ No USB device access
✅ Command line tools কাজ করে (nmap, hydra, metasploit)
```

---

## ১০.৫ Network Configuration

### Host-only Network:
Kali + Metasploitable একসাথে, কিন্তু host Windows থেকে আলাদা।

**Use case:** Lab practice (তোমার main internet access থাকবে কিন্তু VM-গুলো আলাদা net-এ)

```bash
# Kali-তে IP check:
ip a
# দেখবে eth0: 192.168.56.101

# Metasploitable-তে:
ifconfig
# দেখবে eth0: 192.168.56.102
```

### NAT Network:
সব VM internet পাবে, কিন্তু host Windows থেকে আলাদা।

**Use case:** যখন internet লাগবে কিন্তু VM isolated রাখতে চাও

```bash
# Setup:
# VirtualBox → File → Preferences → Network → NAT Networks → Create
# VM settings → Network → NAT Network
```

### Bridged Network:
VM = তোমার network-এর আরেকটা device (এর নিজস্ব IP)।

**Use case:** ভাইরাস analysis, WiFi hacking, real pentesting

```bash
# VM settings → Network → Bridged
# VM তোমার router থেকে IP পাবে (192.168.0.xxx)
```

---

## 📌 মনে রাখো

| Setup | যখন ব্যবহার করবে |
|-------|-----------------|
| **VirtualBox + Kali** | সবচেয়ে ভালো option |
| **Metasploitable2** | Practice target (legal hack) |
| **NetHunter** | Mobile pentesting |
| **WSL Kali** | Quick command-line |
| **Host-only** | Lab (isolated) |
| **NAT** | Internet + isolation |
| **Bridged** | Full network integration |

**পরবর্তী — Parrot Security OS! 🦜**
