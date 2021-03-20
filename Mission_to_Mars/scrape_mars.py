from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import time
import os


def init_browser():
    # NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # NASA Mars News Scrape
    news_url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    #Select latest category
    browser.find_by_id('date').first.click()
    browser.find_option_by_text('Latest').first.click()

    #Select All categories
    browser.find_by_id('categories').first.click()
    browser.find_option_by_text('All Categories').first.click()
    browser.find_by_id('categories').first.click()
    time.sleep(0)
    
    #Collect the latest News Title
    results=soup.find('li', class_="slide")

    # Pase the first title from the results 
    news_title =results.find('div',class_='content_title').text.strip()

    # Parse out the first paragraph associatd with the tile from results
    news_p=results.find('div',class_='article_teaser_body').text.strip()

    # -------------------------------------------------------------------------------
    # JPL Mars Space Images - Featured Image

    #Use splinter to browse through page
    images_url="https://www.jpl.nasa.gov/images?search=&category=Mars"
    browser.visit(images_url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    #Use splinter to clisk on Mars filter
    browser.find_by_id('filter_Mars').click()

    #Find image url and save to variable
    featured_image_url=browser.find_by_css('.BaseImage')['data-src']

    # -------------------------------------------------------------------------------
    # MARS Facts

    #Use splinter to browse through page
    facts_url="https://space-facts.com/mars/"
    browser.visit(facts_url)

    # Use Panda's `read_html` to parse the url
    facts_tables = pd.read_html(facts_url)

    # parse through list of dataframes for Mars Facts
    mars_0_df=facts_tables[0]

    #Rename columns
    column_names={
        0: "Description",
        1: "Mars Fact"
    }

    mars_1_df=mars_0_df.rename(columns=column_names)

    #Set the index of the columns to Description of facts
    mars_df=mars_1_df.set_index("Description")

    #Convers Mars DF to html table
    mars_facts_html=mars_df.to_html()

    # -------------------------------------------------------------------------------
    # Mars Hemispheres

    #Use splinter to browse through page
    hemispheres_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all elements that contain hemisphere information
    #Find the image link to access the high resolution image

    results = soup.find_all('div', class_='item')
    results

    hemisphere_image_urls=[]
    count=0

    for each_result in results: 
        
        title=each_result.find('h3').text
        
        browser.find_by_tag("h3")[count].click()
        time.sleep(0.5)
        
        count=count+1
        
        html = browser.html
        # soup_2 = BeautifulSoup(html, 'html.parser')

        img_url=browser.find_by_text('Sample')['href']
        
        hemisphere_dict={
            "title": title,
            "img_url":img_url
        }
        
        hemisphere_image_urls.append(hemisphere_dict)
        
        time.sleep(0.5)
        
        browser.visit(hemispheres_url)

    browser.quit()

    mars_dict={
        "Title":news_title,
        "Paragraph":news_p,
        "FeaturedImage": featured_image_url,
        "MarsFacts": mars_facts_html,
        "HemisphereImages": hemisphere_image_urls
    }

    return mars_dict