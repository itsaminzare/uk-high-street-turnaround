"""Rebuild the PDF deck from deck.html (needs: pip install playwright && playwright install chromium).

Run analysis/high_street_analysis.py with PLAIN=1 first, so the untitled charts exist.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
with sync_playwright() as p:
    page = p.chromium.launch().new_page(viewport={"width": 1280, "height": 720})
    page.goto((HERE / "deck.html").as_uri())
    page.wait_for_timeout(800)
    page.pdf(path=str(HERE.parent / "High-Street-Turnaround-Deck.pdf"), width="1280px", height="720px", print_background=True)
print("Saved deck/High-Street-Turnaround-Deck.pdf")
