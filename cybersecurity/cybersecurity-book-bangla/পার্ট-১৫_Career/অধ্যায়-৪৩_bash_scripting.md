# অধ্যায় ৪৩: Bash Scripting for Hackers

> **ভাই-বন্ধুর মতো বলছি:** Bash scripting শিখলে তুমি হ্যাকিং টুলস নিজের হাতে বানাতে পারবে। আরে ভাই, এটা কিন্তু সুপারপাওয়ার! স্ক্রিপ্টিং না জানলে তুমি টুলসের ওপর নির্ভরশীল থাকবে। আর জানলে — তুমি নিজেই টুলস বানাবে।

---

## ৪৩.১ সহজ কথায় Bash Scripting

Bash (Bourne Again SHell) হলো Linux-এর কমান্ড ভাষা। তুমি যখন টার্মিনালে কমান্ড দাও, সেটাই bash। আর bash script মানে হচ্ছে একাধিক কমান্ড একসাথে লিখে ফেলা, যাতে এক ক্লিকেই সব কাজ হয়ে যায়।

**হ্যাকিং-এ কেন দরকার?**
- রিকন Automate করতে
- পোর্ট স্ক্যান করে Automate Log পার্স করতে
- পায়েলোড ডেলিভার করতে
- টুলস চেইন করতে (এক টুলের আউটপুট আরেক টুলে ইনপুট)

---

## ৪৩.২ Variables, Loops, Conditions, Functions

### Variables (ভেরিয়েবল)

```bash
#!/bin/bash

# হ্যাশ দিয়ে কমেন্ট করা হয় bash এ
# এইটা একটা variable
target="192.168.1.1"

# variable ব্যবহার করতে $ দিয়ে
echo "আমার টার্গেট: $target"

# ইউজার ইনপুট নেওয়া
read -p "টার্গেট আইপি দাও: " user_target
echo "তুমি দিয়েছো: $user_target"

# কমান্ডের আউটপুট variable এ রাখা
open_ports=$(nmap -p- --min-rate=1000 $target 2>/dev/null | grep ^[0-9])
echo "ওপেন পোর্ট: $open_ports"
```

### Loops (লুপ)

```bash
#!/bin/bash

# ফর লুপ — একটা রেঞ্জের ওপর দিয়ে ঘুরবে
echo "=== ফর লুপ দিয়ে পিং ==="
for ip in $(seq 1 5); do
    ping -c 1 "192.168.1.$ip" -W 1 2>/dev/null | grep "bytes from"
done

# while লুপ — যতক্ষণ কন্ডিশন true
echo "=== ওয়াইল লুপ ==="
counter=1
while [ $counter -le 5 ]; do
    echo "চেক করছি: 192.168.1.$counter"
    ((counter++))
done
```

### Conditions (কন্ডিশন)

```bash
#!/bin/bash

target=$1

# if-elif-else
if [ -z "$target" ]; then
    echo "ভাই! টার্গেট দাও নি। ব্যবহার: ./script.sh <target>"
    exit 1
elif [[ "$target" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "ভালো কথা, ভ্যালিড আইপি: $target"
else
    echo "$target — এইটা আইপি না ভাই। ডোমেইন দিলে। ঠিক আছে।"
fi

# ফাইল চেক করা
if [ -f "results.txt" ]; then
    echo "results.txt ফাইল আছে।"
else
    echo "ফাইল নাই। বানিয়ে ফেলছি।"
    touch results.txt
fi

# && এবং || অপারেটর
ping -c 1 "$target" -W 1 >/dev/null 2>&1 && echo "$target লাইভ!" || echo "$target ডেড!"
```

### Functions (ফাংশন)

```bash
#!/bin/bash

# ফাংশন ডিফাইন
port_scan() {
    local ip=$1      # local মানে এই ফাংশনের ভিতরেই সীমাবদ্ধ
    local port=$2
    timeout 1 bash -c "echo >/dev/tcp/$ip/$port" 2>/dev/null && echo "পোর্ট $port ওপেন" || echo "পোর্ট $port ক্লোজড"
}

# ফাংশন কল
port_scan "192.168.1.1" 80
port_scan "192.168.1.1" 443

# ফাংশন থেকে রিটার্ন ভ্যালু
check_root() {
    if [ "$(id -u)" -eq 0 ]; then
        return 0    # true
    else
        return 1    # false
    fi
}

if check_root; then
    echo "রুট ইউজার! সব ক্ষমতা তোমার!"
else
    echo "নরমাল ইউজার। sudo চাইবা।"
fi
```

---

## ৪৩.৩ Recon Automation Script (Complete Working Code)

এই স্ক্রিপ্ট একটা টার্গেটের ওপর পূর্ণাঙ্গ রিকন করবে। সাবডোমেইন, পোর্ট, HTTP সার্ভিস — সব।

