# Quick Reference - Favicon Scraper

## 🚀 Common Commands

### Setup (First Time)
```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### Main Workflow
```bash
# 1. Automatic scraping (recommended)
python run_continuous_scraper.py urls.csv

# 2. Review favicons in browser
python app.py
# Then open: http://localhost:5000

# 3. Find failed shops
python identify_failed_shops.py

# 4. Prepare failed shops for re-scraping
python cleanup_processed_shops.py failed_shops.csv

# 5. Clean up project when done
python cleanup_project.py
```

### Manual Scraping Options
```bash
# Scrape first 50 shops
python google_favicon_scraper.py urls.csv 0 50

# Scrape shops 100-150
python google_favicon_scraper.py urls.csv 100 50

# Scrape specific range
python google_favicon_scraper.py urls.csv START_INDEX BATCH_SIZE
```

### CSV File Format
```
Shop ID;Shop
1;bol.com
512098;amazon.nl
```

### File Locations
- Input: `urls.csv`
- Output: `favicons/` folder
- Incorrect: `favicons/not_correct/`
- Failed shops: `failed_shops.csv`

### Tips
- Use batch size of 50 or less
- Wait if rate limited by Google
- Check favicons via web interface
- Re-scrape failed shops separately 