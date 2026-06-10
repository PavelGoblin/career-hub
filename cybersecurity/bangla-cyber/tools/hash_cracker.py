"""
বাংলা: হ্যাশ ক্র্যাকার টুল
লেখক: PavelGoblin
"""

import hashlib

BANNER = """
╔══════════════════════════════════╗
║   🔑 হ্যাশ ক্র্যাকার v1.0       ║
║   হ্যাশ ভাঙ্গার টুল              ║
╚══════════════════════════════════╝
"""

HASH_TYPES = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}

def run():
    target_hash = input("হ্যাশ ভ্যালু দিন: ").strip().lower()
    print("হ্যাশ টাইপ নির্বাচন করুন:")
    for i, h in enumerate(HASH_TYPES.keys(), 1):
        print(f"   {i}. {h.upper()}")
    choice = input("পছন্দের নম্বর (ডিফল্ট 1): ").strip() or "1"
    try:
        algo = list(HASH_TYPES.keys())[int(choice) - 1]
    except:
        algo = "md5"
    print(f"\n🔍 {algo.upper()} হ্যাশ ক্র্যাক করা হচ্ছে...")

    common = [
        "password", "123456", "admin", "letmein", "qwerty", "welcome",
        "monkey", "dragon", "master", "passw0rd", "shadow", "football",
        "iloveyou", "sunshine", "princess", "trustno1", "batman", "superman",
        "000000", "111111", "abc123", "pass123", "root", "toor", "test",
        "guest", "user", "secret", "changeme", "default", "Pa$$w0rd",
    ]

    found = False
    for word in common:
        h = HASH_TYPES[algo](word.encode()).hexdigest()
        if h == target_hash:
            print(f"\n✅ পাওয়া গেছে! প্লেইনটেক্সট: {word}")
            found = True
            break

    if not found:
        print("\n❌ সাধারণ পাসওয়ার্ড তালিকায় পাওয়া যায়নি।")
        print("   (বৃহত্তর ওয়ার্ডলিস্ট ব্যবহার করে আবার চেষ্টা করুন)")

if __name__ == "__main__":
    print(BANNER)
    run()
