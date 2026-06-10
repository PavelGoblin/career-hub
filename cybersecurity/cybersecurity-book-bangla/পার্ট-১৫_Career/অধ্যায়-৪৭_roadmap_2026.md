# অধ্যায় ৪৭: Ethical Hacker Roadmap 2026

> **ভাই-বন্ধুর মতো বলছি:** ২০২৬ সালে ইথিক্যাল হ্যাকার হতে চাও? তাহলে এই রোডম্যাপ তোমার জন্য। আমি সপ্তাহে সপ্তাহে বলে দিচ্ছি কীভাবে ৬ মাসে জব-রেডি হওয়া যায়। শুধু পড়লে হবে না — প্র্যাকটিস করতে হবে!

---

## ৪৭.১ সহজ কথায় Roadmap

ইথিক্যাল হ্যাকার হতে গেলে কী কী লাগে:

```
বেসিক স্কিলস:
├── লিনাক্স (কমান্ড লাইন পুরোপুরি জানতে হবে)
├── নেটওয়ার্কিং (TCP/IP, DNS, HTTP)
├── প্রোগ্রামিং (Python + Bash)
├── ওয়েব টেকনোলজি (HTML, JS, PHP বেসিক)
└── ইংলিশ (ডকুমেন্টেশন পড়ার জন্য)

কোর স্কিলস:
├── রিকন (হোস্ট, সাবডোমেইন, এনুমারেশন)
├── স্ক্যানিং (nmap, masscan)
├── এক্সপ্লয়েটেশন (Metasploit, manual)
├── ওয়েব ভুলনেবিলিটি (SQLi, XSS, SSRF, RCE)
├── প্রিভিলেজ এসকেলেশন (Linux + Windows)
└── রিপোর্টিং (সঠিক ডকুমেন্টেশন)
```

---

## ৪৭.২ Week-by-Week (6 Month Plan)