```bash
#!/bin/bash

# =================================================
# রিকন অটোমেশন স্ক্রিপ্ট — সাইবার বই প্রকল্প
# ইউসেজ: ./recon.sh example.com
# =================================================

# রঙিন আউটপুটের জন্য
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# হেডার
echo -e "${BLUE}"
echo "╔══════════════════════════════════╗"
echo "║     রিকন অটোমেশন ইঞ্জিন v1.0    ║"
echo "╚══════════════════════════════════╝"
echo -e "${NC}"

# চেক করি টার্গেট দেওয়া হয়েছে কিনা
if [ $# -eq 0 ]; then
    echo -e "${RED}✖ ভুল: টার্গেট দাও নি!${NC}"
    echo "ব্যবহার: ./recon.sh example.com"
    exit 1
fi

TARGET=$1
OUTPUT_DIR="recon_${TARGET}_$(date +%Y%m%d_%H%M%S)"

# আউটপুট ডিরেক্টরি বানাই
mkdir -p "$OUTPUT_DIR"
echo -e "${GREEN}[+] আউটপুট ডিরেক্টরি: $OUTPUT_DIR${NC}"

# ============================================
# ফেজ ১: WHOIS লুকআপ
# ============================================
echo -e "${YELLOW}[*] ফেজ ১/৫: WHOIS লুকআপ চলছে...${NC}"
whois "$TARGET" > "$OUTPUT_DIR/whois.txt" 2>/dev/null
echo -e "${GREEN}[✓] WHOIS ডেটা সেভ করা হয়েছে${NC}"

# ============================================
# ফেজ ২: DNS রেকর্ড চেক
# ============================================
echo -e "${YELLOW}[*] ফেজ ২/৫: DNS রেকর্ড চেক করছি...${NC}"

# A রেকর্ড
echo "=== A রেকর্ড ===" >> "$OUTPUT_DIR/dns.txt"
dig +short A "$TARGET" >> "$OUTPUT_DIR/dns.txt" 2>/dev/null

# MX রেকর্ড
echo -e "\n=== MX রেকর্ড ===" >> "$OUTPUT_DIR/dns.txt"
dig +short MX "$TARGET" >> "$OUTPUT_DIR/dns.txt" 2>/dev/null

# NS রেকর্ড
echo -e "\n=== NS রেকর্ড ===" >> "$OUTPUT_DIR/dns.txt"
dig +short NS "$TARGET" >> "$OUTPUT_DIR/dns.txt" 2>/dev/null

# TXT রেকর্ড
echo -e "\n=== TXT রেকর্ড ===" >> "$OUTPUT_DIR/dns.txt"
dig +short TXT "$TARGET" >> "$OUTPUT_DIR/dns.txt" 2>/dev/null

echo -e "${GREEN}[✓] DNS ডেটা সেভ করা হয়েছে${NC}"

# ============================================
# ফেজ ৩: সাবডোমেইন এনুমারেশন
# ============================================
echo -e "${YELLOW}[*] ফেজ ৩/৫: সাবডোমেইন খুঁজছি...${NC}"

# কমন সাবডোমেইনের লিস্ট — ছোট্ট একটা লিস্ট
SUBDOMAINS=("www" "mail" "ftp" "admin" "blog" "api" "dev" "test" "portal" "vpn" "webmail" "admin" "cpanel" "whm" "mysql" "database" "backup" "gitlab" "jenkins" "jira" "confluence")

# প্রতিটা সাবডোমেইন চেক
> "$OUTPUT_DIR/subdomains.txt"  # ফাইলের আগের সব ডেটা মুছে দিয়ে খালি করছে
for sub in "${SUBDOMAINS[@]}"; do
    host "$sub.$TARGET" 2>/dev/null | grep "has address" | while read -r line; do
        ip=$(echo "$line" | awk '{print $NF}')
        echo "$sub.$TARGET -> $ip"
        echo "$sub.$TARGET -> $ip" >> "$OUTPUT_DIR/subdomains.txt"
    done
done

echo -e "${GREEN}[✓] সাবডোমেইন চেক শেষ${NC}"

# ============================================
# ফেজ ৪: পোর্ট স্ক্যান (কমন পোর্ট)
# ============================================
echo -e "${YELLOW}[*] ফেজ ৪/৫: পোর্ট স্ক্যান করছি...${NC}"

# কমন পোর্টের লিস্ট
COMMON_PORTS=(21 22 23 25 53 80 110 111 135 139 143 443 445 993 995 1433 1521 2049 3306 3389 5432 5900 5985 5986 6379 8080 8443 9000 27017)

> "$OUTPUT_DIR/ports.txt"
for port in "${COMMON_PORTS[@]}"; do
    timeout 1 bash -c "echo >/dev/tcp/$TARGET/$port" 2>/dev/null && echo "পোর্ট $port — ওপেন" | tee -a "$OUTPUT_DIR/ports.txt"
done

echo -e "${GREEN}[✓] পোর্ট স্ক্যান শেষ${NC}"

# ============================================
# ফেজ ৫: HTTP সার্ভিস চেক
# ============================================
echo -e "${YELLOW}[*] ফেজ ৫/৫: HTTP সার্ভিস চেক করছি...${NC}"

# HTTP হেডার চেক
curl -sI "http://$TARGET" 2>/dev/null > "$OUTPUT_DIR/http_headers.txt"
echo -e "${GREEN}[✓] HTTP হেডার নেওয়া হয়েছে${NC}"

# রোবটস.টিএক্সটি চেক
curl -s "http://$TARGET/robots.txt" 2>/dev/null > "$OUTPUT_DIR/robots.txt"
if [ -s "$OUTPUT_DIR/robots.txt" ]; then
    echo -e "${GREEN}[✓] robots.txt পাওয়া গেছে!${NC}"
else
    echo -e "${YELLOW}[!] robots.txt নাই${NC}"
fi

# ============================================
# সারাংশ
# ============================================
echo ""
echo -e "${BLUE}╔══════════════════════════════════╗${NC}"
echo -e "${BLUE}║        রিকন কমপ্লিট!            ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════╝${NC}"
echo -e "${GREEN}▶ রিপোর্ট ডিরেক্টরি: $OUTPUT_DIR${NC}"
echo -e "${GREEN}▶ ফাইলসমূহ:${NC}"
ls -la "$OUTPUT_DIR/"
```

