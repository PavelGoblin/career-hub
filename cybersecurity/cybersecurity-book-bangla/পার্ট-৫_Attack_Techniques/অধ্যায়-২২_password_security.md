# অধ্যায় ২২: Password Security

## সহজ কথায়:
Password = তোমার ডিজিটাল দরজার চাবি। দুর্বল চাবি → চোর সহজেই ঢুকে পড়ে। শক্ত চাবি → চেষ্টা করেও ভাঙতে পারে না।

---

## ২২.১ Strong Password কীভাবে বানাবে

### Weak Passwords (তোমার password এইগুলোর মধ্যে আছে?):

```
🚫 password123
🚫 123456
🚫 qwerty
🚫 abc123
🚫 iloveyou
🚫 letmein
🚫 admin
🚫 12345678
🚫 password
🚫 বাংলাদেশের নাম, birthday, phone number
```

### Strong Password Formula:

```
📐 Formula: L + N + S + U/L

L = 12+ characters (min 12, better 16)
N = Numbers (0-9)
S = Special chars (!@#$%^&*)
U = Uppercase + Lowercase mix
```

### Example:

```bash
# Weak:         john1990
# Strong:       MyD0g!sC@ll3dR0cky2025#
# Better:       Xk9#mP2$vL8@qR5! (random — ব্যবহার করো password manager)
```

### Passphrase Method (মনে রাখা সহজ):

```bash
# ৪-৫টা random word নাও:
"purple elephant dances under moon"
# → প্রথম letter + special:
"P3lePh!nD@nc3sUnD3rM00n"  # Strong + rememberable
```

---

## ২২.২ Password Manager ব্যবহার

### কেন Password Manager?

```
❌ এক password সব জায়গায় — hack হলে সব account খোলা
❌ কাগজে লেখা — হারিয়ে যায়
❌ মাথায় রাখা — ভুলে যাও (৬৩টা আলাদা password?)
✅ Password Manager — এক master password দিয়ে সব manage
```

### Best Password Managers (২০২৫):

| Tool | Free? | Features |
|------|-------|----------|
| **Bitwarden** | ✅ Free + Open Source | Cross-platform, self-host |
| **KeePass** | ✅ Free + Open Source | Local only (no cloud) |
| **1Password** | ❌ Paid ($3/mo) | Best UX |
| **Dashlane** | ❌ Paid | Dark web monitoring |

### Bitwarden Setup:

```bash
# Browser extension install:
# Chrome/Firefox → Bitwarden

# Desktop app:
https://bitwarden.com/download/

# CLI:
sudo snap install bitwarden

# Best practice:
1. যেকোনো site-এ random 16+ char password
2. master password = strong (write on paper, keep safe)
3. 2FA চালু করো Bitwarden-এ
```

---

## ২২.৩ MFA vs 2FA — পার্থক্য ও গুরুত্ব

### Factor Types:

| Factor | কী | উদাহরণ |
|--------|-----|---------|
| **Something you KNOW** | Password | তোমার পাসওয়ার্ড |
| **Something you HAVE** | Device | Phone, hardware token |
| **Something you ARE** | Biometric | Fingerprint, face |

### 2FA vs MFA:

```
2FA = ঠিক ২টা factor
MFA = ২ বা তার বেশি factor

2FA: Password (know) + OTP (have) = ✅
MFA: Password + OTP + Fingerprint = ✅ (better)
```

### MFA Methods (Security level):

```
Level 1: SMS OTP ⚠️ (SIM swap risk)
Level 2: Authenticator App (Google Auth, Authy) ✅
Level 3: Push Notification (Microsoft Auth) ✅
Level 4: Hardware Key (YubiKey) 🥇 BEST
Level 5: Biometric + Hardware 🥇
```

### MFA Enable করা উচিত যেখানে:

```
🔴 Email (gateway to everything)
🔴 Password Manager
🔴 Social Media (Facebook, Instagram)
🔴 Banking (bKash, Nagad, Bank)
🔴 Cloud (Google, Microsoft, AWS)
🔴 GitHub/Dev accounts
🔴 Domain registrar
```

---

## ২২.৪ WhatsApp সুরক্ষিত রাখার উপায়

### WhatsApp Security Checklist:

```bash
✅ Two-Step Verification চালু করো
   Settings → Account → Two-step verification → Enable
   → 6 digit PIN set করো

✅ Fingerprint/Face unlock
   Settings → Privacy → Fingerprint lock → Enable

✅ Disappearing messages
   Chat → Disappearing messages → 90 days

✅ Privacy settings:
   Last seen → Nobody / My contacts
   Profile photo → My contacts
   About → My contacts
   Status → My contacts

✅ Read receipts off (যদি চাও)
✅ Block unknown callers
✅ Report spam
✅ Forwarding info check
```

### WhatsApp Security Risks:

```
❌ Clicking unknown links (phishing)
❌ Sharing OTP with anyone — NEVER!
❌ Public WhatsApp groups (anyone can see number)
❌ Unencrypted backup (Google Drive/iCloud ke diye → not E2E encrypted)
❌ SIM swap attack (carrier কে ফোন করে SIM new device-এ activate)
```

### SIM Swap Protection:

```bash
# বাংলাদেশ:
✓ GP-তে PIN set করো (dial *123*50#)
✓ Robi-তে SIM lock service
✓ Bank-এ SIM change notification চালু করো
✓ Never share OTP (even "bank"
```

---

## ২২.৫ Common Password Attacks & Defense

| Attack | কীভাবে কাজ করে | Defense |
|--------|---------------|---------|
| **Brute Force** | সব combination try | Strong password |
| **Dictionary** | Common password list | Avoid common words |
| **Rainbow Table** | Pre-computed hash | Salted hash |
| **Keylogging** | keyboard input record | Antivirus, 2FA |
| **Phishing** | Fake login page | Check URL, 2FA |
| **Credential Stuffing** | Leaked password → other sites | Unique password per site |
| **Shoulder Surfing** | পিছন থেকে দেখা | Privacy screen |
| **Social Engineering** | মানুষকে騙ে | Awareness |

---

## 📌 মনে রাখো

| Rule | বিস্তারিত |
|------|-----------|
| **Minimum 12 chars** | Longer = stronger |
| **Unique per site** | Password manager use করো |
| **2FA everywhere** | Especially email + bank |
| **Password Manager** | Bitwarden (free) recommended |
| **WhatsApp PIN** | 2-step verification চালু করো |
| **No SMS for critical** | SMS OTP ঝুঁকিপূর্ণ |

**পার্ট ৬ শুরু হচ্ছে — Web Application Security (OWASP Top 10)! 🌐**
