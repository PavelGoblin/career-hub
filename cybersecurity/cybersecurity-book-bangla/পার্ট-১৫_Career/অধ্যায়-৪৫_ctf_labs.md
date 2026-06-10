# অধ্যায় ৪৫: CTF ও Practical Labs

> **ভাই-বন্ধুর মতো বলছি:** পড়ে আর প্র্যাকটিস না করলে কিছু হবে না ভাই! CTF (Capture The Flag) হলো সেই জায়গা যেখানে তুমি শেখা জিনিস প্র্যাকটিস করতে পারো। এটা হ্যাকিং এর জিমনেশিয়াম। আর হোম ল্যাব বানালে তুমি নিজের মতো করে সব টেস্ট করতে পারবে।

---

## ৪৫.১ সহজ কথায় CTF

CTF মানে Capture The Flag। একটা ফ্ল্যাগ (সাধারণত `FLAG{...}` ফরম্যাটে) খুঁজে বের করতে হয়। বিভিন্ন ক্যাটাগরিতে CTF হয়:

- **Web:** ওয়েব ভুলনেবিলিটি এক্সপ্লয়েট করে ফ্ল্যাগ খোঁজা
- **Binary Exploitation:** বাইনারি প্রোগ্রামের দুর্বলতা কাজে লাগানো
- **Cryptography:** এনক্রিপশন/ডিক্রিপশন চ্যালেঞ্জ
- **Forensics:** ফাইল থেকে লুকানো ডাটা বের করা
- **Reverse Engineering:** প্রোগ্রাম রিভার্স করে ফ্ল্যাগ বের করা
- **OSINT:** পাবলিক ডাটা থেকে ইন্টেলিজেন্স বের করে ফ্ল্যাগ
- **Steganography:** ছবি/অডিও/ভিডিওতে লুকানো মেসেজ

---

## ৪৫.২ HackTheBox, TryHackMe, VulnHub — কীভাবে শুরু করবে

### HackTheBox (HTB)

```
ওয়েবসাইট: https://www.hackthebox.com
খরচ: ফ্রি (ভিআইপি পেইড)
লেভেল: ইন্টারমিডিয়েট থেকে হার্ড
```

**শুরুর স্টেপ:**

```bash
# ১. একাউন্ট ক্রিয়েট করো (hackthebox.com)
# ২. ইনভাইটেশন কোড পেতে হলে:
#    - ওয়েবসাইটে গিয়ে "Getting Started" অপশনে যাও
#    - চ্যালেঞ্জ সলভ করে ইনভাইট কোড পাও

# ৩. ভিপিএন কানেক্ট করো
# HTB থেকে .ovpn ফাইল ডাউনলোড করো
openvpn yourusername.ovpn

# কানেক্ট হলে আইপি চেক করো
ip a show tun0
# সাধারণত: 10.10.14.x বা 10.10.16.x

# ৪. টার্গেট মেশিনে পিং চেক
ping -c 4 10.10.10.x
```

**প্র্যাকটিক্যাল ওয়ার্কফ্লো:**

```bash
# HTB মেশিন সলভ করার প্যাটার্ন:

# স্টেপ ১: নেটওয়ার্ক রিকন
nmap -sC -sV -A -T4 -p- <টার্গেট-আইপি> -oN nmap_scan.txt

# স্টেপ ২: ওয়েব রিকন
gobuster dir -u http://<টার্গেট-আইপি> -w /usr/share/wordlists/dirb/common.txt

# স্টেপ ৩: সার্ভিস ইনভেস্টিগেট
# ওপেন পোর্টের সার্ভিস চেক করো
nc -nv <টার্গেট-আইপি> <পোর্ট>

# স্টেপ ৪: এক্সপ্লয়েট
searchsploit <সার্ভিস-নেম-ভার্সন>
msfconsole
# ব্যবহার modul

# স্টেপ ৫: প্রিভিলেজ এসকেলেশন
sudo -l
find / -perm -4000 2>/dev/null
uname -a
# কার্নেল এক্সপ্লয়েট চেক
```

### TryHackMe (THM)

