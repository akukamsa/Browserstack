import pytest
from pages.elpais_home_page import HomePage
from pages.elpais_opinion_page import OpinionPage
from utils.translator import Translator
from utils.analyser import analyze_repeated_words

def test_homepage_language_spanish(driver):
    home_page = HomePage(driver)
    driver.get(home_page.url)
    html_lang = driver.find_element("tag name","html").get_attribute("lang")
    #checking for html tag
    assert html_lang =="es-ES", f"Expect language to be 'es', but got '{html_lang}'"

def test_opinion_article_scraping(driver):
    home = HomePage(driver)
    opinion = OpinionPage(driver)
    driver.get(home.url)
    home.click_accept_cookie()
    home.click_on_opinion()

    articles = opinion.get_first_n_articles(count=5)

    assert len(articles) == 5, "Less than 5 articles fetched."

    for i, article in enumerate(articles, 1):
        print(f"\n--- Article {i} ---")
        print("Title:", article["title"])
        print("Content:", article["content"])
        print("Image:", article["image"])
        assert article["title"], f"Missing title in article {i}"

def test_translate_article_titles(driver):
    home = HomePage(driver)
    opinion = OpinionPage(driver)
    translator = Translator(api_key="431ed0bee2msha940dc0532ef933p1ab504jsnc46cabd78a6c")

    driver.get(home.url)
    home.click_accept_cookie()
    home.click_on_opinion()

    articles = opinion.get_first_n_articles(count=5)

    print("\nTranslated Titles:")
    for i, article in enumerate(articles, 1):
        title = article["title"]
        translated = translator.translate_text(title)
        print(f"{i}. {translated}")
        assert translated, f"Translation failed for article {i}"

def test_translate_article_titles_counter(driver):
    home = HomePage(driver)
    opinion = OpinionPage(driver)
    translator = Translator(api_key="431ed0bee2msha940dc0532ef933p1ab504jsnc46cabd78a6c")

    driver.get(home.url)
    home.click_accept_cookie()
    home.click_on_opinion()

    articles = opinion.get_first_n_articles(count=5)
    translated_titles=[]
    print("\nTranslated Titles:")
    for i, article in enumerate(articles, 1):
        title = article["title"]
        translated = translator.translate_text(title)
        translated_titles.append(translated)
        print(f"{i}. {translated}")
        assert translated, f"Translation failed for article {i}"
    analyze_repeated_words(translated_titles)
    