import csv
import os

def scan_existing_favicons():
    """Scan existing favicons and return a set of shop IDs that already have favicons"""
    existing_shop_ids = set()
    
    if not os.path.exists('favicons'):
        print("No favicons directory found")
        return existing_shop_ids
    
    favicon_files = [f for f in os.listdir('favicons') if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    print(f"Found {len(favicon_files)} favicon files:")
    
    for favicon_file in favicon_files:
        # Extract shop ID from filename (format: ShopID_domain_name.extension)
        parts = favicon_file.split('_', 1)
        if len(parts) >= 1:
            shop_id = parts[0]
            existing_shop_ids.add(shop_id)
            print(f"  {favicon_file} -> Shop ID: {shop_id}")
    
    print(f"\nTotal unique shop IDs with favicons: {len(existing_shop_ids)}")
    return existing_shop_ids

def create_remaining_shops_csv(input_csv='urls.csv', output_csv='remaining_shops.csv'):
    """Create a new CSV file with only shops that don't have favicons yet"""
    
    # Get existing shop IDs
    existing_shop_ids = scan_existing_favicons()
    
    # Read the original CSV and filter out existing shops
    remaining_shops = []
    total_shops = 0
    skipped_shops = 0
    
    try:
        with open(input_csv, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            headers = next(csv_reader)  # Read header row
            
            print(f"\nProcessing {input_csv}...")
            print(f"Headers: {headers}")
            
            for row in csv_reader:
                total_shops += 1
                shop_id = row[0]
                shop_domain = row[1]
                
                if shop_id in existing_shop_ids:
                    print(f"  Skipping {shop_id}: {shop_domain} (favicon exists)")
                    skipped_shops += 1
                else:
                    remaining_shops.append(row)
        
        # Write the remaining shops to new CSV
        with open(output_csv, 'w', newline='', encoding='utf-8') as output_file:
            csv_writer = csv.writer(output_file, delimiter=';')
            csv_writer.writerow(headers)  # Write header
            csv_writer.writerows(remaining_shops)
        
        print(f"\n=== SUMMARY ===")
        print(f"Total shops in {input_csv}: {total_shops}")
        print(f"Shops with existing favicons: {skipped_shops}")
        print(f"Remaining shops to process: {len(remaining_shops)}")
        print(f"Created {output_csv} with {len(remaining_shops)} shops")
        print(f"Reduction: {(skipped_shops/total_shops*100) if total_shops > 0 else 0:.1f}%")
        
        return len(remaining_shops)
        
    except FileNotFoundError:
        print(f"Error: {input_csv} not found")
        return 0
    except Exception as e:
        print(f"Error processing CSV: {e}")
        return 0

def show_favicon_stats():
    """Show detailed statistics about existing favicons"""
    if not os.path.exists('favicons'):
        print("No favicons directory found")
        return
    
    favicon_files = [f for f in os.listdir('favicons') if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    print(f"\n=== FAVICON STATISTICS ===")
    print(f"Total favicon files: {len(favicon_files)}")
    
    # Count by file type
    extensions = {}
    for favicon_file in favicon_files:
        ext = os.path.splitext(favicon_file)[1].lower()
        extensions[ext] = extensions.get(ext, 0) + 1
    
    print("File types:")
    for ext, count in extensions.items():
        print(f"  {ext}: {count}")
    
    # Show some examples
    print(f"\nFirst 10 favicon files:")
    for favicon_file in sorted(favicon_files)[:10]:
        parts = favicon_file.split('_', 1)
        shop_id = parts[0] if len(parts) >= 1 else "Unknown"
        domain = parts[1].replace('_', '.').rsplit('.', 1)[0] if len(parts) >= 2 else "Unknown"
        print(f"  {favicon_file} -> ID: {shop_id}, Domain: {domain}")
    
    if len(favicon_files) > 10:
        print(f"  ... and {len(favicon_files) - 10} more")

if __name__ == "__main__":
    print("=== Favicon Cleanup Tool ===")
    print("This tool will scan existing favicons and create a clean list of remaining shops to process.\n")
    
    # Show current favicon statistics
    show_favicon_stats()
    
    # Create the remaining shops CSV
    remaining_count = create_remaining_shops_csv()
    
    if remaining_count > 0:
        print(f"\n✅ Success! You can now run:")
        print(f"python google_favicon_scraper.py remaining_shops.csv 0 10")
        print(f"This will process only the {remaining_count} shops that don't have favicons yet.")
    else:
        print(f"\n❌ No remaining shops to process or error occurred.") 