```bash
# ============================================
# ৬ মাসের ইথিক্যাল হ্যাকার প্ল্যান — ২০২৬
# ============================================

echo "╔══════════════════════════════════════════╗"
echo "║    ২৪ সপ্তাহ — জিরো থেকে হিরো           ║"
echo "╚══════════════════════════════════════════╝"

# ============================================
# মাস ১: বেসিক বিল্ডিং (সপ্তাহ ১-৪)
# ============================================
echo ""
echo "━━━ মাস ১: ফাউন্ডেশন (Week 1-4) ━━━"

echo "
সপ্তাহ ১: লিনাক্স বেসিক
─────────────────────
লক্ষ্য: কমান্ড লাইনে ঘর করতে হবে

শেখার লিস্ট:
□ ফাইল সিস্টেম: ls, cd, pwd, mkdir, rm, cp, mv
□ পারমিশন: chmod, chown, umask
□ টেক্সট: cat, grep, sed, awk, head, tail
□ নেটওয়ার্ক: ip, ifconfig, ping, netstat, ss
□ প্রকセス: ps, top, kill, systemctl

রিসোর্স:
• YouTube: NetworkChuck — Linux for Hackers (প্লেলিস্ট)
• TryHackMe: Linux Fundamentals (রুম)
• বুক: 'Linux Basics for Hackers' (OccupyTheWeb)

প্র্যাকটিস টাস্ক:
1. কালি লিনাক্স ইনস্টল করো (VM)
2. প্রতিদিন ২০টি কমান্ড প্র্যাকটিস করো
3. নিজের একটি bash স্ক্রিপ্ট লেখো (যেমন ব্যাকআপ স্ক্রিপ্ট)
"

echo "
সপ্তাহ ২: নেটওয়ার্কিং বেসিক
────────────────────────
লক্ষ্য: TCP/IP, HTTP, DNS — মজ্জাগত করতে হবে

শেখার লিস্ট:
□ OSI মডেল (৭ লেয়ার)
□ TCP 3-way handshake
□ HTTP methods (GET, POST, PUT, DELETE)
□ DNS রেজোলিউশন
□ পোর্ট এবং সার্ভিস

রিসোর্স:
• Professor Messer — Network+ (ইউটিউব, ফ্রি)
• Practice Packet Tracer ব্যবহার করো
• Wireshark দিয়ে প্যাকেট ক্যাপচার করো

প্র্যাকটিস টাস্ক:
1. nc (netcat) দিয়ে HTTP রিকোয়েস্ট পাঠাও
2. Wireshark দিয়ে TCP handshake দেখো
3. নিজের DNS সার্ভার সেটআপ করো (dnsmasq)
"

echo "
সপ্তাহ ৩: পাইথন ফর হ্যাকিং
──────────────────────
লক্ষ্য: টুলস বানানোর জন্য পাইথন শেখো

শেখার লিস্ট:
□ Variables, loops, conditions
□ Functions, classes
□ Requests library (HTTP কল)
□ Socket programming (বেসিক)
□ Scapy (প্যাকেট ক্রাফটিং)

প্র্যাকটিস টাস্ক:
1. পোর্ট স্ক্যানার বানাও (socket দিয়ে)
2. HTTP রিকোয়েস্ট পাঠানোর স্ক্রিপ্ট বানাও
3. Subdomain bruteforcer বানাও
"

echo "
সপ্তাহ ৪: ল্যাব সেটআপ + রিভিউ
─────────────────────────
লক্ষ্য: প্র্যাকটিস এনভায়রনমেন্ট প্রস্তুত

সপ্তাহের কাজ:
□ কুইজ ওয়েবসাইট বানাও (DVWA, Juice Shop)
□ TryHackMe একাউন্ট খোলো
□ HackerOne/Bugcrowd প্রোফাইল সেটআপ
□ মিসট করা টপিক রিভিউ করো
"

# ============================================
# মাস ২: রিকন এবং স্ক্যানিং (সপ্তাহ ৫-৮)
# ============================================
echo ""
echo "━━━ মাস ২: রিকন ও স্ক্যানিং (Week 5-8) ━━━"

echo "
সপ্তাহ ৫-৬: ফুটপ্রিন্টিং (প্যাসিভ রিকন)
────────────────────────────────
□ Google Dorking (site:, filetype:, intitle:)
□ Shodan.io সার্চ
□ theHarvester — ইমেল এবং সাবডোমেইন
□ WHOIS লুকআপ
□ DNS enumuration (dig, nslookup)
□ OSINT ফ্রেমওয়ার্ক

সপ্তাহ ৭-৮: অ্যাকটিভ রিকন
────────────────────────
□ nmap (পূর্ণাঙ্গ): -sC, -sV, -A, -p-, --script
□ masscan (হাই-স্পীড স্ক্যান)
□ gobuster, ffuf, dirb (ডিরেক্টরি এনুম)
□ subfinder, assetfinder (সাবডোমেইন)
□ waybackurls, gau (আর্কাইভ ইউআরএল)

প্র্যাকটিস: HTB এর 'Recon' ট্যাগের মেশিন
"

# ============================================
# মাস ৩: ওয়েব ভুলনেবিলিটি (সপ্তাহ ৯-১২)
# ============================================
echo ""
echo "━━━ মাস ৩: ওয়েব ভুলনেবিলিটি (Week 9-12) ━━━"

echo "
সপ্তাহ ৯: SQL Injection
────────────────────
□ SQLi বেসিক (UNION, Error, Blind)
□ sqlmap অটোমেশন
□ WAF বাইপাস টেকনিক
□ রিসোর্স: PortSwigger SQLi ল্যাব

সপ্তাহ ১০: XSS (Cross-Site Scripting)
─────────────────────────────
□ Reflected, Stored, DOM-based
□ Cookie stealing পিওসি
□ CSP বাইপাস
□ রিসোর্স: PortSwigger XSS ল্যাব

সপ্তাহ ১১: অন্যান্য ওয়েব ভুলনেবিলিটি
─────────────────────────────────
□ IDOR (Insecure Direct Object Reference)
□ SSRF (Server-Side Request Forgery)
□ RCE (Command Injection)
□ File Upload ভুলনেবিলিটি
□ LFI/RFI (Local/Remote File Inclusion)

সপ্তাহ ১২: API সিকিউরিটি টেস্টিং
────────────────────────────
□ REST API টেস্টিং
□ GraphQL ইন্ট্রোস্পেকশন
□ JWT অ্যাটাক
□ রিসোর্স: tryhackme.com — API টিউটোরিয়াল
"

# ============================================
# মাস ৪: এক্সপ্লয়েটেশন (সপ্তাহ ১৩-১৬)
# ============================================
echo ""
echo "━━━ মাস ৪: এক্সপ্লয়েটেশন (Week 13-16) ━━━"

echo "
সপ্তাহ ১৩-১৪: মেটাস্প্লয়েট
─────────────────────────
□ msfconsole বেসিক
□ exploit/search/payload/encoder
□ Meterpreter পোস্ট-এক্সপ্লয়েটেশন
□ Resource script অটোমেশন

সপ্তাহ ১৫: ম্যানুয়াল এক্সপ্লয়েটেশন
─────────────────────────────
□ searchsploit (Exploit-DB)
□ Buffer overflow বেসিক
□ Python exploit লেখা
□ Shellcode বেসিক

সপ্তাহ ১৬: পাসওয়ার্ড অ্যাটাক
─────────────────────────
□ Hydra (অনলাইন ব্রুটফোর্স)
□ John the Ripper (অফলাইন ক্র্যাক)
□ Hashcat (GPU ক্র্যাকিং)
□ Wordlist তৈরি (crunch, cupp)
"

# ============================================
# মাস ৫: প্রিভিলেজ এসকেলেশন + পোস্ট-এক্সপ্লয়েটেশন
# ============================================
echo ""
echo "━━━ মাস ৫: প্রিভ এসকেলেশন (Week 17-20) ━━━"

echo "
সপ্তাহ ১৭-১৮: লিনাক্স প্রিভিলেজ এসকেলেশন
──────────────────────────────────────
□ Kernel exploit (CVE চেক)
□ SUID misconfiguration
□ Sudo privilege
□ Cron jobs
□ Docker/LXC escape
□ লিনাক্স প্রিভ এসকেলেশন চেকলিস্ট

সপ্তাহ ১৯-২০: উইন্ডোজ প্রিভিলেজ এসকেলেশন
─────────────────────────────────────
□ Token manipulation
□ Service misconfiguration
□ DLL hijacking
□ AlwaysInstallElevated
□ UAC bypass
সপ্তাহ ২০: পোস্ট-এক্সপ্লয়েটেশন ল্যাব
"

# ============================================
# মাস ৬: ক্যারিয়ার প্রিপারেশন (সপ্তাহ ২১-২৪)
# ============================================
echo ""
echo "━━━ মাস ৬: ক্যারিয়ার (Week 21-24) ━━━"

echo "
সপ্তাহ ২১-২২: সার্টিফিকেশন
─────────────────────────
□ CompTIA Security+ (বেসিক)
□ CEH (ইসি কাউন্সিল)
□ PNPT (TCM Security — প্র্যাকটিক্যাল)
□ OSCP (অফেনসিভ সিকিউরিটি — অ্যাডভান্সড)

বাংলাদেশে ভালো চাকরির জন্য:
→ CEH বেশি চাওয়া হয়
→ OSCP দিলে সিনিয়র লেভেলের চাকরি সহজে পাওয়া যায়

সপ্তাহ ২৩: পোর্টফোলিও বানানো
─────────────────────────
□ GitHub — হোমল্যাব স্ক্রিপ্ট, টুলস, রাইট-আপ
□ LinkedIn অপটিমাইজেশন
□ রাইট-আপ লেখো (Medium/dev.to)
□ CVE পেতে চেষ্টা করো

সপ্তাহ ২৪: জব অ্যাপ্লাই
─────────────────────
□ রিজিউমি আপডেট
□ Mock ইন্টারভিউ
□ বাংলাদেশের কোম্পানিতে অ্যাপ্লাই
□ Bug Bounty শুরু
"
```

