"""
বাংলা: শক্তিশালী পাসওয়ার্ড জেনারেটর
লেখক: PavelGoblin
"""

import secrets
import string

BANNER = """
╔══════════════════════════════════╗
║   🔒 পাসওয়ার্ড জেনারেটর v1.0    ║
║   শক্তিশালী পাসওয়ার্ড তৈরির টুল  ║
╚══════════════════════════════════╝
"""

def generate(length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    chars = ""
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not chars:
        chars = string.ascii_lowercase

    return "".join(secrets.choice(chars) for _ in range(length))

def strength(password):
    score = 0
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1

    if score <= 2:
        return "দুর্বল 🔴"
    elif score <= 4:
        return "মাঝারি 🟡"
    else:
        return "শক্তিশালী 🟢"

def run():
    try:
        length = int(input("পাসওয়ার্ডের দৈর্ঘ্য (ডিফল্ট 16): ") or "16")
    except:
        length = 16

    print(f"\n🔑 জেনারেটেড পাসওয়ার্ড ({length} অক্ষর):")
    print(f"   {generate(length)}")
    print(f"   {generate(length)}")
    print(f"   {generate(length)}")
    print(f"   {generate(length)}")
    print(f"   {generate(length)}")

    test = input("\nনিজের পাসওয়ার্ডের শক্তি পরীক্ষা করতে চান? (হ্যা/না): ").strip().lower()
    if test in ["হ্যা", "হ্যাঁ", "h", "yes", "y"]:
        pw = input("পাসওয়ার্ড দিন: ")
        print(f"   শক্তি: {strength(pw)}")

if __name__ == "__main__":
    print(BANNER)
    run()
