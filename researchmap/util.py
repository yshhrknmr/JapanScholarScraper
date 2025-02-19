import time
import random
import urllib.parse
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_original_url(duckduckgo_url):
    parsed = urllib.parse.urlparse(duckduckgo_url)
    params = urllib.parse.parse_qs(parsed.query)
    if 'uddg' in params:
        original_url = params['uddg'][0]
        return urllib.parse.unquote(original_url).rstrip('/')
    return duckduckgo_url


def find_researchmap_url_ddgs(chrome_driver, researcher_name):
    query = urllib.parse.quote_plus(f"{researcher_name} researchmap")
    search_url = f"https://duckduckgo.com/html/?q={query}"
    chrome_driver.get(search_url)
    
    try:
        # リンクが表示されるまで最大10秒待機
        wait = WebDriverWait(chrome_driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'researchmap.jp')]")))
        
        # すべての候補リンクを取得
        links = chrome_driver.find_elements(By.XPATH, "//a[contains(@href, 'researchmap.jp')]")
        for link in links:
            href = link.get_attribute("href")
            # もしDuckDuckGoのリダイレクトURLであれば、元のURLを抽出
            if href.startswith("https://duckduckgo.com/l/"):
                href = extract_original_url(href)
            if href.startswith("https://researchmap.jp/"):
                return href
        
        print("  有効な researchmap の URL が見つかりませんでした")
        return None
    except Exception as e:
        print(f"  Exception: {e}")
        return None


def get_researchmap_json(url):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        return response.json()
    except Exception as e:
        print(f"  Exception: {e}")
        return None
