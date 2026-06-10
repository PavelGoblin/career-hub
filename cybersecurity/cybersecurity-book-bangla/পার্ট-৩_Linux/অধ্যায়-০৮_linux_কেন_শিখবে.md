# অধ্যায় ৮: Linux কেন শিখবে?

## সহজ কথায়:
হ্যাকারদের অস্ত্রাগারের সবচেয়ে দামি অস্ত্র হলো Linux। ৯৫% hacker Linux ব্যবহার করে। তুমি যদি Linux না জানো, তুমি hacker-ই না।

---

## ৮.১ Linux vs Windows — Hacking-এর জন্য কোনটা ভালো, কেন

### তুলনা:

| ফিচার | Linux (Kali/Parrot) | Windows |
|-------|-------------------|---------|
| **Open Source** | ✅ সম্পূর্ণ ফ্রি | ❌ লাইসেন্স লাগে |
| **Pre-installed Tools** | ✅ ৬০০+ hacking tool | ❌ আলাদা করে install |
| **Customizability** | ✅ Unlimited | ❌ Limited |
| **Terminal Power** | ✅ Bash (অসাধারণ) | ❌ PowerShell (ভালো কিন্তু কম) |
| **Malware** | ✅ খুব কম ভাইরাস | ❌ লক্ষ্য makes |
| **Transparency** | ✅ কী হচ্ছে দেখা যায় | ❌ অনেক কিছু hidden |
| **Hardware Access** | ✅ Full control | ❌ Limited |

### কেন হ্যাকাররা Linux বেছে নেয়:

```bash
# উইন্ডোজে কোন open port check করতে:
netstat -an | findstr LISTEN

# Linux-এ:
ss -tln
# বা
netstat -tlnp

# Linux → এক লাইনে, সহজ, fast
```

### Argument for Windows:
- কিছু corporate tool শুধু Windows-এ চলে
- কিছু DLL injection/smb exploit Windows-specific
- কিছু beginner-এর জন্য GUI বেশি comfortable

**কিন্তু সিরিয়াস হলে → তোমাকে Linux শিখতেই হবে।**

---

## ৮.২ Linux File System Structure — বাংলায়

Linux file system হলো **tree structure** — root (/) থেকে শুরু। এটা Windows-এর মতো C:, D: না।

```
/ (root — গাছের শিকড়)
├── /bin     → Basic commands (ls, cp, mv) — এখান থেকে run হয়
├── /sbin    → System commands (fdisk, iptables) — admin tools
├── /etc     → Configuration files (network config, password file) ⭐
├── /home    → Users-এর personal folders (/home/kali, /home/alice)
├── /var     → Variable data (logs: /var/log/syslog) ⭐
├── /tmp     → Temporary files (সবার readable) ⭐
├── /root    → Root user-এর home
├── /dev     → Devices (sda, tty, network interfaces)
├── /proc    → Process information (running process detail)
├── /usr     → User programs (installed software)
├── /boot    → Boot files (kernel, initrd)
└── /mnt     → Mount point (external drive)
```

### ⭐ গুরুত্বপূর্ণ Directory (Hacker-দের জন্য):

| Directory | কেন গুরুত্বপূর্ণ | কী আছে |
|-----------|-----------------|---------|
| **/etc/passwd** | User account info | usernames, UID, GID |
| **/etc/shadow** | Encrypted password | ✅ **crack করার target** |
| **/etc/hosts** | Local DNS | Website block/redirect |
| **/var/log** | System logs | Attack detection, cleanup |
| **/tmp** | Temp files | Exploit upload (সবার readable) |
| **/root** | Root-এর personal zone | Flag file (CTF) |

---

## ৮.৩ Linux Distributions: Kali, Parrot OS, Ubuntu

### Kali Linux (হ্যাকারদের প্রিয়)
- **বেস:** Debian
- **জনপ্রিয়:** ★★★★★
- **প্রি-ইনস্টলড:** ৬০০+ pentesting tool
- **ভালো:** সব tool ready-made, vast community support
- **খারাপ:** Desktop environment ভারী, কিছু stability issue

**কে ব্যবহার করবে:** Pentester, security researcher, CTF player

### Parrot Security OS
- **বেস:** Debian Testing
- **জনপ্রিয়:** ★★★★☆
- **প্রি-ইনস্টলড:** ৪০০+ tool (Kali-র চেয়ে কম)
- **ভালো:** Lightweight (১ GB RAM-এ চলে), বিল্ট-ইন anonymity tool
- **খারাপ:** Smaller community, কিছু tool নাও থাকতে পারে

**কে ব্যবহার করবে:** যারা পুরনো ল্যাপটপ ব্যবহার করে, anonymity চায়

### Ubuntu
- **বেস:** Debian
- **জনপ্রিয়:** ★★★★★
- **প্রি-ইনস্টলড:** Basic tools
- **ভালো:** Most stable, best hardware support, daily driver
- **খারাপ:** নিজে tool install করতে হয়

**কে ব্যবহার করবে:** Daily use, server, programming, যারা প্রথম Linux শিখছে

### Comparison Table:

| Feature | Kali | Parrot | Ubuntu |
|---------|------|--------|--------|
| **Tools included** | 600+ | 400+ | 0 (basic utilities) |
| **RAM usage** | 2 GB | 1 GB | 2 GB |
| **Best for** | Pentesting | Anonymity + Pentesting | Daily work + Dev |
| **Community** | Largest | Medium | Largest |
| **Update model** | Rolling | Rolling | LTS (stable) |
| **Learning curve** | Medium | Medium | Easy |

### হ্যাকার-এর Recommended Setup:
```
Dual Boot বা Virtual Machine:
- Kali Linux → Pentesting, CTF, exploitation
- Ubuntu → Daily work, programming, server
```

---

## ৮.৪ Linux vs Windows Command Comparison

| কাজ | Windows (CMD) | Linux (Bash) |
|-----|---------------|--------------|
| Directory list | `dir` | `ls -la` |
| Change directory | `cd folder` | `cd folder` |
| Current directory | `cd` | `pwd` |
| Copy file | `copy a.txt b.txt` | `cp a.txt b.txt` |
| Move file | `move a.txt folder/` | `mv a.txt folder/` |
| Delete file | `del a.txt` | `rm a.txt` |
| Network config | `ipconfig` | `ip a` or `ifconfig` |
| Ping | `ping google.com` | `ping google.com` |
| Process list | `tasklist` | `ps aux` |
| Kill process | `taskkill /PID 1234` | `kill -9 1234` |

---

## 💡 ল্যাব এক্সারসাইজ

```
১. নিচের website-এ গিয়ে Linux file system explorer খেলো:
   https://linuxjourney.com/

২. নিচের directory structure বুঝতে:
   - /etc/passwd ফাইলটা দেখো (Linux VM থাকলে)
   - /var/log/syslog ফাইলটা দেখো (যদি থাকে)
   - /tmp directory-তে একটা file তৈরি করো

৩. কোন distribution নেবে — Kali, Parrot, নাকি Ubuntu?
   লিখো ৩টা কারণ।
```

---

## 📌 মনে রাখো

| Concept | মূল কথা |
|---------|---------|
| **Linux must** | ৯৫% hacker Linux ব্যবহার করে |
| **File System** | / = root → সবকিছু tree structure |
| **মূল directory** | /etc (config), /var (log), /tmp (temp) |
| **Kali** | 600+ tool, pentesting best |
| **Parrot** | Lightweight, anonymity |
| **Ubuntu** | Daily driver, server |

**পরবর্তী অধ্যায় — Linux Commands (Beginner → Advanced)! 🚀**
