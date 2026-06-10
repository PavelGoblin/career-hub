# অধ্যায় ৩৮: SIEM ও Monitoring

> ভাই, নেটওয়ার্কে কী ঘটছে সেটা জানা না থাকলে তুমি অন্ধের মতো যুদ্ধ করবে। SIEM (Security Information and Event Management) হলো সেই চশমা, যা দিয়ে তুমি পুরো নেটওয়ার্কের সবকিছু দেখতে পারো। এই অধ্যায়ে Splunk, ELK Stack, আর IDS নিয়ে আলোচনা।

---

## ৩৮.১ Splunk Basics

Splunk হলো সবচেয়ে জনপ্রিয় SIEM টুল। এটা সব ধরনের লগ এক জায়গায় এনে, সার্চ করে, ভিজুয়ালাইজ করে, আর এলার্ম দেয়।

### Splunk কেমন কাজ করে?

```
ডাটা সোর্স (লগ) → Splunk Forwarder → Splunk Indexer → Search Head → Dashboard
   (সার্ভার, ফায়ারওয়াল,     (লগ কালেক্ট করে)   (লগ সংরক্ষণ)   (সার্চ করে)   (দেখায়)
    রাউটার, অ্যাপ)
```

### Splunk এর মূল কনসেপ্ট:

| টার্ম | মানে | বাংলায় |
|-------|------|---------|
| **Index** | ডাটার ডাটাবেস | লগ রাখার জায়গা |
| **Source** | লগ কোথা থেকে আসছে | যেমন `/var/log/auth.log` |
| **Sourcetype** | লগের টাইপ | `linux_secure`, `apache_access` |
| **Event** | একটা একক লগ এন্ট্রি | একটা লাইন |
| **Forwarder** | লগ পাঠানোর এজেন্ট | যে লগ কালেক্ট করে Splunk-এ পাঠায় |
| **Search** | Splunk-এর সার্চ ভাষা (SPL) | ডাটা খোঁজার ভাষা |

### Splunk ইন্সটল (ফ্রি ভার্সন):

```bash
# লিনাক্সে Splunk ফ্রি ডাউনলোড
wget -O splunk.tgz "https://download.splunk.com/products/splunk/releases/9.0.5/\
linux/splunk-9.0.5-xxx-Linux-x86_64.tgz"

# আনজিপ
tar -xzf splunk.tgz -C /opt

# ইন্সটল (প্রথমবার)
sudo /opt/splunk/bin/splunk start --accept-license

# ওয়েব ইন্টারফেস (পোর্ট ৮০০০)
# Browser: http://localhost:8000
```

### Splunk সার্চ ল্যাঙ্গুয়েজ (SPL) — বাংলা উদাহরণ:

```splunk
# ===== SPL (Search Processing Language) উদাহরণ =====

# ১. সব লগ দেখা
index=*

# ২. নির্দিষ্ট সোর্স থেকে লগ
index=linux_secure sourcetype=linux_secure

# ৩. ফেইলড SSH লগইন খোঁজা
index=linux_secure "Failed password"

# ৪. টপ ১০ অ্যাটাকিং IP
index=linux_secure "Failed password"
| stats count by src_ip
| sort - count
| head 10

# ৫. গত ২৪ ঘণ্টায় ফেইলড লগইন
index=linux_secure "Failed password"
| timechart count by src_ip

# ৬. অ্যালার্ম তৈরি (যেমন ৫ মিনিটে ১০ বার ফেইলড)
index=linux_secure "Failed password"
| stats count by src_ip
| where count > 10

# ৭. Apache ৪০৪ এরর (ওয়েব স্ক্যানিং)
index=apache status=404
| stats count by uri, src_ip
| sort - count
```

### Splunk Dashboard — চোখে দেখা সিকিউরিটি:

```splunk
# ===== ড্যাশবোর্ডের জন্য কোয়েরি =====

# ফেইলড লগইন ট্রেন্ড (লাইন চার্ট)
index=linux_secure "Failed password"
| timechart span=1h count by src_ip

# টপ অ্যাটাকিং কান্ট্রি
index=firewall action=blocked
| iplocation src_ip
| stats count by Country
| sort - count

# রিয়েল-টাইম মনিটরিং
index=* earliest=-5m
| stats count by sourcetype
```

---

## ৩৮.২ ELK Stack (Elasticsearch, Logstash, Kibana)

ELK হলো ওপেন-সোর্স SIEM-এর কিং। Splunk-এর ফ্রি অল্টারনেটিভ।

### ELK আর্কিটেকচার:

```
Logstash (লগ প্রসেস করে) → Elasticsearch (স্টোর করে) → Kibana (ভিজুয়ালাইজ করে)
         ↑                                       ↑
    Beats (লগ কালেক্ট করে)              Kibana Query Language (KQL)
```

### ELK ইন্সটল (দ্রুত সেটআপ):

```bash
# ===== Docker Compose দিয়ে ELK =====

# docker-compose.yml তৈরি করো
cat > docker-compose.yml << 'EOF'
version: '3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5000:5000"
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch
EOF

# চালাও
docker-compose up -d
# Kibana: http://localhost:5601
```

