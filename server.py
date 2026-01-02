# comment to restart action
from flask import Flask

app = Flask(__name__)

@app.route('/')
def temp():
    return ('This is a test message, there is nothing here yet')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

