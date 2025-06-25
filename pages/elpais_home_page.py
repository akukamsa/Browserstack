from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self,driver):
        self.driver = driver
        self.url = "https://elpais.com"
        self.wait = WebDriverWait(driver,10)
        self.hamburger=(By.ID,"btn_open_hamburger")
        self.opinion = (By.XPATH,"//a[contains(@href,'/opinion') and @cmp-ltrk='portada_menu']")
    
    def open_navigation_menu(self):
        hamburger = self.wait.until(EC.element_to_be_clickable(self.hamburger))
        hamburger.click()

    def click_on_opinion(self):
        opinion = self.wait.until(EC.element_to_be_clickable(self.opinion))
        opinion.click()
    
    def click_accept_cookie(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID,"didomi-notice-agree-button"))).click()
        except Exception as e:
            print("No Cookie Popup or couldnt click")