---

## ৪৭.৩ Resources: বই, YouTube, Platform

### বই

| বই | লেখক | লেভেল | কেন পড়বে |
|-----|-------|-------|-----------|
| The Web Application Hacker's Handbook | Stuttard & Pinto | ইন্টারমিডিয়েট | ওয়েব হ্যাকিংয়ের বাইবেল |
| Penetration Testing: A Hands-On Introduction | Georgia Weidman | বিগিনার | প্র্যাকটিক্যাল হ্যান্ডবুক |
| Linux Basics for Hackers | OccupyTheWeb | বিগিনার | লিনাক্স শেখার জন্য সেরা |
| The Hacker Playbook 3 | Peter Kim | ইন্টারমিডিয়েট | রিয়েল-ওয়ার্ল্ড পেন্টেস্ট |
| Red Team Field Manual | Ben Clark | অ্যাডভান্সড | কুইক রেফারেন্স |
| Blue Team Handbook | Don Murdoch | সব | ডিফেন্স শিখতে |

### YouTube চ্যানেল

```bash
echo "=== ইউটিউব চ্যানেল (সাজানো গুরুত্ব অনুযায়ী) ==="
echo ""
echo "বিগিনার লেভেল:"
echo "  1. NetworkChuck — সবচেয়ে ফানি, বিগিনার ফ্রেন্ডলি"
echo "  2. John Hammond — CTF, ম্যালওয়্যার এনালাইসিস"
echo "  3. IppSec — HTB মেশিন ওয়াকথ্রু (বেস্ট!)"
echo "  4. The Cyber Mentor — PNPT কোর্স, রিয়েল ওয়ার্ল্ড"
echo ""
echo "ইন্টারমিডিয়েট লেভেল:"
echo "  5. LiveOverflow — বাইনারি এক্সপ্লয়েটেশন"
echo "  6. STÖK — Bug Bounty ফোকাসড"
echo "  7. InsiderPhD — Bug Bounty, ভুলনেবিলিটি ডিসকভারি"
echo "  8. NahamSec — Bug Bounty টেকনিক"
echo ""
echo "অ্যাডভান্সড লেভেল:"
echo "  9. 0xdf — HTB রাইট-আপ, ডিটেইলড"
echo " 10. Rana Khalil — PortSwigger ল্যাব সলিউশন"
echo " 11. HackerSploit — পেন্টেস্টিং"
echo " 12. Seytonic — হার্ডওয়্যার হ্যাকিং"
```

