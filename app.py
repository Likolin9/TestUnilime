from flask import Flask

from api.api import api_bp
from cache import cache

app = Flask(__name__)
cache.init_app(app)
app.register_blueprint(api_bp, url_prefix='/api')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