### Logstash কনফিগ (বাংলায় ব্যাখ্যা):

```bash
# ===== logstash.conf =====
# Logstash কনফিগারেশন — বাংলায়!
cat > logstash.conf << 'EOF'
input {
  # ফাইল থেকে লগ পড়া
  file {
    path => "/var/log/auth.log"  # যে লগ ফাইল দেখবে
    type => "linux_auth"         # এই লগের টাইপ
    start_position => "beginning"
  }

  # নেটওয়ার্ক থেকে লগ নেওয়া (syslog)
  syslog {
    port => 5000
  }
}

filter {
  # লগ প্যার্স করা
  grok {
    match => {
      "message" => "%{SYSLOGTIMESTAMP:timestamp} %{SYSLOGHOST:hostname} \
                    %{DATA:program}: %{GREEDYDATA:log_message}"
    }
  }

  # ফেইলড পাসওয়ার্ড খোঁজা
  if [log_message] =~ /Failed password/ {
    mutate {
      add_tag => ["failed_login"]
    }
  }
}

output {
  # Elasticsearch-এ পাঠাও
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "linux-auth-%{+YYYY.MM.dd}"  # ডেট অনুযায়ী ইন্ডেক্স
  }

  # ডিবাগিং: কনসোলেও দেখাও
  stdout {
    codec => rubydebug
  }
}
EOF
```

### Kibana ড্যাশবোর্ড — কোয়েরি তৈরি:

```kibana
# ===== Kibana Query Language (KQL) উদাহরণ =====

# সব ইভেন্ট
*

# নির্দিষ্ট ইন্ডেক্স
index:linux-auth*

# ফেইলড লগইন
log_message: "Failed password"

# গত ঘণ্টায় ফেইলড লগইন
@timestamp >= now-1h AND log_message: "Failed password"

# নির্দিষ্ট IP থেকে লগইন
src_ip: 192.168.1.100

# অ্যাটাকিং IP কাউন্ট (aggregation)
# Visualization → Pie Chart → Buckets: Terms (src_ip.keyword)
```

### Beats — লগ কালেক্টরের দুনিয়া:

```bash
# ===== Filebeat (ফাইল লগ কালেক্টর) =====

# ইন্সটল
sudo apt install filebeat -y

# কনফিগ ফাইল
sudo nano /etc/filebeat/filebeat.yml

# গুরুত্বপূর্ণ কনফিগ:
# filebeat.inputs:
#   - type: log
#     paths:
#       - /var/log/auth.log
#       - /var/log/syslog
#
# output.elasticsearch:
#   hosts: ["localhost:9200"]

# চালানো
sudo systemctl start filebeat
sudo systemctl enable filebeat
```

---

## ৩৮.৩ IDS কীভাবে কাজ করে

### IDS (Intrusion Detection System) বনাম IPS (Intrusion Prevention System)

```
IDS: সিসি ক্যামেরা — দেখে আর এলার্ম দেয়, কিন্তু ব্লক করে না
IPS: সিসি ক্যামেরা + অটোমেটিক ডোর লক — দেখে আর সাথে সাথে ব্লক করে
```

### IDS-এর প্রকারভেদ:

| টাইপ | কী দেখে | উদাহরণ |
|------|---------|--------|
| **NIDS** (Network) | নেটওয়ার্ক ট্রাফিক | Snort, Suricata |
| **HIDS** (Host) | একক সিস্টেমে কী ঘটছে | OSSEC, Wazuh |
| **Signature-based** | পরিচিত অ্যাটাক প্যাটার্ন | Snort রুল |
| **Anomaly-based** | অস্বাভাবিক আচরণ | ML বেসড |

### IDS কাজ করার প্রক্রিয়া:

```
প্যাকেট আসছে
    ↓
১. ক্যাপচার (libpcap/npcap দিয়ে)
    ↓
২. ডিকোড (প্রোটোকল বুঝে — TCP? UDP? ICMP?)
    ↓
৩. প্রিপ্রসেসর (নরমালাইজ, ডি-ফ্র্যাগমেন্ট)
    ↓
৪. ডিটেকশন ইঞ্জিন (রুলের সাথে মিলিয়ে দেখা)
    ↓
৫. ম্যাচ? → এলার্ম / লগ / ব্লক
    ↓
৬. আউটপুট (কনসোল / ফাইল / SIEM-এ পাঠানো)
```

### Suricata — Snort-এর আধুনিক ভাই:

```bash
# Suricata ইন্সটল
sudo apt install suricata -y

# কনফিগ
sudo nano /etc/suricata/suricata.yaml

# নেটওয়ার্ক ইন্টারফেস সেট করো
# af-packet:
#   - interface: eth0

# ইমার্জিং থ্রেটস রুল ডাউনলোড
sudo suricata-update

# Suricata চালানো
sudo systemctl start suricata

# লগ দেখা
sudo tail -f /var/log/suricata/fast.log
```

### Suricata রুল উদাহরণ:

```suricata
# ===== Suricata/IDS রুল বাংলায় =====

# HTTP-তে কমান্ড ইনজেকশন
alert http any any -> $HOME_NET any (
    msg: "সন্দেহজনক — কমান্ড ইনজেকশন!";
    content: "cmd.exe|sh|bash|powershell";
    classtype: web-application-attack;
    sid: 2000001;
    rev: 1;
)

# ক্রিপ্টো মাইনার ডিটেক্ট
alert dns any any -> any any (
    msg: "ক্রিপ্টো মাইনার DNS কোয়েরি!";
    content: "|2F|pool.minexmr.com|3A|";
    classtype: trojan-activity;
    sid: 2000002;
    rev: 1;
)
```

### SIEM + IDS — একসাথে কাজ করে:

```
IDS (Snort/Suricata) → Syslog → Logstash → Elasticsearch → Kibana (ড্যাশবোর্ড)
   (অ্যালার্ম পাঠায়)                              ↑
                                        Filebeat (লগ তুলে)
                                             ↑
                                     সার্ভার/ফায়ারওয়াল
```

---

## ৩৮.৪ কীভাবে বাঁচবে (প্র্যাকটিক্যাল)

| কী করবে | কেন করবে |
|----------|----------|
| সব লগ এক সেন্ট্রাল জায়গায় আনো (SIEM) | ছড়ানো লগ বিচ করলে খুঁজে পাওয়া কঠিন |
| অ্যালার্ম থ্রেশহোল্ড সেট করো | খুব বেশি এলার্ম = ফালতু এলার্ম (আলার্ম ফাটিগ) |
| IDS + SIEM কম্বিনেশন | IDS দেখে, SIEM বুঝে |
| Kibana ড্যাশবোর্ড তৈরি করো | চোখে দেখলে দ্রুত বুঝতে পারো |
| লগ রোটেশন সেট করো | জায়গা ফুরিয়ে গেলে পুরনো প্রমাণ মুছে যাবে |

---

## ৩৮.৫ ল্যাব এক্সারসাইজ

### টাস্ক ১: Elasticsearch + Kibana চালানো
```bash
# Docker দিয়ে ELK চালাও
# Kibana ওপেন করো (http://localhost:5601)
# ইনডেক্স প্যাটার্ন তৈরি করো
```

### টাস্ক ২: Filebeat সেটআপ
```bash
# Filebeat ইন্সটল করো
# /var/log/auth.log পাঠানো শুরু করো ES-তে
# Kibana-তে ডাটা আসছে কিনা দেখো
```

### টাস্ক ৩: Logstash দিয়ে লগ প্যার্স
```bash
# Logstash কনফিগ লেখো যা auth.log প্যার্স করে
# ফেইলড পাসওয়ার্ড ইভেন্টগুলো ট্যাগ করো
# আউটপুট Elasticsearch-এ দাও
```

### টাস্ক ৪: Kibana ভিজুয়ালাইজেশন
```bash
# Pie chart: বিভিন্ন IP থেকে ফেইলড লগইন
# Line chart: সময় অনুযায়ী লগইন অ্যাটেম্পট
# Dashboard তৈরি করো — ৩টা ভিজুয়াল যোগ করো
```

### টাস্ক ৫: Suricata IDS ইন্সটল
```bash
# Suricata ইন্সটল + ইমার্জিং রুল ডাউনলোড
# Suricata চালিয়ে দেখো — কোন অ্যালার্ম আসে?
# একটি nmap স্ক্যান দাও — Suricata কি ধরতে পারে?
```

---

## মনে রাখো

| ধারণা | সংক্ষেপ | বাংলায় |
|--------|---------|--------|
| **Splunk** | SIEM টুল, SPL ভাষায় সার্চ | লগের জন্য গুগল |
| **ELK Stack** | Elasticsearch + Logstash + Kibana | ওপেন সোর্স SIEM ত্রিমূর্তি |
| **Beats** | লগ কালেক্টর এজেন্ট | যে লগ তুলে SIEM-এ পাঠায় |
| **IDS vs IPS** | IDS দেখে, IPS ব্লক করে | ক্যামেরা বনাম ক্যামেরা + সিকিউরিটি গার্ড |
| **Signature vs Anomaly** | পরিচিত vs অজানা আক্রমণ | পরিচিত চোরের ফাইল বনাম সন্দেহজনক আচরণ |
| **Logstash** | লগ প্রসেসর | লগ ক্লিনার + ফরম্যাটার |

---

> **ভাইয়ের মেসেজ:** SIEM সেটআপ করা কঠিন, কিন্তু একবার করলে জাদুর মতো কাজ করে। আমি বলবো ELK Stack দিয়ে শুরু করো — ফ্রি, ওপেন সোর্স, আর কমিউনিটিও বিশাল। IDS (Snort/Suricata)-এর সাথে ELK কানেক্ট করলেই তুমি সিকিউরিটি অপারেশন সেন্টার (SOC) এর মতো কিছু তৈরি করতে পারবে। পরের অধ্যায়ে Hardening — শত্রুর জন্য কঠিন করে তোলা!