### প্ল্যাটফর্ম

| প্ল্যাটফর্ম | টাইপ | মূল্য | সেরা ফিচার |
|-------------|------|-------|-------------|
| TryHackMe | লার্নিং | ফ্রি/প্রিমিয়াম ($10/মাস) | গাইডেড লার্নিং পাথ |
| HackTheBox | চ্যালেঞ্জ | ফ্রি/ভিআইপি ($20/মাস) | রিয়েল-ওয়ার্ল্ড মেশিন |
| PortSwigger Web Security Academy | ওয়েব ল্যাব | ১০০% ফ্রি | সবচেয়ে বিস্তারিত ওয়েব ল্যাব |
| PentesterLab | লার্নিং | $20/মাস | প্রোগ্রেসিভ লার্নিং |
| VulnHub | ভিএম | ১০০% ফ্রি | অফলাইন চ্যালেঞ্জ |
| RangeForce | সিমুলেশন | ফ্রি/পেইড | ব্লু টিম ট্রেনিং |
| LetsDefend | ডিফেন্স | ফ্রি/পেইড | সক ট্রেনিং |

---

## ৪৭.৪ Portfolio: GitHub, CVE Report, Writeups

### GitHub প্রোফাইল

```bash
# ============================================
# হ্যাকিং পোর্টফোলিও — গিটহাব স্ট্রাকচার
# ============================================

echo "=== গিটহাব প্রোফাইল === "
echo ""

echo "README.md (প্রোফাইলে পিন করো):"
cat << 'EOF'
# Hi there, I'm [তোমার নাম] 👋

## 🔥 Ethical Hacker | Pentester | CTF Player

### 🛠️ টুলস এবং স্কিলস
- **রিকন:** nmap, masscan, subfinder, amass
- **ওয়েব:** Burp Suite, sqlmap, dirb, ffuf
- **এক্সপ্লয়েট:** Metasploit, python exploit dev
- **প্রিভ এসকেলেশন:** Linux/Windows PE

### 📂 পোর্টফোলিও প্রকল্পসমূহ
- [AutoRecon](link) — রিকন অটোমেশন স্ক্রিপ্ট
- [CTF-Writeups](link) — সিটিএফ সলিউশন
- [Pentest-Checklist](link) — পেন্টেস্ট চেকলিস্ট

### 🏆 সাফল্য
- CVE-2026-XXXX (বাগ রিপোর্ট)
- HTB: অ্যাক্টিভ ইউজার, টপ %৫
- HackerOne: ৫টি ভ্যালিড রিপোর্ট

### 📜 সার্টিফিকেশন
- CEH (২০২৬)
- PNPT (২০২৬)
- CompTIA Security+ (২০২৬)

<!-- ভিজিটর কাউন্ট -->
![](https://komarev.com/ghpvc/?username=তোমার-ইউজারনেম)
EOF

echo ""
echo "=== গিটহাবে কী কী থাকবে ==="
echo ""
echo "১. AutoRecon — তোমার নিজের টুল (স্টার বেশি পাবে)"
echo "   → bash/python/php, যেকোনো ভাষায়"
echo "   → ডকুমেন্টেশন ভালো করে লেখো"
echo ""
echo "২. CTF-Writeups — সিটিএফ সমাধান"
echo "   → ফোল্ডার ভিত্তিক (HTB, THM, VulnHub)"
echo "   → প্রতিটা সলিউশনে ডিটেইলড ব্যাখ্যা"
echo ""
echo "৩. Pentest-Checklist"
echo "   → চেকলিস্ট স্টাইলে (নতুনদের জন্য)"
echo ""
echo "৪. Homelab-Setup"
echo "   → তোমার হোমল্যাব কনফিগ ফাইল"
echo "   → Vagrantfile, Dockerfile"
echo ""
echo "৫. OSCP-Notes"
echo "   → তোমার পড়া নোটস (পাবলিক করো)"
```

