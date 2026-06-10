# অধ্যায় ২৯: Top 10 Free Cybersecurity Tools (2025)

## সহজ কথায়:
Kali tools তো জানো। কিন্তু professional cybersecurity tools আরো অনেক আছে — এবং এগুলোর বেশিরভাগই ফ্রি!

---

## #1: Nessus Essentials (Vulnerability Scanner)

- **কাজ:** Network + web app vulnerability scanning
- **ফ্রি limit:** 16 IPs (বেসরকারি ব্যবহারের জন্য যথেষ্ট)
- **URL:** tenable.com/downloads/nessus

```bash
# Install:
sudo dpkg -i Nessus-*.deb
sudo systemctl start nessusd
# Browser → https://localhost:8834
```

---

## #2: OpenVAS / Greenbone (Vulnerability Scanner)

- **কাজ:** Nessus-এর ফ্রি alternative — full-featured
- **ফ্রি:** সম্পূর্ণ ফ্রি (unlimited IPs)
- **URL:** greenbone.net

```bash
# Install Kali তে:
sudo apt install gvm
sudo gvm-setup
sudo gvm-start
# Browser → https://127.0.0.1:9392
```

---

## #3: Snort (IDS/IPS)

- **কাজ:** Network intrusion detection + prevention
- **ফ্রি:** Community rules ফ্রি (registered required)
- **URL:** snort.org

```bash
# Install:
sudo apt install snort

# Basic rule:
sudo snort -i eth0 -c /etc/snort/snort.conf

# Test:
sudo snort -A console -i eth0 -c /etc/snort/snort.conf
```

---

## #4: Zeek (Formerly Bro — Network Monitor)

- **কাজ:** Network traffic analysis + security monitoring
- **ফ্রি:** সম্পূর্ণ ওপেন সোর্স
- **URL:** zeek.org

```bash
# Install:
sudo apt install zeek

# Run:
sudo zeek -i eth0

# Output logs:
ls /var/log/zeek/current/
# conn.log, http.log, dns.log, ssl.log
```

---

## #5: OSSEC (HIDS — Host Intrusion Detection)

- **কাজ:** File integrity check, log monitoring, rootkit detection
- **ফ্রি:** সম্পূর্ণ ওপেন সোর্স
- **URL:** ossec.net

```bash
# Install (agent/server):
sudo apt install ossec-hids-server
# বা ossec-hids-agent

# Agent config:
/var/ossec/bin/ossec-control start
```

---

## #6: Volatility (Memory Forensics)

- **কাজ:** RAM dump analysis — malware, process, network connection find
- **ফ্রি:** সম্পূর্ণ ওপেন সোর্স
- **URL:** volatilityfoundation.org

```bash
# Install:
sudo apt install volatility

# Basic usage:
volatility -f memory.dump imageinfo
volatility -f memory.dump --profile=Win10x64 pslist
volatility -f memory.dump --profile=Win10x64 netscan
volatility -f memory.dump --profile=Win10x64 cmdscan
```

---

## #7: Autopsy (Digital Forensics)

- **কাজ:** Disk forensics — file recovery, timeline analysis
- **ফ্রি:** GUI-based, easy to use
- **URL:** autopsydigitalforensics.com

```bash
# Install:
sudo apt install autopsy

# Start:
sudo autopsy
# Browser → http://localhost:9999/autopsy
```

---

## #8: REMnux (Malware Analysis Toolkit)

- **কাজ:** Malware analysis — reverse engineering tool collection
- **ফ্রি:** Linux distro (Ubuntu-based)
- **URL:** remnux.org

```bash
# REMnux tools:
# - Didier Stevens' tools (pdf, zip, ole analysis)
# - Strings, FLOSS, XORSearch
# - Malware sandbox tools
```

---

## #9: MISP (Malware Information Sharing Platform)

- **কাজ:** Threat intelligence sharing — IOCs (Indicators of Compromise) share
- **ফ্রি:** সম্পূর্ণ ওপেন সোর্স
- **URL:** misp-project.org

```bash
# Docker install:
docker run -d -p 80:80 -p 443:443 harvarditsecurity/misp
```

---

## #10: TheHive (Incident Response Platform)

- **কাজ:** SOC/case management — alert → investigation → response
- **ফ্রি:** ওপেন সোর্স (commercial version also)
- **URL:** thehive-project.org

```bash
# Docker:
docker run -d -p 9000:9000 strangebee/thehive
```

---

## Bonus: Other Excellent Free Tools

| Tool | কাজ | URL |
|------|-----|-----|
| **Wazuh** | SIEM + XDR (OSSEC-based) | wazuh.com |
| **Grafana** | Visualization + dashboard | grafana.com |
| **ELK Stack** | Log management | elastic.co |
| **ClamAV** | Antivirus (Linux) | clamav.net |
| **rkhunter** | Rootkit hunter | rkhunter.sourceforge.net |
| **chkrootkit** | Rootkit detection | chkrootkit.org |
| **Fail2ban** | Brute force protection | fail2ban.org |
| **osquery** | System query (SQL-interface) | osquery.io |
| **Velociraptor** | Endpoint monitoring | velociraptor.app |
| **Cuckoo** | Malware sandbox | cuckoosandbox.org |

---

## 💡 ল্যাব এক্সারসাইজ

```
১. OpenVAS install + scan করো:
   - Metasploitable2 scan
   - Result analysis
   - Top 3 vuln identify

২. Zeek setup:
   - network traffic monitor
   - conn.log → দেখো কত connection

৩. Autopsy practice:
   - একটি disk image analyze করো
   - File recovery দেখো
```

---

## 📌 মনে রাখো

| Tool | Best for | Cost |
|------|----------|------|
| **Nessus** | Vulnerability scan | 16 IPs free |
| **OpenVAS** | Vulnerability scan | 100% free |
| **Snort** | IDS/IPS | Free |
| **Zeek** | Network monitoring | Free |
| **OSSEC** | Host monitoring | Free |
| **Volatility** | Memory forensics | Free |
| **MISP** | Threat intel | Free |
| **TheHive** | Incident response | Free |

**পরবর্তী — Top 10 Hacking Gadgets! 🛠️**
