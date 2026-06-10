# অধ্যায় ৪৪: OSINT Advanced

> **ভাই-বন্ধুর মতো বলছি:** OSINT শুধু গুগলে সার্চ করা না ভাই! এইটা একটা আর্ট। তুমি যদি গুগল দারঠিকভাবে ব্যবহার করতে পারো, তাহলে যেকোনো টার্গেটের সম্পর্কে প্রায় সবকিছুই বের করতে পারবে। আর টুলস কম্বাইন করে তুমি সুপার OSINT ফ্রেমওয়ার্ক বানাতে পারো।

---

## ৪৪.১ সহজ কথায় OSINT

OSINT (Open Source Intelligence) হলো পাবলিকলি উপলব্ধ ডাটা থেকে ইন্টেলিজেন্স বের করা। ফেসবুক, টুইটার, গিটহাব, শোডান — সবই OSINT-এর সোর্স।

**কেন দরকার?**
- পেন্টেস্টিং-এর প্রথম স্টেপ
- সোশ্যাল ইঞ্জিনিয়ারিং অ্যাটাকের জন্য ইনফো কালেক্ট
- বাগ বাউন্টিতে টার্গেট রিসার্চ
- লোকেশন ট্র্যাকিং
- ইমেল/ফোন নম্বর ভেরিফিকেশন

---

## ৪৪.২ Live Demonstration Techniques

### গুগল ডরকিং (Google Dorking)

```bash
# লাইভ ডেমো কমান্ড — গুগল ডর্কস
# -------------------------------------------------
# এডমিন প্যানেল খোঁজা
site:target.com intitle:"admin" "login"

# শংসাপত্র ফাঁস (password in title)
site:target.com intitle:"index of" "password"

# সাংবিধানিক ফাইল ফাঁস
site:target.com filetype:sql "INSERT INTO" "password"

# এসকিউএল ইনজেকশন পয়েন্ট
site:target.com inurl:".php?id="

# কনফিগ ফাইল
site:target.com filetype:env "DB_PASSWORD"

# সাবডোমেইন খোঁজা
site:*.target.com -site:www.target.com
```

### শোডান (Shodan) — লাইভ ডেমো

```bash
# শোডান সার্চ কমান্ড (CLI)
# -------------------------------------------------
# শোডান ইনস্টল করা
pip install shodan

# এপিআই কী সেট করা
shodan init YOUR_API_KEY

# নির্দিষ্ট সার্ভিস খোঁজা
shodan search "apache country:BD"

# নির্দিষ্ট আইপি চেক
shodan host 8.8.8.8

# ওপেন সিসিটিভি খোঁজা
shodan search "has_screenshot:true webcam"

# নির্দিষ্ট পোর্ট + দেশ
shodan search "port:3389 country:BD os:Windows"
```

### থার্ভেস্টার (theHarvester) — লাইভ

```bash
# থার্ভেস্টার দিয়ে ইমেল + সাবডোমেইন কালেক্ট
# -------------------------------------------------
# বেসিক ইউসেজ
theHarvester -d target.com -b google

# সব উৎস ব্যবহার করে
theHarvester -d target.com -b google,bing,yahoo,linkedin

# রিপোর্ট ফাইলে সেভ
theHarvester -d target.com -b all -f report.html

# লিমিট সেট করা
theHarvester -d target.com -b google -l 500
```

---

## ৪৪.৩ Combine Tools: Maltego + Shodan + theHarvester

এই তিন টুল কম্বাইন করলে তুমি পাবে পূর্ণাঙ্গ OSINT সলিউশন। নিচে দেখাচ্ছি কীভাবে প্রতিটা টুলের আউটপুট অন্যটার ইনপুট হয়:

### Maltego Setup for Advanced OSINT

