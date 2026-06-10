#!/usr/bin/env python3
"""
PDF Generator v3 — Playwright + Chromium based
Properly renders Bengali text in PDF.
"""

import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import markdown
import asyncio
from playwright.async_api import async_playwright

BOOK_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF = os.path.join(BOOK_DIR, 'সাইবার_নিরাপত্তা_শূন্য_থেকে_চাকরি.pdf')
TEMP_HTML = os.path.join(BOOK_DIR, '_temp_book.html')

BOOK_STRUCTURE = [
    ("পার্ট ১: ভিত্তি ও রোডম্যাপ", "পার্ট-১_ভিত্তি_ও_রোডম্যাপ", [
        "অধ্যায়-০১_cybersecurity_কী_ও_কেন_শিখবে.md",
        "অধ্যায়-০২_ethical_hacking_কী.md",
        "অধ্যায়-০৩_certification_roadmap.md",
    ]),
    ("পার্ট ২: Networking", "পার্ট-২_Networking", [
        "অধ্যায়-০৪_internet_কিভাবে_কাজ_করে.md",
        "অধ্যায়-০৫_networking_fundamentals.md",
        "অধ্যায়-০৬_advanced_networking.md",
        "অধ্যায়-০৭_wifi_wireless.md",
    ]),
    ("পার্ট ৩: Linux", "পার্ট-৩_Linux", [
        "অধ্যায়-০৮_linux_কেন_শিখবে.md",
        "অধ্যায়-০৯_linux_commands.md",
        "অধ্যায়-১০_kali_linux_setup.md",
        "অধ্যায়-১১_parrot_security_os.md",
    ]),
    ("পার্ট ৪: Reconnaissance", "পার্ট-৪_Reconnaissance", [
        "অধ্যায়-১২_osint_passive_recon.md",
        "অধ্যায়-১৩_nmap_active_recon.md",
        "অধ্যায়-১৪_spoofing_anonymity.md",
    ]),
    ("পার্ট ৫: Attack Techniques", "পার্ট-৫_Attack_Techniques", [
        "অধ্যায়-১৫_vulnerability_assessment.md",
        "অধ্যায়-১৬_5_stages_of_hacking.md",
        "অধ্যায়-১৭_system_hacking.md",
        "অধ্যায়-১৮_phishing_attacks.md",
        "অধ্যায়-১৯_malware.md",
        "অধ্যায়-২০_network_attacks.md",
        "অধ্যায়-২১_wifi_hacking.md",
        "অধ্যায়-২২_password_security.md",
    ]),
    ("পার্ট ৬: Web Security", "পার্ট-৬_Web_Security", [
        "অধ্যায়-২৩_web_security_basics.md",
        "অধ্যায়-২৪_owasp_top_10.md",
        "অধ্যায়-২৫_advanced_web_attacks.md",
        "অধ্যায়-২৬_gain_maintain_access.md",
    ]),
    ("পার্ট ৭: Tools", "পার্ট-৭_Tools", [
        "অধ্যায়-২৭_metasploit_framework.md",
        "অধ্যায়-২৮_top_10_kali_tools.md",
        "অধ্যায়-২৯_top_10_free_tools.md",
        "অধ্যায়-৩০_top_10_gadgets.md",
    ]),
    ("পার্ট ৮: Mobile Security", "পার্ট-৮_Mobile_Security", [
        "অধ্যায়-৩১_android_mobile_security.md",
    ]),
    ("পার্ট ৯: IoT", "পার্ট-৯_IoT", [
        "অধ্যায়-৩২_cctv_iot_security.md",
    ]),
    ("পার্ট ১০: Dark Web ও Cyber War", "পার্ট-১০_Dark_Web", [
        "অধ্যায়-৩৩_surface_deep_dark_web.md",
        "অধ্যায়-৩৪_cyber_war.md",
    ]),
    ("পার্ট ১১: Cryptography", "পার্ট-১১_Cryptography", [
        "অধ্যায়-৩৫_cryptography.md",
    ]),
    ("পার্ট ১২: Defense & Blue Team", "পার্ট-১২_Defense", [
        "অধ্যায়-৩৬_network_security_defense.md",
        "অধ্যায়-৩৭_incident_response.md",
        "অধ্যায়-৩৮_siem_monitoring.md",
        "অধ্যায়-৩৯_hardening.md",
    ]),
    ("পার্ট ১৩: Domain-specific", "পার্ট-১৩_Domain_Specific", [
        "অধ্যায়-৪০_healthcare_security.md",
        "অধ্যায়-৪১_financial_security.md",
    ]),
    ("পার্ট ১৪: AI", "পার্ট-১৪_AI", [
        "অধ্যায়-৪২_ai_cybersecurity.md",
    ]),
    ("পার্ট ১৫: Career", "পার্ট-১৫_Career", [
        "অধ্যায়-৪৩_bash_scripting.md",
        "অধ্যায়-৪৪_osint_advanced.md",
        "অধ্যায়-৪৫_ctf_labs.md",
        "অধ্যায়-৪৬_bug_bounty.md",
        "অধ্যায়-৪৭_roadmap_2026.md",
        "অধ্যায়-৪৮_interview_prep.md",
    ]),
    ("পার্ট ১৬: বিগিনার রোডম্যাপ ২০২৬", "পার্ট-১৬_২০২৬_রোডম্যাপ", [
        "অধ্যায়-৪৯_বিগিনার_রোডম্যাপ_২০২৬_সম্পূর্ণ.md",
    ]),
]


