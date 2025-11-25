import os
import requests
from bs4 import BeautifulSoup
import time

equipment = [
    {"id": "26VNA1", "url": "https://www.carrier.com/residential/en/us/products/air-conditioners/26vna1/"},
    {"id": "26TPA8", "url": "https://www.carrier.com/residential/en/us/products/air-conditioners/26tpa8/"},
    {"id": "26SPA6", "url": "https://www.carrier.com/residential/en/us/products/air-conditioners/26spa6/"},
    {"id": "26SCA4", "url": "https://www.carrier.com/residential/en/us/products/air-conditioners/26sca4/"},
    {"id": "26SCA5", "url": "https://www.carrier.com/residential/en/us/products/air-conditioners/26sca5/"},
    {"id": "59MN7", "url": "https://www.carrier.com/residential/en/us/products/furnaces/59mn7/"},
    {"id": "59TN6", "url": "https://www.carrier.com/residential/en/us/products/furnaces/59tn6/"},
    {"id": "59TP6", "url": "https://www.carrier.com/residential/en/us/products/furnaces/59tp6/"},
    {"id": "58TP0", "url": "https://www.carrier.com/residential/en/us/products/furnaces/58tp0/"},
    {"id": "58DLA", "url": "https://www.carrier.com/residential/en/us/products/furnaces/58dla/"},
    {"id": "27VNA3", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27vna3/"},
    {"id": "27VNA1", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27vna1/"},
    {"id": "27TPA8", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27tpa8/"},
    {"id": "27SPA6", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27spa6/"},
    {"id": "27SCA5", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27sca5/"},
    {"id": "27VNA0", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27vna0/"},
    {"id": "FE5B", "url": "https://www.carrier.com/residential/en/us/products/fan-coils/fe5b/"},
    {"id": "FT5", "url": "https://www.carrier.com/residential/en/us/products/fan-coils/ft5/"},
    {"id": "FJ5", "url": "https://www.carrier.com/residential/en/us/products/fan-coils/fj5/"},
    {"id": "SYSTXCCITC01-C", "url": "https://www.carrier.com/residential/en/us/products/thermostats/smart-thermostats/systxccitc01-c/"},
    {"id": "SYSTXCCWIC01-C", "url": "https://www.carrier.com/residential/en/us/products/thermostats/smart-thermostats/systxccwic01-c/"},
    {"id": "EB-STATE6ICR-01", "url": "https://www.carrier.com/residential/en/us/products/thermostats/smart-thermostats/eb-state6icr-01/"},
    {"id": "TSTATCCEWF-01", "url": "https://www.carrier.com/residential/en/us/products/thermostats/smart-thermostats/tstatccewf-01/"},
    {"id": "DGAPA", "url": "https://www.carrier.com/residential/en/us/products/indoor-air-quality/air-purifiers/air-purifier-dgapa/"},
    {"id": "UVCAP", "url": "https://www.carrier.com/residential/en/us/products/indoor-air-quality/air-purifiers/carbon-air-purifier-uvcap/"},
    {"id": "EZXCAB", "url": "https://www.carrier.com/residential/en/us/products/indoor-air-quality/air-purifiers/ezxcab/"},
    {"id": "HUMCRSTM", "url": "https://www.carrier.com/residential/en/us/products/indoor-air-quality/humidifiers/humcrstm/"},
    {"id": "37MPRA", "url": "https://www.carrier.com/residential/en/us/products/ductless-mini-splits/37mpra/"},
    {"id": "45MPHA", "url": "https://www.carrier.com/residential/en/us/products/ductless-mini-splits/45mpha/"},
    {"id": "48NG", "url": "https://www.carrier.com/residential/en/us/products/combined-heating-cooling/48ng/"},
    {"id": "50VR", "url": "https://www.carrier.com/residential/en/us/products/combined-heating-cooling/50vr/"}
]

if not os.path.exists('images'):
    os.makedirs('images')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for item in equipment:
    url = item['url']
    item_id = item['id']
    
    # Handle special cases
    search_id = item_id
    if '***' in search_id:
        search_id = search_id.split('***')[0]
    
    print(f"Processing {item_id}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        image_url = None
        
        # Strategy 1: Look for image with ID in src
        images = soup.find_all('img')
        for img in images:
            src = img.get('src', '')
            if not src: continue
            
            # Check for ID match (case insensitive)
            if search_id.lower() in src.lower():
                # Filter out icons or small images if possible
                if 'icon' in src.lower() or 'logo' in src.lower():
                    continue
                image_url = src
                break
        
        # Strategy 2: Look for 'hero' image
        if not image_url:
            for img in images:
                src = img.get('src', '')
                if 'hero' in src.lower() and 'products' in src.lower():
                     image_url = src
                     break

        # Strategy 3: OG Image (Fallback)
        if not image_url:
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                content = og_image.get('content')
                if 'logo' not in content.lower(): # Avoid generic logos
                    image_url = content

        if image_url:
            # Fix relative URLs if necessary (though usually they are absolute on Carrier)
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            elif image_url.startswith('/'):
                # Base URL extraction
                from urllib.parse import urlparse
                parsed_uri = urlparse(url)
                base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                image_url = base + image_url
                
            print(f"  Found image: {image_url}")
            
            # Download
            img_data = requests.get(image_url, headers=headers, timeout=10).content
            with open(f"images/{item_id}.jpg", 'wb') as f:
                f.write(img_data)
            print(f"  Saved to images/{item_id}.jpg")
            
        else:
            print(f"  Could not find image for {item_id}")
            
    except Exception as e:
        print(f"  Error processing {item_id}: {e}")
    
    # Be nice to the server
    time.sleep(1)
