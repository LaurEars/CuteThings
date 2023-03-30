import json
import urllib.request
from random import randint
import re

import flask

app = flask.Flask(__name__)


def fetch_cute_things():
    """Fetches cute images from the top 100 posts in the 'aww' subreddit

    Returns a list of dictionaries, with each dictionary containing information about a cute thing:

    'url': The URL of the cute thing's image.
    'title': The title of the post on Reddit.
    'permalink': The permalink to the post on Reddit.
    Note: This function only handles imgur links that end in '.jpg'.
    """
    req = urllib.request.Request("http://www.reddit.com/r/aww/top/.json?limit=100")
    req.add_header("User-agent", "My reddit cute api bot")
    data = json.load(urllib.request.urlopen(req))
    cute_things = []
    for cute_thing in data['data']['children']:
        link = cute_thing['data']['url']

        match = re.search('.*com/(.*)(?:\.jpg)', link)
        if match:
            image_url = ''.join(['http://i.imgur.com/', match.group(1), '.jpg'])
        else:
            # take imgur links only, for now
            continue

        title = cute_thing['data']['title']
        permalink = 'http://reddit.com' + cute_thing['data']['permalink']
        cute_things.append({'url': image_url, 'title': title, 'permalink': permalink})
        return cute_things


@app.route("/")
def first_page():
    cute_things = fetch_cute_things()
    rand_idx = randint(0, len(cute_things) - 1)
    title = cute_things[rand_idx]['title']
    url = cute_things[rand_idx]['url']
    permalink = cute_things[rand_idx]['permalink']

    return flask.render_template('cute.html', image_url=url, permalink=permalink, title=title)


if __name__ == "__main__":
    app.run(port=3000)
