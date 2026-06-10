# অধ্যায় ৩৯: Hardening

> ভাই, হার্ডেনিং মানে হলো তোমার সিস্টেমকে এত শক্ত করা যে হ্যাকারের মাথা খারাপ হয়ে যাবে। ডিফল্ট সেটিংসে সিস্টেম রাখা মানে চোরকে দরজা খুলে দিয়ে বলা "আরে ভিতরে আসো"। এই অধ্যায়ে Linux, Windows, আর Web Server হার্ডেনিং শিখবো।

---

## ৩৯.১ Linux Server Hardening

লিনাক্স সার্ভার শক্ত করতে নিচের স্টেপগুলো ফলো করো।

### ১. SSH সুরক্ষা

```bash
# ===== SSH কনফিগারেশন =====

# SSH কনফিগ ফাইল
sudo nano /etc/ssh/sshd_config

# এই সেটিংস পরিবর্তন করো:

Port 2222                    # ডিফল্ট ২২ না — হ্যাকাররা ২২ স্ক্যান করে
PermitRootLogin no           # রুট দিয়ে সরাসরি লগইন বন্ধ — বড় ভুল!
PasswordAuthentication no    # পাসওয়ার্ড না — শুধু SSH কী
PubkeyAuthentication yes     # SSH কী ইউজ করো
MaxAuthTries 3               # সর্বোচ্চ ৩ বার চেষ্টা
ClientAliveInterval 300      # ৫ মিনিট নিষ্ক্রিয় থাকলে ডিসকানেক্ট
ClientAliveCountMax 2        # ২ বার পিং করবে, তারপর কেটে দেবে
AllowUsers bhai              # শুধু "bhai" ইউজার SSH করতে পারবে
Protocol 2                   # শুধু SSHv2 (v1 অনিরাপদ)

# চেঞ্জ করার পর রিস্টার্ট
sudo systemctl restart sshd
```

### ২. SSH কী তৈরি

```bash
# তোমার লোকাল মেশিনে কী জেনারেট করো
ssh-keygen -t ed25519 -C "bhai-server-2026"

# পাবলিক কী সার্ভারে কপি করো
ssh-copy-id -p 2222 bhai@server-ip

# এখন পাসওয়ার্ড ছাড়া লগইন হবে
ssh -p 2222 bhai@server-ip
```

### ৩. ইউজার ও পারমিশন ম্যানেজমেন্ট

```bash
# ===== ইউজার ম্যানেজমেন্ট =====

# প্রতিটা সার্ভিসের জন্য আলাদা ইউজার
sudo useradd -m -s /bin/bash nginx_user   # Nginx এর জন্য
sudo useradd -m -s /bin/bash db_user      # Database এর জন্য

# ইউজারকে sudo গ্রুপে না দেওয়া
sudo usermod -aG nginx_user nginx_user    # শুধু নিজের গ্রুপে

# ফাইল পারমিশন ঠিক করা
chmod 600 ~/.ssh/authorized_keys          # শুধু মালিক পড়তে পারবে
chmod 700 ~/.ssh                          # ডিরেক্টরি
chmod 750 /etc/nginx/conf.d               # গ্রুপ পড়তে পারে, অন্যরা না
```

### ৪. ফায়ারওয়াল (UFW — Uncomplicated Firewall)

```bash
# ===== UFW ফায়ারওয়াল সেটআপ =====

sudo ufw default deny incoming   # সব ইনকামিং ব্লক — ডিফল্ট!
sudo ufw default allow outgoing  # আউটগোয়িং অনুমতি

sudo ufw allow 2222/tcp          # SSH পোর্ট (যা সেট করেছি)
sudo ufw allow 80/tcp            # HTTP
sudo ufw allow 443/tcp           # HTTPS

sudo ufw enable                  # ফায়ারওয়াল চালু
sudo ufw status verbose          # স্ট্যাটাস দেখা
```

### ৫. ফাইল ইন্টেগ্রিটি চেক (AIDE)

```bash
# AIDE — ফাইলের পরিবর্তন ট্র্যাক করে
sudo apt install aide -y

# ডাটাবেস তৈরি (প্রথমবার)
sudo aideinit
sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# চেক করা
sudo aide --check
# যদি কোনো ফাইল পরিবর্তন হয়, রিপোর্ট দেখাবে
```

### ৬. অটোমেটিক আপডেট

```bash
# ===== সিকিউরিটি আপডেট অটোমেটিক =====

sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades

# শুধু সিকিউরিটি আপডেট
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
# Unattended-Upgrade::Allowed-Origins {
#     "${distro_id}:${distro_codename}-security";
# };
```

