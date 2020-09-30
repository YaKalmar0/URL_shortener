import redis
from flask import  Flask, request, redirect, abort, render_template
from string import digits, ascii_letters
import secrets

url_len = 7
alphabet = digits + ascii_letters

redis = redis.Redis(password = 'f7pRRwDOfw9Xj8n9a7F/8wfI+z3hUsPJ9BXK6BU38FhcXCASOXdaagPkmyfzTXAc0DBHCiDGkQPAAtvv')

app = Flask(__name__, template_folder='templates/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_path', methods=['POST'])
def create_path():
    data = request.get_json()

    full_url = data['full_url']
    if not full_url.startswith('http://') and not full_url.startswith('https://'):
        abort(400, description='Invalid URL format')

    result = redis.get(full_url)
    if result != None:
        result = redis.get(result)
        return f"Shortened URL for {full_url} is: /{result}"
    else:
        short_url = ''.join(secrets.choice(alphabet) for i in range(url_len))

        while redis.get(short_url):
            short_url = ''.join(secrets.choice(alphabet) for i in range(url_len))
        
        default_life = 90*24*60*60
        redis.set(full_url, short_url, default_life)
        redis.set(short_url, full_url, default_life)

        return f"Shortened URL for {full_url} is: /{short_url}\n"
        

@app.route('/<path:path>', methods=['GET'])
def redirection(path):
    redir = redis.get(path)

    if not redir:
        return f"Could not establish connnection."
    else:
        return redirect(redir, 302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111)
