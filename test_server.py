from flask import Flask, request, jsonify

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    print(f"로그인 시도: {username}")
    
    # 모든 로그인을 성공으로 처리
    return jsonify({
        "success": True,
        "message": "로그인 성공",
        "user": {
            "username": username,
            "email": f"{username}@example.com"
        },
        "token": "sample_jwt_token_here"
    })

@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    print(f"회원가입 시도: {data}")
    
    # 모든 회원가입을 성공으로 처리
    return jsonify({
        "success": True,
        "message": "회원가입 성공",
        "user": {
            "industry": data.get('industry', ''),
            "email": data.get('email', ''),
            "name": data.get('name', ''),
            "age": data.get('age', ''),
            "auth_id": data.get('auth_id', ''),
            "id": "user_123"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
