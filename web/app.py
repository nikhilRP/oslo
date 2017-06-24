import logging
import time

from config import BaseConfig
from flask import Flask, render_template, g, jsonify, request

from cluster import Cluster, LoadClusters
from data_loaders.base import Loader

app = Flask(__name__)
app.config.from_object(BaseConfig)


@app.route('/', methods=['GET', 'POST'])
def index():
    term = request.args.get('term', '')
    if term == '':
        response = LoadClusters().get_queries()
    else:
        response = LoadClusters().get_clusters(term)
    if request.args.get('format', '') == 'json':
        return jsonify(**response)
    return render_template('index.html', data=response)


@app.route('/cluster_listings', methods=['GET', 'POST'])
def cluster_listings():
    if request.args.get('index', '') == 'true':
        Loader('data/za_sample_listings_incl_cat.csv').index_items()

    clusters = Cluster(
        'data/za_queries_sample.csv').start_clustering()

    if request.args.get('format', '') == 'json':
        return jsonify(**clusters)
    return render_template('index.html', data=clusters)


@app.route('/search', methods=['GET', 'POST'])
def search():
    response = Loader('data/za_sample_listings_incl_cat.csv').index_items()
    if request.args.get('format', '') == 'json':
        return jsonify(**response)
    return render_template('index.html', data=response)


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
