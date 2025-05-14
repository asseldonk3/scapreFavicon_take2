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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re

# Create directory for storing images if it doesn't exist
os.makedirs('favicons', exist_ok=True)

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
    # Add anti-detection measures
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    # Add user agent (common Dutch user agent)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # Add language preference for Dutch
    chrome_options.add_argument("--lang=nl-NL")
    
    # Create a new WebDriver instance
    driver = webdriver.Chrome(options=chrome_options)
    
    # Execute JavaScript to prevent detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
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

# Main function to search Google and download favicons
def search_and_download_favicons(csv_path):
    driver = setup_driver()
    
    try:
        # Read the CSV file
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader)  # Skip header row
            
            for row in csv_reader:
                shop_id = row[0]
                shop_domain = row[1]
                
                print(f"Processing {shop_id}: {shop_domain}")
                
                # Create a clean domain name for searching
                domain_for_search = shop_domain.split('.')[0]  # Remove .com, .nl etc.
                
                # Open Google search
                driver.get(f"https://www.google.com/search?q={domain_for_search}")
                
                # Accept cookies if the dialog appears (common for EU visitors)
                try:
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alles accepteren') or contains(., 'Accept all')]"))
                    ).click()
                    time.sleep(1)  # Wait for the cookie dialog to disappear
                except TimeoutException:
                    # Cookie dialog might not appear if already accepted
                    pass
                
                # Wait for search results to load
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "search"))
                    )
                except TimeoutException:
                    print(f"  Timeout waiting for search results for {shop_domain}")
                    continue
                
                # Add a short delay to avoid detection
                time.sleep(2 + (len(shop_domain) % 3))  # Variable delay
                
                # Look for the website in organic search results using multiple approaches
                favicon_found = False
                
                # APPROACH 1: Look for the domain in cite elements and find nearby images
                try:
                    # First look for results with the domain in the cite element
                    cite_elements = driver.find_elements(By.XPATH, f"//cite[contains(text(), '{shop_domain}')]")
                    
                    if cite_elements:
                        for cite in cite_elements:
                            try:
                                # First, try to find the parent div that contains both cite and image
                                parent_div = cite.find_element(By.XPATH, "./ancestor::div[contains(@class, 'yuRUbf') or contains(@class, 'g') or contains(@class, 'MjjYud')]")
                                
                                # Find any image within this parent
                                img_elements = parent_div.find_elements(By.TAG_NAME, "img")
                                
                                if img_elements:
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
                                    
                            except NoSuchElementException:
                                continue
                        
                        if favicon_found:
                            continue  # Move to next domain if favicon was found
                
                except Exception as e:
                    print(f"  Error with approach 1 for {shop_domain}: {e}")
                
                # APPROACH 2: Look for specific favicon structure with XNo5Ab class
                if not favicon_found:
                    try:
                        # Look for the favicon images directly
                        favicon_imgs = driver.find_elements(By.XPATH, "//img[contains(@class, 'XNo5Ab')]")
                        
                        for img in favicon_imgs:
                            # Find the closest cite element to check if it's for our domain
                            try:
                                # Find parent element that might contain the cite
                                parent = img.find_element(By.XPATH, "./ancestor::div[contains(@class, 'g') or contains(@class, 'MjjYud') or contains(@class, 'yuRUbf')]")
                                
                                # Find cite elements in this parent
                                cite_elements = parent.find_elements(By.TAG_NAME, "cite")
                                
                                for cite in cite_elements:
                                    cite_text = cite.text.lower()
                                    if shop_domain.lower() in cite_text:
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
                            continue  # Move to next domain if favicon was found
                    
                    except Exception as e:
                        print(f"  Error with approach 2 for {shop_domain}: {e}")
                
                # APPROACH 3: Look for any image near the cite with our domain
                if not favicon_found:
                    try:
                        all_cites = driver.find_elements(By.TAG_NAME, "cite")
                        for cite in all_cites:
                            cite_text = cite.text.lower()
                            if shop_domain.lower() in cite_text:
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
                
                # If no favicon found after all attempts
                if not favicon_found:
                    print(f"  Could not find favicon for {shop_domain}")
                
                # Add random delay between requests to avoid detection
                time.sleep(3 + (len(shop_domain) % 5))
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the browser
        driver.quit()
        
        # Generate the HTML gallery
        generate_favicon_gallery()

if __name__ == "__main__":
    search_and_download_favicons('urls.csv')