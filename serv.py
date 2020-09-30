import redis
from flask import  Flask, request, redirect, abort
from string import digits, ascii_letters
import secrets

url_len = 7
alphabet = digits + ascii_letters

redis = redis.Redis(password= 'f7pRRwDOfw9Xj8n9a7F/8wfI+z3hUsPJ9BXK6BU38FhcXCASOXdaagPkmyfzTXAc0DBHCiDGkQPAAtvv')

app = Flask(__name__)

@app.route('/')
def index():
    return f'Welcome to my page!'

@app.route('/create_path', methods=['POST'])
def create_path():
    data = request.get_json()

    full_url = data['full_url']
    if not full_url.startswith('http://') and not full_url.startswith('https://'):
        abort(400, description='Invalid URL format')

    result = redis.lindex(urls, full_url)
    if result != None:
        result = redis.lindex(urls, result+1)
        return f"Shotened URL for {full_url} is: {result}"
    else:
        short_url = ''.join(secrets.choice(alphabet) for i in range(url_len))

        while redis.get(short_url):
            short_url = ''.join(secrets.choice(alphabet) for i in range(url_len))
        
        redis.lpush(full_url, short_url)
        redis.lpush(short_url, full_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)