```
ওয়েবসাইট: https://tryhackme.com
খরচ: ফ্রি (প্রিমিয়াম পেইড)
লেভেল: বিগিনার থেকে এক্সপার্ট
```

**শুরুর স্টেপ:**

```bash
# ১. tryhackme.com এ রেজিস্টার করো
# ২. প্রিমিয়াম না থাকলেও অনেক ফ্রি রুম আছে
# ৩. সেরা ফ্রি রুমসমূহ:
#    - "Complete Beginner" — ২৪+ ঘণ্টার লার্নিং পাথ
#    - "Web Fundamentals"
#    - "Linux Fundamentals"
#    - "Windows Fundamentals"
#    - "Metasploit"

# ৪. ওপেন ভিপিএন দিয়ে কানেক্ট
#    সেটিংস > অ্যাক্সেস > ওপেন ভিপিএন কনফিগ ডাউনলোড
openvpn yourconfig.ovpn

# ৫. রুমে এটাক বক্স (ব্রাউজার বেসড ভিএম) ও ইউজ করতে পারো
```

**লার্নিং পাথ (ফ্রি):**

```
TryHackMe লার্নিং পাথ:

Pre Security (১ সপ্তাহ)
  → নেটওয়ার্কিং, ওয়েব বেসিক, লিনাক্স

Complete Beginner (২ সপ্তাহ)
  → টুলস, রিকন, এক্সপ্লয়টেশন

Web Fundamentals (১ সপ্তাহ)
  → ওয়েব ভুলনেবিলিটি, SQLi, XSS

Offensive Pentesting (১ মাস)
  → ফুল পেন্টেস্ট ওয়ার্কফ্লো
```

### VulnHub

```
ওয়েবসাইট: https://www.vulnhub.com
খরচ: ১০০% ফ্রি
লেভেল: বিগিনার থেকে এক্সপার্ট
লক্ষ্য: অফলাইন ভিএম ডাউনলোড করে নিজের ল্যাবে চালাও
```

**শুরুর স্টেপ:**

```bash
# ১. vulnhub.com থেকে মেশিন ডাউনলোড করো (.ova বা .vmx)
# ২. ভার্চুয়ালবক্সে ইম্পোর্ট করো
#    ফাইল > ইম্পোর্ট অ্যাপ্লায়েন্স > .ova সিলেক্ট

# ৩. নেটওয়ার্ক সেটিংস
#    VM > সেটিংস > নেটওয়ার্ক > ব্রিজড অ্যাডাপ্টার
#    (অথবা হোস্ট-অনলি, NAT)

# ৪. মেশিন বুট করে আইপি খোঁজো
#    তোমার সিস্টেমে নেটওয়ার্ক স্ক্যান চালাও
nmap -sn 192.168.x.0/24

# ৫. আইপি পেলে — অ্যাটাক শুরু
```

**সেরা VulnHub মেশিন (বিগিনার ফ্রেন্ডলি):**

```
1. Kioptrix Level 1 — সবচেয়ে ইজি
2. Mr-Robot — টিভি সিরিজের মতো
3. DC-1 — ড্রুপাল এক্সপ্লয়েট শেখার জন্য
4. FristiLeaks — লিনাক্স প্রিভিলেজ এসকেলেশন
5. Stapler — রিকন প্র্যাকটিস
6. Brainpan — বাফার ওভারফ্লো
7. SickOs 1.1 — লিনাক্স পেন্টেস্ট
```

---

## ৪৫.৩ CTF Methodology

