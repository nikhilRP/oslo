import logging
import time

from config import BaseConfig
from flask import Flask, render_template, g, jsonify

app = Flask(__name__)
app.config.from_object(BaseConfig)


@app.route('/', methods=['GET', 'POST'])
def index():
    return jsonify(**{'Name': "Bond, James Bond"})


@app.route('/index_data', methods=['GET', 'POST'])
def index_data():
    from data_loaders.base import Loader
    data = Loader('data/za_sample_listings_incl_cat.csv').index_items()
    app.logger.info(data)
    return jsonify(**{'item_count': data})


@app.before_first_request
def setup_logging():
    """
    Setups logging for each request separately
    """
    app.logger.setLevel(logging.INFO)
    app.logger.propagate = False


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/forbidden_page.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/page_not_found.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/server_error.html"), 500


if __name__ == '__main__':
    app.run(debug=True)
