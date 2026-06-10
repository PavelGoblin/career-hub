# অধ্যায় ১: Cybersecurity কী এবং কেন শিখবে?

## সহজ কথায়:
তোমার বাড়ির দরজায় তালা দাও—ঠিক তেমনি তোমার ডিজিটাল জীবনেও তালা দিতে হয়। Cybersecurity মানে হলো **ডিজিটাল তালা ও পুলিশ** একসাথে।

---

## ১.১ Cybersecurity কী?

Cybersecurity মানে হলো **তথ্য ও সিস্টেমকে রক্ষা করা** — হ্যাকার, ভাইরাস, ransomware, ডেটা চুরি, সবকিছু থেকে।

রিয়েল লাইফ analogy দিই। ধরো, তুমি একটা ফ্ল্যাটে থাকো। তোমার:
- **দরজার লক** → Firewall (বাইরের মানুষ ঠেকায়)
- **সিসি ক্যামেরা** → IDS/IPS (কেউ সন্দেহজনক ঘুরছে কিনা দেখে)
- **গার্ড** → Antivirus (খারাপ লোক ধরে)
- **জানালার গ্রিল** → Encryption (ডেটা এমনভাবে ঘুরিয়ে দেয় যে কেউ চুরি করলেও পড়তে পারবে না)

এই সবকিছু মিলেই **Cybersecurity**।

---

## ১.২ কেন Cybersecurity এত গুরুত্বপূর্ণ?

2025 সালের কিছু সংখ্যা দেখো:

| বছর | গড় ডেটা লিকের খরচ (বিশ্বব্যাপী) |
|-----|------|
| 2020 | $3.86 মিলিয়ন |
| 2023 | $4.45 মিলিয়ন |
| 2025 | $5+ মিলিয়ন |

**বাংলাদেশের কথা বলি:**
- 2023 সালে বাংলাদেশ ব্যাংকের বেশ কয়েকটি phishing attack
- সরকারি ওয়েবসাইটে ঘন ঘন deface attack
- রিক্রুটিং ফার্ম, হাসপাতাল, ব্যাংক — সব জায়গায় র্যানসমওয়্যার

**তুমি cybersecurity শিখলে কী হবে?**
- দেশের ডিজিটাল নিরাপত্তা দিতে পারবে
- ভালো চাকরি পাবে (বাংলাদেশে entry-level 30k-80k, senior-এ 2-3 লাখ)
- ফ্রিল্যান্সিং করতে পারবে (bug bounty, pentesting)

---

## ১.৩ Blue Team vs Red Team vs Purple Team

এইটা muচ—ই মজার জিনিস। তিন ধরনের cybersecurity পেশাজীবী:

### 🔵 Blue Team (ডিফেন্ডার)
যারা **প্রতিরক্ষা** করে। এদের কাজ:
- Firewall, IDS/IPS configure
- Incident response
- সার্ভার harden করা
- Log analysis

**উপমা:** বাড়ির গার্ড। যারা চোর ঢুকতে দেবে না।

### 🔴 Red Team (আক্রমণকারী)
যারা **আক্রমণ করে** (কিন্তু legal উপায়ে)। এদের কাজ:
- Pentesting
- Vulnerability assessment
- Social engineering test

**উপমা:** তুমি বাড়ির নিরাপত্তা টেস্ট করার জন্য hired চোর—যে চুরি করে দেখাবে কোথায় ফাঁকফোকর আছে।

### 🟣 Purple Team (দুজনের সমন্বয়)
Red Team কী পেল, Blue Team কীভাবে ঠিক করবে—এই সমন্বয় করে।

---

## ১.৪ Career Paths in Cybersecurity

বাংলাদেশে cybersecurity-তে কী কী ক্যারিয়ার আছে:

| ক্যারিয়ার | বেতন (entry) | কী করতে হবে |
|------------|-------------|-------------|
| **SOC Analyst** | 25k-50k BDT | ২৪/৭ মনিটরিং, alert দেখে |
| **Pentester** | 40k-80k BDT | কোম্পানির সিস্টেম hack করে দুর্বলতা দেখানো |
| **Security Engineer** | 50k-1.2L BDT | Firewall, VPN, SIEM configure |
| **GRC Analyst** | 40k-70k BDT | compliance check, policy লেখা |
| **Digital Forensics** | 60k-1.5L BDT | crime scene থেকে evidence সংগ্রহ |
| **Cloud Security** | 80k-2L BDT | AWS/Azure secure রাখা |
| **Bug Bounty Hunter** | Variable | freelance, per bug $100-$10k |

