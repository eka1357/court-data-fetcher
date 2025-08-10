from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from urllib.parse import urljoin
import os

DB_FILE = "cases.db"
BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/"

# Ensure DB exists
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnr_number TEXT,
            html TEXT,
            fetched_at TEXT
        )
    """)
    conn.commit()
    conn.close()

# Save query to DB
def save_query(cnr_number, html):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO queries (cnr_number, html, fetched_at) VALUES (?, ?, ?)",
              (cnr_number, html, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# Parse HTML for case details
def parse_case_html(html):
    soup = BeautifulSoup(html, "html.parser")

    case_details = {
        "parties": None,
        "filing_date": None,
        "next_hearing_date": None,
        "orders": []
    }

    try:
        # Parties' names
        parties_tag = soup.find("td", string=lambda x: x and "Petitioner" in x)
        if parties_tag:
            case_details["parties"] = parties_tag.find_next("td").get_text(strip=True)

        # Filing date
        filing_tag = soup.find("td", string=lambda x: x and "Filing Date" in x)
        if filing_tag:
            case_details["filing_date"] = filing_tag.find_next("td").get_text(strip=True)

        # Next hearing date
        next_hearing_tag = soup.find("td", string=lambda x: x and "Next Hearing Date" in x)
        if next_hearing_tag:
            case_details["next_hearing_date"] = next_hearing_tag.find_next("td").get_text(strip=True)

        # All PDF links
        for link in soup.find_all("a", href=lambda x: x and x.endswith(".pdf")):
            title = link.get_text(strip=True) or "Order/Judgment"
            abs_url = urljoin(BASE_URL, link["href"])
            case_details["orders"].append({
                "title": title,
                "link": abs_url
            })

        # Sort orders so newest first (assuming date in title)
        case_details["orders"].sort(key=lambda x: x["title"], reverse=True)

    except Exception as e:
        print(f"⚠️ Parsing error: {e}")

    return case_details

# Main scraping function
def get_case_data(cnr_number):
    init_db()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("🔗 Opening eCourts homepage...")
            page.goto(BASE_URL, timeout=60000)

            print("📄 Clicking on 'CNR Number' tab...")
            page.click("text=CNR Number")

            print("⌛ Waiting for CNR input field...")
            page.wait_for_selector("#cnrno", timeout=15000)

            print("✍️ Typing CNR number...")
            page.fill("#cnrno", cnr_number)

            input("🧑 Please manually solve CAPTCHA in browser, then press ENTER here...")

            print("🚀 Submitting form...")
            page.click("#submit_captcha")

            print("⌛ Waiting for result page to load...")
            page.wait_for_timeout(5000)

            html = page.content()

            # Save raw HTML
            save_query(cnr_number, html)

            # Parse details
            parsed_data = parse_case_html(html)

            return {
                "status": "Fetched",
                "html": html,
                "parsed": parsed_data
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

        finally:
            browser.close()
