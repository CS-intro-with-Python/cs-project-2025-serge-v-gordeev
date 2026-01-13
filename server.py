from flask import Flask, jsonify, request, render_template
from dv_calculator import get_response, hardcode_planets
from database import db
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

app = Flask(__name__)
app.name = "Semester 1 project"

werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.WARNING)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s%(levelname)s %(name)s: %(message)s")
werkzeug_logger.addHandler(handler)
handler.setFormatter(formatter)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:your_password@localhost:5432/ksp_celestial_body_data"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    hardcode_planets()

@app.before_request
def log():
    app.logger.info("Incoming %s request from %s on path %s", request.method, request.remote_addr, request.path)

@app.route('/')
def temp():
    return render_template("form.html")

@app.route('/test', methods=["POST"])
def test():
    received = request.json
    to_return = jsonify(get_response(received))
    return to_return

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=31764)