```bash
# ============================================
# CTF মেথডোলজি — সম্পূর্ণ ওয়ার্কফ্লো
# ============================================

# ফেজ ১: রিকন
echo "=== ফেজ ১: রিকন ==="

# nmap — সার্ভিস এবং ওএস ডিটেক্ট
nmap -sC -sV -A -T4 -p- <টার্গেট> -oN recon/nmap_init.txt

# ওয়েব সার্ভিস চেক (যদি পোর্ট 80 বা 443 থাকে)
nikto -h http://<টার্গেট> -o recon/nikto.html
gobuster dir -u http://<টার্গেট> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# ফেজ ২: ইনভেস্টিগেশন
echo "=== ফেজ ২: ইনভেস্টিগেশন ==="

# সোর্স কোড চেক
curl -s http://<টার্গেট>/ | grep -i "flag\|password\|secret\|comment\|<!--"

# রোবটস.টিএক্সটি চেক
curl -s http://<টার্গেট>/robots.txt

# গোবুরস্টার এক্সটেনশন স্ক্যান
gobuster dir -u http://<টার্গেট> -x php,txt,html,asp,aspx,jsp -w /usr/share/wordlists/dirb/common.txt

# ফেজ ৩: এক্সপ্লয়েট
echo "=== ফেজ ৩: এক্সপ্লয়েট ==="

# সার্ভিস ভার্সন থেকে এক্সপ্লয়েট খোঁজা
searchsploit <সার্ভিস> <ভার্সন>

# অথবা গুগল
# <সার্ভিস> <ভার্সন> exploit

# ফেজ ৪: পোস্ট এক্সপ্লয়েটেশন
echo "=== ফেজ ৪: পোস্ট এক্সপ্লয়েটেশন ==="

# সিস্টেম ইনফো
uname -a
cat /etc/os-release
id

# প্রিভিলেজ এসকেলেশন
sudo -l
find / -perm -4000 2>/dev/null
cat /etc/crontab
cat /etc/passwd | grep -v nologin

# ফ্ল্যাগ সার্চ
find / -name "flag*" -type f 2>/dev/null
find / -name "*.txt" -type f 2>/dev/null | xargs grep -l "flag\|FLAG\|CTF" 2>/dev/null
find / -name "*.txt" -path "/home/*" 2>/dev/null
find / -name "user.*" -type f 2>/dev/null
find / -name "root.*" -type f 2>/dev/null
```

### Web CTF টেকনিক

```bash
# SQL Injection — বেসিক টেস্টিং

# ইউজার ইনপুটে এইগুলো ট্রাই করো
' OR 1=1 --
" OR 1=1 --
admin' --
' UNION SELECT 1,2,3 --

# এসকিউএলম্যাপ অটোমেশন (যখন জানো প্যারামিটার)
sqlmap -u "http://<টার্গেট>/page.php?id=1" --batch --dbs

# XSS টেস্টিং
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>

# LFI টেস্টিং
?page=../../../../etc/passwd
?file=php://filter/convert.base64-encode/resource=index.php

# Command Injection
; ls -la
| whoami
`id`
$(cat /etc/passwd)
```

### Steganography টেকনিক

```bash
# ফাইল টাইপ চেক
file mysterious_file

# স্ট্রিংস — হিডেন টেক্সট খোঁজা
strings mysterious_file | grep -i "flag\|password\|secret"

# বিটওয়াইজ ডেটা এক্সট্র্যাক্ট
steghide extract -sf image.jpg
# পাসওয়ার্ড চাইলে

# জেডএসটিইজি — কোন পাসওয়ার্ড না থাকলে
zsteg image.png

# বিনওয়াক
binwalk -e file.bin

# এক্সটুলস — মেটাডাটা
exiftool image.jpg

# ফরেনসিক্স — ফাইল সাইনেচার চেক
xxd image.jpg | head
# JPG: FF D8 FF
# PNG: 89 50 4E 47
# GIF: 47 49 46 38
# PDF: 25 50 44 46
```

### Cryptography হ্যান্ডলিং

```bash
# বেস৬৪ ডিকোড
echo "RkxBR3t0aGlzX2lzX2ZsYWd9" | base64 -d

# হেক্স ডিকোড
echo "464c41477b" | xxd -r -p

# আরওটি১৩
echo "SYNT{ebg13_qrpbqr}" | rot13

# সিজার সাইফার — অল পসিবিলিটিজ চেক
for i in {1..25}; do
    echo "$i: $(echo "FLAG{...}" | tr "$(echo {a..z} | tr -d ' ')" "$(echo {a..z} | tr -d ' ' | sed "s/^.\{$i\}//;s/$/$(echo {a..z} | tr -d ' ' | cut -c1-$i)/")")" 
done

# হ্যাশ আইডেন্টিফাই
hash-identifier
# অথবা
echo "5d41402abc4b2a76b9719d911017c592" | hashid

# ফ্রিকোয়েন্সি এনালাইসিস
python3 -c "
from collections import Counter
text = '...'
print(Counter(text))
"
```

