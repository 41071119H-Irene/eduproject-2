from flask import Flask, render_template, request, jsonify, send_from_directory
from flask import request
import json
import os
import uuid  # 用於產生唯一的檔案名稱

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
    UPLOAD_FOLDER = 'static/uploads'  # 指定上傳檔案的資料夾
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # 確保資料夾存在
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    photo_file = request.files.get('photo')
    print(photo_file)
    print(request.form)
    
    if photo_file:
        # 生成唯一的檔案名稱
        photo_filename = photo_file.filename
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo_file.save(photo_path)
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
    # Load profile data
    with open('profile.json', 'r') as f:
        profile_data = json.load(f)
    
    # Load learning topics data
    with open('learning.json', 'r') as f:
        learning_data = json.load(f)
    
    # Add learning topics data to profile data
    profile_data['data']['learning_topics'] = learning_data['learning_records']
    
    return render_template('profile.html', data=profile_data['data'])



@app.route('/add_topic', methods=['POST'])
def add_topic():
    # Get the JSON data sent from the client
    new_topic = request.json
    
    # Load existing data from learning.json
    with open('learning.json', 'r') as file:
        data = json.load(file)
    
    # Append the new topic to the list of learning topics
    data['learning_records'].append(new_topic)
    
    # Write the updated data back to learning.json
    with open('learning.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    # Check if Markdown content is sent from the client
    markdown_content = request.form.get('markdownContent')
    if markdown_content:
        # Find the index of the newly added topic
        new_topic_index = len(data['learning_records']) - 1
        # Add Markdown content to the corresponding topic
        data['learning_records'][new_topic_index]['markdownContent'] = markdown_content
        
        # Update the learning.json file with the new data
        with open('learning.json', 'w') as file:
            json.dump(data, file, indent=4)
    
    # Respond with a success message
    return jsonify({'message': 'Topic added successfully'})

@app.route('/learning/<topic_name>')
def learning(topic_name):
    # Load profile data
    with open('profile.json', 'r') as f:
        profile_data = json.load(f)
    
    # Load learning topics data
    with open('learning.json', 'r') as f:
        learning_data = json.load(f)
    
    # Find the topic by its name
    topic = None
    for t in learning_data['learning_records']:
        if t['topicName'] == topic_name:
            topic = t
            break
    
    # Render the learning template with the profile and topic data
    return render_template('learning.html', learning_topics=learning_data['learning_records'], profile=profile_data['data'], topic=topic)


@app.route('/save_markdown', methods=['POST'])
def save_markdown():
    # 获取来自前端的 JSON 数据，包含 Markdown 内容和主题名称
    request_data = request.json
    
    # 加载原始数据
    with open('learning.json', 'r') as file:
        data = json.load(file)
    
    # 根据主题名称找到相应的主题对象，并将 Markdown 内容添加到其中
    for record in data['learning_records']:
        if record.get('topicName') == request_data.get('topicName'):
            record['markdownContent'] = request_data.get('markdownContent', '')
            break
    
    # 将更新后的数据写回到 JSON 文件中
    with open('learning.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    # 响应成功消息
    return jsonify({'message': 'Markdown content saved successfully'})

@app.route('/get_markdown/<topic_name>')
def get_markdown(topic_name):
    # 加载 learning.json 文件中的内容
    with open('learning.json', 'r') as file:
        data = json.load(file)
    
    # 根据主题名称找到相应的主题对象，并返回 Markdown 内容
    for record in data['learning_records']:
        if record.get('topicName') == topic_name:
            markdown_content = record.get('markdownContent', '')
            break
    
    # 返回获取到的 Markdown 内容
    return jsonify({'markdownContent': markdown_content})



if __name__ == '__main__':
    app.run(debug=True)
