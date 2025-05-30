#!/usr/bin/env python3
"""
Identify shops that failed to get favicons
Creates a new CSV file with only the shops that don't have favicons yet
"""

import csv
import os

def get_existing_favicon_shop_ids():
    """Get all shop IDs that have favicons"""
    shop_ids = set()
    
    if not os.path.exists('favicons'):
        return shop_ids
    
    favicon_files = [f for f in os.listdir('favicons') if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    for favicon_file in favicon_files:
        # Extract shop ID from filename (format: ShopID_domain_name.extension)
        parts = favicon_file.split('_', 1)
        if len(parts) >= 1:
            shop_id = parts[0]
            shop_ids.add(shop_id)
    
    return shop_ids

def create_failed_shops_csv(input_csv='remaining_shops2_fresh.csv', output_csv='failed_shops.csv'):
    """Create a CSV with shops that don't have favicons"""
    
    existing_shop_ids = get_existing_favicon_shop_ids()
    print(f"Found {len(existing_shop_ids)} shops with favicons")
    
    failed_shops = []
    total_shops = 0
    
    # Read the input CSV and identify shops without favicons
    with open(input_csv, 'r', encoding='utf-8') as infile:
        csv_reader = csv.reader(infile, delimiter=';')
        headers = next(csv_reader)  # Read headers
        
        for row in csv_reader:
            total_shops += 1
            shop_id = row[0]
            shop_domain = row[1] if len(row) > 1 else ""
            
            if shop_id not in existing_shop_ids:
                failed_shops.append(row)
    
    # Write failed shops to new CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile, delimiter=';')
        csv_writer.writerow(headers)  # Write headers
        csv_writer.writerows(failed_shops)
    
    print(f"\nResults:")
    print(f"  Total shops in {input_csv}: {total_shops}")
    print(f"  Shops with favicons: {len(existing_shop_ids)}")
    print(f"  Failed shops: {len(failed_shops)}")
    print(f"  Created {output_csv} with {len(failed_shops)} shops to retry")
    
    # Display first 10 failed shops as examples
    if failed_shops:
        print(f"\nFirst 10 failed shops:")
        for i, shop in enumerate(failed_shops[:10]):
            print(f"  {i+1}. {shop[0]}: {shop[1] if len(shop) > 1 else 'N/A'}")
    
    return failed_shops

if __name__ == "__main__":
    import sys
    
    input_csv = 'remaining_shops2_fresh.csv'
    output_csv = 'failed_shops.csv'
    
    if len(sys.argv) > 1:
        input_csv = sys.argv[1]
    if len(sys.argv) > 2:
        output_csv = sys.argv[2]
    
    create_failed_shops_csv(input_csv, output_csv) 