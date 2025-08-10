# 🏛 Court Data Fetcher

A Python-based tool to fetch and display case details from the **e-Courts portal**.  
It uses **Playwright** for browser automation and stores queries in a local SQLite database.

---

## ✨ Features
- 🔍 Search cases by CNR number
- 🖥 Fetch and display live case details from e-Courts
- 💾 Save query history in `cases.db` (SQLite)
- 🗂 View past queries with timestamp
- 🌐 Simple web interface (Flask)
- 📄 Display full HTML result for each case

---

## 📋 Requirements
- Python **3.8+**
- `pip` package manager
- Google Chrome (for Playwright)
- Node.js (Playwright dependency)

---

## ⚙️ Installation

```bash
# 1️⃣ Clone this repository
git clone https://github.com/eka1357/court-data-fetcher.git
cd court-data-fetcher

# 2️⃣ Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Install Playwright browsers
python -m playwright install
