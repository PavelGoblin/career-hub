"""
বাংলা: পোর্ট স্ক্যানার টুল
লেখক: PavelGoblin
"""

import socket
import threading
from datetime import datetime

BANNER = """
╔══════════════════════════════════╗
║     🚪 পোর্ট স্ক্যানার v1.0     ║
║     পোর্ট স্ক্যানিং টুল          ║
╚══════════════════════════════════╝
"""

TARGET = ""
PORT_RANGE = (1, 1024)
THREADS = 50

open_ports = []
lock = threading.Lock()

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((TARGET, port))
        if result == 0:
            with lock:
                open_ports.append(port)
        s.close()
    except:
        pass

def run(target=None, port_range=(1, 1024)):
    global TARGET, PORT_RANGE
    TARGET = target or input("টার্গেট আইপি/ডোমেইন দিন: ").strip()
    start_p, end_p = port_range
    print(f"\n🔍 স্ক্যান শুরু হচ্ছে {TARGET} — পোর্ট {start_p}-{end_p}...")
    start = datetime.now()

    threads = []
    for port in range(start_p, end_p + 1):
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()
        if len(threads) >= THREADS:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    elapsed = (datetime.now() - start).total_seconds()
    if open_ports:
        print(f"\n✅ ওপেন পোর্ট পাওয়া গেছে ({len(open_ports)}টি):")
        for p in sorted(open_ports):
            try:
                svc = socket.getservbyport(p)
            except:
                svc = "অজানা"
            print(f"   পোর্ট {p:<5} → {svc}")
    else:
        print("\n❌ কোনো ওপেন পোর্ট পাওয়া যায়নি।")

    print(f"\n⏱ সময় লেগেছে: {elapsed:.2f} সেকেন্ড")
    return open_ports

if __name__ == "__main__":
    print(BANNER)
    run()
