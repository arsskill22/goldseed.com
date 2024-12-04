from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

COMMENTS_FILE = "comments.json"

def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                
                app.logger.error("Файл comments.json пуст или поврежден. Создается новый.")
                return []
    return []


def save_comments(comments):
    try:
        app.logger.info(f"Сохраняем комментарии в файл: {os.path.abspath(COMMENTS_FILE)}")
        with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=4)
        app.logger.info(f"Комментарий успешно сохранен. Всего комментариев: {len(comments)}")
    except Exception as e:
        app.logger.error(f"Ошибка при сохранении комментариев: {e}")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        username = request.form.get('username')
        content = request.form.get('comment')

        if not username or not content:
            return jsonify({'status': 'error', 'message': 'Имя и комментарий обязательны'}), 400
        
        
        comments = load_comments()

        
        new_comment = {'username': username, 'content': content}
        comments.append(new_comment)

        
        save_comments(comments)

        return jsonify({'status': 'success', 'message': 'Комментарий успешно добавлен'})

    
    comments = load_comments()[-5:]  
    return jsonify({'comments': comments})

@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(f"Ошибка: {error}")
    return jsonify({'status': 'error', 'message': 'Произошла ошибка, попробуйте позже.'}), 500

if __name__ == '__main__':
    app.run(debug=True)