### CVE রিপোর্ট

CVE (Common Vulnerabilities and Exposures) পাওয়া মানে তুমি আসলেই কিছু খুঁজে পেয়েছো। এটা তোমার পোর্টফোলিওর জন্য সোনার ডিম!

```bash
# CVE পাওয়ার স্টেপ
echo "=== CVE পাওয়ার গাইড ==="
echo ""
echo "স্টেপ ১: ভুলনেবিলিটি খোঁজো"
echo "  → ওপেন সোর্স প্রজেক্ট চেক করো"
echo "  → WordPress প্লাগিন/থিম চেক করো"
echo "  → npm/pip প্যাকেজ চেক করো"
echo ""
echo "স্টেপ ২: প্রুফ অফ কনসেপ্ট লেখো"
echo "  → পাইথন/ bash স্ক্রিপ্ট"
echo "  → ভিডিও ডেমো (ঐচ্ছিক)"
echo ""
echo "স্টেপ ৩: মেইনটেইনারকে রিপোর্ট করো"
echo "  → ইমেল/গিটহাব ইস্যু"
echo "  → ৪৫-৯০ দিন অপেক্ষা করো"
echo ""
echo "স্টেপ ৪: MITRE-তে CVE রিকোয়েস্ট করো"
echo "  → https://cve.mitre.org/cve/request_id.html"
echo "  → অথবা ডিরেক্ট: CVE Program"
echo ""
echo "স্টেপ ৫: পাবলিশ করো"
echo "  → আপনার ব্লগ/মিডিয়ামে"
echo "  → Twitter/LinkedIn এ শেয়ার করো"
```

### Writeup আপলোড করার সাইট

```
১. GitHub (তোমার নিজের সাইট) — বেস্ট অপশন
২. Medium — বেশি রিচ পাবে
৩. Dev.to — টেক কমিউনিটি
৪. Hashnode — ডেভেলপার ফোকাসড
৫. আপনার নিজের ব্লগ — ওয়ার্ডপ্রেস/গিটহাব পেজ
```

---

## ৪৭.৫ LinkedIn Profile Optimization

