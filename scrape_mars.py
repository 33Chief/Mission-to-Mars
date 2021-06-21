from requests.sessions import should_bypass_proxies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # URLs of pages to be scraped
    nasa_mars_news_url = 'https://mars.nasa.gov/news/'
    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    mars_facts_url = 'http://space-facts.com/mars/'
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    news_response = requests.get(nasa_mars_news_url)
    soup = bs(news_response.text, 'html.parser')
    results = soup.find_all(class_="slide")
    titles_list = []
    paragraphs_list = []

    for result in results:
            links = result.find_all('a')
            title = links[1].text
            paragraph = result.find(class_="rollover_description_inner").text
            titles_list.append(title)
            paragraphs_list.append(paragraph)
    news_title = titles_list[0]
    news_ = paragraphs_list[0]


    image_response = requests.get(mars_image_url)
    soup = bs(image_response.text, 'html.parser')
    results = soup.find_all(class_="carousel_items")

    for result in results:
        article = result.find('article', class_="carousel_item")
        article_link = article['style']
        cleaned_article_link = article['style'].lstrip('background-image: url(')
        cleaned_article_link = cleaned_article_link.rstrip(');')
    cleaned_article_link = cleaned_article_link.replace("'", "")
    featured_image_link = 'https://www.jpl.nasa.gov'+cleaned_article_link


    weather_response = requests.get(mars_weather_url)
    Soup = bs(weather_response.text, 'html.parser')
    results = Soup.find_all(class_="content")
    tweets_list = []
    for result in results:
        tweet = result.find('p', class_="TweetTextSize").text
        tweets_list.append(tweet)
    mars_weather = tweets_list[0]

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    usgs_base_= 'https://astrogeology.usgs.gov'
    links_list = []
    hemispheres_response = requests.get(mars_hemispheres_url)
    soup = bs(hemispheres_response.text, 'html.parser')

    results = Soup.find_all(class_='item')
    for result in results:
        links = result.find('a')
        link=links['href']
        links_list.append(usgs_base_+link)
        browser.visit(mars_hemispheres_url)

    hemispheres_image_urls = []
    titles_list = []

    for x in range(0, 4):
        browser.visit(links_list[x])
        html = browser.html
        soup = bs(html, 'html.parser')
        images = Soup.find(class_='downloads')
        image = images.find('a')
        image_url= image['href']
        hemispheres_image_urls.append(image_url)
        titles = bs.find('h2', class_='title')
        title=titles.text
        title=title.strip('Enhanced')
        titles_list.append(title)

    hemispheres_dict = {'Title': titles_list,
                        'URL': hemispheres_image_urls }
    scraped_dict = {'Title': titles_list,
                    'URL': hemispheres_image_urls,
                    'Weather': mars_weather,
                    'Featured Image': featured_image_link,
                    'News Title': news_title,
                    'News Body': news_
               }
    return (scraped_dict)