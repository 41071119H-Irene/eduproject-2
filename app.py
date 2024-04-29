from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['POST'])
def generate_profile():
    if request.method == 'POST':
        # 獲取表單數據
        name = request.form.get('name')
        email = request.form.get('email')
        feature1 = request.form.get('feature1')
        feature2 = request.form.get('feature2')
        feature3 = request.form.get('feature3')
        facebook = request.form.get('facebook')
        instagram = request.form.get('instagram')
        website = request.form.get('personal_website')
        introduction = request.form.get('introduction')

        # 在這裡使用獲取到的數據生成個人檔案
        # 可以根據你的需求將這些數據儲存到數據庫中，或者生成靜態的 HTML 頁面

        # 假設我們生成了個人檔案的 URL，這裡返回一個 JSON 對象
        return jsonify({'profileUrl': '/generated_profile?name={}&email={}'.format(name, email)})

if __name__ == "__main__":
    app.run(debug=True)
