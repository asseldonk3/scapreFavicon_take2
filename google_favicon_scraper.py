import csv
import os
import time
import base64
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import re
import random # Import random for variable delays

# Create directory for storing images if it doesn't exist
os.makedirs('favicons', exist_ok=True)

# Function to sanitize filename for filesystem compatibility
def sanitize_filename(filename):
    """Remove or replace characters that are invalid in filenames"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Function to extract and save base64 image from src attribute
def save_base64_image(img_src, filename):
    if 'base64' in img_src:
        # Extract the base64 part
        base64_data = img_src.split('base64,')[1]
        # Save the image
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(base64_data))
        return True
    return False

# Function to download regular image URL
def download_image(img_url, filename):
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response:
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Error downloading image: {e}")
    return False

# Set up Chrome options for Selenium with anti-detection measures
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
    chrome_options.add_argument("--lang=nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7") # More realistic accept language
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--profile-directory=Default") # Use default profile if available
    chrome_options.add_argument("--incognito") # Incognito might help, or might be a flag, test this
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['nl-NL', 'nl']});")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});") # Mock plugins
    return driver

# Function to generate the HTML gallery with all favicons
def generate_favicon_gallery():
    # Create favicons directory if it doesn't exist
    favicon_dir = "favicons"
    os.makedirs(favicon_dir, exist_ok=True)
    
    # Get all favicon files
    favicon_files = [f for f in os.listdir(favicon_dir) if os.path.isfile(os.path.join(favicon_dir, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    # Sort by filename
    favicon_files.sort()
    
    # Start building HTML
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shop Favicons Gallery</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f8f9fa;
        }
        h1 {
            color: #1a73e8;
            text-align: center;
            margin-bottom: 30px;
        }
        .favicon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .favicon-item {
            display: flex;
            align-items: center;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .favicon-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .favicon-image {
            width: 32px;
            height: 32px;
            margin-right: 15px;
            /* Google's style for favicons */
            border-radius: 4px;
            object-fit: contain;
        }
        .favicon-details {
            flex: 1;
        }
        .shop-id {
            font-weight: bold;
            color: #202124;
            margin-bottom: 5px;
        }
        .shop-domain {
            color: #5f6368;
            font-size: 14px;
            word-break: break-all;
        }
        .missing {
            color: #ea4335;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>Shop Favicons Gallery</h1>
    <div class="favicon-grid">
"""
    
    # Function to extract shop ID and domain from filename
    def extract_info(filename):
        # Expected format: ShopID_domain_name.png
        parts = filename.split('_', 1)
        if len(parts) >= 2:
            shop_id = parts[0]
            # Convert domain_name.png back to domain.name
            domain = parts[1].replace('_', '.').rsplit('.', 1)[0]
            return shop_id, domain
        return "Unknown", filename
    
    # Add each favicon to the HTML
    for favicon_file in favicon_files:
        shop_id, domain = extract_info(favicon_file)
            
        html += f"""
        <div class="favicon-item">
                <img class="favicon-image" src="./favicons/{favicon_file}" alt="Favicon for {domain}">
            <div class="favicon-details">
                <div class="shop-id">Shop ID: {shop_id}</div>
                <div class="shop-domain">{domain}</div>
            </div>
        </div>"""
    
    # Close HTML
    html += """
    </div>
</body>
</html>
"""
    
    # Write HTML to file
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Generated index.html with {len(favicon_files)} favicon images")
    
    # Create a copy that embeds the images directly to be fully portable
    create_standalone_html()

