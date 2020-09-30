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

@app.route('/create_url', methods=['POST'])
def create_url():
    data = request.get_json()

    full_url = data['full_url']
    url_life = data['url_life']

    if not full_url.startswith('http://') and not full_url.startswith('https://'):
        abort(400, description='Invalid URL format\n')

    result = redis.get(full_url).decode('ascii')
    if result != None:
        short = redis.get(result)
        return f"Shortened URL for {full_url} is: {short}"
    else:
        short_url = ''.join(secrets.choice(alphabet) for i in range(url_len))

        while redis.get(short_url):
            short_url = ''.join(secrets.choice(alphabet) for i in range(url_len))
        
        if not url_life:
            url_life = 90*24*60*60 #90 days
        redis.set(full_url, short_url, url_life)
        redis.set(short_url, full_url, url_life)

        print(short_url)
        return f"Shortened URL for {full_url} is: {short_url}\n\n"
        

@app.route('/<path:path>', methods=['GET'])
def redirection(path):
    redir = redis.get(path)

    if not redir:
        return make_response("Could not establish connection", 404)
    else:
        return redirect(redir, 302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111)
