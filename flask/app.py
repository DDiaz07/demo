from flask import Flask, render_template
import scraper
from pymongo import MongoClient

client = MongoClient()
app = Flask(__name__)

data = {}

@app.route("/scrape")
def scrape():
    # store scraped data into mongo
    client = MongoClient('localhost', 27017)
    db = client['scrape_database']
    collection = db['mars_collection']

    data['nasa'] = scraper.nasa_scrape()
    data['jpl'] = scraper.jpl_scrape()
    data['twitter'] = scraper.twitter_scrape()
    data['mars_f'] = scraper.mars_f()
    data['astro'] = scraper.astro()

    collection.insert(data)

    return str(data)



@app.route("/")
def index():
    client = MongoClient('localhost', 27017)
    db = client['scrape_database']
    collection = db['mars_collection']

    cursor = collection.find({})
    doc = cursor[0]

    return render_template('index.html',jpl_images=doc['jpl'],astro_images=doc['astro'],mars_table=doc['mars_f'],tweeter=doc['twitter'],nasa_info=doc['nasa'])