PDF_CSS = """
@page {
    size: A4;
    margin: 2cm 2.2cm;
}
body {
    font-family: 'Nirmala UI', 'Vrinda', 'Shonar Bangla', 'Noto Sans Bengali', sans-serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #1a1a1a;
}
.cover-page {
    page-break-after: always;
    text-align: center;
    padding-top: 180px;
}
.cover-page h1 {
    font-size: 26pt;
    color: #0a66c2;
    margin-bottom: 12px;
}
.cover-page .subtitle {
    font-size: 13pt;
    color: #555;
    margin-bottom: 40px;
}
.cover-page .meta {
    font-size: 10pt;
    color: #777;
    line-height: 2;
}
.cover-page .badge {
    display: inline-block;
    background: #e8f0fe;
    color: #0a66c2;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 10pt;
    margin-bottom: 15px;
}
.part-divider {
    page-break-before: always;
    text-align: center;
    padding-top: 220px;
}
.part-divider h2 {
    font-size: 20pt;
    color: #0a66c2;
    margin-bottom: 8px;
}
.part-divider .part-line {
    width: 80px;
    height: 3px;
    background: #0a66c2;
    margin: 16px auto;
}
.chapter {
    page-break-before: always;
}
.chapter h1 {
    font-size: 18pt;
    color: #0a66c2;
    border-bottom: 2px solid #0a66c2;
    padding-bottom: 6px;
    margin-bottom: 16px;
}
.chapter h2 {
    font-size: 14pt;
    color: #1a1a1a;
    margin-top: 22px;
    margin-bottom: 8px;
}
.chapter h3 {
    font-size: 12pt;
    color: #333;
    margin-top: 18px;
    margin-bottom: 6px;
}
.chapter p { margin-bottom: 8px; text-align: justify; }
.chapter ul, .chapter ol { margin: 6px 0 10px 18px; }
.chapter li { margin-bottom: 4px; }
.chapter code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
    background: #f4f4f4;
    padding: 1px 4px;
    border-radius: 3px;
}
.chapter pre {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 10px 14px;
    border-radius: 4px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    line-height: 1.35;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 10px 0;
}
.chapter pre code { background: none; padding: 0; color: inherit; }
.chapter table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9pt;
}
.chapter th {
    background: #0a66c2;
    color: white;
    padding: 6px 8px;
    text-align: left;
}
.chapter td { padding: 5px 8px; border: 1px solid #ddd; }
.chapter tr:nth-child(even) td { background: #f8f8f8; }
.chapter blockquote {
    border-left: 4px solid #0a66c2;
    padding: 8px 12px;
    margin: 12px 0;
    background: #f0f7ff;
}
.chapter blockquote p { margin: 0; }
.chapter hr { border: none; border-top: 1px solid #ddd; margin: 20px 0; }
.toc { page-break-after: always; }
.toc h2 { text-align: center; font-size: 18pt; color: #0a66c2; margin-bottom: 24px; }
.toc-entry { margin: 4px 0; font-size: 10pt; }
.toc-part { font-weight: bold; color: #0a66c2; margin-top: 10px; font-size: 10.5pt; }
.toc-chapter { padding-left: 18px; color: #333; }
"""


def read_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def convert_md_to_html(md_text):
    exts = [
        'markdown.extensions.extra',
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
    ]
    return markdown.markdown(md_text, extensions=exts)


