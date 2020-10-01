# URL_shortener
A simple url-shortener based on Flask and Redis.

How to use:
1. Install requirements.txt (you also have to install redis-server on your machine)
2. `python serv.py`
3. Now you are able to test an app!

Example on `create_url`:

```
    curl \
    -H "Content-Type: application/json" \
    --request POST \
    --data '{"full_url":"https://www.linkedin.com/in/yakalmar/", "url_life":1}' \
    localhost:8080/create_url
```

Here you pass `full_url` as a URL you want to shrink and `url_life` as an amount of time (in days) for URL to exist (default - 90 days).

The output is:

```
Shortened URL for https://www.linkedin.com/in/yakalmar/ is: /U9xshKw
```

Here is an example of `GET` request previously shrinked URL:

```
    curl \
    -H "Content-Type: application/json" \
    --request GET \
    localhost:8080/U9xshKw
```

Or you can simply follow the link `localhost:8080/U9xshKw` in  your browser.

**OR**

You can temporarily use my link for testing: `http://yakalmar.tplinkdns.com`