```
Maltego Transform Sequence (ট্রান্সফর্ম চেইন):

১. টার্গেট ডোমেইন ইনপুট দাও
২. DNS থেকে আইপিতে → Transform: DNS to IP
৩. আইপি থেকে শোডানে → Transform: IP to Shodan
৪. শোডান থেকে পোর্টে → Transform: Shodan to Ports
৫. পোর্ট থেকে ব্যানারে → Transform: Port to Banner
৬. ডোমেইন থেকে ইমেলে → Transform: Domain to Email (theHarvester)
৭. ইমেল থেকে সোশ্যালে → Transform: Email to Social Media
```

### অটোমেটেড কম্বিনেশন স্ক্রিপ্ট

```bash
#!/bin/bash
# ============================================
# OSINT টুল চেইন — Maltego + Shodan + theHarvester
# অটোমেটেড ইন্টেলিজেন্স কালেকশন
# ============================================

TARGET=$1
SHODAN_API_KEY=$2

if [ -z "$TARGET" ] || [ -z "$SHODAN_API_KEY" ]; then
    echo "ব্যবহার: $0 <টার্গেট> <শোডান-এপিআই-কী>"
    exit 1
fi

OUTPUT_DIR="osint_${TARGET}"
mkdir -p "$OUTPUT_DIR"

echo "╔══════════════════════════════════════╗"
echo "║   OSINT অ্যাডভান্সড ইঞ্জিন শুরু      ║"
echo "╚══════════════════════════════════════╝"

# ============================================
# ফেজ ১: theHarvester — ইমেল, সাবডোমেইন, আইপি
# ============================================
echo ""
echo "[ফেজ ১/৫] theHarvester চলছে..."
theHarvester -d "$TARGET" -b google,bing,yahoo,linkedin -f "$OUTPUT_DIR/harvester.html" 2>/dev/null

# theHarvester থেকে ইমেল এক্সট্র্যাক্ট
grep -oP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' "$OUTPUT_DIR/harvester.html" | sort -u > "$OUTPUT_DIR/emails.txt"
echo "[✓] ইমেল পাওয়া গেছে: $(wc -l < "$OUTPUT_DIR/emails.txt") টি"

# ============================================
# ফেজ ২: DNS এনুমারেশন
# ============================================
echo "[ফেজ ২/৫] DNS এনুমারেশন চলছে..."

# A রেকর্ড
IP_LIST="$OUTPUT_DIR/ip_list.txt"
dig +short A "$TARGET" > "$IP_LIST"
echo "[✓] আইপি পাওয়া গেছে: $(wc -l < "$IP_LIST") টি"

# MX, NS, TXT
dig +short MX "$TARGET" > "$OUTPUT_DIR/mx_records.txt"
dig +short NS "$TARGET" > "$OUTPUT_DIR/ns_records.txt"
dig +short TXT "$TARGET" > "$OUTPUT_DIR/txt_records.txt"

# ============================================
# ফেজ ৩: Shodan — প্রতিটা আইপির বিস্তারিত
# ============================================
echo "[ফেজ ৩/৫] Shodan স্ক্যান চলছে..."

shodan init "$SHODAN_API_KEY" >/dev/null 2>&1

while IFS= read -r ip; do
    if [ -n "$ip" ]; then
        echo "  → চেক করছি: $ip"
        shodan host "$ip" 2>/dev/null >> "$OUTPUT_DIR/shodan_${ip}.txt"
        
        # শোডান থেকে ওপেন পোর্ট বের করা
        grep -E "^\d+/tcp" "$OUTPUT_DIR/shodan_${ip}.txt" 2>/dev/null | awk '{print $1}' >> "$OUTPUT_DIR/all_ports.txt"
    fi
done < "$IP_LIST"

sort -u "$OUTPUT_DIR/all_ports.txt" -o "$OUTPUT_DIR/all_ports.txt"
echo "[✓] শোডান ডেটা কালেক্ট করা হয়েছে"

# ============================================
# ফেজ ৪: ওয়েব স্ক্রিনশট (যদি gowitness থাকে)
# ============================================
echo "[ফেজ ৪/৫] ওয়েব স্ক্রিনশট নিচ্ছি..."

which gowitness >/dev/null 2>&1
if [ $? -eq 0 ]; then
    # HTTP এবং HTTPS উভয়ই
    echo "http://$TARGET" > "$OUTPUT_DIR/targets.txt"
    echo "https://$TARGET" >> "$OUTPUT_DIR/targets.txt"
    gowitness file -f "$OUTPUT_DIR/targets.txt" -P "$OUTPUT_DIR/screenshots/" 2>/dev/null
    echo "[✓] স্ক্রিনশট নেওয়া হয়েছে"
else
    echo "[!] gowitness ইনস্টল করা নেই — স্কিপ করছি"
fi

# ============================================
# ফেজ ৫: রিপোর্ট জেনারেট
# ============================================
echo "[ফেজ ৫/৫] রিপোর্ট জেনারেট করছি..."

{
    echo "# OSINT রিপোর্ট: $TARGET"
    echo "তারিখ: $(date)"
    echo ""
    echo "## ইমেল লিস্ট"
    cat "$OUTPUT_DIR/emails.txt"
    echo ""
    echo "## আইপি লিস্ট"
    cat "$IP_LIST"
    echo ""
    echo "## ওপেন পোর্টস"
    cat "$OUTPUT_DIR/all_ports.txt"
    echo ""
    echo "## DNS রেকর্ডস"
    echo "### MX"
    cat "$OUTPUT_DIR/mx_records.txt"
    echo "### NS"
    cat "$OUTPUT_DIR/ns_records.txt"
    echo "### TXT"
    cat "$OUTPUT_DIR/txt_records.txt"
} > "$OUTPUT_DIR/final_report.md"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║        OSINT কমপ্লিট!                ║"
echo "╚══════════════════════════════════════╝"
echo "ফাইল চেক করো: $OUTPUT_DIR/final_report.md"
```

