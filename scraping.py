#!/usr/bin/env python
# coding: utf-8


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

#10.5.3

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
## headless = True means you won't see the scraping in action, vice versa for headless= False

    news_title, news_paragraph = mars_news(browser)
    ##this function mars_news pulls the data for news_title and news_paragraph

    ## 10.5.3
    # Run all scraping functions and store results in dictionary 
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_img_URL": hemi_url  ##step 2 - dictionary of img url and title from deliverable 1

    }

    # quit the browser and return data
    browser.quit()
    return data


## Refactored code to use functions and include error handling
# News & title paragraph

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ## JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ## Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


########### 3. scrape the hemisphere data by using your code from the Mission_to_Mars_Challenge.py file

def hemi_url():

    #Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    mars_soup = soup(html, 'html.parser')


    # create a list and confirm there are 4 objects in the list
    links = mars_soup.find_all('div', {"class": "description"})
    len(links)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.


    for i in links:
        
        title = i.find('h3').get_text()
        link_url = i.find('a')['href']
        hemis_url = 'https://astrogeology.usgs.gov/' + link_url
        browser.visit(hemis_url)
        html = browser.html
        mars_soup = soup(html, 'html.parser')
        
        img_new_var = 'https://astrogeology.usgs.gov/' + mars_soup.find('img', class_= 'wide-image')['src']
        
        # append hemisphere object to list
        hemisphere_image_urls.append({'title': title, 'img_url': img_new_var})
        
    # Print the list that holds the dictionary of each image url and title.        
    #hemisphere_image_urls
    
    console.log(hemisphere_image_urls)
    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape_all())



### need to return to app.py