import time
import random
import urllib.parse
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

def find_researchmap_url_ddgs(chrome_driver, researcher_name):
    search_url = f"https://duckduckgo.com/html/?q={researcher_name}+researchmap"
    chrome_driver.get(search_url)
    time.sleep(random.uniform(1, 4))
    try:
        first_result = chrome_driver.find_element(By.PARTIAL_LINK_TEXT, "researchmap.jp")
        url = first_result.get_attribute("href")
        url = urllib.parse.unquote(url).split('?')[0].rstrip('/')
        return url
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
