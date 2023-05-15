from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import os
import time
import threading

app = Flask(__name__)

url = "https://nashville.granicus.com/player/event/2968?&redirect=true"
etag = None
last_modified = None
agenda_number = ''

def scrape_data():
    global etag
    global last_modified
    global agenda_number
    
    headers = {}
    if etag:
        headers['If-None-Match'] = etag
    if last_modified:
        headers['If-Modified-Since'] = last_modified

    response = requests.get(url, headers=headers)

    if response.status_code == 304:
        # No changes
        pass
    else:
        # Data has changed
        soup = BeautifulSoup(response.content, "html.parser")
        current_agenda_item = soup.find(id="current-agenda-item")
        agenda_item_text = current_agenda_item.text.strip()

        # Extract the agenda number from the agenda item text
        agenda_number = agenda_item_text.split(".")[0].strip()

        etag = response.headers.get('ETag')
        last_modified = response.headers.get('Last-Modified')

        # Cache the scraped data to a new text file
        write_cached_data(agenda_number)


def start_scraping():
    while True:
        scrape_data()
        time.sleep(1)

@app.route('/')
def index():
    agenda_item_text = read_cached_data()
    return render_template('index.html', agenda_item=agenda_item_text)

@app.route('/check_data')
def check_data():
    agenda_item_text = read_cached_data()
    return jsonify(data=agenda_item_text)

def read_cached_data():
    try:
        with open('scraped_data.txt', 'r') as file:
            agenda_item_text = file.readline().split(':')[-1].strip()
    except FileNotFoundError:
        agenda_item_text = ''
    return agenda_item_text

def write_cached_data(agenda_item_text):
    global agenda_number
    with open('scraped_data.txt', 'w') as file:
        file.write(f"Agenda Item: {agenda_item_text}\n")
        file.write(f"Agenda Number: {agenda_number}\n")
        file.write(f"Last Update: {time.time()}\n")

if __name__ == '__main__':
    threading.Thread(target=start_scraping, daemon=True).start()
    app.run(debug=True)
