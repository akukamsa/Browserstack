import json
import os
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# The webdriver management will be handled by the browserstack-sdk
# so this will be overridden and tests will run browserstack -
# without any changes to the test files!
def translate_text(text):
    url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"
    print(text)
    payload = {
	"from": "auto",
	"to": "en",
	"text": str(text)
    }
    headers = {
	"x-rapidapi-key": "90e48db542msh364e8bf1bd874f6p1ed89djsnc5f63cd65945",
	"x-rapidapi-host": "google-translate113.p.rapidapi.com",
	"Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers,verify=False)
        result = response.json()
        print(result)
        return result["trans"]
    except Exception as e:
        print(f"Translation failed: {e}")
        return None
def analyze_repeated_words(headers):
    from collections import Counter
    words = " ".join(headers).lower().split()
    counter = Counter(words)
    repeated = {k: v for k, v in counter.items() if v > 2}
    for word, count in repeated.items():
        print(f"'{word}': {count} times")
options = ChromeOptions()
options.set_capability('sessionName', 'BStack Sample Test')
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://elpais.com")
    lang =WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html"))).get_attribute("lang")
    if lang == "es-ES":
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Title contains spanish as lang"}}')
    else:
            driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Title contains spanish as lang"}}')
    #accept cookies - for browser for phone no button
    try:       
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.ID, "didomi-notice-agree-button"))).click() 
    except:
        pass
    #click on opinion
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href,'/opinion') and @cmp-ltrk='portada_menu']"))).click()
    #extract 5 articles    
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//article"))) 
    articles = driver.find_elements(By.XPATH, "//article")[:5]

    os.makedirs("assets", exist_ok=True)
    translated_titles = []

    for idx, article in enumerate(articles):
        title = "No title found"
        content = "No content found"
        img_url = "No image"

        try:
            title = article.find_element(By.TAG_NAME, "h2").text.strip()
        except:
            pass

        try:
            content = article.find_element(By.TAG_NAME, "p").text.strip()
        except:
            pass

        try:
            img = article.find_element(By.TAG_NAME, "img")
            img_url = img.get_attribute("src")
            if img_url:
                img_data = requests.get(img_url).content
                img_path = os.path.join("assets", f"article_{idx+1}.jpg")
                with open(img_path, "wb") as f:
                    f.write(img_data)
        except:
            img_url = "No image"

        print(f"\n--- Article {idx + 1} ---")
        print("Title:", title)
        print("Content:", content)
        print("Image:", img_url)

        translated = translate_text(title)
        translated_titles.append(translated)
    print("\nRepeated Words:")
    analyze_repeated_words(translated_titles)

except NoSuchElementException as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
except Exception as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
finally:
    # Stop the driver
    driver.quit()
