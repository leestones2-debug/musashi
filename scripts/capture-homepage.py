#!/usr/bin/env python3
"""무사시 홈페이지 전체·섹션별 스크린샷 캡처"""
import http.server
import os
import socket
import threading
import time
from datetime import datetime

from playwright.sync_api import sync_playwright

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(SITE_DIR, "captures", "home")
VIEWPORT = {"width": 1280, "height": 900}


def free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_server(port):
    os.chdir(SITE_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


PREPARE_JS = """
() => {
  sessionStorage.setItem('musashi_intro', '1');
  document.getElementById('introCurtain')?.remove();
  document.body.classList.remove('intro-lock');
  document.body.classList.add('hero-ready');
  document.querySelectorAll('.reveal, .hero-pop').forEach(el => {
    el.classList.add('on');
    el.classList.remove('intro-wait');
  });
  document.querySelectorAll('#page-home .stat-card [data-target]').forEach(v => {
    v.textContent = v.dataset.target + (Number(v.dataset.target) >= 1000 ? '+' : '');
  });
  window.scrollTo(0, 0);
}
"""


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    port = free_port()
    httpd = start_server(port)
    url = f"http://127.0.0.1:{port}/index.html"
    stamp = datetime.now().strftime("%Y-%m-%d")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport=VIEWPORT, device_scale_factor=2)
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(1500)
            page.evaluate(PREPARE_JS)
            page.wait_for_timeout(800)

            # 전체 페이지 (한 장 긴 캡처)
            full_path = os.path.join(OUT_DIR, f"00-fullpage-{stamp}.png")
            page.locator("#page-home").screenshot(path=full_path)
            print(f"✓ 전체: {full_path}")

            # 섹션별
            sections = page.locator("#page-home > section, #page-home > .marquee").all()
            labels = page.locator("#page-home .sec-label").all()
            label_idx = 0

            for i, sec in enumerate(sections):
                tag = sec.evaluate("el => el.className")
                if "marquee" in tag:
                    name = f"{i+1:02d}-marquee"
                else:
                    label_el = sec.locator(".sec-label").first
                    if label_el.count():
                        name = f"{i+1:02d}-{label_el.inner_text().strip().lower().replace(' ', '-').replace('·', '')}"
                    else:
                        name = f"{i+1:02d}-section"
                name = "".join(c if c.isalnum() or c in "-_" else "-" for c in name)
                path = os.path.join(OUT_DIR, f"{name}.png")
                try:
                    sec.scroll_into_view_if_needed()
                    page.wait_for_timeout(300)
                    sec.screenshot(path=path)
                    print(f"✓ {path}")
                except Exception as e:
                    print(f"✗ {name}: {e}")

            browser.close()
    finally:
        httpd.shutdown()

    print(f"\n저장 폴더: {OUT_DIR}")


if __name__ == "__main__":
    main()
