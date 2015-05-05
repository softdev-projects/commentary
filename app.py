from flask import Flask, render_template, redirect, session, request, escape


#route for retrieving, storing, and home page


app = Flask(__name__, static_folder="static")
app.secret_key = "hello"


@app.route('/', methods=['GET'])
def index():
    return None

@app.route('/comments', methods=['GET'])
def get_comments():
    return None

@app.route('/comments/new', methods=['POST'])
def store_comments():
    return None


    
