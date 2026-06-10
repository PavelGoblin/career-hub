# অধ্যায় ১৩: Active Reconnaissance (Nmap Bible)

## সহজ কথায়:
Passive reconnaissance ছিল চুপিসারে দেখা। Active reconnaissance মানে সরাসরি target-এর door bell বাজানো, window টোকা দেওয়া — কে respond করে দেখো।

---

## ১৩.১ Nmap — Network Mapper

Nmap = হ্যাকারদের সবচেয়ে বেশি ব্যবহৃত tool। **Port scan, OS detection, service version, script engine** — সবকিছু একসাথে।

### Install (যদি না থাকে):
```bash
# Kali/Parrot — pre-installed
# Ubuntu:
sudo apt install nmap

# Windows:
# https://nmap.org/download.html
```

### Nmap Basics:

```bash
# সবচেয়ে basic scan:
nmap 192.168.1.10

# Output:
# PORT     STATE  SERVICE
# 22/tcp   open   ssh
# 80/tcp   open   http
# 443/tcp  closed https
# 3306/tcp open   mysql
```

---

## ১৩.২ Scan Types (A-Z)

### 1. Basic Scan (TCP Connect)
```bash
# সবচেয়ে basic — TCP three-way handshake complete করে
nmap -sT 192.168.1.10
nmap -sT scanme.nmap.org

# কেন ব্যবহার করবে: Stealth না চাইলে, basic info
# অসুবিধা: Log হয়, ধরা পড়ার chance বেশি
```

### 2. SYN Scan (Stealth Scan) ⭐
```bash
# Half-open scan — handshake complete করে না (SYN → SYN-ACK → RST)
# Root permission লাগে
sudo nmap -sS 192.168.1.10

# কেন ব্যবহার করবে: Fast, stealthy
# Output:
# Starting Nmap... SYN Stealth Scan
# PORT     STATE         SERVICE
# 22/tcp   open          ssh
# 80/tcp   filtered      http (firewall block করছে)
# 443/tcp  open          https
```

### 3. UDP Scan
```bash
# UDP port scan (ধীর, কারণ UDP connectionless)
sudo nmap -sU 192.168.1.10
sudo nmap -sU -p 53,161,500 192.168.1.10  # specific ports

# কেন গুরুত্বপূর্ণ: DNS (53), SNMP (161), DHCP — সব UDP
```

### 4. OS Detection
```bash
# Target-এর operating system বের করে
sudo nmap -O 192.168.1.10

# Output:
# Device type: general purpose
# Running: Linux 3.X
# OS CPE: cpe:/o:linux:linux_kernel:3
# OS details: Linux 3.10 - 4.11

# আরো নির্ভুল:
sudo nmap -O --osscan-guess 192.168.1.10
```

### 5. Service Version Detection ⭐
```bash
# কোন service কোন version চালু আছে?
nmap -sV 192.168.1.10
nmap -sV -p 22,80 192.168.1.10  # specific port

# Output:
# PORT     STATE    SERVICE     VERSION
# 22/tcp   open     OpenSSH     7.2p2 Ubuntu
# 80/tcp   open     Apache      2.4.18
# 3306/tcp open     MySQL       5.7.28

# Version জানলে → exploit খোঁজা যায় (searchsploit)
```

### 6. Script Scan (NSE — Nmap Scripting Engine) ⭐⭐
```bash
# Default scripts:
nmap -sC 192.168.1.10

# Safety scripts:
nmap --script safe 192.168.1.10

# Vulnerability detection:
nmap --script vuln 192.168.1.10

# Specific script:
nmap --script http-enum 192.168.1.10
nmap --script ssh-brute 192.168.1.10
nmap --script smb-vuln-* 192.168.1.10  # SMB vulnerability

# HTTP title:
nmap --script http-title 192.168.1.10
```

### 7. Aggressive Scan
```bash
# সবকিছু একসাথে — OS + version + script + traceroute
nmap -A 192.168.1.10

# Same as:
nmap -O -sV -sC -traceroute 192.168.1.10
```

### 8. Fast Scan
```bash
# ১০০ common port scan (default ১০০০)
nmap -F 192.168.1.10
```

### 9. All Ports Scan
```bash
# সব ৬৫৫৩৫ port scan (খুব ধীর)
nmap -p- 192.168.1.10

# Faster — top ports:
nmap --top-ports 100 192.168.1.10
```

### 10. Ping Sweep (Live host খোঁজা)
```bash
# কোন host alive check
nmap -sn 192.168.1.0/24

# Without DNS resolution:
nmap -sn -n 192.168.1.0/24

# Output:
# Nmap done: 256 IP addresses (3 hosts up)
```

---

## ১৩.৩ Nmap Practical Examples

### Complete Recon:
```bash
# Full scan — target বুঝতে:
sudo nmap -sS -sV -sC -O -A 192.168.1.10 -p-

# Output analysis:
# ✓ কোন OS ব্যবহার করছে
# ✓ কোন ports open
# ✓ কোন services, কোন version
# ✓ কোন vulnerability থাকতে পারে
```

### Firewall Evasion Techniques:

```bash
# 1. Fragmentation (ছোট ছোট packet):
sudo nmap -f 192.168.1.10

# 2. Decoy scan (অনেক IP থেকে আসছে দেখাবে):
sudo nmap -D RND:10 192.168.1.10

# 3. Idle scan (zombie ব্যবহার):
sudo nmap -sI zombie_ip 192.168.1.10

# 4. Source port manipulation:
sudo nmap --source-port 53 192.168.1.10

# 5. Timing — slow scan (avoid detection):
sudo nmap -T2 192.168.1.10

# 6. Data length change:
sudo nmap --data-length 128 192.168.1.10

# 7. Randomize hosts:
sudo nmap --randomize-hosts 192.168.1.0/24
```

