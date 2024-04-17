from flask import Flask, request, jsonify, send_file, url_for
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from flask_cors import CORS
import time
import random
import string 

app = Flask(__name__)
CORS(app)

@app.route('/extract-html', methods=['GET'])
def extract_html():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        response = requests.get(url)
        return jsonify({"url": url, "html_content": response.text})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/screenshot', methods=['GET'])
def screenshot():
    url = request.args.get('url')
    url2 = url
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    #screenshot_path = os.path.join('static', 'images', f"{url.split('//')[1].split('/')[0]}_screenshot.png")
    screenshot_path = "screen" + generate_random_string(10) + ".png"
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url2)
        driver.save_screenshot("static/"+screenshot_path)
        driver.quit()
        return get_image_link(screenshot_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_image_link(filename):
    # Ensure that the file exists in the static directory (you can add additional validation here)
    # Generate the URL for the image file
    image_url = url_for('static', filename=filename, _external=True)
    return jsonify({'image_url': image_url})

def generate_random_string(length):
    # Define the characters to use in the random string
    characters = string.ascii_letters + string.digits
    # Generate a random string
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

if __name__ == '__main__':
    app.run(debug=True)