---

## ৪৫.৪ Write-up লেখার নিয়ম

CTF সলভ করার পর রাইট-আপ লেখা খুব গুরুত্বপূর্ণ। এটা তোমার পোর্টফোলিওকে শক্তিশালী করবে।

### রাইট-আপ স্ট্রাকচার

```markdown
# মেশিন/চ্যালেঞ্জ নাম — CTF রাইট-আপ

## বেসিক ইনফো
- **প্ল্যাটফর্ম:** HackTheBox / TryHackMe / VulnHub
- **মেশিন/চ্যালেঞ্জ:** [নাম]
- **লেভেল:** ইজি / মিডিয়াম / হার্ড
- **ওএস:** লিনাক্স / উইন্ডোজ
- **তারিখ:** [তারিখ]

## রিকন

### nmap
\`\`\`
nmap -sC -sV -A -T4 -p- <আইপি>
\`\`\`

আউটপুট:
\`\`\`
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 7.9
80/tcp   open  http     Apache httpd 2.4.38
\`\`\`

## এনুমারেশন

পোর্ট ৮০ তে ওয়েব সার্ভার আছে। ওয়েবসাইট চেক করে দেখলাম...

## এক্সপ্লয়েটেশন

এসকিউএল ইনজেকশন দিয়ে ডাটাবেস থেকে ইউজারনেম/পাসওয়ার্ড বের করলাম...

## প্রিভিলেজ এসকেলেশন

\`\`\`bash
sudo -l
# দেখলাম /usr/bin/python3 কমান্ড sudo দিয়ে চালানো যায়
sudo python3 -c 'import os; os.system("/bin/bash")'
\`\`\`

## ফ্ল্যাগ
- **User.txt:** FLAG{...}
- **Root.txt:** FLAG{...}

## শেখার পয়েন্ট
1. হ্যাশ ক্র্যাকিং
2. লিনাক্স প্রিভিলেজ এসকেলেশন
3. ওয়েব ডিরেক্টরি এনুমারেশন

## টুলস ব্যবহার করেছি
- nmap
- gobuster
- sqlmap
- john
```

### ভালো রাইট-আপ লেখার টিপস

| টিপস | কী করবে |
|-------|---------|
| স্ক্রিনশট নিও | প্রতিটা স্টেপের স্ক্রিনশট রাখো |
| কোড ব্লক | কমান্ডগুলো কোড ব্লকে দাও |
| ব্যাখ্যা | কেন এই কমান্ড দিলে, তার ব্যাখ্যা দাও |
| অল্টারনেটিভ সলিউশন | যদি অন্য উপায় থাকে, সেটাও দেখাও |
| রেফারেন্স | যে আর্টিকেল/ডক দেখেছো, সেটার লিংক দাও |

---

## ৪৫.৫ Home Lab Setup Guide (Complete)

### ভার্চুয়ালাইজেশন সেটআপ

```bash
# প্রয়োজনীয় সফটওয়্যার
# ১. ভার্চুয়ালবক্স (free) — virtualbox.org
# ২. ভিএমওয়্যার ওয়ার্কস্টেশন প্লেয়ার (free) — vmware.com
# ৩. ভ্যাগ্রান্ট (optional) — vagrantup.com

# ডাউনলোড লিংকসমূহ
# ভার্চুয়ালবক্স: https://www.virtualbox.org/wiki/Downloads
# কালি লিনাক্স: https://www.kali.org/get-kali/#kali-virtual
# মেটাস্প্লোইটেবল: https://sourceforge.net/projects/metasploitable/
# উইন্ডোজ ভিএম: https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/
```

### ল্যাব আর্কিটেকচার

