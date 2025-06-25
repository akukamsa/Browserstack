import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service

@pytest.fixture(scope="function")
def driver():
    driver_path = "msedgedriver.exe"
    service = Service(executable_path=driver_path)
    driver = webdriver.Edge(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()