---

## ৪৩.৪ Port Scanner in Bash

পুরো bash দিয়েই পোর্ট স্ক্যানার। nmap ছাড়া কাজ চলে!

```bash
#!/bin/bash

# ============================================
# ব্যাশ পোর্ট স্ক্যানার — মাল্টি-থ্রেডেড
# ============================================

# ইউসেজ চেক
if [ $# -lt 3 ]; then
    echo "ব্যবহার: $0 <টার্গেট> <স্টার্ট-পোর্ট> <এন্ড-পোর্ট> [থ্রেড]"
    echo "উদাহরণ: $0 192.168.1.1 1 1000 50"
    exit 1
fi

TARGET=$1
START_PORT=$2
END_PORT=$3
THREADS=${4:-20}  # যদি না দেয়, 20 থ্রেড ডিফল্ট

echo "টার্গেট: $TARGET"
echo "পোর্ট রেঞ্জ: $START_PORT-$END_PORT"
echo "থ্রেড: $THREADS"
echo ""

# টাইমার স্টার্ট
START_TIME=$(date +%s)

# পোর্ট চেক করার ফাংশন
check_port() {
    local port=$1
    timeout 1 bash -c "echo >/dev/tcp/$TARGET/$port" 2>/dev/null && echo "পোর্ট $port ওপেন"
}

export -f check_port  # export করছি যাতে parallel চালানো যায়
export TARGET

echo "স্ক্যান চলছে..."

# seq দিয়ে পোর্ট জেনারেট করে xargs-এ পাঠাই
# xargs -P দিয়ে প্যারালাল চালাই
seq $START_PORT $END_PORT | xargs -P $THREADS -I {} bash -c 'check_port "$@"' _ {}

# টাইমার এন্ড
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "স্ক্যান শেষ! সময় লেগেছে: $DURATION সেকেন্ড"
```

---

## ৪৩.৫ Log Parsing Script

ফেলো, সার্ভার লগ থেকেই অনেক সময় ইনফো বের হয়। এই স্ক্রিপ্ট অ্যাপাচি লগ পার্স করে।