### GRC (Governance, Risk, Compliance)
GRC মানে হলো **নিয়মকানুন**। যেমন:
- GDPR (Europe-এর privacy law)
- HIPAA (Healthcare data)
- PCI DSS (Credit card data)
- বাংলাদেশ ডিজিটাল নিরাপত্তা আইন, ২০১৮

এটি comparatively সহজ এবং চাকরির বাজার ভালো।

### Cloud Security
AWS, Azure, Google Cloud — সব ক্লাউড secure রাখা। ২০২৬ সালে সবচেয়ে চাহিদাপূর্ণ স্কিল।

### Digital Forensics
কম্পিউটার ক্রাইম সিন থেকে evidence সংগ্রহ। পুলিশ, গোয়েন্দা, বা প্রাইভেট ফার্মে কাজ।

---

## ১.৫ AI-এর ভবিষ্যৎ Cybersecurity-তে

এটা নিয়ে সবাই চিন্তিত। AI কী আমাদের চাকরি নেবে নাকি?

### AI যা **করবে**:
- Log analysis自動 (SIEM automation)
- Basic vulnerability scan
- Phishing detection
- Malware analysis (speed)

### AI যা **করবে না**:
- Creative attack thinking
- Complex pentesting methodology
- Social engineering (হ্যাঁ, AI social engineering পারে, কিন্তু মানুষের intuition লাগে)
- Strategic decision making
- Incident response (AI suggest করতে পারে, কিন্তু final call মানুষই নেবে)

**মনে রাখো:** AI একটা টুল। যেমন calculator গণিতবিদের চাকরি নেয়নি, বরং সাহায্য করেছে। AI-ও cybersecurity-কে সাহায্য করবে, প্রতিস্থাপন করবে না।

---

## ১.৬ বাংলাদেশে Scope ও চাকরির বাজার

বাংলাদেশে cybersecurity-র বাজার দ্রুত বাড়ছে:

- **সরকারি সেক্টর:** BGD e-GOV, ডিজিটাল নিরাপত্তা এজেন্সি (DNSA)
- **প্রাইভেট সেক্টর:** ব্যাংক, MNO, ISP
- **মাল্টিন্যাশনাল:** Kaspersky, Palo Alto (SE region)
- **Freelancing:** Upwork, Fiverr, HackerOne
- **Startup:** বঙ্গবন্ধু hi-tech park-এ সাইবার নিরাপত্তা startup

### কোথায় চাকরি পাবে?
1. bdjobs.com → search "cyber security" or "network security"
2. linkedin.com → Bangladesh location filter
3. দরজা ওয়েবসাইট → সরকারি চাকরি
4. কোম্পানির ক্যারিয়ার পেজ → bKash, Nagad, Dutch-Bangla Bank, Robi, Grameenphone

---

## 💡 ল্যাব এক্সারসাইজ

```
# নিজের ল্যাব। কোনো software লাগবে না।
# শুধু কাগজ-কলম

১. নিচের scenario পড়ো:
   - তুমি একটি ব্যাংকের security engineer
   - ব্যাংকে অনলাইন ট্রান্সফার সিস্টেম আছে
   - হঠাৎ একজন গ্রাহক বললেন, তার অ্যাকাউন্ট থেকে ৫০,০০০ টাকা চলে গেছে
   - সে password কাউকে দেয়নি

২. উত্তর দাও:
   a) তুমি কীভাবে investigation শুরু করবে?
   b) এটা কি Blue Team নাকি Red Team জিনিস?
   c) কী কী tool ব্যবহার করতে পারো?
```

---

## 📌 মনে রাখো

| কী পয়েন্ট | ব্যাখ্যা |
|------------|----------|
| Cybersecurity = ডিজিটাল নিরাপত্তা | নিজের ডেটা, সিস্টেম, নেটওয়ার্ক বাঁচানো |
| Blue Team বাঁচায়, Red Team আক্রমণ করে | দুটোই দরকার |
| AI সাহায্য করবে, প্রতিস্থাপন করবে না | AI tool, চাকরি নয় |
| বাংলাদেশে scope ভালো | বেতন 25k থেকে শুরু, 2L+ পর্যন্ত |
| ২০২৬ সালে সবচেয়ে চাহিদা | Cloud Security + AI Security |

**এখন তুমি জানো Cybersecurity কী এবং কেন শিখবে। পরবর্তী অধ্যায়ে Ethical Hacking নিয়ে বিস্তারিত আলোচনা করব। আপাতত উপরের ল্যাব এক্সারসাইজটা করে ফেলো! 🚀**