```
তোমার হোম ল্যাব:

┌─────────────────────────────────────────────────┐
│                 হোস্ট মেশিন                      │
│           (উইন্ডোজ/লিনাক্স/ম্যাক)                │
│                   │                              │
│         ভার্চুয়াল সুইচ (NAT/ব্রিজ)              │
│         ┌─────────┼─────────┐                    │
│         │         │         │                    │
│    কালিলিনাক্স   উইন্ডোজ   সার্ভার              │
│    (অ্যাটাকার)   (ক্লায়েন্ট) (লক্ষ্য)           │
│    192.168.1.10  192.168.1.20  192.168.1.30       │
└─────────────────────────────────────────────────┘
```

### কমপ্লিট সেটআপ স্ক্রিপ্ট

```bash
#!/bin/bash
# ============================================
# হোম ল্যাব সেটআপ স্ক্রিপ্ট — লিনাক্স হোস্টের জন্য
# অটোমেটিক্যালি সবকিছু সেট করে দেবে
# ============================================

echo "╔══════════════════════════════════╗"
echo "║      হোম ল্যাব সেটআপ v1.0       ║"
echo "╚══════════════════════════════════╝"

# ভিপিএন ল্যাব সেটআপ (লিনাক্স)
setup_vpn_lab() {
    echo "[*] ভিপিএন সার্ভার সেটআপ করছি..."
    
    # OpenVPN ইনস্টল
    apt update && apt install -y openvpn easy-rsa
    
    # PKI সেটআপ
    make-cadir /etc/openvpn/easy-rsa
    cd /etc/openvpn/easy-rsa
    ./easyrsa init-pki
    ./easyrsa build-ca nopass
    ./easyrsa gen-req server nopass
    ./easyrsa sign-req server server
    ./easyrsa gen-dh
    openvpn --genkey --secret ta.key
    
    echo "[✓] ভিপিএন বেসিক সেটআপ কমপ্লিট"
}

# ডকার কন্টেইনার ল্যাব
setup_docker_lab() {
    echo "[*] ডকার ভুলনেবল কন্টেইনার সেটআপ..."
    
    # ডকার ইনস্টল
    apt install -y docker.io docker-compose
    
    # DVWA সেটআপ
    docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa
    echo "[✓] DVWA চলছে: http://localhost:8080"
    
    # bWAPP সেটআপ
    docker run -d -p 8081:80 --name bwapp raesene/bwapp
    echo "[✓] bWAPP চলছে: http://localhost:8081"
    
    # Juice Shop (ওয়ান অফ দ্য বেস্ট)
    docker run -d -p 3000:3000 --name juice-shop bkimminich/juice-shop
    echo "[✓] Juice Shop চলছে: http://localhost:3000"
}

# অ্যাটাকার মেশিন সেটআপ
setup_attacker_machine() {
    echo "[*] অ্যাটাকার টুলস ইনস্টল করছি..."
    
    # প্রয়োজনীয় প্যাকেজ
    apt install -y nmap nikto gobuster dirb hydra john hashcat sqlmap burpsuite
    
    # পাইথন টুলস
    pip install shodan requests beautifulsoup4 colorama
    
    # গিট টুলস
    git clone https://github.com/danielmiessler/SecLists /opt/SecLists
    git clone https://github.com/trustedsec/social-engineer-toolkit /opt/set
    
    echo "[✓] অ্যাটাকার টুলস রেডি!"
}

# আইএসও ডাউনলোড এবং কনফিগার
setup_target_machines() {
    echo "[*] টার্গেট মেশিন কনফিগার করছি..."
    echo "[!] ডাউনলোড করো:"
    echo "    → Metasploitable 2: https://sourceforge.net/projects/metasploitable/"
    echo "    → OWASP Broken Web Apps: https://owasp.org/www-project-broken-web-applications/"
    echo "    → VulnHub: https://www.vulnhub.com/"
}

# নেটওয়ার্ক ইন্টারফেস সেটআপ
setup_network() {
    echo "[*] ল্যাব নেটওয়ার্ক সেটআপ..."
    
    # ব্রিজ ইন্টারফেস (যদি ভার্চুয়ালবক্স)
    VBoxManage hostonlyif create
    VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0
    
    echo "[✓] হোস্ট-অনলি নেটওয়ার্ক তৈরি হয়েছে: 192.168.56.0/24"
    echo "    অ্যাটাকার: 192.168.56.10"
    echo "    টার্গেট: 192.168.56.20"
}

# ইন্টারেক্টিভ মেনু
echo ""
echo "কী সেটআপ করতে চাও?"
echo "1) ভিপিএন ল্যাব"
echo "2) ডকার কন্টেইনার ল্যাব"
echo "3) অ্যাটাকার টুলস"
echo "4) সম্পূর্ণ ল্যাব (সবকিছু)"
read -p "পছন্দ: " choice

case $choice in
    1) setup_vpn_lab ;;
    2) setup_docker_lab ;;
    3) setup_attacker_machine ;;
    4)
        setup_network
        setup_vpn_lab
        setup_docker_lab
        setup_attacker_machine
        setup_target_machines
        echo "[✓] সম্পূর্ণ ল্যাব প্রস্তুত!"
        ;;
    *) echo "ভুল পছন্দ!" ;;
esac
```

