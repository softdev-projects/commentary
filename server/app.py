from flask import Flask, jsonify, render_template, request

app = Flask(__name__, static_folder="static")
# TODO: pull out to config file
app.secret_key = "hello"


# Homepage
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Only responds with JSON
@app.route('/comments', methods=['GET'])
def get_comments():
    # For now, respond with dummy data
    data = {'url': 'http://www.google.com/',
            'comments': [
                {'comment': 'Fake comment'},
                {'comment': 'Another fake comment'}
            ]}
    resp = jsonify(data)
    return resp


@app.route('/comments/new', methods=['POST'])
def new_comment():
    print 'Received comment \"{0}\" for {1}'.format(
        request.form['comment'], request.form['url'])
    # For now, respond with nothing and 204 No Content
    return ('', 204)

if __name__ == '__main__':
    # TODO: pull out to config file
    app.debug = True
    app.run()
