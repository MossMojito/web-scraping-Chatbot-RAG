import asyncio
import random
import argparse
import pandas as pd
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup

# Original Configuration
BASE_URL = "https://www.yellowpages.co.th"

async def get_subcategories(category_name="กีฬา"):
    """
    Extract all subcategories from a chosen category using BeautifulSoup.
    (Original Logic from Notebook)
    """
    url = f"{BASE_URL}/category/{category_name}"
    print(f"Getting subcategories from {url}...")
    
    # Hybrid: Crawl4AI for Fetching
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(url=url, bypass_cache=True)
        
    if not result.success:
        print(f"Error fetching page: {result.error_message}")
        return []

    # BeautifulSoup for Parsing
    soup = BeautifulSoup(result.html, 'html.parser')
    links = soup.find_all('a', href=True)
    
    subcats = []
    seen_urls = set()
    
    for link in links:
        href = link['href']
        text = link.get_text(strip=True)
        
        if '/heading/' in href and text:
            if not href.startswith('http'):
                full_url = f"https://www.yellowpages.co.th{href}"
            else:
                full_url = href
                
            if full_url not in seen_urls:
                subcats.append({"name": text, "url": full_url})
                seen_urls.add(full_url)
    
    print(f"Found {len(subcats)} subcategories")
    return subcats

async def scraper(category_name="กีฬา"):
    """
    Extract structured data from unstructured web content using Hybrid Approach.
    """
    subcats = await get_subcategories(category_name)
    
    if not subcats:
        print("No subcategories found. Exiting.")
        return

    print(f"Starting V5 SUPER ROBUST Scrape for {len(subcats)} subcategories...")
    print("Features: Gap Tolerance (3 pages), Strict Verification (4 retries), Unlimited Pages.")
    
    all_data = []
    
    async with AsyncWebCrawler(verbose=False) as crawler:
        
        for i, sub in enumerate(subcats):
            sub_name = sub['name']
            sub_url = sub['url']
            print(f"\n[{i+1}/{len(subcats)}] Subcategory: {sub_name}")
            
            page = 1
            empty_streak = 0
            
            while True:
                # Polite delay
                await asyncio.sleep(random.uniform(1.0, 2.0))
                
                target_url = sub_url if page == 1 else f"{sub_url}?page={page}"
                
                # --- RETRY LOGIC for PAGE FETCH (3 attempts) ---
                page_soup = None
                for attempt in range(3):
                    try:
                        res = await crawler.arun(url=target_url, bypass_cache=True)
                        if not res.html: raise Exception("Empty HTML")
                        page_soup = BeautifulSoup(res.html, 'html.parser')
                        break
                    except Exception as e:
                        print(f"   [Page {page}] Load Retry {attempt+1}... ({e})")
                        await asyncio.sleep(3)
                
                # If page load failed completely
                if not page_soup:
                    print(f"   [Page {page}] FAILED to load. Skipping.")
                    empty_streak += 1
                    if empty_streak >= 3:
                        print(f"   Stopped at Page {page} (3 empty pages in a row).")
                        break
                    page += 1
                    continue

                # Check listings
                titles = page_soup.find_all('div', class_='yp-listing-title')
                
                if not titles:
                    print(f"   [Page {page}] 0 items found.")
                    empty_streak += 1
                    if empty_streak >= 3:
                        print(f"   Stopped at Page {page} (3 empty pages in a row).")
                        break
                    page += 1
                    continue
                else:
                    empty_streak = 0
                    print(f"   [Page {page}] Listing {len(titles)} items...")
                
                # Extract URLS
                p_urls = []
                for div in titles:
                    a = div.find('h3').find('a')
                    if a and a.get('href'):
                        href = a['href'] if a['href'].startswith('http') else "https://www.yellowpages.co.th" + a['href']
                        p_urls.append(href)
                
                # --- SCRAPE DETAILS for each item with STRICT RETRY ---
                for p_idx, p_url in enumerate(p_urls):
                    for p_attempt in range(4):
                        try:
                            await asyncio.sleep(random.uniform(0.5, 1.2))
                            
                            res_p = await crawler.arun(url=p_url, bypass_cache=True)
                            soup = BeautifulSoup(res_p.html, 'html.parser')
                            
                            # VALIDATION: Must have a Name (H1)
                            h1 = soup.find('h1')
                            if not h1:
                                raise Exception("Missing H1 Name")
                                
                            name = h1.get_text(strip=True)
                            
                            # B. Address
                            address = "Unknown"
                            addr_label = soup.find('strong', string=lambda t: t and "ที่อยู่" in t)
                            if addr_label and addr_label.parent:
                                val = addr_label.parent.find_next_sibling('div')
                                if val: address = val.get_text(strip=True)
                                
                            # C. Phone
                            phone = "No Phone"
                            l_ph = soup.find('a', href=lambda h: h and h.startswith('tel:'))
                            if l_ph: phone = l_ph.get_text(strip=True)
                            
                            # D. Map
                            map_link = "No Map"
                            l_map = soup.find('a', string=lambda t: t and "นำทาง" in t)
                            if not l_map: l_map = soup.find('a', href=lambda h: h and 'google.com/maps' in h)
                            if l_map: map_link = l_map['href']
                            
                            # E. Description
                            desc = "No Description"
                            dh = soup.find(string=lambda t: t and "สินค้าและบริการ" in t)
                            if dh and dh.parent:
                                cont = dh.parent
                                for sib in cont.find_next_siblings():
                                    txt = sib.get_text(strip=True)
                                    if txt and "Share" not in txt and len(txt) > 10:
                                        desc = txt
                                        break
                                        
                            all_data.append([sub_name, name, address, phone, map_link, desc, p_url])
                            break 
                            
                        except Exception:
                            if p_attempt == 3:
                                print(f"     x Skipping Item: {p_url} (Failed 4 retries)")
                            else:
                                await asyncio.sleep(2)
                
                page += 1
        
    # Save
    cols = ["Subcategory", "Name", "Address", "Phone", "Map", "Description", "Profile URL"]
    df = pd.DataFrame(all_data, columns=cols)
    filename = f"yellowpages_{category_name}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    print(f"\n==========================================")
    print(f"DONE! Saved {len(df)} rows to {filename}")
    print(f"==========================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YellowPages Thailand Scraper")
    parser.add_argument("--category", type=str, default="กีฬา", help="Category to scrape (default: กีฬา)")
    args = parser.parse_args()
    
    asyncio.run(scraper(args.category))
