# @ibrahimsql
# screenshot modules

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

def take_screenshot(url, output_dir="screenshots", full_page=True, viewport_size=(1920, 1080)):
    """
    Take a screenshot of a website
    
    Args:
        url (str): The URL to capture
        output_dir (str): Directory to save screenshots
        full_page (bool): Whether to capture full page or just viewport
        viewport_size (tuple): Browser viewport size (width, height)
    
    Returns:
        str: Path to the saved screenshot or error message
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument(f'--window-size={viewport_size[0]},{viewport_size[1]}')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        # Setup webdriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            # Navigate to URL
            driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Generate filename
            domain = url.split('//')[-1].split('/')[0].replace(':', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{domain}_{timestamp}.png"
            filepath = os.path.join(output_dir, filename)
            
            if full_page:
                # Get full page height
                total_height = driver.execute_script("return document.body.scrollHeight")
                driver.set_window_size(viewport_size[0], total_height)
                time.sleep(1)
            
            # Take screenshot
            driver.save_screenshot(filepath)
            
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename,
                "size": os.path.getsize(filepath) if os.path.exists(filepath) else 0
            }
            
        finally:
            driver.quit()
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def take_multiple_screenshots(urls, output_dir="screenshots", full_page=True):
    """
    Take screenshots of multiple URLs
    
    Args:
        urls (list): List of URLs to capture
        output_dir (str): Directory to save screenshots
        full_page (bool): Whether to capture full page or just viewport
    
    Returns:
        list: List of results for each URL
    """
    results = []
    
    for url in urls:
        print(f"Taking screenshot of: {url}")
        result = take_screenshot(url, output_dir, full_page)
        results.append({"url": url, **result})
        
        # Small delay between screenshots
        time.sleep(1)
    
    return results
