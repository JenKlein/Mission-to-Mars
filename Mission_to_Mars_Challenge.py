#!/usr/bin/env python
# coding: utf-8

# In[62]:


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)


# In[63]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[64]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[65]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

#Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[66]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[67]:


slide_elem.find('div', class_='content_title')


# In[68]:


# use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[69]:


# use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## Featured Images

# In[70]:


#Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[71]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[72]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[73]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[74]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[75]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[76]:


df.to_html()


# In[77]:


browser.quit()


# ## challenge code

# In[78]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[79]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[80]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[81]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[82]:


slide_elem.find('div', class_='content_title')


# In[83]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[84]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[85]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[86]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[87]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[88]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[89]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[90]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[91]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[92]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[93]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)


# In[94]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
mars_soup = soup(html, 'html.parser')


# In[95]:


# create a list and confirm there are 4 objects in the list
links = mars_soup.find_all('div', {"class": "description"})
len(links)


# In[96]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

for i in links:
    
    title = i.find('h3').get_text()
    link_url = i.find('a')['href']
    hemis_url = 'https://astrogeology.usgs.gov/' + link_url
    browser.visit(hemis_url)
    html = browser.html
    mars_soup = soup(html, 'html.parser')
    
    img_new_var = 'https://astrogeology.usgs.gov/' + mars_soup.find('img', class_= 'wide-image')['src']
    
    
#     # create an empty dictionary
#     img_title_dict = {}
    
#     #find the elements on each loop to avoid a stale element exception
#    # for hemisphere in soup.find_all('div', class='item'): ### is this line unnecessary?
        

#     #finding element in each loop
#     browser.find_by_css('a.product-item')[i].click()

    
#     #get image title
#     img_title_dict["title"] = browser.find_by_css('h3').text
    
#     #find and click img link
# #     img_title_dict["title"]
# #     img_soup.find('a.itemLink product-item')[i].click()
    
#     jpg_img = browser.links.find_by_text("Sample")
    
#     img_title_dict["img_url"] = jpg_img["href"]
        
        
    # append hemisphere object to list
    hemisphere_image_urls.append({'title': title, 'img_url': img_new_var})
    
    
# 4. Print the list that holds the dictionary of each image url and title.        
hemisphere_image_urls


# In[97]:


# 5. Quit the browser
browser.quit()


# In[ ]:




