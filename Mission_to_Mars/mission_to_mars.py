from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)



# # Grab the latest news article from the website -'https://mars.nasa.gov/news/'
# ## store the title and paragraph description.

def scrape_latest_news():

    # set the URL 
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # print(soup.prettify())

    # results are returned as an iterable list
    results = soup.body.find('div',class_='slide')

    news_p = results.find('div',class_='rollover_description_inner').text
    news_title=results.find('div',class_='content_title').text

    news = {'title' : news_title, 
            'text' : news_p}

    return (news)

# # Scrape the featured image from the website - https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
# ## Store the image and create an url to the image.

def scrape_feature_image():

    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find('section',class_='content_page module').find('figure',class_='lede').find('a')['href']

    feaured_image_url = {'url' : 'https://www.jpl.nasa.gov' + results}

    
    # Quite the browser after scraping
    browser.quit()

    return feaured_image_url


# # Scrape the Mars facts from https://space-facts.com/mars/
# ## Place them into a dataframe to store in an html file.

def scrape_mars_data():

    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    tables

    df = tables[0]

    # Export the city data into an html file
    df.to_html(open('Resources/mars_facts.html', 'w', encoding="utf-8"))

    with open('Resources/mars_facts.html', 'r') as file:
        data = file.read()
    
    data_dict = {'html' : data,
                'file' : 'Resources/mars_facts.html'}

    return data_dict


# # Scrape the website -  for the 4 urls images
# ## https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

def scrape_mars_hemi():
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # print(soup.prettify())

    results = soup.body.find_all('div',class_='item')

    browser = init_browser()

    hemisphere_image_urls = []

    for result in results:

        # Error handling
        try:
        
            # Identify and return title of listing
            title = result.find('div',class_='description').find('h3').text

            browser.visit(url)
        
            time.sleep(1)
        
            browser.click_link_by_partial_text(title)
            html = browser.html
            soup = BeautifulSoup(html, 'lxml')
            link = soup.body.find('div',class_='container').find('div',class_='downloads').li.a['href']

            # Run only if title, and link are available
            if (title and link):

                # Dictionary to be inserted as a MongoDB document
                post = {
                    'title': title,
                    'url': link
                    }

                hemisphere_image_urls.append(post)
            
        except Exception as e:
            print(e)

    
    # Quite the browser after scraping
    browser.quit()

    return hemisphere_image_urls


