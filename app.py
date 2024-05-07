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
            'learning_topics': []  # 初始化學習主題列表
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

@app.route('/profile')
def profile():
    # 這裡使用已經創建的 profile_data 變數
    with open('profile.json', 'r') as f:
        profile_data = json.load(f)
    return render_template('profile.html', data=profile_data['data'])

@app.route('/add_topic', methods=['POST'])
def add_topic():
    topic_name = request.form.get('topicName')
    topic_description = request.form.get('topicDescription')

    # 讀取現有的 profile.json 檔案
    with open('profile.json', 'r') as f:
        profile_data = json.load(f)

    # 將新的主題資料添加到 profile_data 中
    profile_data['data'].setdefault('learning_topics', []).append({
        'topic_name': topic_name,
        'topic_description': topic_description
    })

    # 將更新後的 profile_data 寫入到 profile.json 檔案中
    with open('profile.json', 'w') as f:
        json.dump(profile_data, f)

    return jsonify({'message': 'Topic added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
