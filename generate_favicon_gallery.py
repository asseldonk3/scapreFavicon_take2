import os
import re
import base64

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
        .favicon-container {
            width: 32px;
            height: 32px;
            margin-right: 15px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .favicon-image {
            max-width: 32px;
            max-height: 32px;
            /* Google's style for favicons */
            border-radius: 50%; /* Full circle like Google search results */
            object-fit: contain;
            background-color: transparent;
        }
        /* For square logos that shouldn't be fully circular */
        .favicon-square {
            border-radius: 16px; /* Rounded square for some icons */
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
        /* Additional styles to match Google's presentation */
        .google-style {
            margin-top: 20px;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            max-width: 600px;
            margin: 20px auto;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
        .google-result {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            padding: 5px;
        }
        .google-site-info {
            margin-left: 12px;
        }
        .google-site-name {
            font-weight: 500;
            color: #202124;
            font-size: 14px;
            margin-bottom: 2px;
        }
        .google-site-url {
            color: #5f6368;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <h1>Shop Favicons Gallery</h1>
    
    <!-- Example of Google's styling -->
    <div class="google-style">
        <h3>Google Search Style Examples:</h3>
        <div class="google-result">
            <div class="favicon-container">
                <img class="favicon-image" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAM1BMVEX////eAADeAADeAADeAADeAADeAADeAADeAADgAADeAADeAADeAADeAADeAADeAADrwhmPAAAAEHRSTlMAKJ7E7f8QHHljjk/aOrMjb7TUAAAAbklEQVR42u3OyQ3AIAxEUdMQ9r3/aukkJM5GKVI0/wq+HiMTg0wy9aSVyJZIVlNxKJMlC6xEtmTtBFSwWTMVbB7ZH0dKUNCDBQsW3ERB/w7sCQoG31FQwHUPTCcoKOjQgR8UFFzDzoIEBV/74QbVjwVeHpmlPAAAAABJRU5ErkJggg==" alt="MediaMarkt">
            </div>
            <div class="google-site-info">
                <div class="google-site-name">MediaMarkt</div>
                <div class="google-site-url">https://www.mediamarkt.nl</div>
            </div>
        </div>
        <div class="google-result">
            <div class="favicon-container">
                <img class="favicon-image" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAM1BMVEUAAAAjQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ71G0DnxAAAAEHRSTlMAEAg4YO/fQM9/IG+/72+vSECLZQAAANJJREFUeF6Fk1cSBCEMQxF19sA6979sJVi9lmf5U0SgLikFr4E7nGT8CcnRBEDgbZYAgvRrwWmAVbwu2IPcPkBhS2KQDtOBG4fNA0rtM5T2HoZyeQJlGV0AykdKQMoBLiB1nUfpAy/gAlxrAPF0pAHE8gSB+8YR8JgORBuYm8AbIPOd4wBkeTQMVGXwjcBGjwnQPf8B2DbQDNvCACm6hhtiXEIBGLvd9dT2n6WRzD0xwTU5vp5lD38W2Vvd6+56f3/Gux/1rvA7DnlP4sF/+gFZlQSF8ATIngAAAABJRU5ErkJggg==" alt="bol.com">
            </div>
            <div class="google-site-info">
                <div class="google-site-name">bol.com</div>
                <div class="google-site-url">https://www.bol.com</div>
            </div>
        </div>
        <div class="google-result">
            <div class="favicon-container">
                <img class="favicon-image" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAM1BMVEX///+kJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiYm3GgsAAAAEHRSTlMAECDfv2+Pv2BQQDDvcK+fz8/obQAAALlJREFUeF6lk1kOxCAMBOm0E8js5f+vHYcDFChPVeIgQc1IJL1p2+xLNrPcZYk2xMTlIyaSdKbKbmUiDRnZz0JXfNE9xKSLzaOJCVBMZmJnAuqWHYBQk5xYtwhALkh6EHOJ84IXr6Sj4LwgrGhsb9BXDfTNDcbmBnYgN0RwHo01hOAII2CcsXp9YG7Qr3uwz8DNuYM3hwbK9gB47dThy1kBINvDcGl7Cv+zzsfxzPvx5vwe9AY+V/8oaW4/UL4AAAAASUVORK5CYII=" alt="Wehkamp">
            </div>
            <div class="google-site-info">
                <div class="google-site-name">Wehkamp</div>
                <div class="google-site-url">https://www.wehkamp.nl</div>
            </div>
        </div>
    </div>
    
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
            <div class="favicon-container">
                <img class="favicon-image" src="./favicons/{favicon_file}" alt="Favicon for {domain}">
            </div>
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
    
    # Also create the standalone version
    create_standalone_html(favicon_files)

def create_standalone_html(favicon_files):
    """Create a standalone HTML file with all images embedded as base64."""
    favicon_dir = "favicons"
    
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
        .favicon-container {
            width: 32px;
            height: 32px;
            margin-right: 15px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .favicon-image {
            max-width: 32px;
            max-height: 32px;
            /* Google's style for favicons */
            border-radius: 50%; /* Full circle like Google search results */
            object-fit: contain;
            background-color: transparent;
        }
        /* For square logos that shouldn't be fully circular */
        .favicon-square {
            border-radius: 16px; /* Rounded square for some icons */
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
        /* Additional styles to match Google's presentation */
        .google-style {
            margin-top: 20px;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            max-width: 600px;
            margin: 20px auto;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
        .google-result {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            padding: 5px;
        }
        .google-site-info {
            margin-left: 12px;
        }
        .google-site-name {
            font-weight: 500;
            color: #202124;
            font-size: 14px;
            margin-bottom: 2px;
        }
        .google-site-url {
            color: #5f6368;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <h1>Shop Favicons Gallery (Standalone Version)</h1>
    <p style="text-align: center; margin-bottom: 30px;">This version has all images embedded and can be moved anywhere.</p>
    
    <!-- Example of Google's styling -->
    <div class="google-style">
        <h3>Google Search Style Examples:</h3>
        <div class="google-result">
            <div class="favicon-container">
                <img class="favicon-image" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAM1BMVEX////eAADeAADeAADeAADeAADeAADeAADeAADgAADeAADeAADeAADeAADeAADeAADrwhmPAAAAEHRSTlMAKJ7E7f8QHHljjk/aOrMjb7TUAAAAbklEQVR42u3OyQ3AIAxEUdMQ9r3/aukkJM5GKVI0/wq+HiMTg0wy9aSVyJZIVlNxKJMlC6xEtmTtBFSwWTMVbB7ZH0dKUNCDBQsW3ERB/w7sCQoG31FQwHUPTCcoKOjQgR8UFFzDzoIEBV/74QbVjwVeHpmlPAAAAABJRU5ErkJggg==" alt="MediaMarkt">
            </div>
            <div class="google-site-info">
                <div class="google-site-name">MediaMarkt</div>
                <div class="google-site-url">https://www.mediamarkt.nl</div>
            </div>
        </div>
        <div class="google-result">
            <div class="favicon-container">
                <img class="favicon-image" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAM1BMVEUAAAAjQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ70jQ71G0DnxAAAAEHRSTlMAEAg4YO/fQM9/IG+/72+vSECLZQAAANJJREFUeF6Fk1cSBCEMQxF19sA6979sJVi9lmf5U0SgLikFr4E7nGT8CcnRBEDgbZYAgvRrwWmAVbwu2IPcPkBhS2KQDtOBG4fNA0rtM5T2HoZyeQJlGV0AykdKQMoBLiB1nUfpAy/gAlxrAPF0pAHE8gSB+8YR8JgORBuYm8AbIPOd4wBkeTQMVGXwjcBGjwnQPf8B2DbQDNvCACm6hhtiXEIBGLvd9dT2n6WRzD0xwTU5vp5lD38W2Vvd6+56f3/Gux/1rvA7DnlP4sF/+gFZlQSF8ATIngAAAABJRU5ErkJggg==" alt="bol.com">
            </div>
            <div class="google-site-info">
                <div class="google-site-name">bol.com</div>
                <div class="google-site-url">https://www.bol.com</div>
            </div>
        </div>
        <div class="google-result">
            <div class="favicon-container">
                <img class="favicon-image" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAM1BMVEX///+kJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiakJiYm3GgsAAAAEHRSTlMAECDfv2+Pv2BQQDDvcK+fz8/obQAAALlJREFUeF6lk1kOxCAMBOm0E8js5f+vHYcDFChPVeIgQc1IJL1p2+xLNrPcZYk2xMTlIyaSdKbKbmUiDRnZz0JXfNE9xKSLzaOJCVBMZmJnAuqWHYBQk5xYtwhALkh6EHOJ84IXr6Sj4LwgrGhsb9BXDfTNDcbmBnYgN0RwHo01hOAII2CcsXp9YG7Qr3uwz8DNuYM3hwbK9gB47dThy1kBINvDcGl7Cv+zzsfxzPvx5vwe9AY+V/8oaW4/UL4AAAAASUVORK5CYII=" alt="Wehkamp">
            </div>
            <div class="google-site-info">
                <div class="google-site-name">Wehkamp</div>
                <div class="google-site-url">https://www.wehkamp.nl</div>
            </div>
        </div>
    </div>
    
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
    embedded_count = 0
    for favicon_file in favicon_files:
        shop_id, domain = extract_info(favicon_file)
        
        # Get the base64 data for the image
        file_path = os.path.join(favicon_dir, favicon_file)
        if os.path.exists(file_path):
            try:
                base64_image = image_to_base64(file_path)
                embedded_count += 1
                
                html += f"""
        <div class="favicon-item">
            <div class="favicon-container">
                <img class="favicon-image" src="{base64_image}" alt="Favicon for {domain}">
            </div>
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
    
    print(f"Generated index_standalone.html with {embedded_count} embedded images - can be moved anywhere")

if __name__ == "__main__":
    generate_favicon_gallery()
