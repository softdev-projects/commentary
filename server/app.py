import os

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
    print database.get_last_comment(g.db.cursor())

    # For now, respond with dummy data
    data = {'url': 'http://www.google.com/',
            'comments': [
                {'user_id': '1',
                 'comment': 'Fake comment'},
                {'user_id': '2',
                 'comment': 'Another fake comment'}
            ]}
    resp = jsonify(data)
    return resp


@app.route('/comments/new', methods=['POST'])
def new_comment():
    print 'Received comment "{0}" for {1} from {2}'.format(
        request.form['comment'], request.form['url'], request.form['user_id'])

    comment = Comment(request.form['user_id'],
                      request.form['url'],
                      request.form['comment'])
    database.insert_comment(g.db.cursor(), comment)
    g.db.commit()

    # TODO: Fix me. For now, respond with nothing and 204 No Content
    return ('', 204)

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
