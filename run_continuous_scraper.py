#!/usr/bin/env python3
"""
Continuous Favicon Scraper
This script runs the favicon scraper continuously until all shops are processed.
"""

import subprocess
import time
import os

def count_favicons():
    """Count the current number of favicon files"""
    if not os.path.exists('favicons'):
        return 0
    
    favicon_files = [f for f in os.listdir('favicons') if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return len(favicon_files)

def count_remaining_shops(csv_file):
    """Count the number of shops in the CSV file"""
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return len(lines) - 1  # Subtract 1 for header
    except FileNotFoundError:
        return 0

def run_continuous_scraper(csv_file='remaining_shops2_fresh.csv', max_iterations=100):
    """Run the favicon scraper continuously until all shops are processed"""
    
    print(f"🚀 Starting continuous favicon scraper...")
    print(f"📁 Processing file: {csv_file}")
    
    initial_favicon_count = count_favicons()
    total_shops = count_remaining_shops(csv_file)
    
    print(f"📊 Initial state:")
    print(f"   - Existing favicons: {initial_favicon_count}")
    print(f"   - Shops to process: {total_shops}")
    print(f"   - Max iterations: {max_iterations}")
    print()
    
    iteration = 0
    start_index = 0
    
    while iteration < max_iterations:
        iteration += 1
        current_favicon_count = count_favicons()
        
        print(f"🔄 Iteration {iteration}/{max_iterations}")
        print(f"   Current favicons: {current_favicon_count}")
        print(f"   Starting from index: {start_index}")
        
        # Run the scraper for a batch of shops
        batch_size = 50  # Process 50 shops per batch
        cmd = [
            'python', 
            'google_favicon_scraper.py', 
            csv_file, 
            str(start_index), 
            str(batch_size)
        ]
        
        try:
            print(f"   Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)  # 10 minute timeout
            
            if result.returncode == 0:
                print(f"   ✅ Batch completed successfully")
                
                # Check if we downloaded any new favicons
                new_favicon_count = count_favicons()
                new_favicons = new_favicon_count - current_favicon_count
                
                if new_favicons > 0:
                    print(f"   📥 Downloaded {new_favicons} new favicons")
                else:
                    print(f"   ⏭️  No new favicons (likely all shops in batch already processed)")
                
                # Move to next batch
                start_index += batch_size
                
                # Check if we've processed all shops
                if start_index >= total_shops:
                    print(f"🎉 All shops processed! Final favicon count: {new_favicon_count}")
                    break
                    
            else:
                print(f"   ❌ Batch failed with return code: {result.returncode}")
                print(f"   Error output: {result.stderr}")
                
                # Try to continue with next batch anyway
                start_index += batch_size
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Batch timed out after 10 minutes")
            start_index += batch_size
            
        except Exception as e:
            print(f"   💥 Unexpected error: {e}")
            start_index += batch_size
        
        # Add a delay between batches to avoid overwhelming Google
        print(f"   😴 Waiting 30 seconds before next batch...")
        time.sleep(30)
        print()
    
    final_favicon_count = count_favicons()
    total_downloaded = final_favicon_count - initial_favicon_count
    
    print(f"🏁 Scraping session completed!")
    print(f"   Total iterations: {iteration}")
    print(f"   Initial favicons: {initial_favicon_count}")
    print(f"   Final favicons: {final_favicon_count}")
    print(f"   New favicons downloaded: {total_downloaded}")
    
    if iteration >= max_iterations:
        print(f"   ⚠️  Stopped due to max iterations limit")
    
    return total_downloaded

if __name__ == "__main__":
    import sys
    
    csv_file = 'remaining_shops2_fresh.csv'
    max_iterations = 100
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    if len(sys.argv) > 2:
        max_iterations = int(sys.argv[2])
    
    run_continuous_scraper(csv_file, max_iterations) 