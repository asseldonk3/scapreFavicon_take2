#!/usr/bin/env python3
"""
Cleanup script to prepare the project for future use.
Removes temporary files while preserving core functionality.
"""

import os
import shutil
import glob

def cleanup_project():
    """Remove temporary files and prepare project for next use"""
    
    print("🧹 Starting project cleanup...")
    
    # Files to remove
    files_to_remove = [
        # Temporary HTML files
        'index.html',
        'index_standalone.html',
        'index_standalone2.html',
        
        # CSV files (except sample)
        'failed_shops.csv',
        'failed_shops_remaining.csv',
        'final_failed_shops.csv',
        'remaining_shops.csv',
        'remaining_shops2.csv',
        'remaining_shops2_clean.csv',
        'remaining_shops2_final.csv',
        'remaining_shops2_fresh.csv',
        'shop_ids.csv',
        
        # Log files
        'scraper_log.txt',
        
        # Debug HTML files
        'debug_*.html'
    ]
    
    # Directories to remove
    dirs_to_remove = [
        'google_search_html',
        '__pycache__'
    ]
    
    # Remove files
    for file_pattern in files_to_remove:
        for file_path in glob.glob(file_pattern):
            try:
                os.remove(file_path)
                print(f"  ✅ Removed: {file_path}")
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"  ❌ Error removing {file_path}: {e}")
    
    # Remove directories
    for dir_name in dirs_to_remove:
        try:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"  ✅ Removed directory: {dir_name}")
        except Exception as e:
            print(f"  ❌ Error removing {dir_name}: {e}")
    
    # Create sample CSV if urls.csv doesn't exist
    if not os.path.exists('urls_sample.csv'):
        with open('urls_sample.csv', 'w', encoding='utf-8') as f:
            f.write("Shop ID;Shop\n")
            f.write("1;bol.com\n")
            f.write("512098;amazon.nl\n")
            f.write("123456;coolblue.nl\n")
        print("  ✅ Created urls_sample.csv")
    
    # Keep urls.csv if it exists, otherwise rename sample
    if not os.path.exists('urls.csv') and os.path.exists('urls_sample.csv'):
        shutil.copy('urls_sample.csv', 'urls.csv')
        print("  ✅ Created urls.csv from sample")
    
    print("\n📁 Project structure after cleanup:")
    print("  - Core scripts: ✅")
    print("  - Flask app: ✅ (recommended for reviewing)")
    print("  - Templates: ✅")
    print("  - Favicons: ✅ (preserved)")
    print("  - Sample CSV: ✅")
    print("\n💡 Note: generate_favicon_gallery.py creates static HTML galleries")
    print("   Use Flask app (python app.py) for interactive review instead")
    print("\n✨ Cleanup complete! Project is ready for next use.")
    print("📖 See README.md for usage instructions.")

if __name__ == "__main__":
    cleanup_project() 