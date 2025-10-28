"""
OLX Car Cover Scraper - Fixed Version
Author: Madhu
Date: October 27, 2025
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from tabulate import tabulate
import time

def setup_driver():
    """Configure Chrome with headless mode"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def extract_ad_data(ad_element):
    """
    Extract title, price, and description from a single ad.
    Returns dict with ad data, or None if extraction fails.
    """
    ad_info = {
        'Title': 'N/A',
        'Description': 'N/A', 
        'Price': 'N/A'
    }
    
    # Extract Title
    try:
        title_elem = ad_element.find_element(By.CSS_SELECTOR, 'span[data-aut-id="itemTitle"]')
        ad_info['Title'] = title_elem.text.strip()
    except:
        try:
            title_elem = ad_element.find_element(By.CSS_SELECTOR, 'span._2tW1I')
            ad_info['Title'] = title_elem.text.strip()
        except:
            pass
    
    # Extract Price
    try:
        price_elem = ad_element.find_element(By.CSS_SELECTOR, 'span[data-aut-id="itemPrice"]')
        ad_info['Price'] = price_elem.text.strip()
    except:
        try:
            price_elem = ad_element.find_element(By.CSS_SELECTOR, 'span._89yzn')
            ad_info['Price'] = price_elem.text.strip()
        except:
            pass
    
    # Extract Description - Multiple attempts with different selectors
    try:
        # Try primary selector
        desc_elem = ad_element.find_element(By.CSS_SELECTOR, 'div[data-aut-id="itemDetails"]')
        ad_info['Description'] = desc_elem.text.strip()
    except:
        try:
            # Try alternative selector
            desc_elem = ad_element.find_element(By.CSS_SELECTOR, 'span._2tW1I ~ span')
            ad_info['Description'] = desc_elem.text.strip()
        except:
            try:
                # Try getting all text from ad and extract after title
                full_text = ad_element.text.strip()
                lines = full_text.split('\n')
                if len(lines) > 1:
                    # Description is usually on second line
                    ad_info['Description'] = lines[1] if len(lines[1]) > 0 else 'N/A'
            except:
                pass
    
    # IMPORTANT: Filter out real estate listings
    # If title contains property-related keywords, skip it
    property_keywords = ['bhk', 'flat', 'apartment', 'house', 'rent', 'rooms', 'halls', 
                        'balconies', 'independent', 'spacious', 'property', 'parking']
    
    title_lower = ad_info['Title'].lower()
    if any(keyword in title_lower for keyword in property_keywords):
        # Check if it's actually about car covers
        car_cover_keywords = ['car cover', 'body cover', 'seat cover', 'car mat']
        if not any(keyword in title_lower for keyword in car_cover_keywords):
            return None  # Skip this ad
    
    # Only return if we got at least the title
    if ad_info['Title'] != 'N/A':
        return ad_info
    return None

def scrape_olx(search_url, max_ads=30):
    """
    Main scraping function with filtering
    """
    print(f"Starting scraper...")
    print(f"URL: {search_url}\n")
    driver = setup_driver()
    results = []
    
    try:
        driver.get(search_url)
        print("Page loaded. Waiting for content...")
        time.sleep(5)
        
        # Find all ad containers
        ad_containers = driver.find_elements(By.CSS_SELECTOR, 'li[data-aut-id="itemBox"]')
        
        if not ad_containers:
            print("Primary selector failed. Trying alternatives...")
            ad_containers = driver.find_elements(By.CSS_SELECTOR, 'div[data-aut-id="itemBox"]')
        
        if not ad_containers:
            ad_containers = driver.find_elements(By.TAG_NAME, 'li')
        
        print(f"Found {len(ad_containers)} potential ads")
        print("Extracting and filtering...\n")
        
        # Extract data
        count = 0
        for idx, ad in enumerate(ad_containers, 1):
            if count >= max_ads:
                break
                
            ad_data = extract_ad_data(ad)
            if ad_data:  # Only add if not filtered out
                results.append(ad_data)
                count += 1
                print(f"  [{count}] ✓ {ad_data['Title'][:60]}...")
        
        print(f"\n{'='*70}")
        print(f"Successfully extracted {len(results)} car cover listings")
        print(f"Filtered out {len(ad_containers) - len(results)} irrelevant ads")
        print(f"{'='*70}\n")
        
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        
    finally:
        driver.quit()
    
    return results

def save_results(data, filename='car_cover_listings.csv'):
    """Save scraped data to CSV and display as table"""
    if not data:
        print("❌ No data to save!")
        return
    
    df = pd.DataFrame(data)
    
    # Display in terminal
    print("\n" + "="*80)
    print(f"CAR COVER LISTINGS - {len(data)} RESULTS")
    print("="*80)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=True))
    
    # Save to CSV
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n✓ Results saved to {filename}")
    print(f"✓ Total records: {len(data)}")

# Main execution
if __name__ == "__main__":
    # UPDATED URLs - Try these in order
    urls_to_try = [
        "https://www.olx.in/cars/spare-parts-accessories/q-car-cover",
        "https://www.olx.in/items/q-car-body-cover",
        "https://www.olx.in/items/q-car-cover?isSearchCall=true"
    ]
    
    print("="*80)
    print("OLX CAR COVER SCRAPER - FIXED VERSION")
    print("="*80 + "\n")
    
    # Try first URL
    scraped_data = scrape_olx(urls_to_try[0], max_ads=25)
    
    # If not enough results, try second URL
    if len(scraped_data) < 10:
        print("\n⚠️  Not enough results. Trying alternative URL...\n")
        scraped_data.extend(scrape_olx(urls_to_try[1], max_ads=25))
    
    # Save and display
    if scraped_data:
        # Remove duplicates by title
        seen_titles = set()
        unique_data = []
        for ad in scraped_data:
            if ad['Title'] not in seen_titles:
                seen_titles.add(ad['Title'])
                unique_data.append(ad)
        
        save_results(unique_data, "car_cover_listings.csv")
    else:
        print("\n❌ No car cover listings found!")
        print("Possible reasons:")
        print("  1. OLX changed their HTML structure")
        print("  2. Search returned only real estate")
        print("  3. Network/firewall issues")