### ৭. লিনাক্স হার্ডেনিং চেকলিস্ট (সাত সতের):

```bash
#!/bin/bash
# ===== লিনাক্স হার্ডেনিং অটোমেটেড চেক =====

echo "===== হার্ডেনিং চেক রিপোর্ট ====="
echo ""

# ১. রুট SSH লগইন বন্ধ?
echo "১. রুট SSH লগইন:"
grep "^PermitRootLogin" /etc/ssh/sshd_config

# ২. খোলা পোর্ট?
echo ""
echo "২. খোলা পোর্ট (লিসেনিং):"
ss -tlnp

# ৩. অপ্রয়োজনীয় সার্ভিস?
echo ""
echo "৩. চলমান সার্ভিস:"
systemctl list-units --type=service --state=running | head -20

# ৪. পাসওয়ার্ড পলিসি?
echo ""
echo "৪. পাসওয়ার্ড পলিসি:"
grep -E "PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_MIN_LEN" /etc/login.defs

# ৫. ফায়ারওয়াল চলছে?
echo ""
echo "৫. ফায়ারওয়াল স্ট্যাটাস:"
ufw status 2>/dev/null || echo "UFW ইনস্টল করা নেই!"
```

---

## ৩৯.২ Windows Hardening

### ১. ইউজার অ্যাকাউন্ট কন্ট্রোল (UAC)

```powershell
# ===== UAC সর্বোচ্চ লেভেলে সেট করো =====

# রেজিস্ট্রি দিয়ে UAC লেভেল সেট
New-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" `
    -Name "EnableLUA" -Value 1 -PropertyType DWord -Force

# UAC লেভেল: Always notify (লেভেল ২)
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" `
    -Name "ConsentPromptBehaviorAdmin" -Value 2
```

### ২. উইন্ডোজ ডিফেন্ডার সর্বোচ্চ

```powershell
# ===== উইন্ডোজ ডিফেন্ডার কনফিগ =====

# রিয়েল-টাইম প্রটেকশন চালু
Set-MpPreference -DisableRealtimeMonitoring $false

# ক্লাউড-ডেলিভারড প্রটেকশন চালু
Set-MpPreference -MAPSReporting Advanced

# PUA (Potentially Unwanted Apps) ব্লক
Set-MpPreference -PUAProtection Enabled

# অ্যাটাক সারফেস রিডাকশন রুল (ASR)
Add-MpPreference -AttackSurfaceReductionRules_Ids `
    "56a863a9-875e-4185-98a7-b882c64b5ce5" `
    -AttackSurfaceReductionRules_Actions Enabled
```

### ৩. লোকাল সিকিউরিটি পলিসি

```powershell
# ===== পাসওয়ার্ড পলিসি =====

# পাসওয়ার্ড জটিলতা
net accounts /minpwlen:14          # ন্যূনতম ১৪ অক্ষর
net accounts /maxpwage:30          # ৩০ দিন পর পরিবর্তন
net accounts /minpwage:1           # ১ দিন আগে আবার চেঞ্জ করা যাবে না
net accounts /lockoutthreshold:5   # ৫ বার ভুল = লক
net accounts /lockoutduration:30   # ৩০ মিনিট লক

# গেস্ট অ্যাকাউন্ট বন্ধ
Disable-LocalUser -Name "Guest"

# এডমিনিস্ট্রেটর রিনেম
Rename-LocalUser -Name "Administrator" -NewName "bhai_admin_2026"
```

### ৪. উইন্ডোজ ফায়ারওয়াল

```powershell
# ===== উইন্ডোজ ফায়ারওয়াল =====

# ডিফল্ট ব্লক
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# নির্দিষ্ট পোর্ট ওপেন
New-NetFirewallRule -DisplayName "SSH অনুমতি" `
    -Direction Inbound -Protocol TCP -LocalPort 22 -Action Allow

# RDP পোর্ট চেঞ্জ
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" `
    -Name "PortNumber" -Value 3399
```

### ৫. অপ্রয়োজনীয় সার্ভিস বন্ধ

```powershell
# ===== অপ্রয়োজনীয় সার্ভিস বন্ধ =====

$অপ্রয়োজনীয়_সার্ভিস = @(
    "RemoteRegistry",       # রিমোট রেজিস্ট্রি এক্সেস
    "Telnet",               # অনিরাপদ প্রোটোকল
    "FTPSVC",               # FTP (যদি না লাগে)
    "lfsvc"                 # জিওলোকেশন
)

