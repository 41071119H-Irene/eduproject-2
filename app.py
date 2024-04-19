# app.py

from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

CONTENT_FILE = 'content.json'

def load_content():
    if os.path.exists(CONTENT_FILE) and os.path.getsize(CONTENT_FILE) > 0:
        with open(CONTENT_FILE, 'r') as f:
            return json.load(f)
    else:
        # 如果文件不存在或內容為空，返回默認值
        return "Enter your content here."

def save_content(content):
    with open(CONTENT_FILE, 'w') as f:
        json.dump(content, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        save_content(content)
        return redirect(url_for('index'))
    else:
        content = load_content()
        return render_template('index.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)