---

## ৪৪.৪ Automated OSINT Script (Working Code)

পুরো ইন্টেলিজেন্স কালেকশনের জন্য একটা পূর্ণাঙ্গ স্ক্রিপ্ট:

```bash
#!/bin/bash

# ============================================
# অ্যাডভান্সড OSINT ফ্রেমওয়ার্ক
# ফিচার: ইমেল, ফোন, সোশ্যাল মিডিয়া, ব্রীচ ডেটা
# ============================================

echo "╔══════════════════════════════════════╗"
echo "║     অ্যাডভান্সড OSINT v2.0          ║"
echo "╚══════════════════════════════════════╝"

select_option() {
    echo ""
    echo "কী করতে চাও?"
    echo "1) ইমেল ও সোশ্যাল মিডিয়া ইনভেস্টিগেশন"
    echo "2) ফোন নম্বর লোকেশন ও ভেরিফিকেশন"
    echo "3) ইউজারনেম ওসিন্ট (একই ইউজারনেম সব জায়গায় খোঁজা)"
    echo "4) ফুল টার্গেট রিকন (ডোমেইন + আইপি + ইমেল)"
    echo "5) ব্রীচ ডেটা চেক"
    echo "6) এক্সিট"
    read -p "তোমার পছন্দ (1-6): " choice
    
    case $choice in
        1) email_osint ;;
        2) phone_osint ;;
        3) username_osint ;;
        4) full_recon ;;
        5) breach_check ;;
        6) exit 0 ;;
        *) echo "ভুল পছন্দ!"; select_option ;;
    esac
}

email_osint() {
    read -p "টার্গেট ইমেল: " email
    
    echo "[*] ইমেল ভেরিফাই করছি..."
    
    # ইমেল ফরম্যাট চেক
    if [[ "$email" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
        echo "[✓] ভ্যালিড ইমেল ফরম্যাট"
    else
        echo "[✗] ইনভ্যালিড ইমেল"
        return
    fi
    
    # ডোমেইন পার্ট বের করা
    domain=$(echo "$email" | cut -d@ -f2)
    echo "[*] ডোমেইন: $domain"
    
    # এমএক্স রেকর্ড চেক
    echo "[*] মেইল সার্ভার চেক করছি..."
    dig +short MX "$domain" 2>/dev/null | head -5
    
    # HaveIBeenPwned চেক (কালার অফ)
    echo "[*] ব্রীচ ডেটা চেক করছি (হ্যাভ আই বিন পাউন্ড)..."
    echo "    → ম্যানুয়ালি চেক করো: https://haveibeenpwned.com/"
    
    # গিটহাবে ইমেল সার্চ
    echo "[*] গিটহাবে ইমেল সার্চ করছি..."
    curl -s "https://api.github.com/search/commits?q=author-email:$email" 2>/dev/null | grep -oP '"login":\s*"[^"]+"' | head -5
    
    read -p "এন্টার চাপো মেনুতে ফিরতে..."
    select_option
}

phone_osint() {
    read -p "টার্গেট ফোন নম্বর (ওয়ান code সহ): " phone
    
    echo "[*] ফোন নম্বর ভেরিফাই করছি..."
    phone_clean=$(echo "$phone" | sed 's/[^0-9]//g')
    
    if [ ${#phone_clean} -lt 10 ]; then
        echo "[✗] খুব ছোট নম্বর"
        return
    fi
    
    # কান্ট্রি কোড ডিটেক্ট
    code="${phone_clean:0:3}"
    echo "[*] কান্ট্রি কোড: $code"
    
    # numverify API (যদি এপিআই থাকে)
    echo "[*] numverify API কল করছি..."
    echo "    → ফ্রি টায়ার: https://numverify.com/"
    
    # Truecaller (কমান্ড লাইন)
    echo "[*] Truecaller ইনফো..."
    echo "    → https://www.truecaller.com/search/"
    
    # হোয়াটসঅ্যাপ চেক
    echo "[*] হোয়াটসঅ্যাপে আছে কিনা চেক করছি..."
    whatsapp_url="https://wa.me/$phone_clean"
    echo "    → $whatsapp_url"
    
    # সোশ্যাল মিডিয়া সার্চ
    echo "[*] সোশ্যাল মিডিয়ায় খুঁজছি..."
    echo "    → facebook.com/search/?q=$phone_clean"
    
    read -p "এন্টার চাপো মেনুতে ফিরতে..."
    select_option
}

username_osint() {
    read -p "টার্গেট ইউজারনেম: " username
    
    echo "[*] ইউজারনেম '$username' খুঁজছি..."
    
    # কমন সাইট চেক
    sites=(
        "https://github.com/$username"
        "https://twitter.com/$username"
        "https://www.instagram.com/$username/"
        "https://www.linkedin.com/in/$username"
        "https://medium.com/@$username"
        "https://reddit.com/user/$username"
        "https://t.me/$username"
        "https://www.youtube.com/@$username"
        "https://facebook.com/$username"
        "https://pinterest.com/$username"
    )
    
    for site in "${sites[@]}"; do
        status=$(curl -s -o /dev/null -w "%{http_code}" "$site" 2>/dev/null)
        if [ "$status" != "404" ]; then
            echo "[✓] পাওয়া গেছে: $site (HTTP $status)"
        fi
    done
    
    # Sherlock টুল চেক (যদি থাকে)
    which sherlock >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "[*] Sherlock দিয়ে গভীর সার্চ..."
        sherlock "$username" 2>/dev/null
    fi
    
    read -p "এন্টার চাপো মেনুতে ফিরতে..."
    select_option
}

full_recon() {
    read -p "টার্গেট ডোমেইন: " domain
    
    echo "[*] ফুল রিকন শুরু হচ্ছে: $domain"
    
    # WHOIS
    echo "[*] WHOIS লুকআপ..."
    whois "$domain" 2>/dev/null | head -20
    
    # DNS
    echo "[*] DNS রেকর্ড..."
    echo "A: $(dig +short A "$domain" | tr '\n' ' ')"
    echo "MX: $(dig +short MX "$domain" | tr '\n' ' ')"
    echo "NS: $(dig +short NS "$domain" | tr '\n' ' ')"
    
    # সাবডোমেইন
    echo "[*] সাবডোমেইন চেক..."
    for sub in www mail ftp admin blog api dev test; do
        host "$sub.$domain" 2>/dev/null | grep "has address" | awk '{print $1, $NF}'
    done
    
    # HTTP হেডার
    echo "[*] HTTP হেডার..."
    curl -sI "https://$domain" 2>/dev/null | head -10
    
    read -p "এন্টার চাপো মেনুতে ফিরতে..."
    select_option
}

breach_check() {
    read -p "ইমেল বা ইউজারনেম: " query
    
    echo "[*] ব্রীচ ডেটা চেক করছি..."
    
    # FireFox Monitor (কালার অফ)
    echo "    → https://monitor.firefox.com/"
    
    # DeHashed (পেইড)
    echo "    → https://dehashed.com/"
    
    # snusbase
    echo "    → https://snusbase.com/"
    
    # LeakCheck
    echo "    → https://leakcheck.io/"
    
    echo ""
    echo "দ্রষ্টব্য: ব্রীচ ডেটা চেক করতে ওপরের সাইটগুলো ভিজিট করো।"
    echo "শুধুমাত্র অনুমতি নিয়েই ব্যবহার করবে।"
    
    read -p "এন্টার চাপো মেনুতে ফিরতে..."
    select_option
}

# স্ক্রিপ্ট শুরু
select_option
```