foreach ($svc in $অপ্রয়োজনীয়_সার্ভিস) {
    Set-Service -Name $svc -StartupType Disabled
    Stop-Service -Name $svc -Force
    Write-Host "বন্ধ করা হয়েছে: $svc"
}
```

---

## ৩৯.৩ Web Server Hardening (Apache/Nginx)

### Apache Hardening:

```bash
# ===== অ্যাপাচি সুরক্ষা =====

# ১. সার্ভার সংস্করণ লুকানো
sudo nano /etc/apache2/conf-enabled/security.conf

ServerTokens Prod              # শুধু "Apache" দেখাবে, ভার্সন না
ServerSignature Off            # এরর পেজে ভার্সন দেখাবে না
TraceEnable Off                # TRACE মেথড বন্ধ (XSS ঝুঁকি)

# ২. ডিরেক্টরি লিস্টিং বন্ধ
# <Directory /var/www/html>
#     Options -Indexes          # ফাইল লিস্টিং বন্ধ
# </Directory>

# ৩. HTTP নিরাপদ হেডার
sudo nano /etc/apache2/sites-available/default-ssl.conf

<IfModule mod_headers.c>
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "DENY"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set Content-Security-Policy "default-src 'self'"
</IfModule>

# ৪. .htaccess ফাইল সুরক্ষা
# <FilesMatch "^\.ht">
#     Require all denied
# </FilesMatch>

# ৫. মডিউল লিমিট
sudo a2dismod autoindex        # ডিরেক্টরি ইনডেক্সিং বন্ধ
sudo a2dismod status           # সার্ভার স্ট্যাটাস বন্ধ
sudo a2dismod info             # সার্ভার ইনফো বন্ধ
sudo a2enmod headers           # HTTP হেডার জন্য
sudo a2enmod ssl               # HTTPS

# রিস্টার্ট
sudo systemctl restart apache2
```

### Nginx Hardening:

```bash
# ===== Nginx সুরক্ষা =====

# ১. সার্ভার টোকেন লুকানো
sudo nano /etc/nginx/nginx.conf

server_tokens off;             # ভার্সন নম্বর লুকাও
more_set_headers "Server: Hidden";  # সার্ভারের নাম লুকাও (যদি ngx_headers_more থাকে)

# ২. HTTP নিরাপদ হেডার
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self'" always;

# ৩. ক্লায়েন্ট বডি সাইজ লিমিট
client_max_body_size 10M;      # ১০ মেগাবাইটের বেশি ফাইল আপলোড নয়
client_body_timeout 10;        # ১০ সেকেন্ডে বডি না এলে কেটে দাও
client_header_timeout 10;

# ৪. রেট লিমিটিং — ব্রুটফোর্স ঠেকাও
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

location /wp-login.php {
    limit_req zone=login burst=3 nodelay;
    # প্রতি মিনিটে ৫ বার, আকস্মিক ৩ বার পর্যন্ত
}

# ৫. ব্লকড ইউজার-এজেন্ট
if ($http_user_agent ~* (curl|python|nikto|sqlmap) ) {
    return 403;
}

# ৬. SLL কনফিগ
ssl_protocols TLSv1.2 TLSv1.3;   # শুধু নিরাপদ TLS
ssl_ciphers HIGH:!aNULL:!MD5;    # শক্তিশালী সাইফার
ssl_prefer_server_ciphers on;

