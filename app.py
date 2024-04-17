from flask import Flask, request, jsonify, send_file
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

app = Flask(__name__)

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
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    screenshot_path = os.path.join('static', 'images', f"{url.split('//')[1].split('/')[0]}_screenshot.png")
    options = Options()
    options.headless = True
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.save_screenshot(screenshot_path)
        driver.quit()
        return send_file(screenshot_path, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