---

## ৪৪.৫ ল্যাব এক্সারসাইজ

| টাস্ক | বিবরণ | টুল/টেকনিক |
|-------|--------|-------------|
| 1 | নিজের ডোমেইনের সব সাবডোমেইন বের করো | subfinder, amass |
| 2 | গুগল ডরকিং দিয়ে তোমার স্কুল/কলেজের পিডিএফ ফাইল খোঁজো | site:edu.bd filetype:pdf |
| 3 | শোডানে বাংলাদেশের ওপেন আরডিপি খোঁজো | port:3389 country:BD |
| 4 | মালটেগো দিয়ে তোমার টার্গেটের গ্রাফ বানাও | Maltego transforms |
| 5 | থার্ভেস্টার দিয়ে ইমেল কালেক্ট করো | theHarvester -d domain -b all |
| 6 | যেকোনো ইউজারনেম ২০+ সাইটে চেক করো | Sherlock / whatsmy.name |
| 7 | হ্যাভ আই বিন পাউন্ডে তোমার ইমেল চেক করো | haveibeenpwned.com |
| 8 | OSINT ফ্রেমওয়ার্ক ডাউনলোড করে ফুল রিকন করো | github.com/lanmaster53/recon-ng |

---

## ৪৪.৬ মনে রাখো

