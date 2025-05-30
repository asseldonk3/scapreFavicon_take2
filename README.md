# Google Favicon Scraper - Complete Guide

A tool to automatically download favicons from Google search results for a list of shop domains, with a web interface to review and manage the results.

## 🎯 Purpose

This application:
1. Reads shop domains from a CSV file
2. Searches each domain on Google
3. Downloads the favicon that appears next to the domain in search results
4. Provides a web interface to review favicons and mark incorrect ones
5. Allows re-scraping of failed/remaining shops

## 📋 Prerequisites

- Python 3.7 or higher
- Chrome browser
- ChromeDriver (automatically installed with selenium)
- Windows/Mac/Linux OS

## 🚀 Quick Start Guide

### Step 1: Initial Setup (First Time Only)

1. **Clone or download the project**
2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```
3. **Activate the virtual environment:**
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Prepare Your Data

1. **Create your shop list CSV file** named `urls.csv` with this format:
   ```csv
   Shop ID;Shop
   1;bol.com
   512098;amazon.nl
   123456;coolblue.nl
   ```
   - Use semicolon (;) as delimiter
   - First column: Shop ID (unique identifier)
   - Second column: Shop domain (without https://)

### Step 3: Run the Favicon Scraper

You have two options:

#### Option A: Manual Scraping (for small batches)
```bash
python google_favicon_scraper.py urls.csv 0 50
```
- Parameters: `csv_file start_index batch_size`
- This will scrape 50 shops starting from index 0

#### Option B: Automatic Continuous Scraping (recommended)
```bash
python run_continuous_scraper.py urls.csv 100
```
- Parameters: `csv_file max_iterations`
- Automatically processes shops in batches of 50
- Adds delays between batches to avoid rate limiting
- Continues until all shops are processed

### Step 4: Review Favicons

1. **Start the web interface:**
   ```bash
   python app.py
   ```
2. **Open your browser** and go to: `http://localhost:5000`
3. **Review favicons:**
   - Click on incorrect favicons to move them to the "not_correct" folder
   - Use pagination to browse through all favicons
   - The interface shows Shop ID and domain name for each favicon

### Step 5: Handle Failed/Remaining Shops

If some shops failed to get favicons:

1. **Identify failed shops:**
   ```bash
   python identify_failed_shops.py
   ```
   This creates `failed_shops.csv` with shops missing favicons

2. **Clean up and prepare for re-scraping:**
   ```bash
   python cleanup_processed_shops.py failed_shops.csv
   ```
   This creates a new CSV file with only the failed shops

3. **Re-run the scraper** with the new CSV file

## 📁 Project Structure

```
favicon_scraper/
├── google_favicon_scraper.py    # Main scraping script
├── run_continuous_scraper.py    # Batch processing script
├── app.py                      # Flask web interface
├── templates/
│   └── gallery.html           # Web interface template
├── identify_failed_shops.py    # Find shops without favicons
├── cleanup_processed_shops.py  # Prepare CSV for re-scraping
├── cleanup_project.py         # Clean temporary files
├── generate_favicon_gallery.py # Optional: Create static HTML gallery
├── requirements.txt           # Python dependencies
├── urls.csv                   # Your shop list (you create this)
├── favicons/                  # Downloaded favicon images
│   └── not_correct/          # Incorrect favicons (moved via web UI)
└── README.md                  # This file
```

## 🔧 Advanced Usage

### Scraping Specific Ranges
```bash
# Scrape shops 100-150
python google_favicon_scraper.py urls.csv 100 50

# Scrape shops 500-600
python google_favicon_scraper.py urls.csv 500 100
```

### Adjusting Scraper Settings

Edit `google_favicon_scraper.py` to adjust:
- `SHOPS_PER_BROWSER_SESSION`: Browser restart frequency (default: 8-12)
- Delays between searches (look for `time.sleep()` calls)
- Timeout values for page loading

### Creating Static HTML Gallery (Optional)

If you need a portable HTML gallery without the Flask app:
```bash
python generate_favicon_gallery.py
```

This creates:
- `index.html`: Gallery with links to favicon files
- `index_standalone.html`: Self-contained gallery with embedded images

**Note**: The Flask app is recommended for reviewing as it allows marking incorrect favicons.

### Cleaning Up Between Projects

Run the cleanup script to remove temporary files:
```bash
python cleanup_project.py
```

This will:
- Remove temporary CSV files
- Remove log files
- Remove debug HTML files
- Keep your favicons and core scripts
- Create a sample CSV file

## ⚠️ Important Notes

1. **Rate Limiting**: Google may block requests if too many are made quickly
   - The scraper includes random delays
   - Browser restarts every 8-12 shops
   - Consider running in smaller batches

2. **Favicon Quality**: Not all favicons may be correct
   - Use the web interface to review
   - Move incorrect ones to the "not_correct" folder
   - Re-scrape failed shops if needed

3. **CSV Format**: Must use semicolon (;) delimiter and include headers

## 🐛 Troubleshooting

### "No favicon found"
- The domain might not appear in Google search results
- Try searching manually to verify
- Domain might be blocked or redirected

### Browser crashes
- Reduce batch size
- Increase delays between searches
- Check ChromeDriver compatibility

### Rate limited by Google
- Wait a few hours before continuing
- Use smaller batch sizes
- Run scraper during off-peak hours

## 📝 Workflow Summary

1. **Prepare**: Create `urls.csv` with your shop list
2. **Scrape**: Run `python run_continuous_scraper.py urls.csv`
3. **Review**: Start web UI with `python app.py` and check favicons
4. **Fix**: Identify failed shops and re-scrape if needed
5. **Clean**: Run `python cleanup_project.py` when done

## 🤝 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your CSV file format
3. Ensure Chrome and ChromeDriver are up to date
4. Try with a smaller batch size first 