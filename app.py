from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['POST'])
def generate_profile():
    # 從 POST 請求中獲取表單資料
    name = request.form.get('name')
    email = request.form.get('email')
    feature1 = request.form.get('feature1')
    feature2 = request.form.get('feature2')
    feature3 = request.form.get('feature3')
    facebook = request.form.get('facebook')
    instagram = request.form.get('instagram')
    personal_website = request.form.get('personal_website')
    introduction = request.form.get('introduction')

    # 上傳的檔案處理
    photo_file = request.files.get('photo')
    if photo_file:
        photo_filename = photo_file.filename
        photo_file.save(os.path.join(app.root_path, 'static', 'uploads', photo_filename))
    else:
        photo_filename = None

    # 將表單資料組合成 JSON 格式
    profile_data = {
        'data': {
            'name': name,
            'email': email,
            'features': {
                'feature1': feature1,
                'feature2': feature2,
                'feature3': feature3
            },
            'social_media': {
                'facebook': facebook,
                'instagram': instagram,
                'personal_website': personal_website
            },
            'introduction': introduction,
            'photo_filename': photo_filename,  # 添加照片檔案名稱到資料中
            'learning_topic_title': ''  # 如果需要，可以填入學習主題標題
        }
    }

    # 將 JSON 資料保存到檔案中
    with open('profile.json', 'w') as f:
        json.dump(profile_data, f)

    # 返回成功訊息
    return jsonify({'profileUrl': '/profile.json'})

@app.route('/profile.json')
def profile_json():
    return send_from_directory('.', 'profile.json', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
