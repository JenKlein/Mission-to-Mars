from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#initialize flask app
app = Flask(__name__)

#use flask_pymonogo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

##Set Up App Routes
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index (1).html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all() ## access database
   mars.update({}, mars_data, upsert=True) ##update database  .update(query_parameter, data, options)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()

## if run in to error that flask_pymong is not installed. Make sure to delete all terminals and start new terminal