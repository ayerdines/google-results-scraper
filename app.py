from flask import Flask, request, render_template
from lib_utils import LPScrapper

app = Flask(__name__)


@app.route('/', methods=['GET'])
def search():
    return render_template('simple_form.html')


@app.route('/app.py', methods=['GET', 'POST'])
def index_page():
    args = request.args
    query = args.get('query')
    image_url = args.get('image_url')
    if image_url and query:
        scraper = LPScrapper()
        response = scraper.start_scraping(image_url, query)
        if response:
            return response
        else:
            return '<h3> NOT FOUND </h3>'
    else:
        return '<h3> Please provide valid image URL and query. </h3>'