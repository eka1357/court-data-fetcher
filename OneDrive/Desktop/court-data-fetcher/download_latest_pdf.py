# download_latest_pdf.py
import sqlite3, requests, os
from urllib.parse import urlparse

DB_FILE = 'cases.db'
OUT_DIR = 'downloads'

def get_latest_pdf_url():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('SELECT html FROM queries ORDER BY id DESC LIMIT 1;')
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    html = row[0]
    import re
    match = re.search(r'href=\"([^\"]+\.pdf)\"', html, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def download(url):
    if not url:
        print('No PDF url found.')
        return
    os.makedirs(OUT_DIR, exist_ok=True)
    if url.startswith('/'):
        url = 'https://services.ecourts.gov.in' + url
    print('Downloading:', url)
    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    filename = os.path.basename(urlparse(url).path) or 'order.pdf'
    out_path = os.path.join(OUT_DIR, filename)
    with open(out_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print('Saved to', out_path)

if __name__ == '__main__':
    url = get_latest_pdf_url()
    print('Found PDF:', url)
    download(url)
