# অধ্যায় ২: Ethical Hacking কী?

## সহজ কথায়:
তুমি যদি লকস্মিথ হও, তুমি তালা খুলতে জানো। এখন তুমি কি চোর নাকি পেশাদার লকস্মিথ? Ethical Hacker হলো পেশাদার লকস্মিথ — যে অনুমতি নিয়ে তালা খোলে, দুর্বলতা দেখায়, আর ঠিক করে দেয়।

---

## ২.১ White Hat vs Black Hat vs Grey Hat

### ⚪ White Hat (Ethical Hacker)
আইনি উপায়ে hack করে। কোম্পানি অনুমতি দিয়েছে, scope (কোথায় hack করবে) ঠিক করা, তারপর কাজ করে রিপোর্ট দেয়।

**বাস্তব উদাহরণ:** তুমি GP-তে চাকরি করো। GP-র নেটওয়ার্ক hack করে দেখাও, "দেখুন, তোমাদের এই server-এ দুর্বলতা আছে। ঠিক করুন।"

### ⚫ Black Hat (Malicious Hacker)
অবৈধ hack করে। চুরি, ক্ষতি, ransomware, ডেটা লিক।

**বাস্তব উদাহরণ:** কেউ bKash hack করে টাকা চুরি করল। এটা criminal offense — জেল হবে।

### 🌑 Grey Hat
দুইয়ের মাঝখানে। Black Hat নয় (ক্ষতি করে না), কিন্তু White Hat-ও নয় (অনুমতি নেয় না)। নিজে থেকে দুর্বলতা খুঁজে, কোম্পানিকে জানায় — কখনো ফ্রি, কখনো বিনিময়ে টাকা চায়।

**বাস্তব উদাহরণ:** তুমি ফেসবুকে একটা দুর্বলতা পেলে। ফেসবুককে না জানিয়ে নিজে টেস্ট করলে, তারপর জানালে। এটা technically grey area।

---

## ২.২ Legal Boundary — কোনটা Legal, কোনটা জেল

বাংলাদেশের **ডিজিটাল নিরাপত্তা আইন, ২০১৮** অনুযায়ী:

| কাজ | Legal? | শাস্তি |
|-----|--------|--------|
| নিজের system-এ pentest | ✅ Legal | - |
| Bug bounty (authorized) | ✅ Legal | - |
| অন্যের system hack | ❌ Illegal | ৭-১৪ বছর জেল |
| অনুমতি ছাড়া scan | ❌ Illegal | ৩-৭ বছর জেল (কিছু ক্ষেত্রে) |
| Phishing / social engineering (অনুমতি ছাড়া) | ❌ Illegal | ১০ বছর পর্যন্ত |
| নিজের কোম্পানির pentest | ✅ Legal | - |
| CTF / lab এ hack | ✅ Legal | - |

### গুরুত্বপূর্ণ!
- তুমি শিখবে **অনুমতি নিয়ে** কাজ করতে
- কখনো production server (যা real user use করে) scan করবে না নিজের ইচ্ছায়
- শুধু lab environment-এ practice করবে যতক্ষণ না professional job পাও

---

## ২.৩ Rules of Engagement (RoE)

Ethical hacking-এর সবচেয়ে গুরুত্বপূর্ণ জিনিস। তুমি যখন professional pentest করো, তখন ক্লায়েন্টের সাথে contractual agreement করো যেখানে **Rules of Engagement (RoE)** থাকে।

RoE-তে কী থাকে:
- **Scope:** কোন IP, কোন system, কোন application test করবে
- **Out of Scope:** কী test করবে না (যেমন backup server, HR database)
- **Timing:** কখন test করবে (রাতে? অফিস টাইমে?)
- **Communication:** emergency contact number
- **Data Handling:** পাওয়া ডেটা কী করবে
- **Legal Protection:** কোম্পানি তোমাকে immune করছে legal action থেকে
- **Emergency Stop:** যেকোনো সময় test বন্ধ করার ক্ষমতা

### 🎯 Real Life Analogy
তুমি ডাক্তার। রোগী (কোম্পানি) বলেছে, "শুধু পা দেখবেন, মাথা দেখবেন না।" তুমি যদি মাথা দেখো, তাহলে unethical। তেমনি ক্লায়েন্ট যদি বলে "শুধু web app test করো, internal network নয়" — তাহলে তুমি network-এ হাত দেবে না।

