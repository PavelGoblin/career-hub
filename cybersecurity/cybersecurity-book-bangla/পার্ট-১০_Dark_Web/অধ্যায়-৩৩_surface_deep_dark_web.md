# অধ্যায় ৩৩: Surface Web, Deep Web, Dark Web

## সহজ কথায়

ইন্টারনেটটা আসলে আইসবার্গের মতো। ওপরে ১০% আমরা সবাই দেখি — সেটা হলো **Surface Web** (Google, Facebook, YouTube)। পানি আর আইসবার্গের মাঝখানের অংশ হলো **Deep Web** — তোমার ইমেইল, ব্যাংক অ্যাকাউন্ট, গুগল ড্রাইভ, প্রাইভেট ডাটাবেজ। আর সবচেয়ে নিচে, অন্ধকারে, আছে **Dark Web** — যেখানে শুধু Tor ব্রাউজার দিয়ে যাওয়া যায়।

> **মজার Analogy:** Surface Web = শহরের মার্কেট স্কোয়ার (সবাই আসে-যায়)। Deep Web = তোমার বাড়ির ভেতরটা (শুধু তুমি ও তোমার পরিবার)। Dark Web = শহরের নিচের সুড়ঙ্গপথ (সেখানে ভালো-মন্দ দুই ধরনের মানুষই থাকে, কিন্তু কেউ চেনে না কে কে)।

---

## ১. পার্থক্য বাংলায়

| বৈশিষ্ট্য | Surface Web | Deep Web | Dark Web |
|-----------|------------|----------|----------|
| **আকার** | ৪% (৪-৫ বিলিয়ন পেজ) | ৯০%+ (১ ট্রিলিয়নেরও বেশি) | <১% |
| **ইনডেক্সিং** | Google, Bing — সব সার্চ ইঞ্জিনে আসে | সার্চ ইঞ্জিনে আসে না | সার্চ ইঞ্জিনে আসে না |
| **অ্যাক্সেস** | সাধারণ ব্রাউজার | লগইন প্রয়োজন | Tor Browser লাগে |
| **উদাহরণ** | Facebook, YouTube, Wikipedia | Gmail, Netflix, Bank Dashboard | .onion সাইট, Signal |
| **বেনামী** | না (IP ট্র্যাক করা যায়) | আংশিক | হ্যাঁ (অনেক লেয়ার) |
| **কন্টেন্ট** | পাবলিক | ব্যক্তিগত/পেইড | বেনামী (ভালো-মন্দ দুই) |

### কে কী ভাবে?

- **তোমার ফেসবুক প্রোফাইল:** Surface Web (সবাই দেখতে পারে)
- **তোমার ফেসবুক মেসেঞ্জার চ্যাট:** Deep Web (শুধু তুমি ও যাদের সাথে কথা বলছো)
- **তোমার ইনবক্সে আসা লিংক:** কিছু Dark Web-এরও হতে পারে (.onion)

---

## ২. Tor — কীভাবে কাজ করে?

Tor মানে **The Onion Router** — পেঁয়াজের মতো স্তরে স্তরে এনক্রিপশন।

### Tor-এর কাজের প্রক্রিয়া (৩ লেয়ার এনক্রিপশন)

```
তুমি (Tor Browser)
    ↓
[Entry Node] — জানে তুমি কে, কিন্তু কী করছো জানে না
    ↓ (এনক্রিপ্টেড লেয়ার ১)
[Middle Node] — জানে না তুমি কে, জানে না কী করছো
    ↓ (এনক্রিপ্টেড লেয়ার ২)
[Exit Node] — জানে কী করছো, কিন্তু জানে না তুমি কে
    ↓ (এনক্রিপ্টেড লেয়ার ৩)
ওয়েবসাইট (উদাহরণ: facebook.com)
```

```python
# # Tor নেটওয়ার্ক — কীভাবে ৩টি নোড কাজ করে (সিমুলেশন)
import requests

# # Tor-এর মাধ্যমে রিকোয়েস্ট পাঠানো
proxies = {
    'http': 'socks5h://127.0.0.1:9050',  # # Tor SOCKS5 প্রক্সি
    'https': 'socks5h://127.0.0.1:9050',
}

try:
    # # এই রিকোয়েস্ট ৩টি Tor নোডের মধ্য দিয়ে যাবে
    response = requests.get('https://check.torproject.org/', 
                           proxies=proxies, timeout=10)
    
    if 'Congratulations' in response.text:
        print("[✓] Tor ঠিকমতো কাজ করছে!")
    else:
        print("[✗] Tor চলছে না। tor.service চেক করো।")

except Exception as e:
    print(f"[!] Error: {e}")
```

