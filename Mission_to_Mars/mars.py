import requests
from bs4 import BeautifulSoup as bs
import splinter
import pandas as pd

# setup to lookup chromedriver.execute file

def init_browser():
    # setup to lookup chromedriver.execute file
    executable_path = {'executable_path': 'Missions_to_Mars/chromedriver.exe'}
    return Browser('chrome', **executable_path)

def scrape_all(): 

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    content = soup.find('div', class_='content_page')

    # Retrieve article text
    titles = content.find_all('div', class_='content_title')
    titles=titles[0].text.strip()

     # Retrieve paragraph text
    article_text = content.find_all('div', class_='article_teaser_body')
    article_text = article_text[0].text

# ### • JPL (Jet Propulsion Laboratory) Mars Space Images - Featured Image

    # URL for featured image webpage
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html

    # parse html with beautiful soup for images
    soup = bs(html, 'html.parser')
    featured_image = soup.find('article', class_='carousel_item')['style']

    # Retrieve the latter part of the image url
    latter = featured_image.split('/spaceimages/')[1].split("'")[0]

    # Retrieve the main part of the image url
    former = url.split('?')[0]

    # Retrieve the full image url
    pic_url = former + latter
    # pic_url

    # ### • Mars Facts

    # url for Mars Facts webpage
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html

    # use Pandas to scrape the table containing facts about Mars
    profile = pd.read_html(url)
    profile_df = profile[0]
    profile_df.columns = ['description', 'information']
    profile_df.set_index('description', inplace=True)
    # profile_df

    # Use Pandas to convert the data to a HTML table string
    mars_facts = profile_df.to_html(classes='table-stripped')
    # print(mars_facts)

    # ### • Mars Hemispheres

    # url for USGS Astrologeology webpage
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html

    # parse html with beautiful soup for images
    soup = bs(html, 'html.parser')
  
    # identifying the require lookups and parameters
    main_url = 'https://astrogeology.usgs.gov'
    images = soup.findAll('div',class_='item')
    image_url_list = []

    # loop through the classes and get the images and url
    for image in images:
        title = image.find('h3').text
        img_url = image.find('a', class_='itemLink product-item')['href']
        browser.visit(main_url + img_url)
        image_html = browser.html
        hemi_soup = bs(image_html, 'html.parser')
        images_urls = main_url + hemi_soup.find('img', class_='wide-image')['src']
        image_url_list.append({'title': title, 'image_url': images_urls})


    # Display the Hemisphere Image URLs
    # image_url_list


    # create dictionary to hold mars data
    mars_data = {
        'titles': titles,
        'article_text': article_text,
        'pic_url': pic_url,
        'mars_facts': mars_facts,
        'image_url_list': image_url_list
    }

    browser.quit()

    return mars_data