def build_html_book():
    parts = []
    total_ch = sum(len(chs) for _, _, chs in BOOK_STRUCTURE)
    ch_num = 0

    # Cover
    cover = f"""
    <div class="cover-page">
        <div class="badge">\u2728 \u09b8\u09ae\u09cd\u09aa\u09c2\u09b0\u09cd\u09a3 \u09ac\u09be\u0999\u09be\u09b2\u09be \u09ac\u0987</div>
        <h1>\u09b8\u09be\u0987\u09ac\u09be\u09b0 \u09a8\u09bf\u09b0\u09be\u09aa\u09a4\u09cd\u09a4\u09be:<br>\u09b6\u09c2\u09a8\u09cd\u09af \u09a5\u09c7\u0995\u09c7 \u099a\u09be\u0995\u09b0\u09bf</h1>
        <div class="subtitle">Zero to Job \u2014 Cybersecurity in Bangla</div>
        <div class="meta">
            <strong>{total_ch} \u099f\u09bf \u0985\u09a7\u09cd\u09af\u09be\u09af\u09bc</strong> | 15\u099f\u09bf \u09aa\u09be\u09b0\u09cd\u099f<br>
            Ethical Hacking | Networking | Linux | Web Security<br>
            Metasploit | OSINT | Cryptography | Defense | Career<br><br>
            \u09b6\u09bf\u0995\u09cd\u09b7\u09be\u09ae\u09c2\u09b2\u0995 \u0989\u09a6\u09cd\u09a6\u09c7\u09b6\u09cd\u09af\u09c7<br>
            \u09b8\u09ac \u0995\u09cb\u09a1 \u09a8\u09bf\u099c\u09c7\u09b0 lab-\u098f practice \u0995\u09b0\u09cb
        </div>
    </div>
    """
    parts.append(cover)

    # TOC
    toc = '<div class="toc"><h2>\u09b8\u09c2\u099a\u09bf\u09aa\u09a4\u09cd\u09b0</h2>'
    ch_num = 1
    for pname, _, chs in BOOK_STRUCTURE:
        toc += f'<div class="toc-entry toc-part">{pname}</div>'
        for cf in chs:
            title = cf.replace('.md', '').split('_', 1)[1] if '_' in cf else cf
            title = title.replace('_', ' ')
            toc += f'<div class="toc-entry toc-chapter">\u0985\u09a7\u09cd\u09af\u09be\u09af\u09bc {ch_num}: {title}</div>'
            ch_num += 1
    toc += '</div>'
    parts.append(toc)

    # Chapters
    ch_num = 1
    for pname, folder, chs in BOOK_STRUCTURE:
        pdir = os.path.join(BOOK_DIR, folder)
        parts.append(f'<div class="part-divider"><div class="part-line"></div><h2>{pname}</h2><p style="color:#666;">{len(chs)} \u099f\u09bf \u0985\u09a7\u09cd\u09af\u09be\u09af\u09bc</p></div>')

        for cf in chs:
            fp = os.path.join(pdir, cf)
            title = cf.replace('.md', '').split('_', 1)[1] if '_' in cf else cf
            title = title.replace('_', ' ')
            safe_title = title.encode('ascii', 'replace').decode('ascii')
            print(f'  [{ch_num}/{total_ch}] {safe_title}')

            if os.path.exists(fp):
                md = read_md(fp)
                html = convert_md_to_html(md)
                parts.append(f'<div class="chapter"><h1>\u0985\u09a7\u09cd\u09af\u09be\u09af\u09bc {ch_num}: {title}</h1>{html}</div>')
            else:
                parts.append(f'<div class="chapter"><h1>\u0985\u09a7\u09cd\u09af\u09be\u09af\u09bc {ch_num}: {title}</h1><p style="color:red;">File not found: {fp}</p></div>')
            ch_num += 1

    full = f'''<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<title>\u09b8\u09be\u0987\u09ac\u09be\u09b0 \u09a8\u09bf\u09b0\u09be\u09aa\u09a4\u09cd\u09a4\u09be: \u09b6\u09c2\u09a8\u09cd\u09af \u09a5\u09c7\u0995\u09c7 \u099a\u09be\u0995\u09b0\u09bf</title>
<style>{PDF_CSS}</style>
</head>
<body>{"".join(parts)}</body>
</html>'''
    return full


async def generate_pdf():
    print('=' * 60)
    print('  PDF Generator — Playwright + Chromium')
    print('=' * 60)

    total_ch = sum(len(chs) for _, _, chs in BOOK_STRUCTURE)

    # Build HTML
    print(f'\n[1/3] Converting {total_ch} chapters to HTML...')
    html = build_html_book()

    with open(TEMP_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Temp HTML: {TEMP_HTML}')

    # Generate PDF with Playwright
    print('\n[2/3] Launching Chromium for PDF generation...')
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print('[3/3] Rendering PDF (this may take a few minutes)...')
        await page.goto(f'file:///{TEMP_HTML}', wait_until='networkidle')

        # PDF options
        await page.pdf(
            path=OUTPUT_PDF,
            format='A4',
            margin={
                'top': '20mm',
                'bottom': '20mm',
                'left': '20mm',
                'right': '20mm'
            },
            print_background=True,
            prefer_css_page_size=True,
        )

        await browser.close()

    # Cleanup
    if os.path.exists(TEMP_HTML):
        os.remove(TEMP_HTML)

    size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    out_path = OUTPUT_PDF.encode('ascii', 'replace').decode('ascii')
    print(f'\n{"=" * 60}')
    print(f'  SUCCESS! PDF created!')
    print(f'  Location: {out_path}')
    print(f'  Size: {size_mb:.1f} MB')
    print(f'  Chapters: {total_ch}')
    print(f'{"=" * 60}')


if __name__ == '__main__':
    asyncio.run(generate_pdf())
