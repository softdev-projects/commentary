import os
import urllib

from flask import g, Flask, jsonify, render_template, request

from comment import Comment
import database

app = Flask(__name__, static_folder="static")
# TODO: pull out to config file
app.secret_key = "hello"


@app.before_request
def before_request():
    g.db = database.connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


# Homepage
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Only responds with JSON
@app.route('/comments', methods=['GET'])
def get_comments():
    # De-encode url
    url = urllib.unquote_plus(request.args['url'])

    comments = database.get_comments_for_url(g.db.cursor(), url)
    comments = [{'user_id': x[1], 'content': x[3]} for x in comments]

    data = {'url': url, 'comments': comments}
    resp = jsonify(data)
    return resp


@app.route('/comments/new', methods=['POST'])
def new_comment():
    data = request.get_json()
    print 'Received comment "{0}" for {1} from {2}'.format(
        data['comment'], data['url'], data['user_id'])

    comment = Comment(data['user_id'],
                      data['url'],
                      data['comment'])
    database.insert_comment(g.db.cursor(), comment)
    g.db.commit()

    # TODO: Fix me. For now, respond with nothing and 204 No Content
    return ('', 204)


@app.route('/team', methods=['GET', 'POST'])
def team():
    return render_template("team.html")


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")

if __name__ == '__main__':
    # If the database is not found, create it
    if not os.path.isfile(database.DATABASE_URI):
        conn = database.connect_db()
        database.create_default_tables(conn.cursor())
        conn.commit()
        conn.close()

    # TODO: pull out to config file
    app.debug = True
    app.run()
