import os
import shutil
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import pandas as pd
import math

app = Flask(__name__)

# Configuration
FAVICONS_PER_PAGE = 200
FAVICON_DIR = 'favicons'
NOT_CORRECT_DIR = os.path.join(FAVICON_DIR, 'not_correct')

# Ensure directories exist
os.makedirs(NOT_CORRECT_DIR, exist_ok=True)

def load_shop_data():
    """Load shop data from CSV file"""
    try:
        df = pd.read_csv('remaining_shops2_clean.csv', sep=';')
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

def get_favicon_path(shop_id, shop_name):
    """Generate favicon filename based on shop ID and name"""
    # Clean the shop name to match the file naming pattern
    clean_shop_name = shop_name.replace('.', '_')
    filename = f"{shop_id}_{clean_shop_name}.png"
    return filename

def favicon_exists(shop_id, shop_name):
    """Check if favicon file exists"""
    filename = get_favicon_path(shop_id, shop_name)
    filepath = os.path.join(FAVICON_DIR, filename)
    return os.path.exists(filepath)

@app.route('/')
def index():
    """Display paginated favicon gallery"""
    page = request.args.get('page', 1, type=int)
    
    # Load shop data
    df = load_shop_data()
    
    # Filter only shops with existing favicons
    shops_with_favicons = []
    for _, row in df.iterrows():
        if favicon_exists(row['Shop ID'], row['Shop']):
            shops_with_favicons.append({
                'id': row['Shop ID'],
                'name': row['Shop'],
                'filename': get_favicon_path(row['Shop ID'], row['Shop'])
            })
    
    # Calculate pagination
    total_shops = len(shops_with_favicons)
    total_pages = math.ceil(total_shops / FAVICONS_PER_PAGE)
    start_idx = (page - 1) * FAVICONS_PER_PAGE
    end_idx = start_idx + FAVICONS_PER_PAGE
    
    # Get shops for current page
    current_shops = shops_with_favicons[start_idx:end_idx]
    
    return render_template('gallery.html', 
                         shops=current_shops,
                         page=page,
                         total_pages=total_pages,
                         total_shops=total_shops)

@app.route('/favicon/<filename>')
def serve_favicon(filename):
    """Serve favicon images"""
    return send_from_directory(FAVICON_DIR, filename)

@app.route('/move_favicon', methods=['POST'])
def move_favicon():
    """Move favicon to not_correct folder"""
    data = request.get_json()
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'success': False, 'error': 'No filename provided'})
    
    source_path = os.path.join(FAVICON_DIR, filename)
    dest_path = os.path.join(NOT_CORRECT_DIR, filename)
    
    try:
        if os.path.exists(source_path):
            shutil.move(source_path, dest_path)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'File not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/undo_move', methods=['POST'])
def undo_move():
    """Move favicon back from not_correct folder"""
    data = request.get_json()
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'success': False, 'error': 'No filename provided'})
    
    source_path = os.path.join(NOT_CORRECT_DIR, filename)
    dest_path = os.path.join(FAVICON_DIR, filename)
    
    try:
        if os.path.exists(source_path):
            shutil.move(source_path, dest_path)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'File not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 