from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd

CONTENT_DIR = "html_content"
NASA_FILE = CONTENT_DIR+'/'+'nasa_2.txt'
JPL_FILE = CONTENT_DIR+'/'+'jpl.html'
MARS_TWITTER = CONTENT_DIR+'/'+'mars_twitter.html'
ASTRO_FILE = CONTENT_DIR+'/'+'Astro.html'
MARS_FACTS = CONTENT_DIR+'/'+'mars_facts.html'

def nasa_scrape():
    with open(NASA_FILE, 'r') as myfile:
      data = myfile.read()

    soup = BeautifulSoup(data, 'html.parser')

    news=[]

    for blurb in soup.find_all("div", {"class": "list_text"}):
        article={}
        article['title']=blurb.find("a").text
        article['para']=blurb.find("div",{"class":"article_teaser_body"}).text
        news.append(article)

    return news


#I copied my codes from jupiter notebook, I want to keep my own pattern.
##########################################################################
def jpl_scrape():
    with open(JPL_FILE, 'r') as myfile:
      data = myfile.read()

    soup = BeautifulSoup(data, 'html.parser')

    images_jpl=[]

    for image in soup.find_all("img", {"class": "thumb"}):
        image_dict={}
        full_img_url = 'https://www.jpl.nasa.gov' + image['src']
        image_dict['featured_image_url']=full_img_url
        images_jpl.append(image_dict)

    return images_jpl
    #images_jpl is a list I am using "append" to add the dictionary to the list
    #print(images_jpl)
############################################################################
def twitter_scrape():
    with open(MARS_TWITTER, 'r') as myfile:
        data = myfile.read()

    soup = BeautifulSoup(data, 'html.parser')

    #print(data)

    tweet_list=[]

    for tweet in soup.find_all("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}):
        tweet_dict={}
        tweet_dict['mars_weather']=tweet.text
        tweet_list.append(tweet_dict)

    return tweet_list
#print(tweet_list)
############################################################################
def mars_f():
    with open(MARS_FACTS, 'r') as myfile:
        data = myfile.read()

    soup = BeautifulSoup(data, 'html.parser')

    #print(data)
    table_html = soup.find("table", {"class":"tablepress tablepress-id-mars"})
    table_df = pd.read_html(str(table_html))[0]
    table_df = table_df.transpose()
    table_dict = table_df.to_dict('dict')
    # print(table_df,table_dict)
    #used transpose in order to switch the rows and the columns
    refined_dict = {}
    for key,val in table_dict.items():
        print(val)
        refined_dict[val[0]]=val[1]

    return refined_dict
#made the df into a dictionary in order to be able to grab the table/collection information later
#############################################################################
def astro():
    with open(ASTRO_FILE, 'r') as myfile:
        data = myfile.read()

    soup = BeautifulSoup(data, 'html.parser')

    #print(data)

    #creating a list
    hemisphere_image_urls=[]

    for blurb in soup.find_all("div", {"class": "item"}):
        m_image={}
        m_image['title']=blurb.find("h3").text
        thumb_img=blurb.find("img",{"class":"thumb"})
        thumb_img_url = thumb_img['src'] #scraped the common sub-string which was the image name, e.g. "schiaparelli_enhanced"
        img_name_p1 = thumb_img_url.split('_',1)[1] #split the first '_' from the thumb url and grabbed [] what was after that
        img_name = img_name_p1.split('.')[0] #split the '.' and grabbed what was infront of the '0'
        full_img_url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/' + img_name + '.tif/full.jpg'
        m_image['img_url'] = full_img_url
        hemisphere_image_urls.append(m_image)

    return hemisphere_image_urls
#print(hemisphere_image_urls)
