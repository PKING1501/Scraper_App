from flask import Flask, request
from temp import first_scraper, name_of_city

app = Flask(__name__)

@app.route('/firstScraper', methods=['POST'])
def scraper1():
    data = request.json
    headers = data.get('headers')
    fetched_link = data.get('urls')
    result = first_scraper(headers, fetched_link)
    return result
    
@app.route('/scraper1name', methods=['POST'])
def nameOfScraper():
    data = request.json
    headers = data.get('headers')
    fetched_link = data.get('urls')
    result = name_of_city(headers, fetched_link)
    return result

if __name__ == '__main__':
    app.run(debug=True)