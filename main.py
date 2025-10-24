from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/hello')
def home():
    return ('{ "message": "Hello, world!"}')

@app.route('/user/<name>')
def greet(name):
    message = '{"message": "Hello, ' + name + '!"}'
    return (message)

@app.route('/search')
def search():
    query = request.args.get('q')
    message = '{ "query": "' + query + '", "length": ' + str(len(query)) + '}'
    return message

if __name__ == '__main__':
    app.run(port=8080)