### ল্যাব চেকলিস্ট

```
প্রথমবার ল্যাব সেটআপের পর এই চেকলিস্ট ফলো করো:

□ কালি লিনাক্স ইনস্টল এবং আপডেটেড
□ nmap, gobuster, sqlmap, hydra, john ইনস্টল
□ SecLists ওয়ার্ডলিস্ট ডাউনলোড
□ কমপক্ষে ১টি ভুলনেবল ভিএম (Metasploitable/DVWA)
□ নেটওয়ার্ক কানেক্টিভিটি টেস্ট (পিং চেক)
□ ভিপিএন/হোস্ট-অনলি নেটওয়ার্ক ওয়ার্কিং
□ স্ন্যাপশট নেওয়া (বেসলাইন)
```

---

## ৪৫.৬ ল্যাব এক্সারসাইজ

| টাস্ক | বিবরণ | প্ল্যাটফর্ম |
|-------|--------|-------------|
| 1 | TryHackMe-তে "Complete Beginner" পাথ শেষ করো | TryHackMe |
| 2 | VulnHub থেকে Kioptrix Level 1 সলভ করো | VulnHub |
| 3 | HTB-তে Starting Point মেশিনগুলো সলভ করো | HackTheBox |
| 4 | নিজের হোম ল্যাবে DVWA সেটআপ করো | Docker |
| 5 | DVWA-তে SQL Injection ল্যাব প্র্যাকটিস করো | Local |
| 6 | CTF চ্যালেঞ্জের একটা রাইট-আপ লেখো | Medium/Twitter |
| 7 | কমপক্ষে ৩টা CTF প্ল্যাটফর্মে একাউন্ট খোলো | সবগুলো |
| 8 | সপ্তাহে ১টা মেশিন সলভ করার লক্ষ্য নাও | সবগুলো |

---

## ৪৫.৭ মনে রাখো

| বিষয় | কী মনে রাখবে |
|-------|-------------|
| HTB | ইনভাইটেশন কোড সলভ করে শুরু করো |
| TryHackMe | বিগিনারদের জন্য বেস্ট — লার্নিং পাথ ফলো করো |
| VulnHub | অফলাইন ভিএম — ভিপিএন লাগে না |
| রিকন → এনুম → এক্সপ্লয়েট → পোস্ট | CTF মেথডোলজি — সবসময় ফলো করো |
| রাইট-আপ | Medium এ পাবলিশ করো — পোর্টফোলিওর জন্য |
| হোম ল্যাব | ভিপিএন + ডকার + ভুলনেবল ভিএম + কালি |
| স্ন্যাপশট | ল্যাব ভাঙ্গলে রিস্টোর করা যাবে |
| Consistent | প্রতিদিন ১ ঘণ্টা — ৬ মাসে মাষ্টার |

> **ভাই-বন্ধুর টিপস:** CTF-এ আটকে গেলে হাল ছাড়ো না। Google, IppSec এর ইউটিউব ভিডিও, এবং CTF রাইট-আপ পড়ো। ১ ঘণ্টা আটকে থাকলে হিন্ট দেখো — এতে দোষের কিছু নেই। আর হ্যাঁ, হোম ল্যাবে যা ইচ্ছা তাই করতে পারো — সেটাই সবচেয়ে বড় সুবিধা!