### Timing Templates:
```bash
-T0 = Paranoid (very slow, IDS evade)  # ৫ min+ per scan
-T1 = Sneaky (slow)
-T2 = Polite
-T3 = Normal (default)
-T4 = Aggressive (fast)
-T5 = Insane (very fast, could miss ports)
```

---

## ১৩.4 Nmap Timing & Performance

```bash
# Timeout calculation:
nmap -T4 -p 22,80,443 192.168.1.10

# Parallelism (কতগুলো host একসাথে):
nmap --min-parallelism 10 --max-parallelism 50 192.168.1.10

# Retries:
nmap --max-retries 2 192.168.1.10
```

---

## ১৩.5 Nmap Output Formats

```bash
# Normal output:
nmap -oN output.txt 192.168.1.10

# XML output (tools-এ import):
nmap -oX output.xml 192.168.1.10

# Greppable (grep-এ use):
nmap -oG output.gnmap 192.168.1.10

# All formats:
nmap -oA output 192.168.1.10

# Open ports only:
nmap --open 192.168.1.10
```

---

## ১৩.6 NSE Scripts (Category-wise)

```bash
# Category list দেখো:
ls /usr/share/nmap/scripts/ | head -50

# Popular categories:
nmap --script auth    192.168.1.10   # Authentication bypass
nmap --script brute   192.168.1.10   # Brute force
nmap --script exploit 192.168.1.10   # Exploit
nmap --script fuzzer  192.168.1.10   # Fuzzing
nmap --script malware 192.168.1.10   # Malware detect
nmap --script dos     192.168.1.10   # DoS check
nmap --script flood   192.168.1.10   # Flood tested?
nmap --script discovery 192.168.1.10 # Info discovery
```

### Specific Useful Scripts:

```bash
# HTTP enumeration:
nmap --script http-enum 192.168.1.10
# → admin panel, backup, directories খুঁজে বের করে

# HTTP methods:
nmap --script http-methods 192.168.1.10

# MySQL info:
nmap --script mysql-info 192.168.1.10

# SMB vulnerability:
nmap --script smb-vuln-ms17-010 192.168.1.10
# → EternalBlue vulnerability (WannaCry ransomware)

# SSL/TLS check:
nmap --script ssl-enum-ciphers -p 443 192.168.1.10

# FTP anonymous login:
nmap --script ftp-anon 192.168.1.10

# DNS zone transfer:
nmap --script dns-zone-transfer 192.168.1.10
```

---

## ১৩.7 Other Active Reconnaissance

### NetBIOS Enumeration (Windows Network):
```bash
# NetBIOS name lookup:
nmblookup -A 192.168.1.10

# Enum4linux (Samba/Linux):
enum4linux 192.168.1.10
```

### LDAP Enumeration:
```bash
# LDAP search (Active Directory):
ldapsearch -x -h 192.168.1.10 -b "dc=example,dc=com"
```

### DNS Enumeration:
```bash
# DNS zone transfer (misconfiguration খুঁজো):
dig @192.168.1.10 example.com AXFR

# DNS brute force subdomain:
dnsrecon -d example.com -D /usr/share/wordlists/dns.txt -t brt

# DNSenum:
dnsenum example.com
```

---

## ১৩.8 Nmap + Other Tools Combined

```bash
# Step 1: Live host find
nmap -sn 192.168.1.0/24 -oG live.txt

# Step 2: Open port scan
nmap -p 22,80,443 -iL live.txt -oG ports.txt

# Step 3: Service version
nmap -sV -iL ports.txt -oX version.xml

# Step 4: Vulnerability
nmap --script vuln -iL version.xml -oN vuln.txt
```

---

## 💡 ল্যাব এক্সারসাইজ

```
🔰 Metasploitable2 target-এ scan:
১. Metasploitable2 এর IP বের করো
২. Basic scan: nmap <Metasploitable_IP>
৩. SYN scan: sudo nmap -sS <Metasploitable_IP>
৪. Version scan: nmap -sV <Metasploitable_IP>
৫. OS detect: sudo nmap -O <Metasploitable_IP>
৬. Full: nmap -A <Metasploitable_IP>

🔰 Report:
৭. কতগুলো open port পেলে?
৮. কোন version-এ vulnerability আছে?
৯. OS কী?
১০. SMB vuln check: nmap --script smb-vuln* <Metasploitable_IP>
```

---

## 📌 মনে রাখো

| Scan Type | কমান্ড | কী কাজ করে |
|-----------|--------|-----------|
| **SYN Scan** | `-sS` | Stealth scan (root চাই) |
| **TCP Scan** | `-sT` | Full connect scan |
| **UDP Scan** | `-sU` | UDP port |
| **OS Detection** | `-O` | অপারেটিং সিস্টেম বের করে |
| **Version** | `-sV` | Service version |
| **Script** | `-sC` | NSE script run |
| **Aggressive** | `-A` | সবকিছু একসাথে |
| **All ports** | `-p-` | সব ৬৫৫৩৫ port scan |
| **Ping Sweep** | `-sn` | Live host খোঁজে |

**পরবর্তী অধ্যায় — IP Spoofing, MAC Spoofing, Anonymity! 🎭**
