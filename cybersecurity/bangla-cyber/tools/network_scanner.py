"""
বাংলা: নেটওয়ার্ক স্ক্যানার (ARP-based)
লেখক: PavelGoblin
"""

import subprocess
import re

BANNER = """
╔══════════════════════════════════╗
║   📡 নেটওয়ার্ক স্ক্যানার v1.0   ║
║   লোকাল নেটওয়ার্ক ডিভাইস খোঁজা  ║
╚══════════════════════════════════╝
"""

def get_arp_table():
    try:
        output = subprocess.check_output("arp -a", shell=True, text=True)
        devices = []
        for line in output.splitlines():
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]{17})", line)
            if match:
                ip = match.group(1)
                mac = match.group(2).replace("-", ":")
                devices.append({"ip": ip, "mac": mac})
        return devices
    except:
        return []

def ping_sweep(subnet="192.168.1"):
    print(f"\n🔍 {subnet}.1-254 স্ক্যান করা হচ্ছে...")
    active = []
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        try:
            result = subprocess.run(
                f"ping -n 1 -w 200 {ip}",
                shell=True, capture_output=True, text=True, timeout=2
            )
            if "TTL=" in result.stdout or "ttl=" in result.stdout:
                active.append(ip)
                print(f"   ✅ {ip}")
        except:
            pass
    return active

def run():
    print("\nপদ্ধতি নির্বাচন করুন:")
    print("   1. ARP টেবিল দেখুন (দ্রুত)")
    print("   2. পিং সুইপ (সব ডিভাইস)")
    choice = input("পছন্দ (1/2): ").strip()

    if choice == "1":
        devs = get_arp_table()
        if devs:
            print(f"\n✅ মোট {len(devs)}টি ডিভাইস পাওয়া গেছে:")
            for d in devs:
                print(f"   IP: {d['ip']:<15} MAC: {d['mac']}")
        else:
            print("\n❌ কিছু পাওয়া যায়নি।")

    elif choice == "2":
        subnet = input("সাবনেট (ডিফল্ট 192.168.1): ").strip() or "192.168.1"
        active = ping_sweep(subnet)
        if active:
            print(f"\n✅ মোট {len(active)}টি অ্যাক্টিভ ডিভাইস:")
            for ip in active:
                print(f"   {ip}")
        else:
            print("\n❌ কোনো অ্যাক্টিভ ডিভাইস পাওয়া যায়নি।")
    else:
        print("❌ ভুল পছন্দ।")

if __name__ == "__main__":
    print(BANNER)
    run()