```bash
echo "=== লিংকডইন প্রোফাইল অপটিমাইজেশন ==="
echo ""

echo "হেডার ইমেজ: হ্যাকিং থিম (কালি লিনাক্স ওয়ালপেপার)"
echo ""

echo "হেডলাইন (শিরোনাম) — সবচেয়ে গুরুত্বপূর্ণ!"
echo "  খারাপ: 'Student' — ❌"
echo "  ভালো:   'Ethical Hacker | Pentester | CEH | OSCP | Web Security Researcher'"
echo ""

echo "সারাংশ (About Section):"
cat << 'EOF'
Ethical Hacker with 2+ years of experience in web application security.
I specialize in:
🔹 Web Application Penetration Testing
🔹 Network Security Assessment
🔹 Bug Bounty Hunting

🏆 CVE-2026-XXXX — Discovered critical vulnerability in X
🏆 Top %5 on HackTheBox
🏆 10+ validated reports on HackerOne

I believe in sharing knowledge — check my GitHub for tools and writeups!

🔗 GitHub: github.com/yourhandle
📧 Email: your.email@domain.com
EOF

echo ""
echo "এক্সপেরিয়েন্স সেকশন:"
echo "  → Bug Bounty (self-employed) — current"
echo "  → Freelance Pentester"
echo "  → Internship at a cybersecurity firm"
echo ""

echo "সার্টিফিকেশন সেকশন:"
echo "  → CEH (সার্ট নম্বর দিয়ে)"
echo "  → PNPT (TCM Security)"
echo "  → Security+ (CompTIA)"
echo "  → HTB CBBH (যদি থাকে)"
echo ""

echo "প্রকল্প সেকশন:"
echo "  → AutoRecon টুল (লিংক)"
echo "  → CTF Writeups (লিংক)"
echo "  → CVE Research (লিংক)"
echo ""

echo "লিংকডইন টিপস:"
echo "✅ #Opentowork ব্যাজ অন করো"
echo "✅ ক্রিয়েটর মোড অন করো (নলেজ শেয়ারিং)"
echo "✅ সপ্তাহে ১ বার সিকিউরিটি নিয়ে পোস্ট দাও"
echo "✅ IppSec, STÖK, NetworkChuck কে ফলো করো"
echo "✅ কমেন্টস করো — ভিজিবিলিটি বাড়বে"
```

---

## ৪৭.৬ ল্যাব এক্সারসাইজ

| সপ্তাহ | টাস্ক | ডেডলাইন |
|--------|-------|----------|
| ১ | কালি লিনাক্স ইন্সটল + বেসিক ৫০ কমান্ড শেখো | ৭ দিন |
| ২ | লিনাক্স বেসিক শেষ + Wireshark চালানো শেখো | ৭ দিন |
| ৪ | হোমল্যাব তৈরি (DVWA + Metasploitable) | ৭ দিন |
| ৮ | ৫টা HTB মেশিন সলভ করো (ইজি) | ১৪ দিন |
| ১২ | PortSwigger ল্যাব (SQLi + XSS, সবগুলো) | ১৪ দিন |
| ১৬ | ৩টা মিডিয়াম HTB মেশিন | ১৪ দিন |
| ২০ | প্রথম CVE/Bug Bounty রিপোর্ট | ১৪ দিন |
| ২৪ | পূর্ণাঙ্গ পোর্টফোলিও তৈরি + জব অ্যাপ্লাই | ৭ দিন |

---

## ৪৭.৭ মনে রাখো

| বিষয় | কী মনে রাখবে |
|-------|-------------|
| Consistency > Intensity | প্রতিদিন ২ ঘণ্টা — ৬ মাসে মাষ্টার |
| Practice > Theory | ৮০% প্র্যাকটিস, ২০% থিওরি |
| Learn by doing | নিজে টুল বানাও, টিউটোরিয়াল শুধু দেখলে হবে না |
| Community | ডিসকর্ড, রেডডিট, টেলিগ্রাম গ্রুপে জয়েন করো |
| Certifications | CEH (বাংলাদেশে চাকরি), OSCP (গ্লোবাল) |
| GitHub | তোমার পোর্টফোলিও — আপডেট রাখো |
| LinkedIn | নেটওয়ার্কিং — পোস্ট দাও, ভিজিবিলিটি বাড়াও |
| English | ডকুমেন্টেশন রিডিং + রিপোর্ট লেখার জন্য দরকার |

> **ভাই-বন্ধুর টিপস:** এই রোডম্যাপ ফলো করলে ৬ মাসে তুমি জব-রেডি হবে। কিন্তু শুনো — শুধু পড়লে হবে না। প্রতিদিন টার্মিনাল ওপেন করো। প্রতিদিন অন্তত ১টা কমান্ড টাইপ করো। আর হ্যাঁ, আটকে গেলে হাল ছাড়ো না — Google আর ChatGPT তোমার বেস্ট ফ্রেন্ড!
