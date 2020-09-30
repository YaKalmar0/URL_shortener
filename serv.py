import redis
from flask import  Flask, request, redirect, make_response
from string import digits, ascii_letters
import secrets

url_len = 7
alphabet = digits + ascii_letters

redis = redis.StrictRedis(password = 'f7pRRwDOfw9Xj8n9a7F/8wfI+z3hUsPJ9BXK6BU38FhcXCASOXdaagPkmyfzTXAc0DBHCiDGkQPAAtvv', decode_responses=True)
app = Flask(__name__, template_folder='templates/')


@app.route('/')
def index():
    return "<h1>Welcome to the URL-shortener!</h1>"


@app.route('/create_url', methods=['POST'])
def create_url():
    data = request.get_json()

    full_url = data['full_url']
    try:
        url_life = data['url_life']
    except KeyError:
        url_life = 90*24*60*60

    if not full_url.startswith('http://') and not full_url.startswith('https://'):
        make_response('<h2>Invalid URL format</h2>', 400)

    result = redis.get(full_url)
    if result != None:
        return f"Shortened URL for {full_url} already exists: /{result}"
    else:
        short_url = ''.join(secrets.choice(alphabet) for i in range(url_len))

        while redis.get(short_url):
            short_url = ''.join(secrets.choice(alphabet) for i in range(url_len))
        
        if url_life<=0:
            url_life = 90*24*60*60 #90 days
        redis.set(full_url, short_url, url_life)
        redis.set(short_url, full_url, url_life)
        return f"Shortened URL for {full_url} is: /{short_url}\n\n"
        

@app.route('/<path:path>', methods=['GET'])
def redirection(path):
    redir = redis.get(path)

    if not redir:
        return make_response("<h2>Could not establish connection</h2>", 404)
    else:
        return redirect(redir, 302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
