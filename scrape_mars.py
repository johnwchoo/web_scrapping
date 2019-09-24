#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from pprint import pprint
import pymongo
import pandas as pd
import requests

def scrape():


    # In[3]:


    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    #browser = Browser('chrome', **executable_path, headless=False)
    browser = Browser("chrome", **executable_path, headless = True)


    # In[4]:


    url = ('https://mars.nasa.gov/news/')

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    type(soup)
    # print(response.text)

    # In[5]:

    # Extract the text from the class="content_title" and clean up the text use strip
    news_title = soup.find_all('div', class_='content_title')[0].find('a').text.strip()

    # print title to check
    # print(news_title)

    # In[6]:

    # Extract the paragraph from the class="rollover_description_inner" and clean up the text use strip
    news_paragraph = soup.find_all('div', class_='rollover_description_inner')[0].text.strip()

    # print paragraph to check
    print(news_paragraph)

    # In[8]:

    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    #img = browser.find_by_id("full_image")
    #img.click()


    # In[11]:


    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    # print(featured_image_url)


    # In[13]:


    # Scrape the latest tweet
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    twitter_html = browser.html
    twitter_soup = bs(twitter_html, 'html.parser')

    tweets = twitter_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    # print(mars_weather)


    # In[14]:


    # Scrape facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)
    # print(mars_facts)


    # In[17]:


    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere = {}

    result = soup.find("div", class_ = "result-list" )
    hemispheres = result.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup= bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"].replace('http', 'https')
        mars_hemisphere.update({"title": title, "img_url": image_url, "paragraph": news_paragraph,\
            "mars_facts": mars_facts, "mars_weather": mars_weather, "featured_image": featured_image_url})

        
    return mars_hemisphere


    # In[ ]:




