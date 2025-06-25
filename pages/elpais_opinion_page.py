import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OpinionPage:
    def __init__(self, driver):
        self.driver = driver

    def get_first_n_articles(self, count=5, image_dir="assets"):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//article"))
        )

        articles = self.driver.find_elements(By.XPATH, "//article")
        output = []

        os.makedirs(image_dir, exist_ok=True)

        for idx, article in enumerate(articles[:count]):
            try:
                title = article.find_element(By.TAG_NAME, "h2").text.strip()
            except:
                title = "No title found"

            try:
                content = article.find_element(By.TAG_NAME, "p").text.strip()
            except:
                content = "No content found"

            try:
                img = article.find_element(By.TAG_NAME, "img")
                img_url = img.get_attribute("src")
                if img_url:
                    img_data = requests.get(img_url).content
                    img_path = os.path.join(image_dir, f"article_{idx+1}.jpg")
                    with open(img_path, "wb") as f:
                        f.write(img_data)
                else:
                    img_url = "No image URL"
            except:
                img_url = "No image"

            output.append({
                "title": title,
                "content": content,
                "image": img_url
            })

        return output