# YellowPages Scraper (Episode 1) 🕷️

This module contains the logic for scraping business data from **YellowPages Thailand**.
It uses a hybrid approach with **Crawl4AI** (for browser handling) and **BeautifulSoup** (for efficient parsing).

## 📂 Structure

-   `main.py`: The executable scraper script.
-   `requirements.txt`: Dependencies for the scraper.
-   `*.ipynb`: Original research notebooks (archived).

## 🚀 How to Run

1.  **Install Dependencies** (Requires Python 3.10+):
    ```bash
    # Create valid venv (if not exists)
    python3.11 -m venv .venv_scraper
    source .venv_scraper/bin/activate
    
    # Install libs
    pip install -r requirements.txt
    playwright install
    ```

2.  **Run the Scraper**:
    ```bash
    python main.py --category "กีฬา"
    ```
    (You can change "กีฬา" to any other category keyword).

## ⚠️ Technical Note: Python Version
This scraper uses `crawl4ai` (v0.4.247) which matches the logic from the original December 2025 notebook.
- **Required**: Python 3.10 or newer (Python 3.11 Recommended).
- **Incompatible**: Python 3.9 (Causes `TypeError: | operator`).
- **Browser**: Requires specific Chromium matching the library. Use `playwright install` inside the venv.

3.  **Output**:
    -   The script will generate a CSV file (e.g., `yellowpages_กีฬา.csv`) with the extracted data.
    -   You can move this file to `../data/raw/` to be processed by the Chatbot AI.