# Function to create a standalone HTML file with embedded images
def create_standalone_html():
    # Create favicons directory if it doesn't exist
    favicon_dir = "favicons"
    
    # Get all favicon files
    favicon_files = [f for f in os.listdir(favicon_dir) if os.path.isfile(os.path.join(favicon_dir, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    # Sort by filename
    favicon_files.sort()
    
    # Start building HTML
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shop Favicons Gallery (Standalone)</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f8f9fa;
        }
        h1 {
            color: #1a73e8;
            text-align: center;
            margin-bottom: 30px;
        }
        .favicon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .favicon-item {
            display: flex;
            align-items: center;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .favicon-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .favicon-image {
            width: 32px;
            height: 32px;
            margin-right: 15px;
            /* Google's style for favicons */
            border-radius: 4px;
            object-fit: contain;
        }
        .favicon-details {
            flex: 1;
        }
        .shop-id {
            font-weight: bold;
            color: #202124;
            margin-bottom: 5px;
        }
        .shop-domain {
            color: #5f6368;
            font-size: 14px;
            word-break: break-all;
        }
        .missing {
            color: #ea4335;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>Shop Favicons Gallery (Standalone Version)</h1>
    <p style="text-align: center; margin-bottom: 30px;">This version has all images embedded and can be moved anywhere.</p>
    <div class="favicon-grid">
"""
    
    # Function to extract shop ID and domain from filename
    def extract_info(filename):
        # Expected format: ShopID_domain_name.png
        parts = filename.split('_', 1)
        if len(parts) >= 2:
            shop_id = parts[0]
            # Convert domain_name.png back to domain.name
            domain = parts[1].replace('_', '.').rsplit('.', 1)[0]
            return shop_id, domain
        return "Unknown", filename
    
    # Function to read image file and convert to base64
    def image_to_base64(file_path):
        with open(file_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Determine MIME type based on file extension
            ext = os.path.splitext(file_path)[1].lower()
            mime_type = 'image/png'  # Default
            if ext == '.jpg' or ext == '.jpeg':
                mime_type = 'image/jpeg'
            elif ext == '.gif':
                mime_type = 'image/gif'
                
            return f"data:{mime_type};base64,{encoded_string}"
    
    # Add each favicon to the HTML with embedded base64 image
    for favicon_file in favicon_files:
        shop_id, domain = extract_info(favicon_file)
            
        # Get the base64 data for the image
        file_path = os.path.join(favicon_dir, favicon_file)
        if os.path.exists(file_path):
            try:
                base64_image = image_to_base64(file_path)
                
                html += f"""
        <div class="favicon-item">
                <img class="favicon-image" src="{base64_image}" alt="Favicon for {domain}">
            <div class="favicon-details">
                <div class="shop-id">Shop ID: {shop_id}</div>
                <div class="shop-domain">{domain}</div>
            </div>
        </div>"""
            except Exception as e:
                print(f"Error embedding image {favicon_file}: {e}")
    
    # Close HTML
    html += """
    </div>
</body>
</html>
"""
    
    # Write HTML to file
    with open("index_standalone.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Generated index_standalone.html with embedded images - can be moved anywhere")

# Function to check if favicon already exists for this shop
def check_existing_favicon(shop_id, shop_domain):
    """Check if favicon already exists for this shop"""
    # Check for various possible filename formats
    possible_filenames = [
        f"favicons/{shop_id}_{shop_domain.replace('.', '_')}.png",
        f"favicons/{shop_id}_{shop_domain.replace('.', '_')}.jpg",
        f"favicons/{shop_id}_{shop_domain.replace('.', '_')}.jpeg",
        f"favicons/{shop_id}_{shop_domain.replace('.', '_')}.gif"
    ]
    
    for filename in possible_filenames:
        if os.path.exists(filename):
            return True, filename
    
    return False, None

def scan_existing_favicons():
    """Scan existing favicons and return a set of shop IDs that already have favicons"""
    existing_shop_ids = set()
    
    if not os.path.exists('favicons'):
        return existing_shop_ids
    
    favicon_files = [f for f in os.listdir('favicons') if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    for favicon_file in favicon_files:
        # Extract shop ID from filename (format: ShopID_domain_name.extension)
        parts = favicon_file.split('_', 1)
        if len(parts) >= 1:
            shop_id = parts[0]
            existing_shop_ids.add(shop_id)
    
    print(f"Found existing favicons for {len(existing_shop_ids)} shops")
    return existing_shop_ids

# Main function to search Google and download favicons
def search_and_download_favicons(csv_path, start_from=0, max_shops=None):
    print(f"Starting favicon scraper...")
    
    existing_shop_ids = scan_existing_favicons()
    driver = None  # Initialize driver to None
    
    # Configuration for browser restart
    SHOPS_PER_BROWSER_SESSION = random.randint(8, 12)  # Restart browser every 8-12 shops
    shops_in_current_session = 0
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            headers = next(csv_reader)  # Skip header row
            
            # Convert to list for easier indexing and counting
            all_shops = list(csv_reader)
            total_shops = len(all_shops)
            
            print(f"Total shops to process: {total_shops}")
            print(f"Starting from index: {start_from}")
            
            if max_shops:
                end_at = min(start_from + max_shops, total_shops)
                print(f"Will process up to shop index: {end_at-1}")
            else:
                end_at = total_shops
            
            shops_processed = 0
            shops_successful = 0
            shops_skipped = 0

            driver = setup_driver() # Setup driver outside the loop initially
            
            for i, row in enumerate(all_shops[start_from:end_at]):
                current_index = start_from + i
                shop_id = row[0]
                shop_domain = row[1]
                
                print(f"Processing ({current_index+1}/{total_shops}) {shop_id}: {shop_domain}")
                
                if shop_id in existing_shop_ids:
                    print(f"  ✓ Favicon already exists for {shop_domain} - skipping")
                    shops_skipped += 1
                    continue
                
                # Check if we need to restart the browser
                if shops_in_current_session >= SHOPS_PER_BROWSER_SESSION:
                    print(f"  🔄 Restarting browser after {shops_in_current_session} shops...")
                    if driver:
                        driver.quit()
                        driver = None
                    # Random delay before starting new browser
                    restart_delay = random.uniform(10, 20)
                    print(f"  😴 Waiting {restart_delay:.1f} seconds before starting new browser session...")
                    time.sleep(restart_delay)
                    driver = setup_driver()
                    shops_in_current_session = 0
                    SHOPS_PER_BROWSER_SESSION = random.randint(8, 12)  # Randomize next session length
                    print(f"  ✅ New browser session started (will process {SHOPS_PER_BROWSER_SESSION} shops)")
                
                try:
                    # Use the full domain name for searching (including extension)
                    domain_for_search = shop_domain
                    print(f"  Searching Google for: {domain_for_search}")
                    
                    if driver is None: # If driver was quit due to an error, restart it
                        print("  Restarting WebDriver...")
                        driver = setup_driver()
                        shops_in_current_session = 0
                    
                    driver.get(f"https://www.google.com/search?q={domain_for_search}")
                    
                    # Accept cookies if the dialog appears (common for EU visitors)
                    try:
                        WebDriverWait(driver, 10).until( # Increased from 5 to 10
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alles accepteren') or contains(., 'Accept all')]"))
                        ).click()
                        time.sleep(random.uniform(1.5, 3.0))  # Wait for the cookie dialog to disappear
                    except TimeoutException:
                        # Cookie dialog might not appear if already accepted
                        pass
                    
                    # Wait for search results to load
                    try:
                        WebDriverWait(driver, 15).until( # Increased from 10 to 15
                            EC.presence_of_element_located((By.ID, "search"))
                        )
                        WebDriverWait(driver, 10).until( # Increased from 5 to 10
                            EC.presence_of_element_located((By.CLASS_NAME, "XNo5Ab"))
                        )
                    except TimeoutException:
                        print(f"  Timeout waiting for search results or favicons for {shop_domain}")
                        # Continue anyway, maybe partial results loaded
                    
                    time.sleep(random.uniform(2.5, 5.5)) # Variable delay, increased base
                    
                    # DEBUG: Save HTML to see what Selenium sees (only for first few shops)
                    if shops_processed < 3:
                        # Sanitize filename by removing invalid characters
                        safe_domain = sanitize_filename(shop_domain)
                        debug_html_file = f"debug_{shop_id}_{safe_domain.replace('.', '_')}.html"
                        with open(debug_html_file, 'w', encoding='utf-8') as f:
                            f.write(driver.page_source)
                        print(f"  DEBUG: Saved HTML to {debug_html_file}")
                    
                    # Also print all cite texts found on the page for debugging
                    all_cites = driver.find_elements(By.TAG_NAME, "cite")
                    print(f"\n  DEBUG: Found {len(all_cites)} total cite elements on page")
                    if all_cites and shops_processed < 3:
                        print("  DEBUG: First 5 cite texts:")
                        for j, cite in enumerate(all_cites[:5]):
                            print(f"    {j+1}. '{cite.text}'")
                    
                    # Look for the website in organic search results using multiple approaches
                    favicon_found = False
                    
                    # APPROACH 1: Look for the domain in cite elements and find nearby images
                    try:
                        # First look for results with the domain in the cite element
                        # Use domain name without TLD for more flexible matching (case-insensitive)
                        domain_name_only = shop_domain.split('.')[0]
                        cite_elements = driver.find_elements(By.XPATH, f"//cite[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{domain_name_only.lower()}')]")
                        
                        print(f"  DEBUG: Found {len(cite_elements)} cite elements containing '{domain_name_only}' (searching without TLD)")
                        
                        if cite_elements:
                            for i, cite in enumerate(cite_elements):
                                try:
                                    # First, try to find the parent div that contains both cite and image
                                    parent_div = cite.find_element(By.XPATH, "./ancestor::div[contains(@class, 'yuRUbf') or contains(@class, 'g') or contains(@class, 'MjjYud')]")
                                    
                                    # Find any image within this parent
                                    img_elements = parent_div.find_elements(By.TAG_NAME, "img")
                                    
                                    print(f"    DEBUG: Cite #{i+1} - Found {len(img_elements)} images in parent div")
                                    
                                    if img_elements:
                                        for j, img in enumerate(img_elements):
                                            img_src = img.get_attribute('src')
                                            
                                            if img_src:
                                                # Create filename
                                                filename = f"favicons/{shop_id}_{shop_domain.replace('.', '_')}.png"
                                                
                                                # Try to save as base64 first, then as a regular image
                                                if save_base64_image(img_src, filename):
                                                    print(f"  Successfully saved favicon for {shop_domain}")
                                                    favicon_found = True
                                                    break
                                                elif download_image(img_src, filename):
                                                    print(f"  Successfully downloaded favicon for {shop_domain}")
                                                    favicon_found = True
                                                    break
                                                else:
                                                    print(f"  Could not save favicon for {shop_domain}: {img_src[:50]}...")
                                    
                                    if favicon_found:
                                        break
                                    
                                except NoSuchElementException:
                                    continue
                            
                            if favicon_found:
                                pass  # Allow loop to continue to the next shop
                    
                    except Exception as e:
                        print(f"  Error with approach 1 for {shop_domain}: {e}")
                    
                    # APPROACH 2: Look for specific favicon structure with XNo5Ab class
                    if not favicon_found:
                        try:
                            # Look for the favicon images directly
                            favicon_imgs = driver.find_elements(By.XPATH, "//img[contains(@class, 'XNo5Ab')]")
                            
                            print(f"  DEBUG: Found {len(favicon_imgs)} images with XNo5Ab class")
                            
                            for img_idx, img in enumerate(favicon_imgs):
                                # Find the closest cite element to check if it's for our domain
                                try:
                                    # Find parent element that might contain the cite
                                    parent = img.find_element(By.XPATH, "./ancestor::div[contains(@class, 'g') or contains(@class, 'MjjYud') or contains(@class, 'yuRUbf')]")
                                    
                                    # Find cite elements in this parent
                                    cite_elements = parent.find_elements(By.TAG_NAME, "cite")
                                    
                                    for cite in cite_elements:
                                        cite_text = cite.text.lower()
                                        domain_name_only = shop_domain.split('.')[0].lower()
                                        # Check if domain name (without TLD) is in cite text
                                        if domain_name_only in cite_text:
                                            img_src = img.get_attribute('src')
                                            
                                            if img_src:
                                                # Create filename
                                                filename = f"favicons/{shop_id}_{shop_domain.replace('.', '_')}.png"
                                                
                                                # Try to save as base64 first, then as a regular image
                                                if save_base64_image(img_src, filename):
                                                    print(f"  Successfully saved favicon for {shop_domain}")
                                                    favicon_found = True
                                                    break
                                                elif download_image(img_src, filename):
                                                    print(f"  Successfully downloaded favicon for {shop_domain}")
                                                    favicon_found = True
                                                    break
                                                else:
                                                    print(f"  Could not save favicon for {shop_domain}: {img_src[:50]}...")
                                    
                                    if favicon_found:
                                        pass  # Allow loop to continue to the next shop
                        
                                except NoSuchElementException:
                                    continue
                            
                            if favicon_found:
                                pass  # Allow loop to continue to the next shop
                        
                        except Exception as e:
                            print(f"  Error with approach 2 for {shop_domain}: {e}")
                    
                    # APPROACH 2.5: Look for the specific Google structure with q0vns class
                    if not favicon_found:
                        try:
                            # Look for the parent div with class q0vns that contains both favicon and cite
                            result_divs = driver.find_elements(By.XPATH, "//div[@class='q0vns']")
                            print(f"  DEBUG: Found {len(result_divs)} result divs with q0vns class")
                            
                            for div in result_divs:
                                try:
                                    # Check if this div contains our domain in the cite
                                    cite = div.find_element(By.TAG_NAME, "cite")
                                    cite_text = cite.text.lower()
                                    # More flexible domain matching - handle www. prefix and path suffixes
                                    domain_lower = shop_domain.lower()
                                    domain_without_www = domain_lower.replace('www.', '')
                                    # Also try without TLD for better matching
                                    domain_name_only = domain_lower.split('.')[0]
                                    
                                    # Check various possible matches
                                    matches = [
                                        domain_lower in cite_text,
                                        domain_without_www in cite_text,
                                        f".{domain_lower}" in cite_text,  # with leading dot
                                        f".{domain_without_www}" in cite_text,
                                        domain_name_only in cite_text and '.' in cite_text,  # domain name with any TLD
                                        cite_text.startswith(f"https://{domain_lower}"),
                                        cite_text.startswith(f"https://www.{domain_without_www}"),
                                        cite_text.startswith(f"www.{domain_lower}"),
                                        cite_text.startswith(domain_lower)
                                    ]
                                    
                                    if any(matches):
                                        print(f"    DEBUG: Found matching cite with text: {cite.text}")
                                        
                                        # Look for the favicon image with XNo5Ab class
                                        try:
                                            favicon_img = div.find_element(By.CLASS_NAME, "XNo5Ab")
                                            img_src = favicon_img.get_attribute('src')
                                            print(f"    DEBUG: Found favicon with src length: {len(img_src) if img_src else 0}")
                                            
                                            if img_src:
                                                filename = f"favicons/{shop_id}_{shop_domain.replace('.', '_')}.png"
                                                
                                                if save_base64_image(img_src, filename):
                                                    print(f"  Successfully saved favicon for {shop_domain}")
                                                    favicon_found = True
                                                    break
                                                elif download_image(img_src, filename):
                                                    print(f"  Successfully downloaded favicon for {shop_domain}")
                                                    favicon_found = True
                                                    break
                                        except NoSuchElementException:
                                            print(f"    DEBUG: No XNo5Ab image found in this result div")
                                except NoSuchElementException:
                                    continue
                        except Exception as e:
                            print(f"  DEBUG: Error with approach 2.5: {e}")
                    
                    # APPROACH 2.6: Look for the specific DDKf1c span structure
                    if not favicon_found:
                        try:
                            # Look for spans with DDKf1c class that contain favicon images
                            favicon_spans = driver.find_elements(By.CLASS_NAME, "DDKf1c")
                            print(f"  DEBUG: Found {len(favicon_spans)} DDKf1c spans")
                            
                            domain_name_only = shop_domain.split('.')[0].lower()
                            
                            for span_idx, span in enumerate(favicon_spans):
                                try:
                                    # Find the XNo5Ab image within this span
                                    favicon_img = span.find_element(By.CLASS_NAME, "XNo5Ab")
                                    
                                    # Now find the nearest cite element to verify it's for our domain
                                    # Go up to find a common parent, then look for cite
                                    parent = span
                                    for _ in range(5):  # Try up to 5 levels up
                                        try:
                                            parent = parent.find_element(By.XPATH, "..")
                                            cites = parent.find_elements(By.TAG_NAME, "cite")
                                            if cites:
                                                for cite in cites:
                                                    if domain_name_only in cite.text.lower():
                                                        print(f"    DEBUG: Found matching domain in cite: {cite.text}")
                                                        img_src = favicon_img.get_attribute('src')
                                                        if img_src:
                                                            filename = f"favicons/{shop_id}_{shop_domain.replace('.', '_')}.png"
                                                            if save_base64_image(img_src, filename):
                                                                print(f"  Successfully saved favicon for {shop_domain}")
                                                                favicon_found = True
                                                                break
                                            if favicon_found:
                                                break
                                        except:
                                            continue
                                    if favicon_found:
                                        break
                                except NoSuchElementException:
                                    continue
                        except Exception as e:
                            print(f"  DEBUG: Error with approach 2.6: {e}")
                    
                    # APPROACH 3: Look for any image near the cite with our domain
                    if not favicon_found:
                        try:
                            all_cites = driver.find_elements(By.TAG_NAME, "cite")
                            domain_name_only = shop_domain.split('.')[0].lower()
                            for cite in all_cites:
                                cite_text = cite.text.lower()
                                if domain_name_only in cite_text:
                                    # Get parent node to look for nearby images
                                    try:
                                        parent_node = cite.find_element(By.XPATH, "./..")
                                        img_elements = parent_node.find_elements(By.TAG_NAME, "img")
                                        
                                        if not img_elements:
                                            # Try one level up
                                            parent_node = parent_node.find_element(By.XPATH, "./..")
                                            img_elements = parent_node.find_elements(By.TAG_NAME, "img")
                                        
                                        for img in img_elements:
                                            img_src = img.get_attribute('src')
                                            
                                            if img_src:
                                                # Create filename
                                                filename = f"favicons/{shop_id}_{shop_domain.replace('.', '_')}.png"
                                                
                                                # Try to save as base64 first, then as a regular image
                                                if save_base64_image(img_src, filename):
                                                    print(f"  Successfully saved favicon for {shop_domain}")
                                                    favicon_found = True
                                                    break
                                                elif download_image(img_src, filename):
                                                    print(f"  Successfully downloaded favicon for {shop_domain}")
                                                    favicon_found = True
                                                    break
                                                else:
                                                    print(f"  Could not save favicon for {shop_domain}: {img_src[:50]}...")
                                        
                                        if favicon_found:
                                            break
                                        
                                    except Exception:
                                        continue
                        
                        except Exception as e:
                            print(f"  Error with approach 3 for {shop_domain}: {e}")
                    
                    # Track success and increment processed count
                    if favicon_found:
                        shops_successful += 1
                    else:
                        print(f"  Could not find favicon for {shop_domain}")
                    
                    shops_processed += 1
                    shops_in_current_session += 1  # Increment session counter
                    
                    # Increased and randomized delay between requests
                    delay = random.uniform(7, 15) # Random delay between 7 and 15 seconds
                    print(f"  😴 Sleeping for {delay:.1f} seconds...")
                    time.sleep(delay)
                
                except WebDriverException as wde:
                    print(f"  ❌ WebDriverException for {shop_domain}: {wde}")
                    print("  Attempting to quit current WebDriver and restart for the next shop.")
                    if driver:
                        driver.quit()
                        driver = None # Signal to restart driver in the next iteration
                    favicon_found = False # Ensure it counts as a failure
                
                except Exception as e:
                    print(f"  💥 Unexpected error for {shop_domain}: {e}")
                    # Potentially quit and restart driver here too if it seems to cause persistent issues
                    favicon_found = False # Ensure it counts as a failure

                # Track success and increment processed count
                if favicon_found:
                    shops_successful += 1
                else:
                    print(f"  Could not find favicon for {shop_domain}")
                
                shops_processed += 1
                
                # Increased and randomized delay between requests
                delay = random.uniform(7, 15) # Random delay between 7 and 15 seconds
                print(f"  😴 Sleeping for {delay:.1f} seconds...")
                time.sleep(delay)
            
            print(f"\nCompleted processing!")
            total_processed = shops_processed + shops_skipped
            print(f"  Total processed: {total_processed}")
            print(f"  Successful downloads: {shops_successful}")
            print(f"  Skipped (already exist): {shops_skipped}")
            print(f"  Failed: {shops_processed - shops_successful}")
            print(f"  Success rate: {(shops_successful/total_processed*100) if total_processed > 0 else 0:.1f}%")
            
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        if driver: # Ensure driver is quit if it exists
            driver.quit()
        generate_favicon_gallery()

if __name__ == "__main__":
    import sys
    
    # Default values
    csv_file = 'remaining_shops.csv'
    start_index = 0
    max_to_process = None
    
    # Parse command line arguments if provided
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    if len(sys.argv) > 2:
        start_index = int(sys.argv[2])
    if len(sys.argv) > 3:
        max_to_process = int(sys.argv[3])
    
    print(f"Starting scraper with CSV: {csv_file}, Starting at index: {start_index}" + 
          (f", Processing up to {max_to_process} shops" if max_to_process else ""))
    
    search_and_download_favicons(csv_file, start_index, max_to_process)