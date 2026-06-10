"""
বাংলা: সিজার সাইফার এনক্রিপ্ট/ডিক্রিপ্ট
লেখক: PavelGoblin
"""

BANNER = """
╔══════════════════════════════════╗
║   🔐 সিজার সাইফার v1.0          ║
║   ক্লাসিক্যাল এনক্রিপশন টুল      ║
╚══════════════════════════════════╝
"""

def caesar(text, shift, decrypt=False):
    result = ""
    if decrypt:
        shift = -shift
    for ch in text:
        if ch.isupper():
            result += chr((ord(ch) - 65 + shift) % 26 + 65)
        elif ch.islower():
            result += chr((ord(ch) - 97 + shift) % 26 + 97)
        else:
            result += ch
    return result

def run():
    print("কাজ নির্বাচন করুন:")
    print("   1. এনক্রিপ্ট (বার্তা লুকান)")
    print("   2. ডিক্রিপ্ট (বার্তা উদ্ধার)")
    print("   3. ব্রুটফোর্স (সব শিফট চেষ্টা)")
    choice = input("পছন্দ (1/2/3): ").strip()

    if choice == "1":
        text = input("বার্তা দিন: ")
        try:
            shift = int(input("শিফট সংখ্যা: "))
        except:
            shift = 3
        print(f"\n✅ এনক্রিপ্টেড: {caesar(text, shift)}")

    elif choice == "2":
        text = input("এনক্রিপ্টেড বার্তা: ")
        try:
            shift = int(input("শিফট সংখ্যা: "))
        except:
            shift = 3
        print(f"\n✅ ডিক্রিপ্টেড: {caesar(text, shift, decrypt=True)}")

    elif choice == "3":
        text = input("এনক্রিপ্টেড বার্তা: ")
        print("\n🔍 সব শিফট চেষ্টা করা হচ্ছে:\n")
        for s in range(26):
            decoded = caesar(text, s, decrypt=True)
            print(f"   শিফট {s:>2}: {decoded}")
    else:
        print("❌ ভুল পছন্দ।")

if __name__ == "__main__":
    print(BANNER)
    run()
