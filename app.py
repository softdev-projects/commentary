from flask import Flask, render_template, redirect, session, request, escape


#route for retrieving, storing, and home page


app = Flask(__name__, static_folder="static")
app.secret_key = "hello"


@app.route('/', methods=['GET'])
def index():
    return None

@app.route('/comments', methods=['GET'])
def get_comments():

    return [{'url':"555.555.co.uk",'comment':"Fake Real Comment"}
            ,{'url':"hello.world.com",'comment':"Fake Comment"}
            ,{'url':"www.why.org",'comment':"Not Real Comment"}
            ,{'url':"www.dummy.net",'comment':"Test Comment"}]
@app.route('/comments/new', methods=['POST'])
def store_comments():
    return None



#All Boring Names that Justin gives me and no Fun Benedict Names makes Ben a dull boy
    
if __name__ == '__main__':
    app.debug = True
    app.run()
