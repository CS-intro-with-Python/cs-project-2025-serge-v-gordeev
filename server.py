from flask import Flask, jsonify, request, render_template
import dv_calculator

app = Flask(__name__)

@app.route('/')
def temp():
    return render_template("form.html")

@app.route('/test', methods=["POST"])
def test():
    received = request.json
    to_return = jsonify(dv_calculator.get_response(received))
    return to_return

# if __name__ == '__main__':
app.run(host="0.0.0.0", port=31764)