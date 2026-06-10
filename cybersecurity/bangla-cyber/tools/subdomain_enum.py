"""
বাংলা: সাবডোমেইন এনুমারেটর
লেখক: PavelGoblin
"""

import socket
import concurrent.futures

BANNER = """
╔══════════════════════════════════╗
║   🌐 সাবডোমেইন এনুমারেটর v1.0   ║
║   সাবডোমেইন আবিষ্কার টুল         ║
╚══════════════════════════════════╝
"""

WORDLIST = [
    "www", "mail", "ftp", "admin", "api", "dev", "test", "blog",
    "shop", "forum", "wiki", "remote", "webmail", "server", "ns1",
    "ns2", "smtp", "pop3", "dns", "vpn", "cdn", "static", "img",
    "docs", "support", "status", "app", "beta", "demo", "stage",
    "backup", "portal", "secure", "login", "register", "dashboard",
    "console", "manager", "git", "jenkins", "jira", "confluence",
    "nexus", "artifactory", "docker", "k8s", "grafana", "prometheus",
    "monitor", "alert", "proxy", "gateway", "router", "switch",
    "auth", "oauth", "identity", "sso", "ldap", "radius",
]

def resolve(subdomain):
    try:
        ip = socket.gethostbyname(subdomain)
        return (subdomain, ip)
    except:
        return None

def run(domain=None):
    domain = domain or input("ডোমেইন নাম দিন (যেমন: example.com): ").strip()
    print(f"\n🔍 সাবডোমেইন খোঁজা হচ্ছে: {domain}")
    found = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futs = {executor.submit(resolve, f"{sub}.{domain}"): sub for sub in WORDLIST}
        for fut in concurrent.futures.as_completed(futs):
            result = fut.result()
            if result:
                found.append(result)
                print(f"   ✅ {result[0]} → {result[1]}")

    if found:
        print(f"\n✅ মোট {len(found)}টি সাবডোমেইন পাওয়া গেছে:")
        for sub, ip in sorted(found, key=lambda x: x[0]):
            print(f"   {sub:<30} {ip}")
    else:
        print("\n❌ কোনো সাবডোমেইন পাওয়া যায়নি।")

    return found

if __name__ == "__main__":
    print(BANNER)
    run()
