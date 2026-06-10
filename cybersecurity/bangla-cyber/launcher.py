"""
বাংলা: বাংলা সাইবার শেখার টুল — লঞ্চার
লেখক: PavelGoblin
"""

import os
import sys
import importlib

BANNER = r"""
╔══════════════════════════════════════════════════════════╗
║     ██████  █████  ███    ██  ██████  ██       █████      ║
║     ██   ██ ██   ██ ████   ██ ██       ██      ██   ██     ║
║     ██████  ███████ ██ ██  ██ ██   ███ ██      █████      ║
║     ██   ██ ██   ██ ██  ██ ██ ██    ██ ██      ██   ██     ║
║     ██████  ██   ██ ██   ████  ██████  ███████  █████      ║
║                                                            ║
║     🌐 বাংলা সাইবার সিকিউরিটি লার্নিং প্ল্যাটফর্ম         ║
║     ═══════════════════════════════════════════════════     ║
║     শিখুন সুরক্ষিত থাকার জন্য | শেখান অন্যদের              ║
╚══════════════════════════════════════════════════════════╝
"""

TOOLS = {
    "1": ("🔍 পোর্ট স্ক্যানার", "port_scanner"),
    "2": ("🌐 সাবডোমেইন এনুমারেটর", "subdomain_enum"),
    "3": ("🔑 হ্যাশ ক্র্যাকার", "hash_cracker"),
    "4": ("🔐 সিজার সাইফার", "caesar_cipher"),
    "5": ("🔒 পাসওয়ার্ড জেনারেটর", "password_gen"),
    "6": ("📡 নেটওয়ার্ক স্ক্যানার", "network_scanner"),
}

MODULES = [
    "সাইবার সিকিউরিটি পরিচিতি",
    "নেটওয়ার্কিং বেসিক",
    "রিকনেসান্স (তথ্য সংগ্রহ)",
    "স্ক্যানিং ও এনুমারেশন",
    "ভালনারেবিলিটি অ্যানালাইসিস",
    "এক্সপ্লয়টেশন বেসিক",
    "ওয়েব অ্যাপ্লিকেশন সিকিউরিটি",
    "ওয়্যারলেস নেটওয়ার্ক হ্যাকিং",
    "ক্রিপ্টোগ্রাফি",
    "ম্যালওয়্যার অ্যানালাইসিস",
    "সোশ্যাল ইঞ্জিনিয়ারিং",
    "পেনিট্রেশন টেস্টিং",
    "ফরেন্সিকস",
    "ডিফেন্সিভ সিকিউরিটি",
    "CTF ও প্রতিযোগিতা",
    "ক্যারিয়ার ও সার্টিফিকেশন",
]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_main_menu():
    clear()
    print(BANNER)
    print("\n📌 মূল মেনু:\n")
    print("   1. 🔧 টুলস চালু করুন")
    print("   2. 📚 লার্নিং মডিউল দেখুন")
    print("   3. ℹ️  এই প্রজেক্ট সম্পর্কে")
    print("   0. 🚪 প্রস্থান")
    return input("\n👉 আপনার পছন্দ: ").strip()

def show_tools_menu():
    clear()
    print(BANNER)
    print("\n🔧 উপলব্ধ টুলস:\n")
    for key, (name, _) in TOOLS.items():
        print(f"   {key}. {name}")
    print("   0. 🔙 মূল মেনুতে ফিরুন")
    choice = input("\n👉 টুল নির্বাচন করুন: ").strip()
    if choice == "0":
        return
    if choice in TOOLS:
        name = TOOLS[choice][1]
        try:
            mod = importlib.import_module(f"tools.{name}")
            if hasattr(mod, "BANNER"):
                print(mod.BANNER)
            if hasattr(mod, "run"):
                mod.run()
        except Exception as e:
            print(f"❌ ত্রুটি: {e}")
        input("\n\n⏎ চালিয়ে যেতে এন্টার চাপুন...")
        show_tools_menu()
    else:
        print("❌ ভুল পছন্দ।")
        input("⏎ চালিয়ে যেতে এন্টার চাপুন...")
        show_tools_menu()

def show_modules_menu():
    clear()
    print(BANNER)
    print("\n📚 লার্নিং মডিউল সমূহ:\n")
    for i, mod in enumerate(MODULES, 1):
        print(f"   {i:>2}. {mod}")
    print("   0. 🔙 মূল মেনুতে ফিরুন")
    choice = input("\n👉 মডিউল নির্বাচন করুন (বিস্তারিত জানতে): ").strip()
    if choice == "0":
        return
    try:
        idx = int(choice)
        if 1 <= idx <= len(MODULES):
            clear()
            print(BANNER)
            print(f"\n📖 {MODULES[idx-1]}\n")
            print("   (বিস্তারিত জানতে README.md দেখুন)\n")
            input("⏎ ফিরতে এন্টার চাপুন...")
    except:
        pass
    show_modules_menu()

def show_about():
    clear()
    print(BANNER)
    print("\nℹ️  এই প্রজেক্ট সম্পর্কে:\n")
    print("   📛 নাম: বাংলা সাইবার সিকিউরিটি লার্নিং")
    print("   👤 নির্মাতা: PavelGoblin")
    print("   📝 ভাষা: বাংলা (Bangla)")
    print("   🎯 উদ্দেশ্য: বাংলাভাষীদের সাইবার সিকিউরিটি শেখানো")
    print("   🔓 লাইসেন্স: MIT")
    print("   📂 রিপোজিটরি: github.com/PavelGoblin/bangla-cyber")
    print("\n   🌟 বৈশিষ্ট্য:")
    print("   ✅ সম্পূর্ণ বাংলায় সাইবার সিকিউরিটি শিক্ষা")
    print("   ✅ হাতে-কলমে শেখার জন্য বিল্ট-ইন টুলস")
    print("   ✅ বিগিনার থেকে অ্যাডভান্সড পর্যন্ত কন্টেন্ট")
    print("   ✅ প্রতিটি টপিকের বিস্তারিত ব্যাখ্যা")
    print("\n   📚 কভার করা টপিক:")
    print("   নেটওয়ার্কিং, রিকনেসান্স, স্ক্যানিং, এক্সপ্লয়টেশন,")
    print("   ওয়েব সিকিউরিটি, ক্রিপ্টোগ্রাফি, ম্যালওয়্যার,")
    print("   সোশ্যাল ইঞ্জিনিয়ারিং, ফরেন্সিকস এবং আরও অনেক কিছু!")
    input("\n⏎ ফিরতে এন্টার চাপুন...")

def main():
    while True:
        choice = show_main_menu()
        if choice == "1":
            show_tools_menu()
        elif choice == "2":
            show_modules_menu()
        elif choice == "3":
            show_about()
        elif choice == "0":
            clear()
            print("\n👋 ধন্যবাদ! সুরক্ষিত থাকুন।\n")
            sys.exit(0)
        else:
            print("❌ ভুল পছন্দ। আবার চেষ্টা করুন।")
            input("⏎ চালিয়ে যেতে এন্টার চাপুন...")

if __name__ == "__main__":
    main()
