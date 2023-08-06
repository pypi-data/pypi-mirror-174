from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    name = request.args.get("name", "World111")
    return f'Hello, {name}!'
