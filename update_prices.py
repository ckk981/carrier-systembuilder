import json
import time
import urllib.parse
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
SEED_FILE = 'seed_equipment.json'
BASE_URL = 'https://www.carrierenterprise.com'
IMAGE_DIR = 'images'

def main():
    # 1. Load Data
    print(f"Loading {SEED_FILE}...")
    with open(SEED_FILE, 'r') as f:
        data = json.load(f)

    # Ensure image directory exists
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    # 2. Initialize Browser
    print("Initializing Browser... (This may take a moment to download the driver)")
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless') # NOT headless
        
        # Use webdriver_manager to get the driver path
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        print("Browser initialized successfully!")
    except Exception as e:
        print("Error initializing Chrome driver.")
        print("Ensure you have Chrome installed on this machine.")
        print(f"Details: {e}")
        return

    try:
        # 3. Login Interruption
        print("\n" + "="*60)
        print("OPENING BROWSER FOR LOGIN")
        print("1. The browser will open to Carrier Enterprise.")
        print("2. Please LOG IN manually.")
        print("3. Return here and press ENTER once you are logged in and ready.")
        print("="*60 + "\n")
        
        driver.get(BASE_URL)
        
        print("\n" + "="*60)
        print("WAITING FOR LOGIN...")
        print("1. Please log in to Carrier Enterprise in the browser window.")
        print("2. The script will automatically detect when you are logged in.")
        print("="*60 + "\n")

        # Loop to check for login with manual override
        print("Waiting for login... (The script will verify, or you can press ENTER in the terminal to force continue if you are sure)")
        
        # Simple blocking input is safest to avoid "never asked" issue if detection fails
        input(">>> Press ENTER here once you are logged in to Carrier Enterprise <<<")
        print("Proceeding...")
        
        print("\nStarting pricing update... (Press Ctrl+C to stop early and save)")
        
        # 4. Iterate and Scrap
        updated_count = 0
        img_count = 0
        
        # Prepare session for image downloading (to use cookies if needed, though often public)
        # We'll valid cookies from selenium if images are protected, but let's try standard requests first.
        # Actually, CE images usually public CDN.
        
        for item in data:
            model = item.get('id')
            query = model.split('*')[0] 
            
            search_url = f"{BASE_URL}/search?query={urllib.parse.quote(query)}"
            driver.get(search_url)
            
            # Artificial pause
            time.sleep(3)
            
            try:
                # --- PRICE FINDING ---
                # Strategy: Find first valid price on the page
                price_data = driver.execute_script("""
                    function findPrice() {
                        // Priority 1: Specific price classes locally or text-nowrap spans
                        // We iterate all candidates and take the first valid one we see.
                        // This handles the "generic ID -> list of specific items" case by taking the first one.
                        let candidates = Array.from(document.querySelectorAll('.price-container, .product-price, .price, span.text-nowrap'));
                        for (let c of candidates) {
                            let txt = c.innerText.trim();
                            if (txt.match(/^\\$[\\d,]+\\.\\d{2}$/)) {
                                return parseFloat(txt.replace('$', '').replace(',', ''));
                            }
                        }
                        return null;
                    }
                    return findPrice();
                """)
                
                if price_data:
                    item['price'] = price_data
                    updated_count += 1
                    print(f"Updated {model}: Price ${price_data}")
                else:
                    print(f"Price NOT found for {model}")

                # --- IMAGE FINDING ---
                # Strategy: Find first product image
                # Look for img tag inside product card or main image
                img_src = driver.execute_script("""
                    let img = document.querySelector('img.product-image, .product-listing-item img, .product-detail img');
                    if (img) return img.src;
                    return null;
                """)
                
                if img_src and not img_src.startswith('data:'):
                    # Download image
                    try:
                        ext = img_src.split('.')[-1].split('?')[0]
                        if len(ext) > 4: ext = 'jpg' # minimal fallback
                        filename = f"{model.replace('*','-').replace('/','-')}.{ext}"
                        local_path = os.path.join(IMAGE_DIR, filename)
                        
                        # Download using requests
                        # Use cookies from selenium to be safe?
                        # Using headers to look like browser
                        headers = {"User-Agent": driver.execute_script("return navigator.userAgent;")}
                        r = requests.get(img_src, headers=headers, stream=True, timeout=5)
                        if r.status_code == 200:
                            with open(local_path, 'wb') as f:
                                for chunk in r.iter_content(1024):
                                    f.write(chunk)
                            item['img'] = local_path # Update data model
                            img_count += 1
                            print(f"  - Image saved: {local_path}")
                        else:
                            print(f"  - Image download failed: {r.status_code}")
                    except Exception as err:
                        print(f"  - Image processing error: {err}")
                        
            except Exception as e:
                print(f"Error scraping {model}: {e}")
                
            # Rate limit
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping and saving progress...")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        # 5. Save Data
        print(f"Saving updated data to {SEED_FILE}...")
        with open(SEED_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Done. Prices: {updated_count}, Images: {img_count}")
        
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()