---

## ২.৪ Ethics ও Professional দায়িত্ব

### Ethical Hacker-এর Golden Rules:
1. **অনুমতি নাও** — কাজ শুরু করার আগে written permission
2. **Scope-র বাইরে যেও না** — শুধু যা বলা হয়েছে তাই করো
3. **ডেটা protect করো** — ক্লায়েন্টের পাওয়া ডেটা secure রাখো
4. **Damage করবে না** — pentest-এ system crash/ডেটা loss হলে দায়
5. **Report দাও** — কী পেয়েছ, কীভাবে ঠিক করবে, সব documentation
6. **Confidentiality** — ক্লায়েন্টের দুর্বলতা গোপন রাখো

### Ethical Hacker কীভাবে কাজ করে (step-by-step):
```
Step 1: Client কোম্পানি যোগাযোগ করে — "আমাদের system test করে দেন"
Step 2: Scope agreement সই হয় — কী test হবে, কী হবে না
Step 3: NDA (Non-Disclosure Agreement) সই — গোপন রাখবে
Step 4: Pentest শুরু — তথ্য সংগ্রহ, scan, exploitation
Step 5: Report জমা — দুর্বলতা, risk level, fix suggestion
Step 6: Remediation — তারা ঠিক করে, তুমি retest করো
Step 7: Close — প্রকল্প শেষ
```

---

## ২.৫ Ethical Hacking Methodology (সাধারণ কাঠামো)

সমস্ত pentest এই পাঁচ ধাপে হয় — একে বলে **5 Stages of Hacking** (আমরা Part 5-এ বিস্তারিত দেখব):

```
1️⃣ Reconnaissance (তথ্য সংগ্রহ)
    ↓
2️⃣ Scanning & Enumeration
    ↓
3️⃣ Gaining Access (exploit)
    ↓
4️⃣ Maintaining Access (persistence)
    ↓
5️⃣ Clearing Tracks
```

**Blue Team version:** এই পাঁচ ধাপ জানলে বুঝবে attacker কী করে। তখনই defense plan করতে পারবে।

---

## 💡 ল্যাব এক্সারসাইজ

তোমার প্রথম ethical hacking assignment:
```
Scenario: 
"ABC Ltd." নামে একটি কোম্পানি তোমাকে তাদের web application
test করতে বলেছে। তারা নিচের তথ্য দিয়েছে:
- Test scope: 192.168.1.10 (web server)
- Out of scope: 192.168.1.20 (backup server), 192.168.1.30 (mail server)
- Timing: রাত ৮টা-১২টা
- Test type: Black Box (তুমি কিছুই জানো না)

প্রশ্ন:
১. তুমি কী কী tool ব্যবহার করবে প্রথমে?
২. Scope-র বাইরে server scan করলে কী হবে?
৩. তুমি যদি backup server-এ vulnerability পাও, report করবে কি করবে না?
```

**উত্তর:** নিচের উত্তর পড়ার আগে নিজে চিন্তা করো।

<details>
<summary>উত্তর দেখো</summary>

১. প্রথমে reconnaissance tool: Nmap (scan), theHarvester (info gathering)
২. Scope-র বাইরে scan করলে agreement ভঙ্গ হবে। Legal problem হতে পারে।
৩. Report করবে শুধু যদি emergency/critical হয় এবং আগে client-কে বলো। সাধারণত scope-র বাইরের জিনিস report না করাই ভালো।
</details>

---

## 📌 মনে রাখো

| কী পয়েন্ট | ব্যাখ্যা |
|------------|----------|
| White Hat ↔ অনুমতি নিয়ে কাজ | সম্পূর্ণ আইনি |
| Black Hat ↔ চুরি/ক্ষতি | জেল হবে |
| RoE সবচেয়ে গুরুত্বপূর্ণ | scope, timing, rules |
| 5 Stages of Hacking | Recon → Scan → Exploit → Maintain → Clear |

**পরবর্তী অধ্যায়ে আমরা দেখব কীভাবে certification নিয়ে এই ফিল্ডে professional হতে পারো।**
