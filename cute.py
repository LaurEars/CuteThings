import json
import urllib2
from random import randint

import flask
import re

app = flask.Flask(__name__)

req = urllib2.Request("http://www.reddit.com/r/aww/top/.json?limit=100")
req.add_header("User-agent", "My reddit cute api bot")
data = json.load(urllib2.urlopen(req))
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

@app.route("/")
def first_page():
    rand_idx = randint(0, len(cute_things))
    title = cute_things[rand_idx]['title']
    url = cute_things[rand_idx]['url']
    permalink = cute_things[rand_idx]['permalink']

    return flask.render_template('cute.html', image_url=url, permalink=permalink, title=title)

if __name__ == "__main__":
    app.run(port=3000)
