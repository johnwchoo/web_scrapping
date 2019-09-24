from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

#create instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
	mars = mongo.db.mars.find_one() #placeholder
	print(mars)
	return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
	mars = mongo.db.mars
	mars_data = scrape_mars.scrape()
	print(mars_data)
	mars.update({}, mars_data, upsert = True)
	return "Scraping Successful!"


if __name__ == "__main__":
    app.run(debug=True)

# boilderplate = setting up flask app (line 4 - 13)