# রিস্টার্ট
sudo nginx -t                    # কনফিগ টেস্ট
sudo systemctl restart nginx
```

### Web Server Hardening — চেকলিস্ট:

```
□ সার্ভার ভার্সন লুকানো (ServerTokens/ServerSignature)
□ ডিরেক্টরি লিস্টিং বন্ধ
□ HTTPS বাধ্যতামূলক (HSTS)
□ HTTP নিরাপদ হেডার (XSS, CSP, X-Frame-Options)
□ ফাইল আপলোড সাইজ লিমিট
□ রেট লিমিটিং
□ SQL Injection প্রিভেনশন (WAF?)
□ অপ্রয়োজনীয় HTTP মেথড বন্ধ (TRACE, DELETE)
□ SSL/TLS — শুধু আধুনিক ভার্সন
□ রেগুলার আপডেট
```

---

## ৩৯.৪ কীভাবে বাঁচবে

| কী করবে | কেন করবে |
|----------|----------|
| SSH কী ইউজ করো, পাসওয়ার্ড না | পাসওয়ার্ড ব্রুটফোর্স করা যায়, SSH কী-র প্রাইভেট কী চাই |
| রুট SSH বন্ধ করো | রুটের পূর্ণ ক্ষমতা — হ্যাকার পেলে সর্বনাশ |
| ন্যূনতম সার্ভিস (Minimal) | যত কম সার্ভিস, তত কম অ্যাটাক সারফেস |
| অটোমেটিক আপডেট | পুরনো সফটওয়্যার = জানা দুর্বলতা |
| হার্ডেনিং চেকলিস্ট ফলো করো | কিছু ভুলে যাওয়া স্বাভাবিক, চেকলিস্ট বাঁচায় |
| ফাইল ইন্টেগ্রিটি মনিটর (AIDE/Tripwire) | কেউ ফাইল বদলালে জানতে পারবে |
| নিয়মিত অডিট | প্রতি মাসে একবার হার্ডেনিং চেক করো |

---

## ৩৯.৫ ল্যাব এক্সারসাইজ

### টাস্ক ১: SSH সুরক্ষা
```bash
# SSH পোর্ট ২২২২ এ চেঞ্জ করো
# রুট লগইন বন্ধ করো
# কী-অনলি অথেনটিকেশন সেট করো
# চেক করো: nmap -p 22 <server> — ২২ বন্ধ দেখাবে?
```

### টাস্ক ২: UFW ফায়ারওয়াল
```bash
# UFW সক্রিয় করো
# শুধু ৮০, ৪৪৩, আর তোমার SSH পোর্ট ওপেন রাখো
# অন্য পোর্ট থেকে কানেক্ট করে দেখো — ব্লক হচ্ছে কিনা
```

### টাস্ক ৩: অ্যাপাচি সুরক্ষা
```bash
# অ্যাপাচি ইন্সটল করো
# সার্ভার টোকেন লুকাও
# HTTP হেডার অ্যাড করো (XSS, CSP, HSTS)
# curl -I http://localhost — হেডার চেক করো
```

### টাস্ক ৪: উইন্ডোজ হার্ডেনিং
```bash
# গেস্ট অ্যাকাউন্ট ডিজেবল করো
# পাসওয়ার্ড পলিসি শক্ত করো (১৪ অক্ষর, ৩০ দিন)
# অপ্রয়োজনীয় সার্ভিস বন্ধ করো
# ফায়ারওয়াল এনাবল করো
```

### টাস্ক ৫: হার্ডেনিং অডিট স্ক্রিপ্ট
```bash
# একটা ব্যাশ/পাওয়ারশেল স্ক্রিপ্ট লেখো যা:
# - ওপেন পোর্ট চেক করে
# - রুট SSH লগইন চেক করে
# - অপ্রয়োজনীয় সার্ভিস চেক করে
# - ফায়ারওয়াল স্ট্যাটাস চেক করে
# আর ফলাফল রিপোর্ট আকারে দেখায়
```

---

## মনে রাখো

| ধারণা | সংক্ষেপ | বাংলায় |
|--------|---------|--------|
| **SSH Hardening** | পোর্ট চেঞ্জ, কী-অনলি, রুট নিষিদ্ধ | চোরের জন্য দরজা শক্ত করা |
| **UFW/Firewall** | ডিফল্ট ডিনাই | যা দাওনি, ওপেন না |
| **Server Tokens** | ভার্সন লুকানো | "আমার দুর্বলতা জানতে চাস? না পাবি!" |
| **HTTP Headers** | XSS, HSTS, CSP, X-Frame | ব্রাউজার লেভেলে সুরক্ষা |
| **AIDE/Tripwire** | ফাইল ইন্টেগ্রিটি চেক | কেউ কিছু বদলালে এলার্ম |
| **Rate Limiting** | ব্রুটফোর্স ঠেকানো | ১ মিনিটে ১ লাখ রিকোয়েস্ট নয় |
| **Minimal Service** | অনাবশ্যক সার্ভিস বন্ধ | যত কম দরজা, তত কম ঝুঁকি |

---

> **ভাইয়ের মেসেজ:** হার্ডেনিং বিরক্তিকর কাজ — কিন্তু সবচেয়ে কার্যকরী। আমি নিজের প্রথম সার্ভারে "শুধু পাসওয়ার্ড দিলেই হবে" ভেবে ২৪ ঘণ্টায় হ্যাক খেয়েছিলাম। তারপর থেকে SSH কী, ফায়ারওয়াল, আর টোকেন লুকানো — এই তিনটা সবসময় করি। তুমিও করো। পরের অধ্যায় থেকে ডোমেইন-স্পেসিফিক সিকিউরিটি শুরু — হেলথকেয়ার!
