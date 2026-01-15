from flask import Flask

app = Flask(__name__)
app.name = "Semester 1 project bare test"

@app.route('/')
def temp():
    return "abcd"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=31764)
