import os
import csv
import re

def extract_shop_ids_from_favicons():
    """
    Extract shop IDs and shop names from favicon filenames in the favicons directory.
    Filenames follow the pattern: {shopid}_{shopname}.png
    """
    favicon_dir = "favicons"
    shop_data = []
    
    # Check if favicon directory exists
    if not os.path.exists(favicon_dir):
        print(f"Error: {favicon_dir} directory not found")
        return
    
    # Get all PNG files in the favicon directory
    png_files = [f for f in os.listdir(favicon_dir) if f.endswith('.png')]
    
    print(f"Found {len(png_files)} PNG files in {favicon_dir} directory")
    
    # Extract shop IDs and shop names from filenames
    for filename in png_files:
        # Use regex to extract the shop ID and shop name
        # Pattern: {shopid}_{shopname}.png
        match = re.match(r'^(\d+)_(.+)\.png$', filename)
        if match:
            shop_id = match.group(1)
            shop_name = match.group(2)  # Keep the full name including extensions
            shop_data.append((shop_id, shop_name))
        else:
            print(f"Warning: Could not extract shop ID and name from filename: {filename}")
    
    # Sort by shop ID numerically
    shop_data.sort(key=lambda x: int(x[0]))
    
    # Write to CSV file
    csv_filename = "shop_ids.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['shop_id', 'shop_name'])  # Headers
        for shop_id, shop_name in shop_data:
            writer.writerow([shop_id, shop_name])
    
    print(f"Successfully extracted {len(shop_data)} shop records")
    print(f"CSV file created: {csv_filename}")
    if shop_data:
        print(f"Shop ID range: {min(shop_data, key=lambda x: int(x[0]))[0]} to {max(shop_data, key=lambda x: int(x[0]))[0]}")
        print(f"Sample entries:")
        for i, (shop_id, shop_name) in enumerate(shop_data[:5]):
            print(f"  {shop_id}: {shop_name}")

if __name__ == "__main__":
    extract_shop_ids_from_favicons() 