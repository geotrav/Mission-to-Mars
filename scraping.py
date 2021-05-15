
# Import Splinter and BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

#Scrape all and initialize browser and WebDriver
def scrape_all():
    #Initiate headless driver for deployment
    # Setup Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres": hemispheres_path (browser)
    }
     # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    #url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
#Add try/except for error handling
    try:    
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

# ## JPL Space Images Featured Image
# Image feature function
def featured_image (browser):    
    # Visit URL
    url = 'https://spaceimages-mars.com'
    #url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    #Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    #img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

# ## Mars Facts
def mars_facts():
    #Add try/except
    try:
    # Extract Table to Pandas Dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        #df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
        df.head()
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

# Covert back to html
    return df.to_html(classes="table table-striped")


## Hemispheres URL scrape
def hemispheres_path (browser):
    # Use browser to visit the URL 
    url = 'https://marshemispheres.com'
    browser.visit(url)
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # Write code to retrieve the image urls and titles for each hemisphere.
    #initiate browser html and parser using parser and Beautiful soup
    html = browser.html
    img_soup = soup (html,'html.parser')
    # find all images on page using div class
    results = img_soup.find_all('div',class_="description")

    # set counter to iterate through links
    i=0
    for result in results:
        #create dictionary
        hemispheres ={}
        #get image titles
        parent =result.find('a', class_='itemLink product-item')
        title= parent.find('h3').text
        #browse to image page by clicking
        images = browser.find_by_tag('h3')
        images[i].click()
        #find sample images
        sample_elem =browser.find_by_text('Sample').first
        #store title and url
        hemispheres['title']=title
        hemispheres['img_url']=sample_elem['href']                
        hemisphere_image_urls.append(hemispheres)
        i+=1
        browser.back()

    return hemisphere_image_urls
    browser.quit()


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