```bash
# # Tor ইন্সটল ও রান
# # Linux
sudo apt install tor
sudo systemctl start tor

# # Tor প্রক্সি লোকাল পোর্ট 9050-এ চালু হবে
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/

# # Tor-এর মাধ্যমে আমার IP কী?
curl --socks5-hostname 127.0.0.1:9050 https://api.ipify.org

# # নরমাল ব্রাউজার দিয়ে আমার IP
curl https://api.ipify.org
```

### Tor Circuit — কীভাবে বদলায়?

```bash
# # Tor সার্কিট রিনিউ করা
# # নতুন Tor আইডি পেতে (একই সার্কিটে থাকলে ট্র্যাক করা সহজ)
sudo systemctl restart tor

# # Nyx — Tor মনিটরিং টুল
pip install nyx
nyx

# # Tor Browser-এ "New Identity" = পুরনো সার্কিট ড্রপ + নতুন
```

---

## ৩. Dark Web — Website বানানো (Hidden Service)

### ৩.১ Hidden Service (.onion) কীভাবে কাজ করে?

```
যন্ত্র (Tor Client)
    ↓
[Introduction Point] — সার্ভারের সাথে পরিচয় করিয়ে দেয়
    ↓
[Rendezvous Point] — দুই পক্ষ মিলে এনক্রিপ্টেড চ্যানেল বানায়
    ↓
Hidden Service (তোমার ওয়েবসাইট — কোনো IP দরকার নেই!)
```

### ৩.২ নিজের .onion সাইট বানানো

```bash
# # ধাপ ১: Tor ইন্সটল
sudo apt install tor

# # ধাপ ২: torrc এডিট করে Hidden Service চালু
sudo nano /etc/tor/torrc
```

```conf
# # /etc/tor/torrc — এই লাইনগুলো আনকমেন্ট করো

HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 80 127.0.0.1:8080
HiddenServicePort 22 127.0.0.1:22
```

```bash
# # ধাপ ৩: Tor রিস্টার্ট
sudo systemctl restart tor

# # ধাপ ৪: .onion অ্যাড্রেস দেখা
sudo cat /var/lib/tor/hidden_service/hostname
# # আউটপুট: abcdefghijklmnop.onion — এই লিংক দিয়ে সাইট অ্যাক্সেস হবে

# # ধাপ ৫: লোকাল ওয়েব সার্ভার চালু (পোর্ট 8080)
python3 -m http.server 8080

# # এবার Tor Browser দিয়ে তোমার .onion সাইট ওপেন করো!
```

### ৩.৩ Python দিয়ে Dark Web-এর কন্টেন্ট স্ক্র্যাপিং

```python
# # .onion সাইট থেকে ডাটা নেওয়া (Tor প্রক্সি দিয়ে)
import requests
from bs4 import BeautifulSoup

# # Tor SOCKS5 প্রক্সি
session = requests.Session()
session.proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050',
}

# # একটি .onion সাইটে কানেক্ট করা
onion_url = "http://example1234567.onion"

try:
    response = session.get(onion_url, timeout=30)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # # পেজের টাইটেল বের করা
    title = soup.title.string if soup.title else "No title"
    print(f"[✓] সাইট: {onion_url}")
    print(f"[✓] টাইটেল: {title}")
    
except requests.exceptions.ConnectTimeout:
    print("[!] টাইমআউট — সাইট ডাউন থাকতে পারে")
except requests.exceptions.ConnectionError:
    print("[!] কানেক্ট করতে পারেনি — Tor চলছে কিনা চেক করো")
```

---

## ৪. Safety Guidelines — Dark Web-এ নিরাপদ থাকার নিয়ম

### Dark Web Danger Levels

```
ঝুঁকি লেভেল ১ (নিরাপদ) — Signal, ProtonMail, Facebook .onion
ঝুঁকি লেভেল ২ (সাবধান) — ফোরাম, ব্লগ, সংবাদ সাইট
ঝুঁকি লেভেল ৩ (বিপজ্জনক) — মার্কেটপ্লেস, হ্যাকিং ফোরাম
ঝুঁকি লেভেল ৪ (খুব বিপজ্জনক) — Child abuse, weapons, illegal services
```

### কীভাবে নিরাপদ থাকবে:

```python
# # Dark Web Safety Checklist
safety_rules = [
    "কখনো আসল নাম ব্যবহার করো না",
    "কখনো আসল ইমেইল দিয়ে রেজিস্টার করো না",
    "JavaScript বন্ধ করে দিও (NoScript)",
    "Camera ও Microphone ব্লক করে দিও",
    "কখনো ফাইল ডাউনলোড করো না (ম্যালওয়্যার)",
    "কখনো ক্রেডিট কার্ড দিয়ে কিছু কিনো না",
    "VPN + Tor একসাথে ব্যবহার করো (Tor Over VPN)",
    "উইন্ডোজ নয় — Tails বা Whonix OS ব্যবহার করো",
    ".onion লিংকে ক্লিক করার আগে ১০ বার ভাবো",
    "Exit Node-তে ট্রাফিক এনক্রিপ্টেড না থাকলে সব দেখা যাবে",
]

for i, rule in enumerate(safety_rules, 1):
    print(f"[{i}] {rule}")
```

### Tor Browser সিকিউরিটি সেটিংস:

```
Tor Browser → Shield আইকন → Security Level

🔵 Standard: সাধারণ ব্রাউজিং
🟡 Safer: JavaScript বন্ধ (নির্দিষ্ট সাইটে)
🔴 Safest: সব JavaScript বন্ধ, SVG বন্ধ, কিছু ফন্ট বন্ধ
```

### Tor Over VPN — সবচেয়ে নিরাপদ পদ্ধতি

```
তুমি → VPN → Tor → ইন্টারনেট

# # ভিপিএন তোমাকে ISP-এর কাছ থেকে লুকায়
# # Tor তোমাকে ওয়েবসাইটের কাছ থেকে লুকায়
# # উভয়েই জানে না তুমি কে — সত্যিকারের বেনামী
```

---

## ল্যাব এক্সারসাইজ

> **ল্যাব ১:** Tor Browser ডাউনলোড করে ইন্সটল করো। `check.torproject.org`-এ গিয়ে চেক করো Tor ঠিকমতো কাজ করছে কিনা।

> **ল্যাব ২:** Terminal থেকে `curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/` দিয়ে চেক করো।

> **ল্যাব ৩:** নিজের একটি .onion hidden service বানাও — Python HTTP সার্ভার চালিয়ে তাতে একটি HTML পেজ দেখাও।

> **ল্যাব ৪:** Facebook-এর .onion সাইটে যাও (facebookcorewwwi.onion) — Tor Browser দিয়ে।

> **ল্যাব ৫:** Tails OS একটি USB-তে ইন্সটল করে বুট করো — সম্পূর্ণ বেনামী পরিবেশে Dark Web ব্রাউজ করো।

---

## মনে রাখো

| টপিক | মূল পয়েন্ট |
|-------|------------|
| Surface Web | ৪% — Google, Facebook, সব সার্চ ইঞ্জিনে আসে |
| Deep Web | ৯০% — লগইন পেজ, ব্যাংক, ইমেইল — বেনামী না |
| Dark Web | <১% — শুধু Tor দিয়ে যায় — .onion অ্যাড্রেস |
| Tor Network | ৩ লেয়ার এনক্রিপশন — Entry → Middle → Exit Node |
| Hidden Service | নিজের IP লুকিয়ে .onion সাইট হোস্ট করা |
| Safety | VPN + Tor + Tails + NoScript + No Downloads |
| .onion সাইট বানানো | torrc এডিট → HiddenServiceDir → Tor Restart |

> **শেষ কথা:** ভাই, Dark Web খারাপ জায়গা না — এটা শুধু ইন্টারনেটের অন্ধকার দিক। পুলিশ, গোয়েন্দা, জার্নালিস্ট, হুইসেলব্লোয়ার — সবাই Tor ব্যবহার করে। কিন্তু মনে রাখবে — **অন্ধকারে যেমন ভালো মানুষ থাকে, ভূত-প্রেতও থাকে**। সাবধানে থাকো!