| বিষয় | কী মনে রাখবে |
|-------|-------------|
| Google Dorking | site:, filetype:, intitle:, inurl: — এগুলো মুখস্থ! |
| Shodan | port:, country:, os:, city: — ফিল্টার শেখো |
| theHarvester | -b দিয়ে সোর্স সিলেক্ট করো |
| Maltego | ট্রান্সফর্ম চেইন — একের পর এক ডাটা লিংক করো |
| Sherlock | ইউজারনেম ওসিন্টের জন্য বেস্ট টুল |
| HaveIBeenPwned | ব্রীচ ডেটা চেক করার জন্য |
| OSINT Framework | osintframework.com — সব টুলের লিস্ট |
| বিবেচনা | শুধুমাত্র অনুমতি নিয়ে OSINT করো। আইনগত জটিলতা এড়াও |

> **ভাই-বন্ধুর টিপস:** OSINT-এর সবচেয়ে গুরুত্বপূর্ণ টুল হলো терпение (ধৈর্য)। একদিনে সব ডাটা পাবে না। প্রতিদিন একটু করে ডাটা কালেক্ট করো। এবং সবসময় ভিপিএন ব্যবহার করো — কারণ তুমি কিন্তু টার্গেটের সার্ভারে হিট দিচ্ছো!
