# Google Favicon Scraper

This script searches Google for each domain in the provided CSV file and downloads the favicon image that appears next to the domain name in the search results.

## Prerequisites

You need to have the following installed:
- Python 3.7 or higher
- Chrome browser
- ChromeDriver compatible with your Chrome version

## Required Python Packages

Install the required packages using:

```bash
pip install selenium requests
```

## CSV File Format

The CSV file should have the following format:
- Semicolon (;) delimited
- First column: Shop ID
- Second column: Shop domain
- Header row is expected and will be skipped

Example:
```
Shop ID;Shop
1;bol.com
512098;Amazon.nl
```

## Usage

1. Make sure you have the CSV file named `urls.csv` in the same directory as the script
2. Run the script:

```bash
python google_favicon_scraper.py
```

The script will:
1. Search Google for each domain
2. Extract the favicon image if the domain appears in the search results
3. Save the image with the filename format `ShopID_shopdomain.png` in a folder named `favicons`

## Anti-Detection Measures

The script includes several measures to avoid being detected as automated browsing:
- Custom user agent
- Disabled automation flags
- Random delays between requests
- Maximized browser window
- Dutch language settings

## Notes

- The script might be blocked by Google if too many requests are made in a short time
- Make sure you're complying with Google's terms of service when running this script
- Cookie acceptance is handled automatically for EU users 