```bash
#!/bin/bash

# ============================================
# লগ পার্সার — অ্যাপাচি/এনজিনেক্স লগ বিশ্লেষণ
# ============================================

LOG_FILE=${1:-"/var/log/apache2/access.log"}

# চেক করি লগ ফাইল আছে কিনা
if [ ! -f "$LOG_FILE" ]; then
    echo "লগ ফাইল পাওয়া যায় নি: $LOG_FILE"
    echo "ব্যবহার: $0 <লগ-ফাইল-পাথ>"
    exit 1
fi

echo "╔══════════════════════════════════╗"
echo "║        লগ বিশ্লেষক v1.0         ║"
echo "╚══════════════════════════════════╝"
echo "ফাইল: $LOG_FILE"
echo ""

# ১. মোট রিকুয়েস্ট সংখ্যা
total_requests=$(wc -l < "$LOG_FILE")
echo "📊 মোট রিকুয়েস্ট: $total_requests"

# ২. ইউনিক আইপি অ্যাড্রেস
unique_ips=$(awk '{print $1}' "$LOG_FILE" | sort -u | wc -l)
echo "📊 ইউনিক আইপি: $unique_ips"

# ৩. টপ ১০ আইপি
echo ""
echo "=== টপ ১০ আইপি (সবচেয়ে বেশি রিকুয়েস্ট) ==="
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10

# ৪. HTTP স্ট্যাটাস কোড ডিস্ট্রিবিউশন
echo ""
echo "=== HTTP স্ট্যাটাস কোড ==="
awk '{print $9}' "$LOG_FILE" | sort | uniq -c | sort -rn

# ৫. টপ ১০ ইউআরএল
echo ""
echo "=== টপ ১০ ইউআরএল ==="
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10

# ৬. ৪০৪ এরর (/etc/passwd স্ক্যানিং টাইপ)
echo ""
echo "=== ৪০৪ এরর (নট ফাউন্ড) ==="
grep " 404 " "$LOG_FILE" | awk '{print $7}' | sort | uniq -c | sort -rn | head -10

# ৭. সাসপিশিয়াস প্যাটার্ন (sql injection, xss attempt)
echo ""
echo "=== সাসপিশিয়াস রিকুয়েস্ট ==="
patterns=("union" "select" "drop" "alert(" "<script" "../" "passwd" "admin")
for pattern in "${patterns[@]}"; do
    count=$(grep -ci "$pattern" "$LOG_FILE" 2>/dev/null)
    if [ "$count" -gt 0 ]; then
        echo "⚠️ '$pattern' পাওয়া গেছে: $count বার"
    fi
done

# ৮. টাইমলাইন — প্রতি ঘণ্টায় রিকুয়েস্ট
echo ""
echo "=== টাইমলাইন (প্রতি ঘণ্টায়) ==="
awk '{print $4}' "$LOG_FILE" | cut -d: -f2 | sort | uniq -c | sort -n | head -24

echo ""
echo "✅ লগ বিশ্লেষণ শেষ!"
```

---

## ৪৩.৬ ল্যাব এক্সারসাইজ

| টাস্ক | বিবরণ | হিন্ট |
|-------|--------|-------|
| 1 | নিজের আইপি বের করার স্ক্রিপ্ট লেখো | `curl ifconfig.me` |
| 2 | পিং স্ক্যানার বানাও — ১৯২.১৬৮.১.১-২৫৪ | `for` লুপ + `ping` |
| 3 | HTTP রেসপন্স টাইম চেক করার টুল বানাও | `curl -o /dev/null -s -w %{time_total}` |
| 4 | ডিরেক্টরি ব্রুটফোর্সার বানাও | `curl` + ওয়ার্ডলিস্ট |
| 5 | ম্যাসক্যান প্রতিস্থাপন করে bash দিয়ে fast port scan | xargs -P |
| 6 | ফাইল মনিটর — কোন ফাইল চেঞ্জ হল ট্র্যাক করো | `inotifywait` বা `watch` |
| 7 | এসএসএইচ ব্রুটফোর্স লগ পার্সার | `/var/log/auth.log` পার্স করো |
| 8 | মাল্টি-টার্গেট স্ক্রিপ্ট — একাধিক আইপি থেকে রিকন | ফাংশন + ফাইল ইনপুট |

---

## ৪৩.৭ মনে রাখো

| বিষয় | কী মনে রাখবে |
|-------|-------------|
| `$1`, `$2`, ... | স্ক্রিপ্টে আর্গুমেন্ট |
| `$?` | লাস্ট কমান্ডের এক্সিট স্ট্যাটাস (0=success) |
| `2>/dev/null` | এরর মেসেজ লুকাও |
| `$(command)` | কমান্ডের আউটপুট ভেরিয়েবলে |
| `&&` `\|\|` | কন্ডিশনাল এক্সিকিউশন |
| `for` লুপ | লিস্টের ওপর ঘোরা |
| `while` লুপ | কন্ডিশন true থাকা পর্যন্ত |
| Functions | কোড রিইউজ |
| `tee` | স্ক্রিনে দেখাও + ফাইলে সেভ করো |
| `xargs -P` | প্যারালাল এক্সিকিউশন — ব্যাশেই মাল্টি-থ্রেডিং! |

> **ভাই-বন্ধুর টিপস:** শুরুতে এক লাইনের স্ক্রিপ্ট লেখো। ধীরে ধীরে বড় করো। আর হ্যাঁ, `#!/bin/bash` না দিলে স্ক্রিপ্ট চলবে না — এইটা দিতেই হবে। ব্যাশ শেখা মানে হ্যাকিং এর ৫০% শেখা!
